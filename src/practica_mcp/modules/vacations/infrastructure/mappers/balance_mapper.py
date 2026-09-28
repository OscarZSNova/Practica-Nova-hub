from typing import Any

from practica_mcp.modules.vacations.domain.balance import VacationBalance


def to_domain(raw: dict[str, Any]) -> VacationBalance:
    return VacationBalance(
        employee_id=raw["empleado"],
        year=int(raw["anio"]),
        entitled_days=int(raw["dias_ley"]),
        used_days=int(raw["dias_tomados"]),
    )
