from typing import Annotated

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

from practica_mcp.modules.vacations.application.use_cases.get_balance import GetBalance
from practica_mcp.modules.vacations.domain.errors import VacationError
from practica_mcp.modules.vacations.interfaces.mcp.schemas import BalanceOutput


def register_tools(mcp: MCPServer, *, get_balance: GetBalance) -> None:
    @mcp.tool(
        name="vacations.balance.get",
        description="Saldo de vacaciones de un empleado: días otorgados, usados y restantes.",
    )
    async def get_balance_tool(
        employee_id: Annotated[str, Field(description="ID del empleado, ej. EMP-001")],
    ) -> BalanceOutput:
        try:
            balance = await get_balance.execute(employee_id)
        except VacationError as error:
            raise ToolError(str(error)) from error
        return BalanceOutput.from_domain(balance)

    # EJERCICIO (Persona 2): agregar aquí la tool "vacations.request.create".
    # Ver EJERCICIOS.md.
