from __future__ import annotations

import pytest


@pytest.mark.test_id("T-PAY-01")
@pytest.mark.requirement("B6", "3.5")
@pytest.mark.metric("M6", "M7")
def test_cash_on_delivery_payment_method_available(page, adapter):
    adapter.add_first_boat_to_cart(page)
    adapter.goto(page, "checkout")
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
    }.items():
        adapter.fill_by_name(page, key, value)
    adapter.submit_form_with_fields(page, ["first_name", "last_name", "email", "phone"])
    page.wait_for_load_state("domcontentloaded")
    assert adapter.has_any_text(page, ["contra", "reembolso", "pendiente", "entrega", "pagar al momento"])


@pytest.mark.test_id("T-PAY-02")
@pytest.mark.requirement("B6", "3.5")
@pytest.mark.metric("M6", "M7")
def test_paypal_sandbox_payment_method_available(page, adapter):
    adapter.add_first_boat_to_cart(page)
    adapter.goto(page, "checkout")
    assert adapter.has_any_text(page, ["paypal", "sandbox"]) or page.locator('[src*="paypal"], script[src*="paypal"]').count() > 0


@pytest.mark.test_id("T-TRACK-01")
@pytest.mark.requirement("B7", "3.5")
@pytest.mark.metric("M6", "M7")
def test_tracking_code_generated_after_checkout(page, adapter):
    code = adapter.run_basic_checkout(page, "contra_reembolso")
    assert code


@pytest.mark.test_id("T-TRACK-02")
@pytest.mark.requirement("B10", "3.7")
@pytest.mark.metric("M6", "M7")
def test_tracking_code_query_without_login(page, adapter):
    code = adapter.run_basic_checkout(page, "contra_reembolso")
    if not code:
        pytest.skip("blocked: no se pudo obtener codigo de seguimiento previo")
    adapter.goto(page, "logout")
    adapter.goto(page, "tracking")
    tracking_field = adapter.config.get("fields", {}).get("tracking_code")
    if tracking_field:
        adapter.fill_by_name(page, tracking_field, code)
        adapter.submit_first_form(page)
    else:
        page.goto(adapter.url("tracking", reservation=code), wait_until="domcontentloaded")
    page.wait_for_load_state("domcontentloaded")
    assert adapter.has_any_text(page, [code.lower(), "reserva", "pendiente", "pagado", "estado"])


@pytest.mark.test_id("T-TRACK-03")
@pytest.mark.requirement("B9", "3.6")
@pytest.mark.metric("M6", "M7")
def test_cancel_pending_reservation_rule_observable(page, adapter):
    code = adapter.run_basic_checkout(page, "contra_reembolso")
    if not code:
        pytest.skip("blocked: no se pudo crear reserva pendiente observable")
    adapter.goto(page, "tracking")
    tracking_field = adapter.config.get("fields", {}).get("tracking_code")
    if tracking_field:
        adapter.fill_by_name(page, tracking_field, code)
        adapter.submit_first_form(page)
    page.wait_for_load_state("domcontentloaded")
    assert adapter.has_any_text(page, ["cancel", "pendiente"])
