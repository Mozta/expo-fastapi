from fastapi import FastAPI, APIRouter
from app.routers import evaluations, projects

app = FastAPI(title="Mini Evaluación Expo IBERO")

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(projects.router)
api_v1.include_router(evaluations.router)

app.include_router(api_v1)

@app.get("/")
def raiz():
    return {"mensaje": "Hola mundo desde FastAPI! 😎"}