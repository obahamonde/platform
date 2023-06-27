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
        tokens = 0
        ref = request.user
        prompt_request = request.prompt
        # Similarity Search
        user_ada_response = await openai.get_embeddings(EmbeddingRequest(input=prompt_request))        
        tokens += user_ada_response.usage.total_tokens
        user_embedding = user_ada_response.data[0].embedding
        pinecone_response = await pinecone.query(EmbeddingQuery(vector=user_embedding))
        pinecone_matches = pinecone_response.matches
        context = [Context(key=match.metadata["text"],value=match.score) for match in pinecone_matches]
        # Get the response from OpenAI
        request.context = context
        openai_response = await openai.get_completion(request)
        gpt_response = openai_response.choices[0].message.content
        tokens += openai_response.usage.total_tokens
        # Retrieve GPT Embedding
        gpt_ada_response = await openai.get_embeddings(EmbeddingRequest(input=gpt_response))
        gpt_embedding = gpt_ada_response.data[0].embedding
        tokens += gpt_ada_response.usage.total_tokens
        # Upsert the embeddings on Pinecone
        await pinecone.upsert(EmbeddingUpsert(vector=user_embedding, id=str(uuid4()), metadata={"text": prompt_request}))
        await pinecone.upsert(EmbeddingUpsert(vector=gpt_embedding, id=str(uuid4()), metadata={"text": gpt_response}))
        # Return the response
        return await ChatGpt(
            user=ref,
            prompt=prompt_request,
            response=gpt_response,
            tokens=tokens,
            context=context,
        ).save()
        
        
  
  
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