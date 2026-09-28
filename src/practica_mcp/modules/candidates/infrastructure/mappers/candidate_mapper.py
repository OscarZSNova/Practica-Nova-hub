from typing import Any

from practica_mcp.modules.candidates.domain.candidate import Candidate


def to_domain(raw: dict[str, Any]) -> Candidate:
    # El sistema externo guarda las habilidades como texto "A, B, C";
    # el dominio las quiere como conjunto normalizado. Eso es trabajo del mapper.
    skills = frozenset(s.strip().casefold() for s in raw["habilidades"].split(",") if s.strip())
    return Candidate(
        id=raw["folio"],
        full_name=raw["nombre_completo"],
        applied_position=raw["vacante"],
        years_experience=int(raw["anios_exp"]),
        skills=skills,
    )
