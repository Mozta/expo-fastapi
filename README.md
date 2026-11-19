# Mini Evaluación Expo IBERO

API sencilla en FastAPI para registrar y consultar proyectos de la Expo IBERO. Material de la materia Tópicos Avanzados (unidad de FastAPI).

## Requisitos

- Python 3.12

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Base de datos

La API guarda los datos con SQLModel. La conexión se lee de la variable `DATABASE_URL` (desde el entorno o desde un archivo `.env` en la raíz):

```bash
cp .env.example .env   # y ajusta usuario, contraseña, puerto y base de datos
```

Si no hay `DATABASE_URL`, se usa SQLite en `./expo.db`. Las tablas se crean solas al arrancar el servidor. Con `SQL_ECHO=true` se imprimen en consola las consultas SQL.

## Ejecutar

```bash
fastapi dev app/main.py
```

El servidor queda en http://127.0.0.1:8000 y la documentación interactiva en http://127.0.0.1:8000/docs.

## Estructura

```
app/
├── main.py            # crea la app y monta los routers bajo /api/v1
├── config.py          # Settings: DATABASE_URL y SQL_ECHO (pydantic-settings)
├── database.py        # engine, crear_tablas() y la sesión por petición (SessionDep)
├── models.py          # tablas SQLModel: ProyectoDB y EvaluacionDB
├── schemas.py         # modelos Pydantic (entrada/salida de la API)
├── repository_sql.py  # RepositorySQL: consultas con SQLModel
├── repository.py      # RepositoryMemory: versión anterior en memoria (referencia)
├── errors.py          # Conflicto: se responde como 409
├── dependencies.py    # RepositorioDep y ProyectoDep (404 si no existe)
└── routers/
    ├── projects.py    # /proyectos y /proyectos/{id}/resumen
    └── evaluations.py # /proyectos/{id}/evaluaciones
```

## Endpoints

Todas las rutas, salvo `/`, van bajo el prefijo `/api/v1`.

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/` | Mensaje de bienvenida |
| POST | `/api/v1/proyectos` | Crea un proyecto (201; 409 si ya existe otro con el mismo nombre) |
| GET | `/api/v1/proyectos` | Lista proyectos. Parámetros opcionales: `categoria` y `limite` (1–100, por defecto 10) |
| GET | `/api/v1/proyectos/{proyecto_id}` | Obtiene un proyecto por id (404 si no existe) |
| POST | `/api/v1/proyectos/{proyecto_id}/evaluaciones` | Registra una evaluación del proyecto (201; 404 si el proyecto no existe) |
| GET | `/api/v1/proyectos/{proyecto_id}/evaluaciones` | Lista las evaluaciones del proyecto (404 si el proyecto no existe) |
| GET | `/api/v1/proyectos/{proyecto_id}/resumen` | Promedio por criterio y promedio general (`null` si aún no hay evaluaciones) |

Categorías válidas: `Software`, `Hardware`, `Impacto social`, `Inteligencia Artificial`.

Una evaluación lleva `evaluador` (3 a 80 caracteres), `innovacion`, `viabilidad` y `presentacion` (enteros de 0 a 10) y un `comentario` opcional de máximo 500 caracteres.

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/proyectos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Robot clasificador", "equipo": ["Ana", "Luis"], "categoria": "Hardware"}'

curl -X POST http://127.0.0.1:8000/api/v1/proyectos/1/evaluaciones \
  -H "Content-Type: application/json" \
  -d '{"evaluador": "Dra. López", "innovacion": 9, "viabilidad": 7, "presentacion": 8}'
```

El nombre del proyecto es único y los datos persisten en la base de datos entre reinicios.

## Demo de concurrencia

En `scripts/` hay una demo que compara `async def` con `time.sleep`, `async def` con `await asyncio.sleep` y `def` con `time.sleep`:

```bash
fastapi dev scripts/demo_async.py      # terminal 1
python scripts/prueba_concurrencia.py  # terminal 2
```

El segundo script lanza 5 peticiones simultáneas a cada endpoint e imprime cuánto tardó cada grupo.

## Licencia

[MIT](LICENSE)
