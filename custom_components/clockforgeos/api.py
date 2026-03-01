from __future__ import annotations

from typing import Any

import aiohttp


class ClockForgeApi:
    def __init__(self, host: str, username: str | None, password: str | None, session: aiohttp.ClientSession) -> None:
        self._base_url = f"http://{host}"
        self._auth = aiohttp.BasicAuth(username, password) if username and password else None
        self._session = session

    async def get_status(self) -> dict[str, Any]:
        return await self._request_json("GET", "/api/status")

    async def get_settings(self) -> dict[str, Any]:
        return await self._request_json("GET", "/api/settings")

    async def post_command(self, action: str, **extra: Any) -> dict[str, Any]:
        payload = {"action": action}
        payload.update(extra)
        return await self._request_json("POST", "/api/command", data=payload)

    async def post_settings(self, **extra: Any) -> dict[str, Any]:
        return await self._request_json("POST", "/api/settings", data=extra)

    async def _request_json(self, method: str, path: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        async with self._session.request(
            method,
            f"{self._base_url}{path}",
            auth=self._auth,
            data=data,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            response.raise_for_status()
            return await response.json()
