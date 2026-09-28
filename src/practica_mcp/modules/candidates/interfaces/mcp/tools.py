from typing import Annotated

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

from practica_mcp.modules.candidates.application.use_cases.get_candidate import GetCandidate
from practica_mcp.modules.candidates.domain.errors import CandidateError
from practica_mcp.modules.candidates.interfaces.mcp.schemas import CandidateOutput


def register_tools(mcp: MCPServer, *, get_candidate: GetCandidate) -> None:
    @mcp.tool(
        name="candidates.candidate.get",
        description="Obtiene el perfil de un candidato por su folio (formato CAN-000).",
    )
    async def get_candidate_tool(
        candidate_id: Annotated[str, Field(description="Folio del candidato, ej. CAN-101")],
    ) -> CandidateOutput:
        try:
            candidate = await get_candidate.execute(candidate_id)
        except CandidateError as error:
            raise ToolError(str(error)) from error
        return CandidateOutput.from_domain(candidate)

    # EJERCICIO (Persona 3): agregar aquí la tool "candidates.screening.validate".
    # Ver EJERCICIOS.md.
