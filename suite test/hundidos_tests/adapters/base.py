from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import time
from urllib.parse import urlencode

import yaml
from playwright.sync_api import Page, expect


class BlockedTest(RuntimeError):
    """Raised when an observable precondition is not available."""


@dataclass
class ProductAdapter:
    config: dict[str, Any]

    @classmethod
    def from_file(cls, path: Path, base_url: str | None = None) -> "ProductAdapter":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if base_url:
            data["base_url"] = base_url.rstrip("/")
        return cls(data)

    @property
    def name(self) -> str:
        return self.config["name"]

    @property
    def base_url(self) -> str:
        return self.config["base_url"].rstrip("/")

    def path(self, key: str, required: bool = True) -> str | None:
        value = self.config.get("paths", {}).get(key)
        if required and not value:
            raise BlockedTest(f"Ruta no configurada: {key}")
        return value

    def url(self, key: str, **query: str) -> str:
        path = self.path(key)
        url = f"{self.base_url}{path}"
        clean_query = {k: v for k, v in query.items() if v not in (None, "")}
        if clean_query:
            url = f"{url}?{urlencode(clean_query, doseq=True)}"
        return url

    def query_name(self, key: str) -> str:
        value = self.config.get("query", {}).get(key)
        if not value:
            raise BlockedTest(f"Parametro de query no configurado: {key}")
        return value

    def field(self, group: str, name: str | None = None) -> str:
        fields = self.config.get("fields", {})
        value = fields.get(group, {}).get(name) if name else fields.get(group)
        if not value:
            raise BlockedTest(f"Campo no configurado: {group}.{name}" if name else f"Campo no configurado: {group}")
        return value

    def selector(self, key: str) -> str:
        value = self.config.get("selectors", {}).get(key)
        if not value:
            raise BlockedTest(f"Selector no configurado: {key}")
        return value

    def data(self, key: str, default: str = "") -> str:
        return self.config.get("test_data", {}).get(key, default)

    def credential(self, role: str, key: str) -> str:
        value = self.config.get("credentials", {}).get(role, {}).get(key)
        if not value:
            raise BlockedTest(f"Credencial no configurada: {role}.{key}")
        return value

    def credential_candidates(self, role: str) -> list[dict[str, str]]:
        configured = self.config.get("credential_candidates", {}).get(role, [])
        candidates = [item for item in configured if item.get("email") and item.get("password")]
        primary = self.config.get("credentials", {}).get(role, {})
        if primary.get("email") and primary.get("password"):
            candidates.insert(0, primary)
        seen = set()
        unique = []
        for item in candidates:
            key = (item["email"], item["password"])
            if key not in seen:
                seen.add(key)
                unique.append(item)
        return unique

    def goto(self, page: Page, key: str, **query: str) -> None:
        page.goto(self.url(key, **query), wait_until="domcontentloaded")

    def assert_ok_page(self, page: Page) -> None:
        expect(page.locator("body")).to_be_visible()

    def fill_by_name(self, page: Page, name: str, value: str) -> bool:
        locator = page.locator(f'[name="{name}"]').first
        if locator.count() == 0:
            return False
        locator.fill(value)
        return True

    def choose_by_name(self, page: Page, name: str, value: str) -> bool:
        locator = page.locator(f'[name="{name}"]').first
        if locator.count() == 0:
            return False
        tag = locator.evaluate("el => el.tagName.toLowerCase()")
        input_type = locator.get_attribute("type") or ""
        if tag == "select":
            locator.select_option(value=value)
        elif input_type in {"checkbox", "radio"}:
            page.locator(f'[name="{name}"][value="{value}"]').first.check()
        else:
            locator.fill(value)
        return True

    def click_first(self, page: Page, selector: str) -> None:
        locator = page.locator(selector)
        if locator.count() == 0:
            raise BlockedTest(f"No se encontro elemento: {selector}")
        for index in range(locator.count()):
            candidate = locator.nth(index)
            if candidate.is_visible():
                candidate.click()
                return
        raise BlockedTest(f"No se encontro elemento visible: {selector}")

    def submit_first_form(self, page: Page) -> None:
        submit = page.locator(self.selector("submit"))
        if submit.count() == 0:
            raise BlockedTest("No se encontro boton submit")
        for index in range(submit.count()):
            candidate = submit.nth(index)
            if candidate.is_visible():
                candidate.click()
                return
        raise BlockedTest("No se encontro boton submit visible")

    def submit_form_with_fields(self, page: Page, field_names: list[str]) -> None:
        selectors = "".join(f':has([name="{name}"])' for name in field_names)
        submit = page.locator(f"form{selectors} {self.selector('submit')}")
        if submit.count() == 0:
            self.submit_first_form(page)
            return
        for index in range(submit.count()):
            candidate = submit.nth(index)
            if candidate.is_visible():
                candidate.click()
                return
        raise BlockedTest("No se encontro boton submit visible en el formulario esperado")

    def visible_text(self, page: Page) -> str:
        return page.locator("body").inner_text(timeout=5000).lower()

    def has_any_text(self, page: Page, terms: list[str]) -> bool:
        text = self.visible_text(page)
        return any(term.lower() in text for term in terms)

    def login(self, page: Page, role: str = "customer") -> None:
        candidates = self.credential_candidates(role)
        if not candidates:
            raise BlockedTest(f"Credenciales no configuradas: {role}")

        for credentials in candidates:
            self.goto(page, "login")
            self.assert_ok_page(page)
            self.fill_by_name(page, self.field("login", "email"), credentials["email"])
            self.fill_by_name(page, self.field("login", "password"), credentials["password"])
            self.submit_form_with_fields(page, [self.field("login", "email"), self.field("login", "password")])
            page.wait_for_load_state("domcontentloaded")
            if self.has_any_text(page, ["cerrar", "salir", "logout", "mi cuenta", "dashboard", "panel"]):
                return
        if role == "customer":
            email = f"ft-login-{int(time.time() * 1000)}@example.com"
            password = "Test1234!"
            self.register_unique_customer(page, email, password)
            self.goto(page, "logout")
            page.wait_for_load_state("domcontentloaded")
            self.goto(page, "login")
            self.fill_by_name(page, self.field("login", "email"), email)
            self.fill_by_name(page, self.field("login", "password"), password)
            self.submit_form_with_fields(page, [self.field("login", "email"), self.field("login", "password")])
            page.wait_for_load_state("domcontentloaded")
            if self.has_any_text(page, ["cerrar", "salir", "logout", "mi cuenta", "dashboard", "panel"]):
                return
        raise BlockedTest(f"No se pudo iniciar sesion como {role} con credenciales seed")

    def register_unique_customer(self, page: Page, email: str, password: str) -> None:
        self.goto(page, "register")
        self.assert_ok_page(page)
        register_fields = self.config.get("fields", {}).get("register", {})
        values = {
            "username": email,
            "first_name": "Test",
            "last_name": "Funcional",
            "phone_number": "600000000",
            "email": email,
            "password": password,
            "confirm_password": password,
            "password1": password,
            "password2": password,
        }
        filled = 0
        for logical_name, html_name in register_fields.items():
            if html_name and self.fill_by_name(page, html_name, values.get(logical_name, "Test")):
                filled += 1
        if filled < 2:
            raise BlockedTest("Formulario de registro no reconocible")
        expected_fields = [html_name for html_name in register_fields.values() if html_name]
        self.submit_form_with_fields(page, expected_fields[:2])
        page.wait_for_load_state("domcontentloaded")

    def open_first_boat_detail(self, page: Page) -> None:
        self.goto(page, "catalog")
        self.assert_ok_page(page)
        link = page.locator(self.selector("boat_link"))
        for index in range(link.count()):
            candidate = link.nth(index)
            href = candidate.get_attribute("href") or ""
            if candidate.is_visible() and href and href.rstrip("/") != self.path("catalog").rstrip("/"):
                candidate.click()
                page.wait_for_load_state("domcontentloaded")
                return
        detail_path = self.config.get("test_data", {}).get("known_boat_path")
        if detail_path:
            page.goto(f"{self.base_url}{detail_path}", wait_until="domcontentloaded")
            self.assert_ok_page(page)
            return
        raise BlockedTest("No hay enlace visible a ficha de barco")

    def add_first_boat_to_cart(self, page: Page, quantity: str = "1") -> None:
        self.open_first_boat_detail(page)
        quantity_field = self.config.get("fields", {}).get("quantity")
        if quantity_field:
            self.fill_by_name(page, quantity_field, quantity)
        self.click_first(page, self.selector("add_to_cart"))
        page.wait_for_load_state("domcontentloaded")

    def get_tracking_code_from_page(self, page: Page) -> str:
        text = page.locator("body").inner_text(timeout=5000)
        import re

        patterns = [
            r"[Cc]odigo de [Ss]eguimiento[:\s]+([A-Za-z0-9-]{6,64})",
            r"[Cc]ódigo de [Ss]eguimiento[:\s]+([A-Za-z0-9-]{6,64})",
            r"\b([0-9a-fA-F]{8}-[0-9a-fA-F-]{8,})\b",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        raise BlockedTest("No se encontro codigo de seguimiento observable")

    def run_basic_checkout(self, page: Page, payment_value: str = "contra_reembolso") -> str | None:
        self.add_first_boat_to_cart(page)
        checkout = self.path("checkout", required=False)
        if checkout:
            page.goto(f"{self.base_url}{checkout}", wait_until="domcontentloaded")
        self.assert_ok_page(page)

        for key, value in {
            "first_name": "Test",
            "last_name": "Funcional",
            "email": "cliente.test@example.com",
            "phone": "600000000",
            "address_line_1": "Puerto de prueba",
            "address_line_2": "S/N",
            "country": "Espana",
            "city": "Sevilla",
            "state": "28001",
            "fecha_inicio": "2026-06-10",
            "fecha_fin": "2026-06-12",
            "start_date": "2026-06-10",
            "end_date": "2026-06-12",
        }.items():
            self.fill_by_name(page, key, value)

        payment_field = self.config.get("fields", {}).get("payment_method")
        if payment_field:
            self.choose_by_name(page, payment_field, payment_value)
        for terms_name in ["aceptar_terminos", "terms", "accept_terms"]:
            locator = page.locator(f'[name="{terms_name}"]').first
            if locator.count():
                locator.check()

        for _ in range(3):
            if self.has_any_text(page, ["confirmacion", "confirmación", "codigo de seguimiento", "código de seguimiento"]):
                break
            submit = page.locator(self.selector("submit")).first
            if submit.count() == 0:
                break
            submit.click()
            page.wait_for_load_state("domcontentloaded")

        try:
            return self.get_tracking_code_from_page(page)
        except BlockedTest:
            return None
