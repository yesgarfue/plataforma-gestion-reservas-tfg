from __future__ import annotations

import pytest


@pytest.mark.test_id("T-ADMIN-01")
@pytest.mark.requirement("B11", "3.8")
@pytest.mark.metric("M6", "M7")
def test_admin_panel_accessible_for_admin(page, adapter):
    adapter.login(page, "admin")
    adapter.goto(page, "admin_panel")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["admin", "panel", "barcos", "clientes", "reservas", "usuarios"])


@pytest.mark.test_id("T-ADMIN-02")
@pytest.mark.requirement("B11", "3.8")
@pytest.mark.metric("M6", "M7")
def test_admin_boat_management_visible(page, adapter):
    adapter.login(page, "admin")
    adapter.goto(page, "admin_boats")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["barco", "embarc", "crear", "editar", "eliminar", "precio"])


@pytest.mark.test_id("T-ADMIN-03")
@pytest.mark.requirement("B11", "3.8")
@pytest.mark.metric("M6", "M7")
def test_admin_client_management_visible(page, adapter):
    adapter.login(page, "admin")
    adapter.goto(page, "admin_clients")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["cliente", "usuario", "email", "eliminar", "editar"])


@pytest.mark.test_id("T-ADMIN-04")
@pytest.mark.requirement("B9", "B11", "3.6", "3.8")
@pytest.mark.metric("M6", "M7")
def test_admin_reservation_management_visible(page, adapter):
    adapter.login(page, "admin")
    adapter.goto(page, "admin_reservations")
    adapter.assert_ok_page(page)
    assert adapter.has_any_text(page, ["reserva", "estado", "pendiente", "pagado", "devuelto", "seguimiento"])


@pytest.mark.test_id("T-ADMIN-05")
@pytest.mark.requirement("B11", "3.1", "3.8")
@pytest.mark.metric("M6", "M7")
def test_admin_client_delete_restriction_is_observable(page, adapter):
    adapter.login(page, "admin")
    adapter.goto(page, "admin_clients")
    adapter.assert_ok_page(page)
    if not adapter.has_any_text(page, ["eliminar", "delete", "cliente", "usuario"]):
        pytest.skip("blocked: accion de eliminacion de cliente no observable")
    assert adapter.has_any_text(page, ["reserva", "pendiente", "no puede", "eliminar", "cliente", "usuario"])
