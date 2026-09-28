"""ADAPTER: implementación REAL del Port `EmployeeRepository`.

Aquí sí se permite tecnología concreta (leer archivos, SQL, httpx, SDK cloud...).
Este lee un JSON local que simula el "source of truth". En el proyecto real
sería, por ejemplo, un cliente GraphQL de NovaHub en infrastructure/novahub/.

Fíjate que NO hereda de EmployeeRepository: basta con tener los mismos métodos.
"""

import json
from pathlib import Path

from practica_mcp.modules.employees.domain.employee import Employee, EmployeeId
from practica_mcp.modules.employees.infrastructure.mappers.employee_mapper import to_domain

DEFAULT_DATA_FILE = Path(__file__).parent / "data" / "employees.json"


class JsonEmployeeRepository:
    def __init__(self, data_file: Path = DEFAULT_DATA_FILE) -> None:
        self._data_file = data_file

    def _load(self) -> list[Employee]:
        raw_items = json.loads(self._data_file.read_text(encoding="utf-8"))
        return [to_domain(item) for item in raw_items]

    async def get_by_id(self, employee_id: EmployeeId) -> Employee | None:
        return next((e for e in self._load() if e.id == employee_id), None)

    async def list_all(self) -> list[Employee]:
        return self._load()
