from typing import *

from aiofauna import ApiClient
from bs4 import BeautifulSoup
from pydantic import BaseModel  # pylint=disable=all
from pydantic import Field as Item
from pydantic import HttpUrl


class GoogleQueryRequest(BaseModel):
    query: str = Item(..., description="Human input that led to a google search result")
    page: int = Item(default=1, description="Page number of the google search result")
    lang: str = Item(default="en", description="Language of the google search result")

    def build_qs(self):
        return f"q={self.query}&start={self.page}&hl={self.lang}"


class GoogleQueryResponse(BaseModel):
    title: str = Item(..., description="Title of the google search result")
    url: HttpUrl = Item(..., description="Url of the result website")


class GoogleSearch(BaseModel):
    query: GoogleQueryRequest = Item(..., description="Google search query")
    results: List[GoogleQueryResponse] = Item(
        ..., description="List of google search results"
    )


class GoogleSearchTool(ApiClient):
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }

    async def search(self, query: GoogleQueryRequest) -> GoogleSearch:
        qs = query.build_qs()
        response = await self.text(qs)
        assert isinstance(response, str)
        soup = BeautifulSoup(response, "html.parser")
        results = soup.find_all("div", class_="yuRUbf")
        return GoogleSearch(
            query=query,
            results=[
                GoogleQueryResponse(
                    title=result.find("h3").text, url=result.find("a").get("href")
                )
                for result in results
            ],
        )
