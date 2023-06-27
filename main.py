import aiohttp_cors
from aiofauna import FaunaModel

from server import bootstrap

app = bootstrap()

@app.on_event("startup")
async def startup(_):
    await FaunaModel.create_all()
    
    
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
    
})



for route in list(app.router.routes()):
    cors.add(route)
    
    
app.run()