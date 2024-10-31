import uvicorn
from fastapi import FastAPI


from service.views import service_router
from settings import HOST, PORT

app = FastAPI()
app.include_router(service_router)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
