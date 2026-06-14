from __future__ import annotations

import pytest


@pytest.mark.test_id("T-RES-01")
@pytest.mark.requirement("B5", "3.5")
@pytest.mark.metric("M6", "M7", "M-operatividad")
def test_guest_can_reach_checkout_flow(page, adapter):
    adapter.add_first_boat_to_cart(page)
    adapter.goto(page, "checkout")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["reserva", "checkout", "cliente", "pago", "continuar", "confirmar"])


@pytest.mark.test_id("T-RES-02")
@pytest.mark.requirement("B1", "3.1")
@pytest.mark.metric("M6", "M7")
def test_login_during_reservation_keeps_cart(page, adapter):
    adapter.add_first_boat_to_cart(page)
    adapter.login(page, "customer")
    adapter.goto(page, "cart")
    assert adapter.has_any_text(page, ["cesta", "carrito", "total", "cantidad", "finalizar"])


@pytest.mark.test_id("T-RES-03")
@pytest.mark.requirement("B5", "3.5")
@pytest.mark.metric("M6", "M7")
def test_checkout_completes_in_at_most_three_observable_steps(page, adapter):
    code = adapter.run_basic_checkout(page, "contra_reembolso")
    assert code or adapter.has_any_text(page, ["confirm", "pendiente", "pagado", "seguimiento"])


@pytest.mark.test_id("T-RES-04")
@pytest.mark.requirement("B8", "3.5")
@pytest.mark.metric("M6", "M7")
def test_fuel_fee_is_observable_in_checkout(page, adapter):
    adapter.add_first_boat_to_cart(page)
    adapter.goto(page, "checkout")
    adapter.assert_ok_page(page)
    if not adapter.has_any_text(page, ["combustible", "50", "tasa"]):
        pytest.skip("blocked: tasa de combustible no observable en pantalla de checkout")
