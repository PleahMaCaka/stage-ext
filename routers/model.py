from fastapi import APIRouter, Depends

from extensions.stage.auth import verify_token
from modules.utils import get_available_models

router = APIRouter()


@router.get("/", dependencies=[Depends(verify_token)])
async def model_root():
    res = []
    for m in get_available_models():
        if m != "None":
            res.append(m)
        # more if statements here
    return {"models": res}
