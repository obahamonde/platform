from aiofauna import ApiClient

from ..config import env
from ..utils import nginx_render


class CloudFlare(ApiClient):
    """Domain provisioning service"""

    base_url = "https://api.cloudflare.com/client/v4/"
    headers = {
        "X-Auth-Email": env.CF_EMAIL,
        "X-Auth-Key": env.CF_API_KEY,
        "Content-Type": "application/json",
    }
    
    def __init__(self):
        super().__init__(self.base_url, headers=self.headers)

    async def provision(self, name: str, port: int):
        """
        Provision a new domain
        """
        try:
            response = await self.fetch(
                f"/zones/{env.CF_ZONE_ID}/dns_records",
                "POST",
                json={
                    "type": "A",
                    "name": name,
                    "content": env.IP_ADDR,
                    "ttl": 1,
                    "priority": 10,
                    "proxied": True,
                },
            )
            print(response)
            assert isinstance(response, dict)
           
            data = response["result"]
            nginx_render(name=name, port=port)
            return {
                "url": f"https://{name}.aiofauna.com",
                "ip": f"https://{env.IP_ADDR}:{port}",
                "data": data,
            }
        except Exception as exc:
            raise exc
