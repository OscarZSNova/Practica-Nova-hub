"""Esquemas de SALIDA de las Tools (contrato público del MCP).

Pydantic genera el JSON Schema que ve el cliente MCP (Copilot/Claude) y habilita
"structured output". Mantenerlo separado del Domain permite cambiar el dominio
sin romper el contrato MCP (y viceversa).
"""

from pydantic import BaseModel, Field

from practica_mcp.modules.employees.domain.employee import Employee


class EmployeeOutput(BaseModel):
    employee_id: str = Field(description="ID del empleado, formato EMP-000")
    full_name: str
    department: str
    position: str
    active: bool

    @classmethod
    def from_domain(cls, employee: Employee) -> "EmployeeOutput":
        return cls(
            employee_id=str(employee.id),
            full_name=employee.full_name,
            department=employee.department,
            position=employee.position,
            active=employee.active,
        )
