from fastapi import FastAPI
from app.routes import users

app = FastAPI(
    title="Horizon Backend",
    version="1.0",
    description="API base com autenticação e gerenciamento de usuários"
)

# Rotas
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Backend FastAPI está funcionando "}

