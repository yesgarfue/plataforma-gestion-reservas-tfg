from __future__ import annotations

import time

import pytest


@pytest.mark.test_id("T-AUTH-01")
@pytest.mark.requirement("B1", "3.1")
@pytest.mark.metric("M6", "M7")
def test_customer_registration(page, adapter):
    email = f"ft-{int(time.time() * 1000)}@example.com"
    adapter.register_unique_customer(page, email, "Test1234!")
    assert adapter.has_any_text(page, ["salir", "logout", "dashboard", "perfil", "sesion", "sesión", "registr"])


@pytest.mark.test_id("T-AUTH-02")
@pytest.mark.requirement("B1", "3.1")
@pytest.mark.metric("M6", "M7")
def test_customer_login(page, adapter):
    adapter.login(page, "customer")
    assert adapter.has_any_text(page, ["salir", "logout", "dashboard", "perfil", "mi cuenta", "cerrar"])


@pytest.mark.test_id("T-AUTH-03")
@pytest.mark.requirement("B1", "3.1")
@pytest.mark.metric("M6", "M7")
def test_explicit_logout(page, adapter):
    adapter.login(page, "customer")
    adapter.goto(page, "logout")
    page.wait_for_load_state("domcontentloaded")
    assert adapter.has_any_text(page, ["login", "entrar", "iniciar", "registro", "registr"])
