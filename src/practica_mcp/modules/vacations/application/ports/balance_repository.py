from typing import Protocol

from practica_mcp.modules.vacations.domain.balance import VacationBalance


class BalanceRepository(Protocol):
    async def get_by_employee(self, employee_id: str) -> VacationBalance | None: ...
