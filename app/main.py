from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.database import crear_tablas
from app.errors import Conflicto
from app.routers import evaluations, projects

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield

app = FastAPI(title="Mini Evaluación Expo IBERO", lifespan=lifespan)

@app.exception_handler(Conflicto)
def manejar_conflicto(request: Request, exc: Conflicto):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": exc.mensaje})

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(projects.router)
api_v1.include_router(evaluations.router)

app.include_router(api_v1)

@app.get("/")
def raiz():
    return {"mensaje": "Hola mundo desde FastAPI! 😎"}
