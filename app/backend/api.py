from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings

from app.common.logger import get_logger
logger = get_logger(__name__)

from app.common.custom_exception import CustomException

app = FastAPI(title="MULTI AI AGENT", version="1.0.0")

class RequestState(BaseModel):
    model_name: str = 'openai/gpt-oss-120b'
    system_prompt: Optional[str]
    messeges:List[str]
    allow_search: Optional[bool] = False
    
@app.post("/chat", status_code=200)
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for the model: {request.model_name}")
    
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.error(f"Model {request.model_name} is not allowed.")
        raise HTTPException(status_code=400, detail=f"Model {request.model_name} is not allowed.")
    try:
        response = get_response_from_ai_agents(
            llm_id=request.model_name,
            query=request.messeges,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
            )
        logger.info(f"Response generated successfully from AI agent using the model: {request.model_name}")
        
        return {"response": response.strip()}
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(CustomException("Failed to get response from AI agent", error_detail=e)))
    