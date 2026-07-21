from fastapi import FastAPI

from src.task_manager.routers.notes import router as notes_router
from src.task_manager.routers.tasks import router as tasks_router

app = FastAPI()
app.include_router(router=tasks_router)
app.include_router(router=notes_router)


@app.get('/')
def root():
    return {'message': 'Hello World!'}
