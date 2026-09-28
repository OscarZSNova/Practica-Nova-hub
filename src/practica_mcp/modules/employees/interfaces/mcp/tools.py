"""INTERFACES / MCP: las Tools. Adaptan MCP -> Application.

Una Tool debe ser DELGADA:
  1. recibir argumentos
  2. llamar al use case
  3. traducir errores de dominio a ToolError
  4. devolver el schema de salida

Nunca: SQL, lectura de archivos, llamadas HTTP o reglas de negocio aquí.
"""

from typing import Annotated

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

from practica_mcp.modules.employees.application.use_cases.get_employee import GetEmployee
from practica_mcp.modules.employees.domain.errors import EmployeeError
from practica_mcp.modules.employees.interfaces.mcp.schemas import EmployeeOutput


def register_tools(mcp: MCPServer, *, get_employee: GetEmployee) -> None:
    # Nombre público: <bounded_context>.<resource>.<operation>
    @mcp.tool(
        name="employees.employee.get",
        description="Obtiene los datos básicos de un empleado por su ID (formato EMP-000).",
    )
    async def get_employee_tool(
        employee_id: Annotated[str, Field(description="ID del empleado, ej. EMP-001")],
    ) -> EmployeeOutput:
        try:
            employee = await get_employee.execute(employee_id)
        except EmployeeError as error:
            # Error de negocio esperado -> se muestra al cliente como error de la Tool.
            raise ToolError(str(error)) from error
        return EmployeeOutput.from_domain(employee)

    # EJERCICIO (Persona 1): agregar aquí la tool "employees.employee.search".
    # Ver EJERCICIOS.md.
