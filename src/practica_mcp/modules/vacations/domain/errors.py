class VacationError(Exception):
    """Error base del dominio Vacations."""


class InvalidBalanceError(VacationError):
    pass


class BalanceNotFoundError(VacationError):
    def __init__(self, employee_id: str) -> None:
        super().__init__(f"No hay saldo de vacaciones para el empleado '{employee_id}'")
