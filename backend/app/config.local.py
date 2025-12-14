from __future__ import annotations

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # ✅ IMPORTANT: keep this as a STRING so pydantic doesn't json.loads it automatically
    ALLOWED_EXTENSIONS: str = "pdf,docx"

    @property
    def allowed_extensions_list(self) -> List[str]:
        """
        Safe parsing:
        - supports: "pdf,docx"
        - supports: '["pdf","docx"]'
        - supports: empty -> default
        """
        v = (self.ALLOWED_EXTENSIONS or "").strip()
        if not v:
            return ["pdf", "docx"]

        # JSON list support
        if v.startswith("["):
            import json
            try:
                data = json.loads(v)
                if isinstance(data, list):
                    return [str(x).strip().lstrip(".") for x in data if str(x).strip()]
            except Exception:
                pass

        # CSV / single support
        return [x.strip().lstrip(".") for x in v.split(",") if x.strip()]


settings = Settings()
