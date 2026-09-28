"""Architecture tests: hacen cumplir las reglas hexagonales automáticamente.

Si alguien rompe una regla (p. ej. importa `mcp` desde domain/, o el módulo
vacations importa algo de employees), este test falla en CI.
"""

import ast
from pathlib import Path

import pytest

MODULES_DIR = Path(__file__).parents[2] / "src" / "practica_mcp" / "modules"
MODULES = sorted(p.name for p in MODULES_DIR.iterdir() if (p / "module.py").exists())

# Qué NO puede importar cada capa (prefijos de import).
FORBIDDEN_BY_LAYER = {
    "domain": ["mcp", "pydantic", "httpx", "json", "sqlalchemy", "boto3", "azure"],
    "application": ["mcp", "httpx", "json", "sqlalchemy", "boto3", "azure"],
}


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
    return names


def _python_files(directory: Path) -> list[Path]:
    return list(directory.rglob("*.py"))


def _matches(name: str, prefix: str) -> bool:
    return name == prefix or name.startswith(prefix + ".")


@pytest.mark.parametrize("module", MODULES)
def test_un_modulo_no_importa_a_otro(module):
    others = [f"practica_mcp.modules.{m}" for m in MODULES if m != module]
    for file in _python_files(MODULES_DIR / module):
        for name in _imports(file):
            bad = [o for o in others if _matches(name, o)]
            assert not bad, f"{file.relative_to(MODULES_DIR)} importa {name}"


@pytest.mark.parametrize("module", MODULES)
@pytest.mark.parametrize("layer", list(FORBIDDEN_BY_LAYER))
def test_capas_internas_no_dependen_de_tecnologia(module, layer):
    for file in _python_files(MODULES_DIR / module / layer):
        for name in _imports(file):
            bad = [f for f in FORBIDDEN_BY_LAYER[layer] if _matches(name, f)]
            assert not bad, f"{file.relative_to(MODULES_DIR)} ({layer}) importa {name}"


@pytest.mark.parametrize("module", MODULES)
def test_domain_no_depende_de_capas_externas(module):
    base = f"practica_mcp.modules.{module}"
    outer = [f"{base}.application", f"{base}.infrastructure", f"{base}.interfaces"]
    for file in _python_files(MODULES_DIR / module / "domain"):
        for name in _imports(file):
            bad = [o for o in outer if _matches(name, o)]
            assert not bad, f"{file.relative_to(MODULES_DIR)} importa {name}"


@pytest.mark.parametrize("module", MODULES)
def test_application_no_depende_de_infrastructure_ni_interfaces(module):
    base = f"practica_mcp.modules.{module}"
    outer = [f"{base}.infrastructure", f"{base}.interfaces"]
    for file in _python_files(MODULES_DIR / module / "application"):
        for name in _imports(file):
            bad = [o for o in outer if _matches(name, o)]
            assert not bad, f"{file.relative_to(MODULES_DIR)} importa {name}"
