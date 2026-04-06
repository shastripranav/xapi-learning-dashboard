"""HTTP client for communicating with xAPI-conformant Learning Record Stores."""

import httpx

from ..config import settings

# TODO: add retry logic for transient network failures


class LRSClient:
    """Async client for fetching statements from an xAPI LRS."""

    def __init__(self, endpoint: str, username: str, password: str):
        self.endpoint = endpoint.rstrip("/")
        self.auth = (username, password)
        self.headers = {
            "X-Experience-API-Version": "1.0.3",
            "Content-Type": "application/json",
        }

    async def test_connection(self) -> bool:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.endpoint}/about",
                auth=self.auth,
                headers=self.headers,
                timeout=10.0,
            )
            return resp.status_code == 200

    async def fetch_statements(
        self, since: str | None = None, limit: int = 500
    ) -> list[dict]:
        """Fetch statements with pagination via the 'more' token."""
        all_statements = []
        params: dict = {"limit": limit}
        if since:
            params["since"] = since

        async with httpx.AsyncClient() as client:
            url = f"{self.endpoint}/statements"
            while url:
                resp = await client.get(
                    url,
                    params=params if url.endswith("/statements") else None,
                    auth=self.auth,
                    headers=self.headers,
                    timeout=30.0,
                )
                resp.raise_for_status()
                data = resp.json()

                stmts = data.get("statements", [])
                all_statements.extend(stmts)

                # LRS pagination uses opaque 'more' tokens, not offset
                more = data.get("more", "")
                if more:
                    url = more if more.startswith("http") else f"{self.endpoint}{more}"
                    params = {}
                else:
                    url = ""

        return all_statements

    async def post_statements(self, statements: list[dict]) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.endpoint}/statements",
                json=statements,
                auth=self.auth,
                headers=self.headers,
                timeout=30.0,
            )
            resp.raise_for_status()
            return resp.text


def get_lrs_client() -> LRSClient | None:
    if not settings.lrs_endpoint:
        return None
    return LRSClient(settings.lrs_endpoint, settings.lrs_username, settings.lrs_password)
