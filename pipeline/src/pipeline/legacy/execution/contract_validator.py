from __future__ import annotations
import re
from dataclasses import dataclass, field


FORBIDDEN_IMPORTS = [
    "requests", "httpx", "celery", "redis",
    "rest_framework", "graphene", "channels",
]

# Patrones que indican deriva arquitectónica en el código generado
FORBIDDEN_CODE_PATTERNS = [
    (r"fetch\(|axios\.|XMLHttpRequest",         "JS async/fetch detectado (patrón SPA)"),
    (r"{% load (?!static|i18n|crispy_forms)\w+","tag {% load %} no aprobado"),
]


@dataclass
class ValidationReport:
    sprint_id  : str
    passed     : bool = True
    violations : list[str] = field(default_factory=list)
    warnings   : list[str] = field(default_factory=list)

    def fail(self, msg: str):
        self.violations.append(msg)
        self.passed = False

    def warn(self, msg: str):
        self.warnings.append(msg)

    def to_dict(self) -> dict:
        return {
            "sprint_id" : self.sprint_id,
            "passed"    : self.passed,
            "violations": self.violations,
            "warnings"  : self.warnings,
        }


class ContractValidator:
    """
    Validador 100% determinista.
    Compara el output generado contra los contratos congelados.
    No llama a ningún modelo.
    """

    def __init__(
        self,
        sprint_contract : dict,   # 11_sprint_contract.json (subcontrato del sprint)
        routes_contract : dict,   # 09a_routes_required.json
        entities_contract: dict,  # 09b_domain_entities_required.json
    ):
        self.sprint_id       = sprint_contract.get("sprint_id", "?")
        self.allowed_models  = set(sprint_contract.get("models", []))
        self.allowed_routes  = set(sprint_contract.get("routes", []))
        self.allowed_templates = set(sprint_contract.get("templates", []))

        # Universo global de rutas aprobadas (09a)
        self.global_routes = {
            r.get("name", r) if isinstance(r, dict) else r
            for r in routes_contract.get("routes", [])
        }

        # Universo global de entidades aprobadas (09b)
        self.global_entities = {
            e.get("name", e) if isinstance(e, dict) else e
            for e in entities_contract.get("entities", [])
        }

    def validate(self, generated: dict) -> ValidationReport:
        report = ValidationReport(sprint_id=self.sprint_id)

        for art in generated.get("artifacts", []):
            name    = art.get("name", "?")
            content = art.get("content", "")
            atype   = art.get("type", "?")
            path    = art.get("path", "")

            self._check_forbidden_imports(content, name, report)
            self._check_forbidden_patterns(content, name, report)

            if atype == "model":
                self._check_model(name, content, report)
            elif atype == "template":
                self._check_template(name, path, report)
            elif atype == "urls":
                self._check_urls(content, report)
            elif atype == "view":
                self._check_view(name, content, report)

        return report

    # ── checks individuales ──────────────────────────────────────────────────

    def _check_forbidden_imports(self, content: str, name: str, report: ValidationReport):
        for pkg in FORBIDDEN_IMPORTS:
            if re.search(rf"\bimport\s+{pkg}\b|from\s+{pkg}\b", content):
                report.fail(f"[{name}] Import prohibido: '{pkg}'")

    def _check_forbidden_patterns(self, content: str, name: str, report: ValidationReport):
        for pattern, label in FORBIDDEN_CODE_PATTERNS:
            if re.search(pattern, content):
                report.fail(f"[{name}] {label}")

    def _check_model(self, name: str, content: str, report: ValidationReport):
        # El nombre de la clase debe estar en el contrato del sprint
        if name not in self.allowed_models:
            report.fail(
                f"Modelo '{name}' no está en el contrato de este sprint.\n"
                f"  Permitidos: {sorted(self.allowed_models)}"
            )
        # El nombre de la clase debe estar en el universo global de entidades (09b)
        if name not in self.global_entities:
            report.fail(
                f"Modelo '{name}' no existe en 09b_domain_entities_required.\n"
                f"  Entidades globales: {sorted(self.global_entities)}"
            )

    def _check_template(self, name: str, path: str, report: ValidationReport):
        # Comprueba por nombre de archivo
        filename = path.split("/")[-1] if "/" in path else name
        if filename not in self.allowed_templates:
            report.fail(
                f"Template '{filename}' no está en el contrato de este sprint.\n"
                f"  Permitidos: {sorted(self.allowed_templates)}"
            )

    def _check_urls(self, content: str, report: ValidationReport):
        found = re.findall(r'name=["\'](\w+)["\']', content)
        for route_name in found:
            if route_name not in self.global_routes:
                report.fail(f"[urls] Ruta '{route_name}' no existe en 09a (contrato global).")
            elif route_name not in self.allowed_routes:
                report.fail(f"[urls] Ruta '{route_name}' no es parte de este sprint.")

    def _check_view(self, name: str, content: str, report: ValidationReport):
        # Avisa si la vista referencia templates no declarados en el sprint
        refs = re.findall(r'render\(.*?["\']([^"\']+\.html)["\']', content)
        for t in refs:
            fname = t.split("/")[-1]
            if fname not in self.allowed_templates:
                report.warn(
                    f"[{name}] Vista referencia template '{t}' no declarado en este sprint."
                )