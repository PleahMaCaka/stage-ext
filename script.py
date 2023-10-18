import uvicorn
from fastapi import FastAPI, Depends

from extensions.stage.auth import verify_token
from extensions.stage.routers.model import router as model_router
from threading import Thread

params = {
    "display_name": "Stage Extension",
    "is_tab": False,
}

print("Stage extension loaded.")

app = FastAPI()

app.include_router(model_router, prefix="/model", tags=["model"])


@app.get("/", dependencies=[Depends(verify_token)])
async def root():
    return {"message": "Stage API is online!"}


print("Stage extension loaded.")


def run_server(do_host=True):
    uvicorn.run(app, host="0.0.0.0" if do_host else None, port=9999)


def run_server_threaded():
    t = Thread(target=run_server)
    t.start()

    return t


run_server_threaded()
