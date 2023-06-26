from typing import *
from uuid import uuid4

from aiofauna import ApiClient
from pydantic import BaseModel
from pydantic import Field as Data

from ..config import env
from ..schemas.models import *


class EmbeddingUpsert(BaseModel):
    """
    EmbeddingUpsert
        - vector: List[float]
        - metadata: Dict[str, Scalar]
        - id: str
    """

    vector: List[float] = Data(..., description="The vector of the embedding.")
    metadata: Dict[str, Scalar] = Data(
        default_factory=dict,
        description="The metadata of the embedding. Must be a dictionary of strings.",
    )
    id: str = Data(..., description="The ID of the embedding. Must be a string.")


class EmbeddingQuery(BaseModel):
    """
    EmbeddingQuery
        - namespace: str
        - topK: int
        - embedding: List[float]
    """

    topK: int = Data(default=1, description="The number of results to return.")
    embedding: List[float] = Data(..., description="The vector of the embedding")


class SparsedValues(BaseModel):
    """
    SparsedValues
        - indices: List[int]
        - values: List[float]
        - shape: List[int]
    """

    indices: List[int] = Data(..., description="The indices of the embedding.")
    values: List[float] = Data(..., description="The values of the embedding.")


class EmbeddingMatch(BaseModel):
    """
    EmbeddingMatch
        - id: str
        - score: float
        - values: List[float]
        - sparseValues: SparsedValues
    """

    id: str = Data(..., description="The ID of the embedding.")
    score: float = Data(..., description="The score of the embedding.")
    values: List[float] = Data(..., description="The vector of the embedding.")
    sparseValues: SparsedValues = Data(
        ..., description="The sparse values of the embedding."
    )


class EmbeddingResponse(BaseModel):
    """
    EmbeddingResponse
        - namespace: str
        - matches: List[EmbeddingMatch]
    """

    namespace: str = Data(..., description="The namespace of the embedding.")
    matches: List[EmbeddingMatch] = Data(
        ..., description="The matches of the embedding."
    )


class PineConeService(ApiClient):
    """
    PineConeService
       - upsert(request:EmbeddingUpsert)->None
       - query(request:EmbeddingQuery)->EmbeddingResponse
    """

    def __init__(
        self,
        base_url: str = env.PINECONE_API_URL,
        headers: dict = {"api-key": env.PINECONE_API_KEY},
    ):
        super().__init__(base_url=base_url, headers=headers)

    async def upsert(self, request: EmbeddingUpsert) -> None:
        await self.fetch("/vectors/upsert", method="POST", json=request.dict())

    async def query(self, request: EmbeddingQuery):
        response = await self.fetch(
            "/vectors/query", method="POST", json=request.dict()
        )
        assert isinstance(response, dict)
        return EmbeddingResponse(**response)
