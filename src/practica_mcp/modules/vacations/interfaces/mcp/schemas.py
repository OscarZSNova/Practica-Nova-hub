from pydantic import BaseModel

from practica_mcp.modules.vacations.domain.balance import VacationBalance


class BalanceOutput(BaseModel):
    employee_id: str
    year: int
    entitled_days: int
    used_days: int
    remaining_days: int

    @classmethod
    def from_domain(cls, balance: VacationBalance) -> "BalanceOutput":
        return cls(
            employee_id=balance.employee_id,
            year=balance.year,
            entitled_days=balance.entitled_days,
            used_days=balance.used_days,
            remaining_days=balance.remaining_days,  # calculado por el DOMAIN, no aquí
        )
