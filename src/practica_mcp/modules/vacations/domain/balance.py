"""DOMAIN: saldo de vacaciones.

Ojo: este módulo NO importa nada de `employees`. Para Vacations, el empleado
es solo un `employee_id` (str). Cada bounded context tiene su propio modelo;
así mañana se pueden separar en MCPs distintos sin romper nada.
"""

from dataclasses import dataclass

from .errors import InvalidBalanceError


@dataclass(frozen=True)
class VacationBalance:
    employee_id: str
    year: int
    entitled_days: int
    used_days: int

    def __post_init__(self) -> None:
        # Invariantes: un saldo inválido no puede ni construirse.
        if self.entitled_days < 0 or self.used_days < 0:
            raise InvalidBalanceError("Los días no pueden ser negativos")
        if self.used_days > self.entitled_days:
            raise InvalidBalanceError("Los días usados no pueden superar los días otorgados")

    @property
    def remaining_days(self) -> int:
        return self.entitled_days - self.used_days

    def can_take(self, days: int) -> bool:
        """Regla de negocio: ¿alcanza el saldo para tomar `days` días?"""
        return 0 < days <= self.remaining_days
