import os
from dotenv import load_dotenv


current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)


class LLMConfig:
    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str | None = None,
        timeout: int = 60,
    ):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    @classmethod
    def from_env(cls):
        timeout_env = os.getenv("LLM_TIMEOUT")

        return cls(
            model=os.getenv("LLM_MODEL_ID"),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
            timeout=int(timeout_env) if timeout_env else 60,
        )


class ToolConfig:
    def __init__(self, serpapi_api_key: str | None):
        self.serpapi_api_key = serpapi_api_key

    @classmethod
    def from_env(cls):
        return cls(
            serpapi_api_key=os.getenv("SERPAPI_API_KEY")
        )


class Settings:
    def __init__(self):
        self.llm = LLMConfig.from_env()
        self.tools = ToolConfig.from_env()


settings = Settings()


if __name__ == "__main__":
    print("[+] LLM Config:")
    print(f"[+] Model: {settings.llm.model}")
    print(f"[+] API Key: {settings.llm.api_key}")
    print(f"[+] Base URL: {settings.llm.base_url}")
    print(f"[+] Timeout: {settings.llm.timeout}")

    print("\n[+] Tool Config:")
    print(f"[+] SerpAPI API Key: {settings.tools.serpapi_api_key}")
