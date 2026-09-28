from mcp.server import MCPServer

from practica_mcp.modules.vacations.application.ports.balance_repository import BalanceRepository
from practica_mcp.modules.vacations.application.use_cases.get_balance import GetBalance
from practica_mcp.modules.vacations.infrastructure.persistence.json_balance_repository import (
    JsonBalanceRepository,
)
from practica_mcp.modules.vacations.interfaces.mcp.tools import register_tools


def register(mcp: MCPServer, repository: BalanceRepository | None = None) -> None:
    repository = repository or JsonBalanceRepository()

    register_tools(
        mcp,
        get_balance=GetBalance(repository),
    )
