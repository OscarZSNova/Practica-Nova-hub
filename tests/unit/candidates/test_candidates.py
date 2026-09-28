import pytest

from practica_mcp.modules.candidates.application.use_cases.get_candidate import GetCandidate
from practica_mcp.modules.candidates.domain.candidate import Candidate
from practica_mcp.modules.candidates.domain.errors import (
    CandidateNotFoundError,
    InvalidCandidateError,
)
from practica_mcp.modules.candidates.infrastructure.mappers.candidate_mapper import to_domain


class FakeCandidateRepository:
    def __init__(self, candidates: list[Candidate]) -> None:
        self._candidates = {c.id: c for c in candidates}

    async def get_by_id(self, candidate_id: str) -> Candidate | None:
        return self._candidates.get(candidate_id)


SOFIA = Candidate("CAN-101", "Sofía Ramírez", "Backend", 4, frozenset({"python", "sql"}))


# --- Domain ---


def test_candidato_con_id_invalido():
    with pytest.raises(InvalidCandidateError):
        Candidate("X-1", "Nadie", "Backend", 1, frozenset())


def test_has_skill_ignora_mayusculas():
    assert SOFIA.has_skill(" Python ")
    assert not SOFIA.has_skill("Java")


# --- Mapper ---


def test_mapper_normaliza_habilidades():
    raw = {
        "folio": "CAN-101",
        "nombre_completo": "Sofía Ramírez",
        "vacante": "Backend",
        "anios_exp": 4,
        "habilidades": "Python,  SQL , ",
    }
    assert to_domain(raw).skills == frozenset({"python", "sql"})


# --- Application ---


async def test_get_candidate():
    use_case = GetCandidate(FakeCandidateRepository([SOFIA]))
    assert await use_case.execute("can-101") == SOFIA


async def test_get_candidate_inexistente():
    use_case = GetCandidate(FakeCandidateRepository([]))
    with pytest.raises(CandidateNotFoundError):
        await use_case.execute("CAN-999")
