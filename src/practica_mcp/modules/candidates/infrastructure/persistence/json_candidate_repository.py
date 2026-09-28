import json
from pathlib import Path

from practica_mcp.modules.candidates.domain.candidate import Candidate
from practica_mcp.modules.candidates.infrastructure.mappers.candidate_mapper import to_domain

DEFAULT_DATA_FILE = Path(__file__).parent / "data" / "candidates.json"


class JsonCandidateRepository:
    def __init__(self, data_file: Path = DEFAULT_DATA_FILE) -> None:
        self._data_file = data_file

    async def get_by_id(self, candidate_id: str) -> Candidate | None:
        raw_items = json.loads(self._data_file.read_text(encoding="utf-8"))
        raw = next((item for item in raw_items if item["folio"] == candidate_id), None)
        return to_domain(raw) if raw else None
