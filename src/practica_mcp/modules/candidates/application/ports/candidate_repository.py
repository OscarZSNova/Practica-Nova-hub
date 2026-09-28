from typing import Protocol

from practica_mcp.modules.candidates.domain.candidate import Candidate


class CandidateRepository(Protocol):
    async def get_by_id(self, candidate_id: str) -> Candidate | None: ...
