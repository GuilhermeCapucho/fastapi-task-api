from fastapi import FastAPI
from routes.tasks import router as tasks_router
from routes.auth import router as auth_router
from routes.admin import router as admin_router

app = FastAPI()

#Registro de rotas
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Welcome to the Task API"}