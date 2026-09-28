"""Unit tests de DOMAIN: sin red, sin archivos, sin MCP. Solo reglas puras."""

import pytest

from practica_mcp.modules.employees.domain.employee import Employee, EmployeeId
from practica_mcp.modules.employees.domain.errors import InvalidEmployeeIdError


def test_employee_id_valido():
    assert str(EmployeeId("EMP-001")) == "EMP-001"


@pytest.mark.parametrize("value", ["", "EMP-1", "emp-001", "XYZ-001", "EMP-0001"])
def test_employee_id_invalido(value):
    with pytest.raises(InvalidEmployeeIdError):
        EmployeeId(value)


def test_belongs_to_ignora_mayusculas_y_espacios():
    employee = Employee(EmployeeId("EMP-001"), "Ana", "Finanzas", "Analista", True)
    assert employee.belongs_to("  finanzas ")
    assert not employee.belongs_to("Tecnología")
