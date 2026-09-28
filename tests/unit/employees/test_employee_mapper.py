"""Mapper tests: protegen el contrato con el sistema externo."""

from practica_mcp.modules.employees.infrastructure.mappers.employee_mapper import to_domain


def test_mapea_formato_externo_a_dominio():
    raw = {
        "num_empleado": "EMP-004",
        "nombre": "Jorge",
        "apellidos": "Pérez Vega",
        "depto": "Recursos Humanos",
        "puesto": "Reclutador",
        "estatus": "BAJA",
    }
    employee = to_domain(raw)

    assert str(employee.id) == "EMP-004"
    assert employee.full_name == "Jorge Pérez Vega"
    assert employee.active is False
