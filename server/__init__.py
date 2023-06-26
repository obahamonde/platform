from aiofauna import Api, FaunaModel, Request, Response
from boto3.resources import base

from .middleware import middleware_stack
from .services import *


@middleware_stack()
class AioFauna(Api):
    ...
        
        
def bootstrap():
    """Bootstrap the application"""

    app = AioFauna()

    pinecone = PineConeService()

    openai = OpenAIService()

    aws = AmazonWebServices()


    cf = CloudFlare()
 



    @app.get("/api/user")
    async def users():
        return await User.all()


    @app.post("/api/chat")
    async def completion(request: ChatCompletionRequest):
        instance = await User.get(request.user)
        assert isinstance(instance, User)
        user = instance.name
        response = await openai.get_completion(request)
        # Retrieve embeddings from Ada
        user_embedding = await openai.get_embeddings(EmbeddingRequest(input=request.prompt))
        open_ai_embedding = await openai.get_embeddings(
            EmbeddingRequest(input=response.choices[0].message.content)
        )
        # Insert Messages into FaunaDB
        chatgpt_message, user_message = (
            await Message(
                content=response.choices[0].message.content,
                author="openai",
                tokens=response.usage.completion_tokens,
            ).save(),
            await Message(
                content=request.prompt, author=user, tokens=response.usage.prompt_tokens
            ).save(),
        )
        await pinecone.upsert(EmbeddingUpsert(id=chatgpt_message.ref, vector=open_ai_embedding.data[0].embedding))  # type: ignore
        await pinecone.upsert(EmbeddingUpsert(id=user_message.ref, vector=user_embedding.data[0].embedding))  # type: ignore
        return response.choices[0].message.content

  
    @app.post("/api/upload")
    async def upload(request: Request):
        params = dict(request.query)
        file = (await request.post())["file"]
        size = int(params.pop("size"))
        assert isinstance(file, FileField)
        return await aws.upload(UploadRequest(file=file, size=size, **params))
    
        

    @app.post("/api/github")
    async def callback(code: CodeRequest):
        try:
            github = GitHubService()
            github.base_url = "https://github.com"
            payload = {
                "client_id": env.GH_CLIENT_ID,
                "client_secret": env.GH_CLIENT_SECRET,
                "redirect_uri": f"http://{env.CLIENT_URL}/login",
                "code": code.code,
                "state": "1234",
            }
            response = await github.fetch("/login/oauth/access_token", "POST", json=payload)
            assert isinstance(response, dict)
            access_token = response["access_token"]
            github_api = GitHubService(access_token)
            gh_user = await github_api.fetch("/user")
            assert isinstance(gh_user, dict)
            user = await User(
                **{
                    "sub": gh_user["id"],
                    "name": gh_user["login"],
                    "email": gh_user["email"],
                    "picture": gh_user["avatar_url"],
                    "emailverified": gh_user["email"] is not None,
                }
            ).save()

            assert isinstance(user, User)
            return {"user": user.dict() , "token": access_token}
        except Exception as e:
            raise Exception from e


    @app.get("/api/github/repos")
    async def search_own_repos(token: str, query: str, login: str):
        gh = GitHubService(token)
        return await gh.search_repos(query, login)
        
    @app.post("/api/github/workspace")
    async def ci_pipeline(body: ContainerCreate):
        try:
            # Retrieve github token
            token = body.token
            # Instantiate github client
            github = GitHubService(body.token)
            # Instantiate Docker client
            docker = DockerService()
            # Create Docker volume
            volume = await docker.create_volume(tag=body.login + "-" + body.repo)
            # Create App container
            _app = await docker.create_container(body, volume)
            # Provision App Container [ERROR]
            dns_app = await cf.provision(body.login + "-" + body.repo, _app.host_port)

            # instantiate IDE container
            ide = ContainerCreate(
                login=body.login,
                repo=body.repo,
                token=token,
                email=body.email,
                image="codeserver",
            )
            # Create IDE container
            codeserver = await docker.create_code_server(ide, volume)
            # Provision IDE container
            dns_codeserver = await cf.provision(
                body.login + "-" + body.image, codeserver.host_port
            )
            # Create Repo from template
            repo_response = await github.create_repo_from_template(
                RepoTemplateCreate(
                    name=body.repo,
                    template_owner="obahamonde",
                    template_repo=body.image,
                    login=body.login,
                    token=token,
                    email=body.email,
                )
            )
            assert isinstance(repo_response, dict)
            
            # Construct response payload
            preview = {
            "url": dns_app["url"],
            "ip": f"{env.IP_ADDR}:{_app.host_port}",
            "container": _app.container_id,
            "repo": 1#repo_response["html_url"],
        }
            workspace = {
            "url": dns_codeserver["url"],
            "ip": f"{env.IP_ADDR}:{codeserver.host_port}",
            "container": codeserver.container_id,
        }
            return {"workspace": workspace, "preview": preview}
        except Exception as e:
            raise e   
            
                 
    return app