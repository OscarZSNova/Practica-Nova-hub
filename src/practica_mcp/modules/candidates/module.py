from mcp.server import MCPServer

from practica_mcp.modules.candidates.application.ports.candidate_repository import (
    CandidateRepository,
)
from practica_mcp.modules.candidates.application.use_cases.get_candidate import GetCandidate
from practica_mcp.modules.candidates.infrastructure.persistence.json_candidate_repository import (
    JsonCandidateRepository,
)
from practica_mcp.modules.candidates.interfaces.mcp.tools import register_tools


def register(mcp: MCPServer, repository: CandidateRepository | None = None) -> None:
    repository = repository or JsonCandidateRepository()

    register_tools(
        mcp,
        get_candidate=GetCandidate(repository),
    )
