from __future__ import annotations

from typing import *

from aiofauna.odm import ModelMetaclass
from pydantic import BaseModel, Field

from server.services import ChatMessage, OpenAIService

Schema = Dict[str, Any]

class FunctionRequest(BaseModel):
    """
    FunctionRequest
        - model: str
        - input: str
    """
    model: str = Field(
        default="gpt-3.5-turbo-16k-0613",
        description="The ID of the engine to use for completion.",
    )
    messages: List[ChatMessage] = Field(
        default=[], description="Pair of messages from system and human", max_items=2
    )
    functions: List[Schema] = Field(default=[], description="Functions to call")
    temperature: float = Field(
        default=0.75,
        description="What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).",
    )
    max_tokens: int = Field(
        default=2048,
        description="The maximum number of tokens to generate. Requests can use up to 2048 tokens shared between prompt and completion.",
    )
    top_p: float = Field(
        default=1.0,
        description="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
    )
    frequency_penalty: float = Field(
        default=0.25,
        description="What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).",
    )
    presence_penalty: float = Field(
        default=0.25,
        description="What we call the 'creativity' of the AI. 0.0 is very conservative (highly repetitive), 1.0 is very creative (may say strange things or diverge from the topic at hand).",
    )
    n: int = Field(
        default=1, description="The number of completions to generate for each prompt."
    )


class Get(FunctionModel):
    """Fetches an URL with the GET method"""
    url:str

    
    
print(Get.function)