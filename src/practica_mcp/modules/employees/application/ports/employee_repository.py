"""PORT: la interfaz que Application NECESITA del mundo exterior.

Application dice "necesito obtener empleados", pero NO dice cómo
(JSON, SQL, GraphQL de NovaHub...). Eso lo decide un Adapter en infrastructure/.

Usamos `Protocol` (tipado estructural): cualquier clase con estos métodos
cumple el contrato, sin necesidad de heredar.
"""

from typing import Protocol

from practica_mcp.modules.employees.domain.employee import Employee, EmployeeId


class EmployeeRepository(Protocol):
    async def get_by_id(self, employee_id: EmployeeId) -> Employee | None: ...

    async def list_all(self) -> list[Employee]: ...
