"""Errores de negocio del dominio Employees.

Son excepciones "puras": no saben nada de MCP ni HTTP.
La capa interfaces/mcp decide cómo mostrarlas al cliente.
"""


class EmployeeError(Exception):
    """Error base del dominio."""


class InvalidEmployeeIdError(EmployeeError):
    def __init__(self, value: str) -> None:
        super().__init__(f"ID de empleado inválido: '{value}'. Formato esperado: EMP-000")


class EmployeeNotFoundError(EmployeeError):
    def __init__(self, employee_id: str) -> None:
        super().__init__(f"No existe el empleado '{employee_id}'")
