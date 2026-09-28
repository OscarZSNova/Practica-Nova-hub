"""Configuración compartida.

En el proyecto real aquí irían URLs de NovaHub, credenciales (vía secret manager),
timeouts, etc. Aquí solo leemos variables de entorno sencillas.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    server_name: str = "practica-people-mcp"
    log_level: str = "INFO"


def get_settings() -> Settings:
    return Settings(
        server_name=os.getenv("PRACTICA_SERVER_NAME", "practica-people-mcp"),
        log_level=os.getenv("PRACTICA_LOG_LEVEL", "INFO"),
    )
