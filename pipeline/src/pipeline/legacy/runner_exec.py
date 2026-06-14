from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


# ============================================================
# Execution runner scaffold for a hybrid human-AI Django pipeline
# ============================================================
# Intent:
# - Keep architecture frozen after Dev phase
# - Materialize repo bootstrap from the freeze when no base repo exists
# - Derive a strict execution manifest per sprint
# - Accept model output only as a validated patch set
# - Apply patch set to the repository only after deterministic checks
# - Emit validation and change-request artifacts
#
# Notes:
# - This file is intentionally deterministic-first.
# - CrewAI/Flow should orchestrate this module, not replace its logic.
# - A few extractor methods are tolerant because the exact JSON schemas were
#   not provided in this chat. Replace/adapt them once your final schemas are fixed.
# ============================================================


REQUIRED_INPUTS = {
    "09_stack": "09_stack_y_restricciones.json",
    "09a_routes": "09a_routes_required.json",
    "09b_entities": "09b_domain_entities_required.json",
    "10_design": "10_diseno_tecnico.json",
    "10a_map": "10a_sprint_contract_map.json",
}

STATUS_OK = {"approved", "aprobado"}
PATCH_OPS = {"create", "update"}


# -----------------------------
# Utility helpers
# -----------------------------
def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("/")


def path_in_allowed(path: str, allowed_paths: Sequence[str]) -> bool:
    normalized = normalize_path(path)
    for allowed in allowed_paths:
        allowed_norm = normalize_path(allowed)
        if normalized == allowed_norm:
            return True
        if allowed_norm.endswith("/") and normalized.startswith(allowed_norm):
            return True
    return False


