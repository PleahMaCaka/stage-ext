from fastapi import APIRouter, Depends, HTTPException
from extensions.stage.auth import verify_token
from modules.utils import get_available_instruction_templates
from modules import shared

router = APIRouter()


@router.get("/", dependencies=[Depends(verify_token)])
async def instruct_root():
    return [m for m in get_available_instruction_templates() if m != "None"]


@router.get("/current", dependencies=[Depends(verify_token)])
async def instruct_current():
    name = shared.settings['instruction_template']

    if name == "None":
        raise HTTPException(status_code=404, detail="No instruction template is currently loaded")

    return name
