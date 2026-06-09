import os
import re

import httpx


class TextSummaryService:
    def __init__(
        self,
        provider: str,
        enabled: bool,
        api_key: str | None = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        model: str = "meta/llama-3.1-8b-instruct",
    ):
        self.provider = provider
        self.enabled = enabled
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    @classmethod
    def from_env(cls) -> "TextSummaryService":
        nvidia_base_url = os.getenv(
            "NVIDIA_BASE_URL",
            "https://integrate.api.nvidia.com/v1",
        )

        return cls(
            provider=os.getenv("SUMMARY_PROVIDER", "local").lower(),
            enabled=os.getenv("ENABLE_TEXT_SUMMARY", "true").lower() == "true",
            api_key=os.getenv("NVIDIA_API_KEY"),
            base_url=nvidia_base_url,
            model=os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct"),
        )

    async def summarize(self, text: str) -> str:
        clean_text = self._clean_text(text)

        if not self.enabled:
            return "Resumen deshabilitado por configuracion."

        if not clean_text:
            return "No hay texto suficiente para resumir."

        if self.provider == "nvidia":
            return await self._summarize_with_nvidia(clean_text)

        return self._summarize_locally(clean_text)

    def _clean_text(self, text: str) -> str:
        return " ".join(text.split())

    def _summarize_locally(self, text: str) -> str:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        selected_sentences = sentences[:3]
        summary = " ".join(selected_sentences)

        if len(summary) > 800:
            return summary[:800].rsplit(" ", 1)[0] + "..."

        return summary

    async def _summarize_with_nvidia(self, text: str) -> str:
        if not self.api_key:
            return "No se configuro NVIDIA_API_KEY."

        prompt_text = text[:12000]

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Sos un asistente que resume documentos en espanol "
                        "de forma breve, clara y precisa."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Resumi el siguiente texto en un parrafo:\n\n{prompt_text}",
                },
            ],
            "temperature": 0.2,
            "max_tokens": 300,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
