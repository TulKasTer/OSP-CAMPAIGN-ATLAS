"""Provider-agnostic LLM client powered by LiteLLM and Instructor with local RAM/VRAM controls."""

from __future__ import annotations

from typing import Any, Literal, TypeVar
import instructor
import litellm
from pydantic import BaseModel

from ..config import LLMSettings, get_settings
from ..schemas.api import ModelOverrideConfig

T = TypeVar("T", bound=BaseModel)


class StructuredLLMClient:
    """Wrapper around LiteLLM + Instructor for structured Pydantic extraction."""

    def __init__(self, settings: LLMSettings | None = None) -> None:
        self.settings = settings or get_settings()
        self._tool_client = instructor.from_litellm(litellm.completion)
        self._json_client = instructor.from_litellm(
            litellm.completion,
            mode=instructor.Mode.JSON,
        )

    def _resolve_temperature(
        self,
        phase: Literal["gates", "coding", "default"],
        override: ModelOverrideConfig | None,
    ) -> float:
        if override and override.temperature is not None:
            return override.temperature
        if phase == "gates" and self.settings.gates_temperature is not None:
            return self.settings.gates_temperature
        if phase == "coding" and self.settings.coding_temperature is not None:
            return self.settings.coding_temperature
        return self.settings.temperature

    def extract(
        self,
        response_model: type[T],
        system_prompt: str,
        user_prompt: str,
        override: ModelOverrideConfig | None = None,
        phase: Literal["gates", "coding", "default"] = "default",
    ) -> T:
        """Execute a structured LLM completion and validate into `response_model`."""
        model = (override.model if override and override.model else None) or self.settings.model
        api_key = (override.api_key if override and override.api_key else None) or self.settings.api_key
        api_base = (override.api_base if override and override.api_base else None) or self.settings.api_base
        is_ollama = model.lower().startswith(("ollama/", "ollama_chat/"))

        if not api_base and is_ollama:
            api_base = self.settings.local_api_base

        temperature = self._resolve_temperature(phase, override)
        top_p = (override.top_p if override and override.top_p is not None else None) or self.settings.top_p
        max_tokens = (
            override.max_tokens if override and override.max_tokens is not None else None
        ) or self.settings.max_tokens
        seed = (override.seed if override and override.seed is not None else None) or self.settings.seed

        kwargs: dict[str, Any] = {
            "model": model,
            "response_model": response_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_retries": self.settings.max_retries,
            "timeout": self.settings.timeout_seconds,
        }
        if api_key:
            kwargs["api_key"] = api_key
        if api_base:
            kwargs["api_base"] = api_base
        if top_p is not None:
            kwargs["top_p"] = top_p
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        if seed is not None:
            kwargs["seed"] = seed
        if not is_ollama and self.settings.presence_penalty is not None:
            kwargs["presence_penalty"] = self.settings.presence_penalty
        if not is_ollama and self.settings.frequency_penalty is not None:
            kwargs["frequency_penalty"] = self.settings.frequency_penalty

        # Forward local hardware (RAM / VRAM) and Ollama-specific sampling options
        if is_ollama:
            # Qwen reasoning models otherwise place the structured payload in
            # reasoning_content, while Instructor expects it in message.content.
            kwargs["reasoning_effort"] = "none"
            num_ctx = (
                override.num_ctx if override and override.num_ctx is not None else self.settings.num_ctx
            )
            num_gpu = (
                override.num_gpu if override and override.num_gpu is not None else self.settings.num_gpu
            )
            num_thread = (
                override.num_thread
                if override and override.num_thread is not None
                else self.settings.num_thread
            )
            num_batch = (
                override.num_batch
                if override and override.num_batch is not None
                else self.settings.num_batch
            )
            top_k = (
                override.top_k if override and override.top_k is not None else self.settings.top_k
            )
            keep_alive = (
                override.keep_alive
                if override and override.keep_alive is not None
                else self.settings.keep_alive
            )

            kwargs["num_ctx"] = num_ctx
            kwargs["keep_alive"] = keep_alive

            ollama_options: dict[str, Any] = {
                "num_ctx": num_ctx,
                "num_gpu": num_gpu,
                "main_gpu": self.settings.main_gpu,
                "num_batch": num_batch,
                "use_mmap": self.settings.use_mmap,
                "use_mlock": self.settings.use_mlock,
                "low_vram": self.settings.low_vram,
            }
            if num_thread > 0:
                ollama_options["num_thread"] = num_thread
            if top_k is not None:
                ollama_options["top_k"] = top_k
            if self.settings.min_p is not None:
                ollama_options["min_p"] = self.settings.min_p
            if self.settings.repeat_penalty is not None:
                ollama_options["repeat_penalty"] = self.settings.repeat_penalty
            if seed is not None:
                ollama_options["seed"] = seed

            kwargs["extra_body"] = {"options": ollama_options, "keep_alive": keep_alive}

        client = self._json_client if is_ollama else self._tool_client
        return client.chat.completions.create(**kwargs)
