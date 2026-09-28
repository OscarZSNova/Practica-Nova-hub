"""Fábrica de servidores MCP.

Este archivo SOLO cambia cuando se agrega o quita un bounded context completo.
Agregar una Tool nueva a un módulo NO debe requerir tocar este archivo:
cada módulo registra sus propias Tools en su `module.py`.
"""

from collections.abc import Callable, Sequence

from mcp.server import MCPServer

from practica_mcp.modules.candidates import module as candidates_module
from practica_mcp.modules.employees import module as employees_module
from practica_mcp.modules.vacations import module as vacations_module
from practica_mcp.platform.config.settings import get_settings
from practica_mcp.platform.observability.logging import configure_logging

ModuleRegistrar = Callable[[MCPServer], None]

MODULES: dict[str, ModuleRegistrar] = {
    "employees": employees_module.register,
    "vacations": vacations_module.register,
    "candidates": candidates_module.register,
}


def create_server(name: str, modules: Sequence[str]) -> MCPServer:
    settings = get_settings()
    configure_logging(settings.log_level)

    mcp = MCPServer(name=name)
    for module_name in modules:
        MODULES[module_name](mcp)
    return mcp
