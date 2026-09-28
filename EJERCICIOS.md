# Ejercicios

Cada persona crea **una Tool nueva en su módulo**, siguiendo el mismo orden que usaremos en NovaHub:

```text
1. Confirmar caso de uso y contrato (input / output / errores)   ← ya viene definido abajo
2. Elegir nombre MCP                                             ← ya viene definido abajo
3. Domain: entidades / reglas
4. Port (si necesita algo del exterior)
5. Use Case
6. Adapter
7. Mapper (si hace falta)
8. Tool MCP (+ schema de salida)
9. Registrar en module.py
10. Tests (unit + contract)
```

Usa el módulo `employees` como referencia: tiene comentarios explicando cada capa.

Al terminar, agrega el nombre de tu Tool a `EXPECTED_TOOLS` en
`tests/contract/mcp/test_tools_contract.py` y agrega tus casos a los tests parametrizados.

---

## Persona 1: `employees.employee.search`

**Caso de uso:** buscar empleados por departamento.

| | |
|---|---|
| Input | `department: str`, `only_active: bool = True` |
| Output | `{ "total": int, "employees": [EmployeeOutput, ...] }` |
| Errores | ninguno de negocio: si no hay resultados, `total = 0` |
| Tipo | read |

**Pistas**

- El Port `EmployeeRepository` ya tiene `list_all()` y el domain ya tiene `Employee.belongs_to()`.
  ¿Hace falta cambiar el Port? (Respuesta: no. Piensa por qué está bien reutilizarlos.)
- Crea `application/use_cases/search_employees.py` con la clase `SearchEmployees`.
  El filtro (departamento + activo) va en el use case usando las reglas del domain,
  **no** en la Tool ni en el Adapter.
- Crea `EmployeeSearchOutput` en `interfaces/mcp/schemas.py`.
- Registra la Tool en `tools.py` y conecta el use case en `module.py`.

**Tests mínimos**

- Unit: "Finanzas" devuelve EMP-001 y EMP-005; "recursos humanos" con `only_active=True` devuelve 0
  y con `only_active=False` devuelve EMP-004.
- Contract: la Tool existe y devuelve `total` en `structured_content`.

**Reto extra:** que el departamento sea opcional (si no llega, lista todos).

---

## Persona 2: `vacations.request.create`

**Caso de uso:** un empleado solicita vacaciones. Es una operación de **escritura**, con reglas de
negocio de verdad.

| | |
|---|---|
| Input | `employee_id: str`, `start_date: date`, `end_date: date` |
| Output | `{ "request_id", "employee_id", "start_date", "end_date", "days", "status": "PENDIENTE", "remaining_days_after" }` |
| Errores | fechas invertidas, saldo insuficiente, empleado sin saldo |
| Tipo | write |

**Pistas**

- Domain: crea `domain/request.py` con una entidad `VacationRequest`.
  - Invariante: `end_date >= start_date` (si no, lanza un error de dominio nuevo).
  - Propiedad `days` = días naturales entre ambas fechas, incluyendo los dos extremos.
  - Usa `VacationBalance.can_take(days)`; si no alcanza, lanza `InsufficientBalanceError`.
- Port nuevo: `application/ports/request_repository.py` con `async def save(request) -> None`.
- Adapter: `infrastructure/persistence/in_memory_request_repository.py` (una lista en memoria basta;
  no hace falta escribir en el JSON).
- Use case `CreateVacationRequest` recibe **dos** ports: `BalanceRepository` y `RequestRepository`.
- ¿Quién genera `request_id`? Discútanlo: ¿domain, use case o adapter? (En sistemas reales suele
  generarlo el source of truth.)

**Tests mínimos**

- Unit domain: fechas invertidas fallan; 3 días del 10 al 12 cuentan como 3.
- Unit use case: EMP-001 (7 días restantes) puede pedir 7 y no puede pedir 8; EMP-002 (0 restantes)
  no puede pedir nada. Verifica con el Fake que `save` se llamó solo en el caso válido.
- Contract: una llamada inválida devuelve `is_error=True`.

**Reto extra:** marcar la Tool con `annotations=ToolAnnotations(readOnlyHint=False,
destructiveHint=False)` (`from mcp.types import ToolAnnotations`) y comentar por qué las
operaciones de escritura se separan de las de lectura.

---

## Persona 3: `candidates.screening.validate`

**Caso de uso:** pre-screening: ¿un candidato cumple los requisitos mínimos de una vacante?

| | |
|---|---|
| Input | `candidate_id: str`, `min_years: int`, `required_skills: list[str]` |
| Output | `{ "candidate_id", "passed": bool, "meets_experience": bool, "missing_skills": [str] }` |
| Errores | candidato inexistente; `min_years` negativo |
| Tipo | read (valida, no guarda nada) |

**Pistas**

- Domain: crea `domain/screening.py` con:
  - `ScreeningCriteria` (value object: `min_years`, `required_skills`), que valida que `min_years >= 0`
    y normaliza las skills igual que el mapper.
  - `ScreeningResult` (value object con el resultado).
  - Una función o método `evaluate(candidate, criteria) -> ScreeningResult`. **Toda** la lógica de
    decisión va aquí, así se prueba sin MCP ni JSON.
- El Port `CandidateRepository` ya tiene `get_by_id`: reutilízalo.
- Use case `ValidateScreening`: obtiene el candidato y llama a `evaluate`.

**Tests mínimos**

- Unit domain: CAN-101 con `min_years=3, ["python", "sql"]` pasa; CAN-102 con lo mismo falla por
  experiencia y le falta `sql`.
- Contract: la Tool devuelve `passed` y `missing_skills`.

**Reto extra:** en lugar de recibir los requisitos como input, crea `data/vacancies.json`, un Port
`VacancyRepository` y su Adapter, y que la Tool reciba solo `candidate_id` + `vacancy_id`.

---

## Retos para el equipo completo (después)

1. **Cambiar un Adapter sin tocar nada más:** reemplazar `JsonEmployeeRepository` por uno con SQLite
   (`sqlite3` es de la librería estándar). Solo deberían cambiar `infrastructure/` y `module.py`;
   los tests unitarios y de contrato no deben cambiar.
2. **Romper una regla a propósito:** importar algo de `employees` desde `vacations` y ver cómo falla
   `tests/architecture`. Luego discutir: si Vacations necesita el nombre del empleado, ¿cómo se
   resuelve sin acoplar módulos?
3. **Observabilidad:** en `platform/observability/`, un decorador que loggee `tool_name`, duración y
   éxito/error de cada Tool (a stderr, sin datos personales).
4. **Separar un MCP:** apuntar `.vscode/mcp.json` a `practica-candidates-mcp` y comprobar que funciona
   solo, sin los otros módulos.
