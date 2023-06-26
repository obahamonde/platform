from typing import *

from aiofauna import ApiClient, BaseModel
from aiofauna import FaunaModel as Model
from aiofauna import Field

from ..utils import gen_port

TemplatesAvailable = Literal[
    "react", "vue", "flask", "express", "fastapi", "php", "codeserver", "ruby"
]


class ContainerCreate(BaseModel):
    """
    - ContainerCreate
        - login:str
        - repo:str
        - token:str
        - email:str
        - image:str = "codeserver"
    """

    login: str = Field(..., description="User reference")
    repo: str = Field(..., description="Repo reference")
    token: str = Field(..., description="Github token")
    email: str = Field(..., description="Email of the user")
    image: TemplatesAvailable = Field(..., description="Image to use")


class CodeServer(Model):
    """
    - CodeServer
        - login:str
        - repo:str
        - container_id:str
        - image:str
        - host_port:int
        - env_vars:List[str]

        - payload(token:str, volume:str) -> Dict[str, Any]
    """

    login: str = Field(..., index=True, description="User reference")
    repo: str = Field(..., description="User reference", unique=True)
    container_id: Optional[str] = Field(default=None)
    image: str = Field(default="codeserver", description="Image to use")
    host_port: int = Field(default_factory=gen_port, description="Port to expose")
    email: str = Field(..., description="Email of the user")
    env_vars: Optional[List[str]] = Field(
        default=[], description="Environment variables"
    )

    def payload(self, token: str, volume: str):
        extensions = [
            "ms-python.isort",
            "ms-python.python",
            "TabNine.tabnine-vscode",
            "PKief.material-icon-theme",
            "esbenp.prettier-vscode",
            "ms-python.isort",
            "ms-pyright.pyright",
            "RobbOwen.synthwave-vscode"
        ]
        assert isinstance(self.env_vars, list)
        self.env_vars.append(f"GITHUB_TOKEN={token}")
        self.env_vars.append(f"GITHUB_REPO=https://github.com/{self.login}/{self.repo}")
        self.env_vars.append(f"EMAIL={self.email}")
        self.env_vars.append(f"PASSWORD={self.login}")
        self.env_vars.append("TZ=America/New_York")
        self.env_vars.append(f"USER={self.login}")
        self.env_vars.append(f"SUDO_PASSWORD={self.login}")
        self.env_vars.append(f"EXTENSIONS={','.join(extensions)}")
        git_startup_script = f"""
        set -e\n
        export HOME=/root\n
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash\n
        export NVM_DIR="$HOME/.nvm"\n
        [ -s "$NVM_DIR/nvm.sh" ] && \\. "$NVM_DIR/nvm.sh"\n
        [ -s "$NVM_DIR/bash_completion" ] && \\. "$NVM_DIR/bash_completion"\n
        nvm install 16\n
        nvm use 16\n
        npm install -g yarn\n
        export PATH=$PATH:/app/code-server/bin\n
        export GIT_TERMINAL_PROMPT=0\n
        export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"\n
        export GIT_COMMITTER_NAME={self.login}\n
        git config --global user.name {self.login}\n
        git config --global user.email {self.login}@github.com\n
        git config --global credential.helper 'store --file=/tmp/git_credentials'\n
        cd /config/workspace\n
        git init\n
        """
        for extension in extensions:
            git_startup_script += f"code-server --install-extension {extension}\n"
        git_startup_script += """
        code-server --disable-telemetry
        """
        
        return {
            "Image": self.image,
            "Env": self.env_vars,
            "ExposedPorts": {"8443/tcp": {"HostPort": str(self.host_port)}},
            "HostConfig": {
                "PortBindings": {"8443/tcp": [{"HostPort": str(self.host_port)}]},
                "Binds": [f"{volume}:/config/workspace"],
            },
            "Cmd": ["/usr/bin/bash", "-c", git_startup_script],
        }


class Container(Model):  # pylint:disable=all
    """
    - Container
        - login:str
        - repo:str
        - container_id:str
        - image:str
        - host_port:int
        - env_vars:List[str]

        - payload(token:str, volume:str) -> Json
    """

    login: Optional[str] = Field(default=None, index=True)
    repo: str = Field(..., description="Github Repo", unique=True)
    image: str = Field(..., description="Image to use")
    host_port: int = Field(default_factory=gen_port, description="Port to expose")
    container_port: int = Field(default=8080, description="Port to expose")
    env_vars: List[str] = Field(
        default=["DOCKER=1"], description="Environment variables"
    )
    container_id: Optional[str] = Field(default=None)

    def payload(self, token: str, volume: str):
        assert isinstance(self.env_vars, list)
        if self.image == "php":
            dir_ = "/var/www/html"
        else:
            dir_ = "/app"
        self.env_vars.append(f"GH_TOKEN={token}")
        self.env_vars.append(f"GH_REPO=https://github.com/{self.login}/{self.repo}]")
        return {
            "Image": self.image,
            "Env": self.env_vars,
            "ExposedPorts": {
                f"{self.container_port}/tcp": {"HostPort": str(self.host_port)}
            },
            "HostConfig": {
                "PortBindings": {
                    f"{self.container_port}/tcp": [{"HostPort": str(self.host_port)}]
                },
                "Binds": [f"{volume}:/{dir_}"],
            },
        }


class DockerService(ApiClient):
    """
    DockerService
        - start_container(container_id:str) -> None
        - create_volume(tag:str) -> str
        - create_container(body:ContainerCreate, volume:str) -> Container
    """

    def __init__(self, *args, **kwargs):
        self.base_url = "http://localhost:9898"
        super().__init__(base_url=self.base_url, *args, **kwargs)

    async def start_container(self, container_id: str):
        """
        Starts a container
        - (container_id:str) -> None
        """
        await self.text(f"/containers/{container_id}/start", method="POST")

    async def create_volume(self, tag: str) -> str:
        """Create a volume
        - (tag:str) -> str
        """
        payload = {"Name": tag, "Driver": "local"}
        await self.fetch(
            "/volumes/create",
            method="POST",
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        return tag

    async def create_container(self, body: ContainerCreate, volume: str):
        """Create a python container
        - (body:ContainerCreate) -> Container
        """
        container = Container(**body.dict())
        payload = container.payload(body.token, volume)
        response = await self.fetch(
            "/containers/create",
            method="POST",
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        assert isinstance(response, dict)
        container.container_id = response["Id"]
        instance = await container.save()
        assert isinstance(instance, Container)
        assert isinstance(instance.container_id, str)
        await self.start_container(instance.container_id)
        return instance

    async def create_code_server(
        self, body: ContainerCreate, volume: str
    ) -> CodeServer:
        """
        Create a code-server container
        - (body:ContainerCreate) -> CodeServer
        """
        codeserver = CodeServer(**body.dict())
        payload = codeserver.payload(body.token, volume)
        response = await self.fetch(
            "/containers/create",
            method="POST",
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        assert isinstance(response, dict)
        codeserver.container_id = response["Id"]
        instance = await codeserver.save()
        assert isinstance(instance, CodeServer)
        assert isinstance(instance.container_id, str)
        await self.start_container(instance.container_id)
        return instance
