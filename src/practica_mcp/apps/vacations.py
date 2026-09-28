"""Servidor MCP solo con el módulo 'vacations'.

Demuestra que separar el monolito en MCPs independientes es solo empaquetado.
"""

from practica_mcp.apps.factory import create_server

mcp = create_server("practica-vacations-mcp", ["vacations"])


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
