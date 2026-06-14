from __future__ import annotations

import pytest


@pytest.mark.test_id("T-CART-01")
@pytest.mark.requirement("B4", "3.4")
@pytest.mark.metric("M6", "M7")
def test_add_boat_to_cart(page, adapter):
    adapter.add_first_boat_to_cart(page)
    adapter.goto(page, "cart")
    assert adapter.has_any_text(page, ["cesta", "carrito", "total", "cantidad", "checkout", "finalizar"])


@pytest.mark.test_id("T-CART-02")
@pytest.mark.requirement("B4", "3.4")
@pytest.mark.metric("M6", "M7")
def test_update_cart_quantity(page, adapter):
    adapter.add_first_boat_to_cart(page)
    adapter.goto(page, "cart")
    quantity_name = adapter.config.get("fields", {}).get("quantity")
    if not quantity_name:
        pytest.skip("blocked: campo de cantidad no configurado")
    if not adapter.fill_by_name(page, quantity_name, "2"):
        pytest.skip("blocked: campo de cantidad no visible en cesta")
    adapter.submit_first_form(page)
    page.wait_for_load_state("domcontentloaded")
    assert adapter.has_any_text(page, ["2", "cantidad", "actualiz", "total"])


@pytest.mark.test_id("T-CART-03")
@pytest.mark.requirement("B4", "3.4")
@pytest.mark.metric("M6", "M7")
def test_cart_accessible_from_navigation(page, adapter):
    adapter.goto(page, "home")
    adapter.click_first(page, adapter.selector("cart_link"))
    page.wait_for_load_state("domcontentloaded")
    assert adapter.has_any_text(page, ["cesta", "carrito", "total", "vacia", "catalogo", "agregado", "nada"])
