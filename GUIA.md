# Práctica: MCP Tools con arquitectura hexagonal

Proyecto **de práctica** para que un equipo de 3 personas aprenda a:

1. Crear Tools para un servidor MCP.
2. Trabajar en una estructura **modular monolith + hexagonal (Ports & Adapters)**, la misma idea
   que usa NovaHub People MCP, pero con un dominio sencillo y datos falsos (archivos JSON).

No hay base de datos ni APIs reales: los "sistemas externos" son JSON dentro de cada módulo.

---

## 1. Idea en 30 segundos

```text
Copilot / Claude (cliente MCP)
        │  llama a "employees.employee.get"
        ▼
interfaces/mcp/tools.py      ← Tool: delgada, solo adapta MCP → use case
        ▼
application/use_cases/       ← Use Case: orquesta (valida, pide datos, aplica reglas)
        ▼
application/ports/           ← Port: interfaz (Protocol) "necesito empleados"
        ▼
infrastructure/persistence/  ← Adapter: implementación real (aquí lee un JSON)
infrastructure/mappers/      ← Mapper: formato externo → Domain
        ▼
domain/                      ← Entidades + reglas de negocio puras
```

Regla central: **Tool → Use Case → Port → Adapter → Sistema externo**.
Nunca: Tool → leer JSON / SQL / HTTP directamente.

Las dependencias apuntan **hacia adentro**: `domain` no conoce a nadie; `application` solo conoce a
`domain`; `infrastructure` e `interfaces` conocen a los de adentro. Lo comprueban los tests de
`tests/architecture/`.

---

## 2. Estructura

```text
src/practica_mcp/
├── apps/                    ← puntos de entrada (armar servidores)
│   ├── factory.py           ← solo cambia al agregar/quitar un MÓDULO completo
│   ├── combined.py          ← los 3 módulos en un solo MCP
│   ├── employees.py         ← MCP solo de employees
│   ├── vacations.py         ← MCP solo de vacations
│   └── candidates.py        ← MCP solo de candidates
├── platform/                ← transversal (config, logging)
└── modules/
    ├── employees/           ← Persona 1   (MÓDULO DE REFERENCIA, muy comentado)
    ├── vacations/           ← Persona 2
    └── candidates/          ← Persona 3
        ├── domain/                  entidades, value objects, errores, reglas
        ├── application/
        │   ├── ports/               interfaces (Protocol)
        │   └── use_cases/           casos de uso
        ├── infrastructure/
        │   ├── persistence/         adapters (+ data/*.json = "sistema externo")
        │   └── mappers/             externo → domain
        ├── interfaces/mcp/
        │   ├── schemas.py           salida pública de las Tools (pydantic)
        │   └── tools.py             las Tools MCP
        └── module.py                composition root: conecta Adapter → Use Case → Tool

tests/
├── unit/<modulo>/           domain, use cases (con Fakes) y mappers
├── contract/mcp/            habla con el servidor como un cliente MCP real
└── architecture/            reglas hexagonales automáticas
```

**Empieza leyendo el módulo `employees` en este orden:**
`domain/employee.py` → `application/ports/` → `application/use_cases/get_employee.py` →
`infrastructure/mappers/` → `infrastructure/persistence/` → `interfaces/mcp/` → `module.py`.

---

## 3. Tools incluidas

| Tool | Módulo | Qué hace |
|---|---|---|
| `employees.employee.get` | employees | Datos de un empleado (`EMP-001`…`EMP-005`) |
| `vacations.balance.get` | vacations | Saldo de vacaciones, con días restantes calculados en el domain |
| `candidates.candidate.get` | candidates | Perfil de un candidato (`CAN-101`…`CAN-104`) |

Nomenclatura (igual que en NovaHub): `<bounded_context>.<resource>.<operation>`.

---

## 4. Instalar y probar

