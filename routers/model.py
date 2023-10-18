from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from extensions.stage.auth import verify_token
from modules import shared
from modules.models import unload_model, load_model, reload_model
from modules.utils import get_available_models

router = APIRouter()


@router.get("/", dependencies=[Depends(verify_token)])
async def model_root():
    return [m for m in get_available_models() if m != "None"]


@router.get("/current", dependencies=[Depends(verify_token)])
async def model_current():
    name = shared.model_name

    if name == "None":
        raise HTTPException(status_code=404, detail="No model is currently loaded")

    return name


@router.post("/unload", dependencies=[Depends(verify_token)])
async def model_unload():
    unload_model()

    return {"message": "Model unloaded"}


@router.post("/load", dependencies=[Depends(verify_token)])
async def model_load(name: str, loader: Optional[str] = None):
    """
    :param name: The name of the model to load
    :param loader: The loader to use - If None, the default loader is used.
    """

    # Is the model available?
    if name == "None":
        raise HTTPException(
            status_code=400,
            detail="The model name cannot be 'None', if you want to unload the model, use the /unload endpoint")

    if name not in get_available_models():
        raise HTTPException(status_code=400, detail=f"Model {name} not found")

    # Is the loader available?

    # Loaders can find here :
    # https://github.com/oobabooga/text-generation-webui/blob/c0ffb77fd8471c1cade593879d17d2e817a1ed0b/modules/models.py#L54-L67
    loaders = ["Transformers", "AutoGPTQ", "GPTQ-for-LLaMa", "llama.cpp", "llamacpp_HF", "RWKV", "ExLlama",
               "ExLlama_HF", "ExLlamav2", "ExLlamav2_HF", "ctransformers", "AutoAWQ"]

    if loader is not None and loader not in loaders:
        raise HTTPException(status_code=400, detail=f"Loader {loader} not found")

    load_model(name, loader)

    return {"message": f"Model {name} loaded with {loader}"}


@router.get("/reload", dependencies=[Depends(verify_token)])
async def model_reload():
    if shared.model_name == "None":
        raise HTTPException(status_code=404, detail="No model is currently loaded")

    reload_model()

    return {"message": "Model reloaded"}
