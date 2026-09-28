"""Servidor MCP solo con el módulo 'employees'.

Demuestra que separar el monolito en MCPs independientes es solo empaquetado.
"""

from practica_mcp.apps.factory import create_server

mcp = create_server("practica-employees-mcp", ["employees"])


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
