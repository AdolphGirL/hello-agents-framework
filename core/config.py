import os
from dotenv import load_dotenv


current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)


def get_bool(env_key: str, default: str = "false") -> bool:
    return os.getenv(env_key, default).lower() == "true"


class LLMConfig:
    def __init__(
        self,
        source: str,
        model: str,
        base_url: str,
        api_key: str | None,
        timeout: int = 60,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ):
        self.source = source
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens

    @classmethod
    def from_env(cls):
        source = os.getenv("LLM_SOURCE", "aihubmix")

        timeout = int(os.getenv("LLM_TIMEOUT", "60"))
        temperature = float(os.getenv("TEMPERATURE", "0.7"))
        max_tokens_env = os.getenv("MAX_TOKENS")
        max_tokens = int(max_tokens_env) if max_tokens_env else None

        if source == "ollama":
            return cls(
                source=source,
                model=os.getenv("LLM_OLLAMA_MODEL_ID"),
                base_url=os.getenv("LLM_OLLAMA_BASE_URL"),
                api_key="ollama",
                timeout=timeout,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        if source == "aihubmix":
            return cls(
                source=source,
                model=os.getenv("LLM_AIHUBMIX_MODEL_ID"),
                base_url=os.getenv("LLM_AIHUBMIX_BASE_URL"),
                api_key=os.getenv("LLM_AIHUBMIX_API_KEY"),
                timeout=timeout,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        raise ValueError(f"Unsupported LLM_SOURCE: {source}")


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
        self.debug = get_bool("DEBUG", "false")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        self.llm = LLMConfig.from_env()
        self.tools = ToolConfig.from_env()


settings = Settings()


if __name__ == "__main__":
    print("[+] Global Settings:")
    print(f"[+] Debug: {settings.debug}")
    print(f"[+] Log Level: {settings.log_level}")

    print("\n[+] LLM Config:")
    print(f"[+] Source: {settings.llm.source}")
    print(f"[+] Model: {settings.llm.model}")
    print(f"[+] Base URL: {settings.llm.base_url}")
    print(f"[+] Timeout: {settings.llm.timeout}")
    print(f"[+] Temperature: {settings.llm.temperature}")
    print(f"[+] Max Tokens: {settings.llm.max_tokens}")

    # 🔐 避免完整洩漏 API Key
    api_key = settings.llm.api_key
    masked_key = api_key[:4] + "****" + api_key[-4:] if api_key else None
    print(f"[+] API Key: {masked_key}")

    print("\n[+] Tool Config:")
    serp_key = settings.tools.serpapi_api_key
    serp_masked = serp_key[:4] + "****" + serp_key[-4:] if serp_key else None
    print(f"[+] SerpAPI API Key: {serp_masked}")
