"""Unit tests de APPLICATION: el use case se prueba con un FAKE del Port.

Esta es la gran ventaja de hexagonal: no necesitamos el JSON/DB/API real
para probar la lógica del caso de uso.
"""

import pytest

from practica_mcp.modules.employees.application.use_cases.get_employee import GetEmployee
from practica_mcp.modules.employees.domain.employee import Employee, EmployeeId
from practica_mcp.modules.employees.domain.errors import (
    EmployeeNotFoundError,
    InvalidEmployeeIdError,
)


class FakeEmployeeRepository:
    """Cumple el Protocol EmployeeRepository sin heredar de él."""

    def __init__(self, employees: list[Employee]) -> None:
        self._employees = {e.id: e for e in employees}

    async def get_by_id(self, employee_id: EmployeeId) -> Employee | None:
        return self._employees.get(employee_id)

    async def list_all(self) -> list[Employee]:
        return list(self._employees.values())


ANA = Employee(EmployeeId("EMP-001"), "Ana López", "Finanzas", "Analista", True)


async def test_devuelve_el_empleado():
    use_case = GetEmployee(FakeEmployeeRepository([ANA]))
    assert await use_case.execute("EMP-001") == ANA


async def test_empleado_inexistente():
    use_case = GetEmployee(FakeEmployeeRepository([ANA]))
    with pytest.raises(EmployeeNotFoundError):
        await use_case.execute("EMP-999")


async def test_id_invalido_no_llega_al_repositorio():
    use_case = GetEmployee(FakeEmployeeRepository([ANA]))
    with pytest.raises(InvalidEmployeeIdError):
        await use_case.execute("hola")
