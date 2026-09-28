"""Servidor MCP con los 3 módulos juntos (modular monolith)."""

from practica_mcp.apps.factory import MODULES, create_server
from practica_mcp.platform.config.settings import get_settings

mcp = create_server(get_settings().server_name, list(MODULES))


def main() -> None:
    mcp.run()  # stdio por defecto


if __name__ == "__main__":
    main()
