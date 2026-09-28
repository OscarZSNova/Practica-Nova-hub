from pydantic import BaseModel

from practica_mcp.modules.candidates.domain.candidate import Candidate


class CandidateOutput(BaseModel):
    candidate_id: str
    full_name: str
    applied_position: str
    years_experience: int
    skills: list[str]

    @classmethod
    def from_domain(cls, candidate: Candidate) -> "CandidateOutput":
        return cls(
            candidate_id=candidate.id,
            full_name=candidate.full_name,
            applied_position=candidate.applied_position,
            years_experience=candidate.years_experience,
            skills=sorted(candidate.skills),
        )
