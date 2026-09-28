import pytest

from practica_mcp.modules.vacations.application.use_cases.get_balance import GetBalance
from practica_mcp.modules.vacations.domain.balance import VacationBalance
from practica_mcp.modules.vacations.domain.errors import BalanceNotFoundError, InvalidBalanceError
from practica_mcp.modules.vacations.infrastructure.mappers.balance_mapper import to_domain


class FakeBalanceRepository:
    def __init__(self, balances: list[VacationBalance]) -> None:
        self._balances = {b.employee_id: b for b in balances}

    async def get_by_employee(self, employee_id: str) -> VacationBalance | None:
        return self._balances.get(employee_id)


# --- Domain ---


def test_dias_restantes():
    assert VacationBalance("EMP-001", 2026, 12, 5).remaining_days == 7


def test_no_se_puede_usar_mas_de_lo_otorgado():
    with pytest.raises(InvalidBalanceError):
        VacationBalance("EMP-001", 2026, 12, 13)


@pytest.mark.parametrize(("days", "expected"), [(0, False), (1, True), (7, True), (8, False)])
def test_can_take(days, expected):
    assert VacationBalance("EMP-001", 2026, 12, 5).can_take(days) is expected


# --- Mapper ---


def test_mapper():
    raw = {"empleado": "EMP-001", "anio": 2026, "dias_ley": 12, "dias_tomados": 5}
    assert to_domain(raw) == VacationBalance("EMP-001", 2026, 12, 5)


# --- Application ---


async def test_get_balance_normaliza_el_id():
    use_case = GetBalance(FakeBalanceRepository([VacationBalance("EMP-001", 2026, 12, 5)]))
    balance = await use_case.execute(" emp-001 ")
    assert balance.remaining_days == 7


async def test_get_balance_inexistente():
    use_case = GetBalance(FakeBalanceRepository([]))
    with pytest.raises(BalanceNotFoundError):
        await use_case.execute("EMP-404")
