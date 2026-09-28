from practica_mcp.modules.vacations.application.ports.balance_repository import BalanceRepository
from practica_mcp.modules.vacations.domain.balance import VacationBalance
from practica_mcp.modules.vacations.domain.errors import BalanceNotFoundError


class GetBalance:
    def __init__(self, repository: BalanceRepository) -> None:
        self._repository = repository

    async def execute(self, employee_id: str) -> VacationBalance:
        balance = await self._repository.get_by_employee(employee_id.strip().upper())
        if balance is None:
            raise BalanceNotFoundError(employee_id)
        return balance
