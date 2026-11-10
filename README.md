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

## Ejecutar

```bash
fastapi dev main.py
```

El servidor queda en http://127.0.0.1:8000 y la documentación interactiva en http://127.0.0.1:8000/docs.

## Endpoints

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/` | Mensaje de bienvenida |
| POST | `/proyectos` | Crea un proyecto (responde 201) |
| GET | `/proyectos` | Lista proyectos. Parámetros opcionales: `categoria` y `limite` (1–100, por defecto 10) |
| GET | `/proyectos/{proyecto_id}` | Obtiene un proyecto por id (404 si no existe) |
| POST | `/proyectos/{proyecto_id}/evaluaciones` | Registra una evaluación del proyecto (201; 404 si el proyecto no existe) |
| GET | `/proyectos/{proyecto_id}/evaluaciones` | Lista las evaluaciones del proyecto |
| GET | `/proyectos/{proyecto_id}/resumen` | Promedio por criterio y promedio general (`null` si aún no hay evaluaciones) |

Categorías válidas: `Software`, `Hardware`, `Impacto social`, `Inteligencia Artificial`.

Una evaluación lleva `evaluador` (3 a 80 caracteres), `innovacion`, `viabilidad` y `presentacion` (enteros de 0 a 10) y un `comentario` opcional de máximo 500 caracteres.

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/proyectos \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Robot clasificador", "equipo": ["Ana", "Luis"], "categoria": "Hardware"}'

curl -X POST http://127.0.0.1:8000/proyectos/1/evaluaciones \
  -H "Content-Type: application/json" \
  -d '{"evaluador": "Dra. López", "innovacion": 9, "viabilidad": 7, "presentacion": 8}'
```

Los datos se guardan en memoria, así que se pierden al reiniciar el servidor.

## Demo de concurrencia

En `scripts/` hay una demo que compara `async def` con `time.sleep`, `async def` con `await asyncio.sleep` y `def` con `time.sleep`:

```bash
fastapi dev scripts/demo_async.py      # terminal 1
python scripts/prueba_concurrencia.py  # terminal 2
```

El segundo script lanza 5 peticiones simultáneas a cada endpoint e imprime cuánto tardó cada grupo.

## Licencia

[MIT](LICENSE)
