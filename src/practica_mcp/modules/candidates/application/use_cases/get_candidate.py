from practica_mcp.modules.candidates.application.ports.candidate_repository import (
    CandidateRepository,
)
from practica_mcp.modules.candidates.domain.candidate import Candidate
from practica_mcp.modules.candidates.domain.errors import CandidateNotFoundError


class GetCandidate:
    def __init__(self, repository: CandidateRepository) -> None:
        self._repository = repository

    async def execute(self, candidate_id: str) -> Candidate:
        candidate = await self._repository.get_by_id(candidate_id.strip().upper())
        if candidate is None:
            raise CandidateNotFoundError(candidate_id)
        return candidate
