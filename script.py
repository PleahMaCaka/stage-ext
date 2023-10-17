from threading import Thread

import uvicorn
from fastapi import FastAPI, Depends

from extensions.stage.auth import verify_token

params = {
    "display_name": "Stage Extension",
    "is_tab": False,
}

print("Stage extension loaded.")

app = FastAPI()


@app.get("/")
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
