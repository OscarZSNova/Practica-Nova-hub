"""COMPOSITION ROOT del módulo: donde se "conectan los cables".

Aquí (y solo aquí) se decide qué Adapter concreto implementa cada Port,
se construyen los use cases y se registran las Tools.

Agregar una Tool nueva = tocar este archivo y tools.py; NUNCA apps/factory.py.
"""

from mcp.server import MCPServer

from practica_mcp.modules.employees.application.ports.employee_repository import (
    EmployeeRepository,
)
from practica_mcp.modules.employees.application.use_cases.get_employee import GetEmployee
from practica_mcp.modules.employees.infrastructure.persistence.json_employee_repository import (
    JsonEmployeeRepository,
)
from practica_mcp.modules.employees.interfaces.mcp.tools import register_tools


def register(mcp: MCPServer, repository: EmployeeRepository | None = None) -> None:
    # `repository` es opcional para que los tests puedan inyectar un Fake.
    repository = repository or JsonEmployeeRepository()

    register_tools(
        mcp,
        get_employee=GetEmployee(repository),
    )
