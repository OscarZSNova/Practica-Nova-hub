"""MAPPER: traduce el formato EXTERNO al modelo de DOMAIN.

El "sistema externo" (aquí un JSON que simula NovaHub/DB) usa sus propios nombres:
`num_empleado`, `depto`, `estatus: "ACTIVO"`... El dominio no debe depender de eso.
Si mañana cambia la API, solo cambia este archivo.

Un mapper normaliza datos, pero NO decide política de negocio.
"""

from typing import Any

from practica_mcp.modules.employees.domain.employee import Employee, EmployeeId


def to_domain(raw: dict[str, Any]) -> Employee:
    return Employee(
        id=EmployeeId(raw["num_empleado"]),
        full_name=f"{raw['nombre']} {raw['apellidos']}".strip(),
        department=raw["depto"],
        position=raw["puesto"],
        active=raw["estatus"] == "ACTIVO",
    )
