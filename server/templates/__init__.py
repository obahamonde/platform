from pathlib import Path
from typing import *

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from pydantic import Field as Data

jenv = Environment(
    loader=FileSystemLoader(Path(__file__).parent),
    autoescape=select_autoescape(["html", "xml"]),
)


class Context(BaseModel):
    key: str
    value: Union[str, int, float, bool]


class SystemMessageTemplate(BaseModel):
    context: List[Context] = Data(..., description="The context of the message")
    persona: str = Data(
        default="github copilot x", description="The role that the LLM should play"
    )
    name: str = Data(..., description="The name of the user")
    template: str = Data(default="base.j2", description="The Template to use")

    def get_template(self):
        return jenv.get_template(self.template)

    def render(self):
        return self.get_template().render(
            **{"name": self.name, "role": self.persona, "context": self.context}
        )
