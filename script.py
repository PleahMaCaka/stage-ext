import uvicorn
from fastapi import FastAPI

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

uvicorn.run(app, host="0.0.0.0", port=9999)
