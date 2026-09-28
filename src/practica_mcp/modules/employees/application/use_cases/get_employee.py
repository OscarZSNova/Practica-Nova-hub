"""USE CASE: orquesta UN caso de uso.

Pasos típicos: validar entrada -> pedir datos vía Port -> aplicar reglas -> devolver.
No conoce MCP, ni JSON, ni SQL. Solo Domain + Ports.
"""

from practica_mcp.modules.employees.application.ports.employee_repository import (
    EmployeeRepository,
)
from practica_mcp.modules.employees.domain.employee import Employee, EmployeeId
from practica_mcp.modules.employees.domain.errors import EmployeeNotFoundError


class GetEmployee:
    def __init__(self, repository: EmployeeRepository) -> None:
        # Recibe el Port por constructor (inyección de dependencias).
        # En tests le pasamos un Fake; en producción, el Adapter real.
        self._repository = repository

    async def execute(self, employee_id: str) -> Employee:
        emp_id = EmployeeId(employee_id)  # valida formato (puede lanzar InvalidEmployeeIdError)
        employee = await self._repository.get_by_id(emp_id)
        if employee is None:
            raise EmployeeNotFoundError(employee_id)
        return employee
