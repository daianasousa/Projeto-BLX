from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.routers import rotas_produtos, rotas_auth, rotas_pedidos
from src.jobs.write_notification import write_notification
from src.middlewares.timer import SimpleASGIMiddleware

app = FastAPI()

# CORS
origins = ['http://localhost:3000', 
            'http://myapp.vercel.com']

app.add_middleware(CORSMiddleware, 
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],)

app.add_middleware(SimpleASGIMiddleware)


#Rotas PRODUTOS
app.include_router(rotas_produtos.router)

#Rotas SEGURANÇA: Autenticação e Autorização
app.include_router(rotas_auth.router, prefix="/auth")

#Rotas PEDIDOS
app.include_router(rotas_pedidos.router)

# Background Tasks
@app.post('/send_email/{email}')
def send_email(email: str, background: BackgroundTasks):
    background.add_task(write_notification,
                        email, 'Ola tudo bem?!')
    return {'OK': 'Mensagem enviada'}