Requisitos: [uv](https://docs.astral.sh/uv/) (instala Python solo).

```bash
uv sync --dev
uv run pytest                  # todos los tests
uv run ruff check .            # lint
uv run ruff format .           # formato
```

### Probar las Tools con el Inspector MCP (requiere Node.js)

```bash
uv run mcp dev src/practica_mcp/apps/combined.py
```

### Probarlas desde GitHub Copilot (VS Code)

Ya está configurado en `.vscode/mcp.json`. Abre el archivo, pulsa **Start** sobre el servidor
`practica-people`, abre el chat de Copilot en modo **Agent** y pregunta, por ejemplo:
*"¿Cuántos días de vacaciones le quedan a EMP-001?"*.

### Probarlas desde Claude Code

Ya está configurado en `.mcp.json` (en la raíz). Abre Claude Code en esta carpeta y acepta el servidor.

### Ejecutar servidores sueltos (stdio)

```bash
uv run practica-people-mcp        # los 3 módulos
uv run practica-employees-mcp     # solo employees
uv run practica-vacations-mcp     # solo vacations
uv run practica-candidates-mcp    # solo candidates
```

> Con stdio, **stdout es el canal del protocolo**: nunca uses `print()` en el servidor.
> Usa el logger de `platform/observability/logging.py` (escribe a stderr).

---

## 5. Cómo trabajar en equipo

| Persona | Es dueña de | Ejercicio |
|---|---|---|
| 1 | `modules/employees/**`, `tests/unit/employees/**` | `employees.employee.search` |
| 2 | `modules/vacations/**`, `tests/unit/vacations/**` | `vacations.request.create` |
| 3 | `modules/candidates/**`, `tests/unit/candidates/**` | `candidates.screening.validate` |

- Una rama por persona/ejercicio: `feature/employees-search`, `feature/vacations-request-create`, …
- Como cada quien toca **solo su módulo**, casi no debería haber conflictos de merge.
  Los únicos archivos compartidos son `tests/contract/mcp/test_tools_contract.py` (agregar el nombre
  de tu tool a `EXPECTED_TOOLS`) y, si acaso, `platform/`.
- **No** hace falta tocar `apps/factory.py` para agregar una Tool.
- Antes de abrir PR: `uv run ruff check . && uv run ruff format --check . && uv run pytest`.
- Revisión cruzada: cada PR lo revisa alguien de otro módulo, usando el checklist de la sección 6.

Los ejercicios detallados están en **[EJERCICIOS.md](EJERCICIOS.md)**.

---

## 6. Checklist para revisar una Tool nueva

- [ ] ¿El nombre sigue `<contexto>.<recurso>.<operación>` y usa un verbo explícito (`get`, `search`,
      `create`, `validate`…)? Evitar `process`, `handle`, `do_task`.
- [ ] ¿La Tool es delgada (sin lectura de archivos, sin reglas de negocio)?
- [ ] ¿Las reglas de negocio están en `domain/` y tienen unit test?
- [ ] ¿El use case recibe el Port por constructor y tiene tests con un Fake?
- [ ] ¿El formato externo se traduce en un mapper, no en el use case?
- [ ] ¿Los errores de negocio se convierten en `ToolError` (el cliente ve `is_error=True`)?
- [ ] ¿La salida es un schema pydantic en `interfaces/mcp/schemas.py`?
- [ ] ¿El módulo no importa nada de otro módulo? (`tests/architecture` lo verifica)
- [ ] ¿Se registró en `module.py` y no en `apps/factory.py`?

---

## 7. Cómo se traduce esto a NovaHub People MCP

| Aquí (práctica) | En NovaHub People MCP |
|---|---|
| `employees` / `vacations` / `candidates` | `payroll` / `talent_acquisition` / `talent_management` |
| `infrastructure/persistence/*.json` | `infrastructure/novahub/` (GraphQL/REST), `persistence/` (DB), `cloud/` |
| `platform/config`, `platform/observability` | lo mismo + `platform/http`, `database`, `security`, `cloud` |
| `apps/combined.py` + `apps/<modulo>.py` | `apps/combined.py` + `apps/payroll.py`, etc. |
| Fakes en tests unitarios | Igual: los use cases se prueban sin NovaHub real |

Cambiar el JSON por una API real significa escribir **otro Adapter** que cumpla el mismo Port y
conectarlo en `module.py`. Domain, use cases, Tools y tests de contrato no cambian.
