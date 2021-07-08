from fastapi import Request
from starlette.types import ASGIApp, Scope, Receive, Send


class SimpleASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app


    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await self.app(scope, receive, send)
        assert scope['type'] == 'http'

        print('Interceptou Chegada')
        
        response = Request(scope, receive)

        print(response.method)

        print('Interceptou a Volta')