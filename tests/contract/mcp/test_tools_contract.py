"""MCP contract tests: hablan con el servidor como lo haría Copilot/Claude.

`Client(server)` se conecta en memoria (sin abrir puertos ni procesos) y verifica:
- que la Tool existe con su nombre público
- que una llamada válida devuelve structured output
- que los errores de negocio llegan como `is_error=True`
"""

import pytest
from mcp import Client

from practica_mcp.apps.combined import mcp as combined_server
from practica_mcp.apps.factory import create_server

EXPECTED_TOOLS = {
    "employees.employee.get",
    "vacations.balance.get",
    "candidates.candidate.get",
}


async def test_el_servidor_combinado_expone_todas_las_tools():
    async with Client(combined_server) as client:
        tools = await client.list_tools()
    assert EXPECTED_TOOLS <= {tool.name for tool in tools.tools}


@pytest.mark.parametrize(
    ("module", "prefix"),
    [("employees", "employees."), ("vacations", "vacations."), ("candidates", "candidates.")],
)
async def test_servidores_separados_solo_exponen_su_modulo(module, prefix):
    async with Client(create_server(f"test-{module}", [module])) as client:
        tools = await client.list_tools()
    assert tools.tools, "el módulo debería registrar al menos una tool"
    assert all(tool.name.startswith(prefix) for tool in tools.tools)


@pytest.mark.parametrize(
    ("tool", "args", "expected"),
    [
        ("employees.employee.get", {"employee_id": "EMP-002"}, {"department": "Tecnología"}),
        ("vacations.balance.get", {"employee_id": "EMP-001"}, {"remaining_days": 7}),
        ("candidates.candidate.get", {"candidate_id": "CAN-101"}, {"years_experience": 4}),
    ],
)
async def test_llamada_valida_devuelve_structured_output(tool, args, expected):
    async with Client(combined_server) as client:
        result = await client.call_tool(tool, args)

    assert result.is_error is False
    assert expected.items() <= result.structured_content.items()


@pytest.mark.parametrize(
    ("tool", "args"),
    [
        ("employees.employee.get", {"employee_id": "no-es-un-id"}),
        ("employees.employee.get", {"employee_id": "EMP-999"}),
        ("vacations.balance.get", {"employee_id": "EMP-004"}),
        ("candidates.candidate.get", {"candidate_id": "CAN-999"}),
    ],
)
async def test_error_de_negocio_se_reporta_como_error_de_tool(tool, args):
    async with Client(combined_server) as client:
        result = await client.call_tool(tool, args)

    assert result.is_error is True
