import json
from pathlib import Path

from practica_mcp.modules.vacations.domain.balance import VacationBalance
from practica_mcp.modules.vacations.infrastructure.mappers.balance_mapper import to_domain

DEFAULT_DATA_FILE = Path(__file__).parent / "data" / "balances.json"


class JsonBalanceRepository:
    def __init__(self, data_file: Path = DEFAULT_DATA_FILE) -> None:
        self._data_file = data_file

    async def get_by_employee(self, employee_id: str) -> VacationBalance | None:
        raw_items = json.loads(self._data_file.read_text(encoding="utf-8"))
        raw = next((item for item in raw_items if item["empleado"] == employee_id), None)
        return to_domain(raw) if raw else None
