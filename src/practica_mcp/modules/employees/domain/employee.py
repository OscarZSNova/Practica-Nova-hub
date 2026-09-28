"""DOMAIN: entidades y value objects. Negocio puro.

Reglas de esta capa:
- NO importa mcp, pydantic, httpx, SQL ni SDKs cloud.
- Solo Python estándar + otras piezas del mismo dominio.
- Aquí viven las invariantes (reglas que SIEMPRE deben cumplirse).
"""

import re
from dataclasses import dataclass

from .errors import InvalidEmployeeIdError

_EMPLOYEE_ID_PATTERN = re.compile(r"^EMP-\d{3}$")


@dataclass(frozen=True)
class EmployeeId:
    """Value object: un ID que no puede existir si es inválido."""

    value: str

    def __post_init__(self) -> None:
        if not _EMPLOYEE_ID_PATTERN.match(self.value):
            raise InvalidEmployeeIdError(self.value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Employee:
    """Entidad: un empleado."""

    id: EmployeeId
    full_name: str
    department: str
    position: str
    active: bool

    def belongs_to(self, department: str) -> bool:
        """Regla de negocio: compara el departamento sin importar mayúsculas ni espacios."""
        return self.department.casefold() == department.strip().casefold()
