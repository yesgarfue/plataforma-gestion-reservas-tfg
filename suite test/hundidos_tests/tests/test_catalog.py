from __future__ import annotations

from datetime import date, timedelta

import pytest


@pytest.mark.test_id("T-CAT-01")
@pytest.mark.requirement("B2", "3.2")
@pytest.mark.metric("M6", "M7", "M-operatividad")
def test_catalog_lists_boats(page, adapter):
    adapter.goto(page, "catalog")
    adapter.assert_ok_page(page)
    assert page.locator(adapter.selector("boat_card")).count() > 0
    assert adapter.has_any_text(page, ["barco", "embarcacion", "embarcación", "precio", "puerto"])


@pytest.mark.test_id("T-CAT-02")
@pytest.mark.requirement("B3", "3.3")
@pytest.mark.metric("M6", "M7")
def test_boat_detail_is_accessible(page, adapter):
    adapter.open_first_boat_detail(page)
    assert adapter.has_any_text(page, ["capacidad", "precio", "puerto", "fabricante", "categoria", "categoría"])


@pytest.mark.test_id("T-CAT-03")
@pytest.mark.requirement("B2", "3.2")
@pytest.mark.metric("M6", "M7")
def test_search_by_boat_name(page, adapter):
    query_name = adapter.query_name("search")
    term = adapter.data("known_boat_name", "a")
    page.goto(adapter.url("catalog", **{query_name: term}), wait_until="domcontentloaded")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["barco", "embarcacion", "embarcación", "resultado", "precio"])


@pytest.mark.test_id("T-CAT-04")
@pytest.mark.requirement("B2", "3.2")
@pytest.mark.metric("M6", "M7")
def test_filter_by_port(page, adapter):
    value = adapter.data("puerto")
    if not value:
        pytest.skip("blocked: puerto seed no configurado en adaptador")
    page.goto(adapter.url("catalog", **{adapter.query_name("puerto"): value}), wait_until="domcontentloaded")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, [value, "barco", "precio"])


@pytest.mark.test_id("T-CAT-05")
@pytest.mark.requirement("B2", "3.2")
@pytest.mark.metric("M6", "M7")
def test_filter_by_manufacturer(page, adapter):
    value = adapter.data("fabricante")
    if not value:
        pytest.skip("blocked: fabricante seed no configurado en adaptador")
    page.goto(adapter.url("catalog", **{adapter.query_name("fabricante"): value}), wait_until="domcontentloaded")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, [value, "barco", "precio"])


@pytest.mark.test_id("T-CAT-06")
@pytest.mark.requirement("B2", "3.2")
@pytest.mark.metric("M6", "M7")
def test_combined_port_manufacturer_price_filters(page, adapter):
    puerto = adapter.data("puerto")
    fabricante = adapter.data("fabricante")
    if not puerto or not fabricante:
        pytest.skip("blocked: puerto/fabricante seed no configurados en adaptador")
    query = {
        adapter.query_name("puerto"): puerto,
        adapter.query_name("fabricante"): fabricante,
        adapter.query_name("min_price"): adapter.data("min_price", "0"),
        adapter.query_name("max_price"): adapter.data("max_price", "9999"),
    }
    page.goto(adapter.url("catalog", **query), wait_until="domcontentloaded")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["barco", "precio", puerto, fabricante])


@pytest.mark.test_id("T-CAT-07")
@pytest.mark.requirement("B2", "3.2")
@pytest.mark.metric("M6", "M7")
def test_date_availability_filter_keeps_catalog_visible(page, adapter):
    start = (date.today() + timedelta(days=30)).isoformat()
    end = (date.today() + timedelta(days=32)).isoformat()
    query = {
        adapter.query_name("start_date"): start,
        adapter.query_name("end_date"): end,
    }
    page.goto(adapter.url("catalog", **query), wait_until="domcontentloaded")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["barco", "precio", "disponible", "no disponible", "embarc"])
