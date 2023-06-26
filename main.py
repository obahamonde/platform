from aiofauna import FaunaModel

from server import bootstrap

app = bootstrap()

@app.on_event("startup")
async def startup(_):
    await FaunaModel.create_all()
    
app.run()