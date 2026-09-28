class CandidateError(Exception):
    """Error base del dominio Candidates."""


class InvalidCandidateError(CandidateError):
    pass


class CandidateNotFoundError(CandidateError):
    def __init__(self, candidate_id: str) -> None:
        super().__init__(f"No existe el candidato '{candidate_id}'")
