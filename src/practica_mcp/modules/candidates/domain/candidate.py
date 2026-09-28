from dataclasses import dataclass

from .errors import InvalidCandidateError


@dataclass(frozen=True)
class Candidate:
    id: str
    full_name: str
    applied_position: str
    years_experience: int
    skills: frozenset[str]

    def __post_init__(self) -> None:
        if not self.id.startswith("CAN-"):
            raise InvalidCandidateError(f"ID de candidato inválido: '{self.id}'")
        if self.years_experience < 0:
            raise InvalidCandidateError("Los años de experiencia no pueden ser negativos")

    def has_skill(self, skill: str) -> bool:
        return skill.strip().casefold() in self.skills