def render_key_value_md(title: str, data: Dict[str, Any]) -> str:
    lines = [f"# {title}", ""]
    for key, value in data.items():
        lines.append(f"## {key}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(value, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def recursive_find_values(obj: Any, target_keys: Iterable[str]) -> List[Any]:
    found: List[Any] = []
    target_keys = set(target_keys)
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in target_keys:
                found.append(value)
            found.extend(recursive_find_values(value, target_keys))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(recursive_find_values(item, target_keys))
    return found


def flatten_to_strings(value: Any) -> List[str]:
    results: List[str] = []
    if isinstance(value, str):
        results.append(value)
    elif isinstance(value, list):
        for item in value:
            results.extend(flatten_to_strings(item))
    elif isinstance(value, dict):
        for v in value.values():
            results.extend(flatten_to_strings(v))
    return results


# -----------------------------
# Domain extraction (schema-tolerant)
# -----------------------------
def extract_status(data: Dict[str, Any]) -> str:
    raw = str(data.get("estado", data.get("status", ""))).strip().lower()
    return raw


def extract_freeze_id(data: Dict[str, Any]) -> Optional[str]:
    candidates = [
        data.get("freeze_id"),
        data.get("metadata", {}).get("freeze_id") if isinstance(data.get("metadata"), dict) else None,
    ]
    for candidate in candidates:
        if candidate:
            return str(candidate)
    return None


def extract_project_name(stack_data: Dict[str, Any], design_data: Dict[str, Any]) -> str:
    candidates = recursive_find_values(stack_data, {"project_name", "django_project_name", "repo_name"})
    candidates += recursive_find_values(design_data, {"project_name", "django_project_name", "repo_name"})
    flattened = [x for x in flatten_to_strings(candidates) if x.strip()]
    if flattened:
        return flattened[0].strip()
    return "project"


def extract_app_names(design_data: Dict[str, Any], sprint_map_data: Dict[str, Any]) -> List[str]:
    apps: List[str] = []
    for raw in recursive_find_values(design_data, {"app", "app_name", "apps"}):
        apps.extend(flatten_to_strings(raw))
    for raw in recursive_find_values(sprint_map_data, {"app", "app_name", "apps"}):
        apps.extend(flatten_to_strings(raw))

    cleaned: List[str] = []
    for app in apps:
        app = app.strip()
        if not app:
            continue
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", app):
            cleaned.append(app)
    return sorted(set(cleaned))


def extract_routes(routes_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates = []
    for key in ("routes", "items", "data"):
        value = routes_data.get(key)
        if isinstance(value, list):
            candidates.extend([x for x in value if isinstance(x, dict)])
    if not candidates and isinstance(routes_data, list):
        candidates = [x for x in routes_data if isinstance(x, dict)]
    return candidates


def extract_entities(entities_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates = []
    for key in ("entities", "items", "data"):
        value = entities_data.get(key)
        if isinstance(value, list):
            candidates.extend([x for x in value if isinstance(x, dict)])
    if not candidates and isinstance(entities_data, list):
        candidates = [x for x in entities_data if isinstance(x, dict)]
    return candidates

def extract_sprint_block(sprint_map_data: Dict[str, Any], sprint_id: Any) -> Dict[str, Any]:
    for key in ("sprints", "items", "contracts", "map"):
        value = sprint_map_data.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    # Compara contra "sprint_id", "id" o "sprint" en int y string
                    for field in ("sprint_id", "id", "sprint"):
                        val = item.get(field)
                        if val is not None and str(val) == str(sprint_id):
                            return item
        if isinstance(value, dict) and str(sprint_id) in value:
            return value[str(sprint_id)]
    raise ValueError(
        f"No se encontró el sprint '{sprint_id}' dentro de 10a_sprint_contract_map.json"
    )

def extract_scope_names(block: Dict[str, Any], candidate_keys: Iterable[str]) -> List[str]:
    names: List[str] = []
    for raw in recursive_find_values(block, set(candidate_keys)):
        names.extend(flatten_to_strings(raw))
    return sorted({x.strip() for x in names if isinstance(x, str) and x.strip()})


def route_identifier(route: Dict[str, Any]) -> str:
    name = str(route.get("name", "")).strip()
    path = str(route.get("path", "")).strip()
    if name:
        return name
    return path


def entity_identifier(entity: Dict[str, Any]) -> str:
    for key in ("entity", "name", "id"):
        value = entity.get(key)
        if value:
            return str(value).strip()
    return ""


# -----------------------------
# Patch-set validation / application
# -----------------------------
def validate_patch_set_schema(patch_set: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(patch_set, dict):
        return ["El patch set no es un objeto JSON."]
    if not isinstance(patch_set.get("operations"), list) or not patch_set["operations"]:
        errors.append("El patch set debe contener 'operations' como lista no vacía.")
        return errors
    for idx, op in enumerate(patch_set["operations"], start=1):
        if not isinstance(op, dict):
            errors.append(f"Operación #{idx}: debe ser un objeto.")
            continue
        action = str(op.get("op", "")).strip().lower()
        if action not in PATCH_OPS:
            errors.append(f"Operación #{idx}: 'op' debe ser create/update.")
        path = str(op.get("path", "")).strip()
        if not path:
            errors.append(f"Operación #{idx}: falta 'path'.")
        content = op.get("content")
        if not isinstance(content, str):
            errors.append(f"Operación #{idx}: 'content' debe ser string con el archivo completo.")
    return errors


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    warnings: List[str]


class ExecutionRunner:
    def __init__(self, artifact_root: Path, repo_root: Path) -> None:
        self.artifact_root = artifact_root
        self.repo_root = repo_root
        self.outputs_root = artifact_root / "outputs" / "execution"
        self.json_root = self.outputs_root / "json"
        self.docs_root = self.outputs_root / "docs"
        self.logs_root = self.outputs_root / "logs"
        self.json_root.mkdir(parents=True, exist_ok=True)
        self.docs_root.mkdir(parents=True, exist_ok=True)
        self.logs_root.mkdir(parents=True, exist_ok=True)

    # ---------- file access ----------
    def path_for_input(self, key: str) -> Path:
        return self.artifact_root / REQUIRED_INPUTS[key]

    def load_required_inputs(self) -> Dict[str, Dict[str, Any]]:
        missing = [name for name, filename in REQUIRED_INPUTS.items() if not (self.artifact_root / filename).exists()]
        if missing:
            raise FileNotFoundError(f"Faltan artefactos obligatorios: {', '.join(missing)}")
        return {name: load_json(self.artifact_root / filename) for name, filename in REQUIRED_INPUTS.items()}

    def status(self) -> Dict[str, Any]:
        exists = {filename: (self.artifact_root / filename).exists() for filename in REQUIRED_INPUTS.values()}
        result = {
            "artifact_root": str(self.artifact_root),
            "repo_root": str(self.repo_root),
            "required_inputs": exists,
            "repo_exists": self.repo_root.exists(),
            "repo_has_manage_py": (self.repo_root / "manage.py").exists(),
            "generated_outputs": sorted(str(p.relative_to(self.outputs_root)) for p in self.outputs_root.rglob("*") if p.is_file()),
        }
        return result

    def preflight(self) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        try:
            inputs = self.load_required_inputs()
        except FileNotFoundError as e:
            return ValidationResult(False, [str(e)], warnings)

        for key in ("09_stack", "09a_routes", "09b_entities", "10_design"):
            status = extract_status(inputs[key])
            if status and status not in STATUS_OK:
                errors.append(f"{REQUIRED_INPUTS[key]} no está aprobado. Estado detectado: '{status}'.")
            elif not status:
                warnings.append(f"{REQUIRED_INPUTS[key]} no tiene campo de estado legible. Revísalo.")

        freeze_10 = extract_freeze_id(inputs["10_design"])
        freeze_10a = extract_freeze_id(inputs["10a_map"])
        if freeze_10 and freeze_10a and freeze_10 != freeze_10a:
            errors.append(f"Freeze inconsistente entre 10 y 10a: {freeze_10} != {freeze_10a}")
        if not freeze_10:
            warnings.append("10_diseno_tecnico.json no expone freeze_id legible.")
        if not freeze_10a:
            warnings.append("10a_sprint_contract_map.json no expone freeze_id legible.")

        if not self.repo_root.exists():
            warnings.append("El repositorio aún no existe. Será necesario ejecutar bootstrap.")

        return ValidationResult(not errors, errors, warnings)

    # ---------- manifests ----------
    def build_bootstrap_manifest(self) -> Dict[str, Any]:
        inputs = self.load_required_inputs()
        stack = inputs["09_stack"]
        design = inputs["10_design"]
        sprint_map = inputs["10a_map"]
        routes = extract_routes(inputs["09a_routes"])
        entities = extract_entities(inputs["09b_entities"])
        project_name = extract_project_name(stack, design)
        apps = extract_app_names(design, sprint_map)
        freeze_id = extract_freeze_id(design) or extract_freeze_id(sprint_map) or "UNKNOWN_FREEZE"

        base_allowed_files = [
            "manage.py",
            f"{project_name}/",
            f"{project_name}/__init__.py",
            f"{project_name}/settings.py",
            f"{project_name}/urls.py",
            f"{project_name}/wsgi.py",
            f"{project_name}/asgi.py",
            "requirements.txt",
            "templates/",
            "static/",
        ]
        for app in apps:
            base_allowed_files.extend(
                [
                    f"{app}/",
                    f"{app}/__init__.py",
                    f"{app}/apps.py",
                    f"{app}/models.py",
                    f"{app}/views.py",
                    f"{app}/urls.py",
                    f"{app}/forms.py",
                    f"{app}/admin.py",
                    f"{app}/tests.py",
                    f"{app}/migrations/",
                    f"templates/{app}/",
                ]
            )

        manifest = {
            "doc_id": "11_repo_bootstrap_manifest",
            "generated_at": now_iso(),
            "freeze_id": freeze_id,
            "purpose": "Materializar la estructura inicial del repositorio Django sin rediseñar la arquitectura.",
            "source_artifacts": list(REQUIRED_INPUTS.values()),
            "project_name": project_name,
            "scope": {
                "apps": apps,
                "route_count": len(routes),
                "entity_count": len(entities),
            },
            "allowed_paths": sorted(set(normalize_path(p) for p in base_allowed_files)),
            "forbidden": {
                "new_dependencies": True,
                "new_apps_outside_contract": True,
                "extra_services": True,
                "spa_frontend": True,
            },
            "notes": [
                "Este bootstrap no define funcionalidades completas por sprint.",
                "Solo crea la base mínima compatible con el freeze para permitir ejecución controlada.",
            ],
            "human_gate": {
                "required": True,
                "status": "Pending",
            },
        }
        return manifest

    def build_sprint_manifest(self, sprint_id: str) -> Dict[str, Any]:
        inputs = self.load_required_inputs()
        stack = inputs["09_stack"]
        design = inputs["10_design"]
        sprint_map = inputs["10a_map"]
        all_routes = extract_routes(inputs["09a_routes"])
        all_entities = extract_entities(inputs["09b_entities"])
        sprint_block = extract_sprint_block(sprint_map, sprint_id)
        freeze_id = extract_freeze_id(design) or extract_freeze_id(sprint_map) or "UNKNOWN_FREEZE"
        project_name = extract_project_name(stack, design)

        scope_route_names = set(extract_scope_names(sprint_block, {"routes", "route_names", "route_ids", "route"}))
        scope_entity_names = set(extract_scope_names(sprint_block, {"entities", "entity_names", "domain_entities", "entity"}))
        scope_apps = set(extract_scope_names(sprint_block, {"apps", "app_names", "app"}))
        scope_templates = set(extract_scope_names(sprint_block, {"templates", "template_paths", "template"}))
        scope_tests = set(extract_scope_names(sprint_block, {"tests", "test_targets", "test_files"}))

        scoped_routes = [r for r in all_routes if route_identifier(r) in scope_route_names] if scope_route_names else []
        scoped_entities = [e for e in all_entities if entity_identifier(e) in scope_entity_names] if scope_entity_names else []

        allowed_paths = {
            f"{project_name}/urls.py",
            f"{project_name}/settings.py",
            "manage.py",
            "templates/",
            "static/",
        }
        for app in scope_apps:
            allowed_paths.update(
                {
                    f"{app}/models.py",
                    f"{app}/views.py",
                    f"{app}/urls.py",
                    f"{app}/forms.py",
                    f"{app}/admin.py",
                    f"{app}/tests.py",
                    f"{app}/migrations/",
                    f"templates/{app}/",
                }
            )
        for template_path in scope_templates:
            allowed_paths.add(template_path)
        for test_target in scope_tests:
            allowed_paths.add(test_target)

        forbidden_routes = sorted({route_identifier(r) for r in all_routes} - scope_route_names) if scope_route_names else []
        forbidden_entities = sorted({entity_identifier(e) for e in all_entities} - scope_entity_names) if scope_entity_names else []

        manifest = {
            "doc_id": f"12_sprint_execution_manifest_{sprint_id}",
            "generated_at": now_iso(),
            "freeze_id": freeze_id,
            "sprint_id": sprint_id,
            "source_artifacts": [
                REQUIRED_INPUTS["09_stack"],
                REQUIRED_INPUTS["09a_routes"],
                REQUIRED_INPUTS["09b_entities"],
                REQUIRED_INPUTS["10_design"],
                REQUIRED_INPUTS["10a_map"],
            ],
            "scope": {
                "apps": sorted(scope_apps),
                "routes": scoped_routes,
                "entities": scoped_entities,
                "templates": sorted(scope_templates),
                "tests": sorted(scope_tests),
                "raw_sprint_block": sprint_block,
            },
            "allowed_paths": sorted(normalize_path(p) for p in allowed_paths),
            "forbidden": {
                "routes": forbidden_routes,
                "entities": forbidden_entities,
                "apps_outside_scope": True,
                "dependencies": True,
                "new_architecture_decisions": True,
            },
            "acceptance_checks": [
                "patch_set_valid",
                "files_only_within_allowed_paths",
                "no_new_apps_outside_scope",
                "no_new_entities_outside_scope",
                "no_new_routes_outside_scope",
                "django_checks_pass",
                "tests_for_sprint_pass",
            ],
            "human_gate": {
                "required": True,
                "status": "Pending",
            },
        }
        return manifest

    def save_manifest_pair(self, manifest: Dict[str, Any]) -> Tuple[Path, Path]:
        doc_id = manifest["doc_id"]
        json_path = self.json_root / f"{doc_id}.json"
        md_path = self.docs_root / f"{doc_id}.md"
        save_json(json_path, manifest)
        save_text(md_path, render_key_value_md(doc_id, manifest))
        return json_path, md_path

    # ---------- patch set ----------
    def validate_patch_set_against_manifest(self, manifest: Dict[str, Any], patch_set: Dict[str, Any]) -> ValidationResult:
        errors = validate_patch_set_schema(patch_set)
        warnings: List[str] = []
        if errors:
            return ValidationResult(False, errors, warnings)

        if patch_set.get("freeze_id") and patch_set.get("freeze_id") != manifest.get("freeze_id"):
            errors.append("El patch set usa un freeze_id distinto al del manifest.")
        if patch_set.get("sprint_id") and manifest.get("sprint_id") and patch_set.get("sprint_id") != manifest.get("sprint_id"):
            errors.append("El patch set usa un sprint_id distinto al del manifest.")

        allowed_paths = manifest.get("allowed_paths", [])
        seen_paths = set()
        for idx, op in enumerate(patch_set["operations"], start=1):
            target = normalize_path(str(op["path"]))
            if target in seen_paths:
                warnings.append(f"La ruta '{target}' aparece repetida en varias operaciones.")
            seen_paths.add(target)
            if not path_in_allowed(target, allowed_paths):
                errors.append(f"Operación #{idx}: ruta fuera de contrato: {target}")
            if ".." in Path(target).parts:
                errors.append(f"Operación #{idx}: ruta insegura: {target}")

        return ValidationResult(not errors, errors, warnings)

    def apply_patch_set(self, patch_set: Dict[str, Any]) -> List[str]:
        changed_paths: List[str] = []
        for op in patch_set["operations"]:
            path = self.repo_root / normalize_path(op["path"])
            path.parent.mkdir(parents=True, exist_ok=True)
            content = op["content"]
            path.write_text(content, encoding="utf-8")
            changed_paths.append(str(path.relative_to(self.repo_root)))
        return changed_paths

    # ---------- validation / reporting ----------
    def collect_repo_snapshot(self) -> Dict[str, str]:
        snapshot: Dict[str, str] = {}
        if not self.repo_root.exists():
            return snapshot
        for file in self.repo_root.rglob("*"):
            if file.is_file():
                rel = str(file.relative_to(self.repo_root)).replace("\\", "/")
                try:
                    snapshot[rel] = sha256_text(file.read_text(encoding="utf-8"))
                except UnicodeDecodeError:
                    snapshot[rel] = "<binary-or-non-utf8>"
        return snapshot

    def diff_snapshots(self, before: Dict[str, str], after: Dict[str, str]) -> Dict[str, List[str]]:
        before_keys = set(before)
        after_keys = set(after)
        created = sorted(after_keys - before_keys)
        deleted = sorted(before_keys - after_keys)
        changed = sorted(k for k in before_keys & after_keys if before[k] != after[k])
        return {"created": created, "changed": changed, "deleted": deleted}

    def validate_repo_diff_against_manifest(self, manifest: Dict[str, Any], diff: Dict[str, List[str]]) -> ValidationResult:
        errors: List[str] = []
        warnings: List[str] = []
        allowed_paths = manifest.get("allowed_paths", [])
        touched = diff["created"] + diff["changed"]
        for path in touched:
            if not path_in_allowed(path, allowed_paths):
                errors.append(f"Archivo modificado fuera de whitelist: {path}")
        if diff["deleted"]:
            errors.append(f"No se permite borrar archivos en esta fase: {', '.join(diff['deleted'])}")
        return ValidationResult(not errors, errors, warnings)

    def build_delivery_report(
        self,
        sprint_or_bootstrap_id: str,
        manifest: Dict[str, Any],
        patch_set: Dict[str, Any],
        diff: Dict[str, List[str]],
        validation: ValidationResult,
    ) -> Dict[str, Any]:
        is_bootstrap = manifest["doc_id"] == "11_repo_bootstrap_manifest"
        prefix = "14" if not is_bootstrap else "11a"
        doc_id = f"{prefix}_delivery_report_{sprint_or_bootstrap_id}"
        report = {
            "doc_id": doc_id,
            "generated_at": now_iso(),
            "freeze_id": manifest.get("freeze_id"),
            "sprint_id": manifest.get("sprint_id"),
            "mode": "bootstrap" if is_bootstrap else "sprint",
            "applied_operations": len(patch_set.get("operations", [])),
            "touched_files": diff["created"] + diff["changed"],
            "created_files": diff["created"],
            "changed_files": diff["changed"],
            "deleted_files": diff["deleted"],
            "validation": {
                "ok": validation.ok,
                "errors": validation.errors,
                "warnings": validation.warnings,
            },
        }
        return report

    def build_contract_validation(
        self,
        sprint_id: str,
        manifest: Dict[str, Any],
        patch_validation: ValidationResult,
        diff_validation: ValidationResult,
    ) -> Dict[str, Any]:
        ok = patch_validation.ok and diff_validation.ok
        return {
            "doc_id": f"14a_sprint_contract_validation_{sprint_id}",
            "generated_at": now_iso(),
            "freeze_id": manifest.get("freeze_id"),
            "sprint_id": sprint_id,
            "ok": ok,
            "checks": {
                "patch_set": {
                    "ok": patch_validation.ok,
                    "errors": patch_validation.errors,
                    "warnings": patch_validation.warnings,
                },
                "repo_diff": {
                    "ok": diff_validation.ok,
                    "errors": diff_validation.errors,
                    "warnings": diff_validation.warnings,
                },
            },
            "human_gate": {
                "required": True,
                "status": "Pending" if not ok else "Review",
            },
        }

    def build_change_request(
        self,
        sprint_id: str,
        manifest: Dict[str, Any],
        reason: str,
        requested_changes: List[Dict[str, Any]],
        impact: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "doc_id": f"14b_change_request_{sprint_id}",
            "generated_at": now_iso(),
            "freeze_id": manifest.get("freeze_id"),
            "sprint_id": sprint_id,
            "reason": reason,
            "requested_changes": requested_changes,
            "impact": impact,
            "decision": {
                "required": True,
                "status": "Pending",
                "approved_by": None,
                "approved_at": None,
            },
        }


# -----------------------------
# CLI
# -----------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Execution runner scaffold for the hybrid human-AI pipeline")
    parser.add_argument("--artifact-root", required=True, help="Directorio donde viven 09/09a/09b/10/10a")
    parser.add_argument("--repo-root", required=True, help="Repositorio Django objetivo")

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")
    sub.add_parser("preflight")
    sub.add_parser("bootstrap-manifest")

    p_prepare = sub.add_parser("prepare-sprint")
    p_prepare.add_argument("--sprint-id", required=True)

    p_validate_patch = sub.add_parser("validate-patchset")
    p_validate_patch.add_argument("--manifest", required=True)
    p_validate_patch.add_argument("--patchset", required=True)

    p_apply = sub.add_parser("apply-patchset")
    p_apply.add_argument("--manifest", required=True)
    p_apply.add_argument("--patchset", required=True)
    p_apply.add_argument("--report-id", required=True, help="bootstrap o sprint id para nombrar el reporte")

    p_change = sub.add_parser("create-change-request")
    p_change.add_argument("--sprint-id", required=True)
    p_change.add_argument("--manifest", required=True)
    p_change.add_argument("--reason", required=True)
    p_change.add_argument("--requested-changes-json", required=True)
    p_change.add_argument("--impact-json", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    runner = ExecutionRunner(Path(args.artifact_root), Path(args.repo_root))

    if args.cmd == "status":
        print(stable_json_dumps(runner.status()))
        return

    if args.cmd == "preflight":
        result = runner.preflight()
        print(stable_json_dumps({"ok": result.ok, "errors": result.errors, "warnings": result.warnings}))
        return

    if args.cmd == "bootstrap-manifest":
        manifest = runner.build_bootstrap_manifest()
        json_path, md_path = runner.save_manifest_pair(manifest)
        print(stable_json_dumps({"ok": True, "json": str(json_path), "md": str(md_path)}))
        return

    if args.cmd == "prepare-sprint":
        manifest = runner.build_sprint_manifest(args.sprint_id)
        json_path, md_path = runner.save_manifest_pair(manifest)
        print(stable_json_dumps({"ok": True, "json": str(json_path), "md": str(md_path)}))
        return

    if args.cmd == "validate-patchset":
        manifest = load_json(Path(args.manifest))
        patch_set = load_json(Path(args.patchset))
        result = runner.validate_patch_set_against_manifest(manifest, patch_set)
        print(stable_json_dumps({"ok": result.ok, "errors": result.errors, "warnings": result.warnings}))
        return

    if args.cmd == "apply-patchset":
        manifest = load_json(Path(args.manifest))
        patch_set = load_json(Path(args.patchset))

        patch_validation = runner.validate_patch_set_against_manifest(manifest, patch_set)
        if not patch_validation.ok:
            print(stable_json_dumps({"ok": False, "stage": "validate_patch_set", "errors": patch_validation.errors}))
            raise SystemExit(2)

        before = runner.collect_repo_snapshot()
        runner.repo_root.mkdir(parents=True, exist_ok=True)
        changed = runner.apply_patch_set(patch_set)
        after = runner.collect_repo_snapshot()
        diff = runner.diff_snapshots(before, after)
        diff_validation = runner.validate_repo_diff_against_manifest(manifest, diff)

        report = runner.build_delivery_report(args.report_id, manifest, patch_set, diff, diff_validation)
        report_json = runner.json_root / f"{report['doc_id']}.json"
        report_md = runner.docs_root / f"{report['doc_id']}.md"
        save_json(report_json, report)
        save_text(report_md, render_key_value_md(report["doc_id"], report))

        out = {
            "ok": diff_validation.ok,
            "applied_operations": len(changed),
            "changed": changed,
            "report_json": str(report_json),
            "report_md": str(report_md),
            "errors": diff_validation.errors,
            "warnings": diff_validation.warnings,
        }
        print(stable_json_dumps(out))
        return

    if args.cmd == "create-change-request":
        manifest = load_json(Path(args.manifest))
        requested_changes = json.loads(Path(args.requested_changes_json).read_text(encoding="utf-8"))
        impact = json.loads(Path(args.impact_json).read_text(encoding="utf-8"))
        cr = runner.build_change_request(args.sprint_id, manifest, args.reason, requested_changes, impact)
        cr_json = runner.json_root / f"{cr['doc_id']}.json"
        cr_md = runner.docs_root / f"{cr['doc_id']}.md"
        save_json(cr_json, cr)
        save_text(cr_md, render_key_value_md(cr["doc_id"], cr))
        print(stable_json_dumps({"ok": True, "json": str(cr_json), "md": str(cr_md)}))
        return

    parser.error("Comando no soportado")


if __name__ == "__main__":
    main()
