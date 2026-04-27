from hello_agents import SimpleAgent, HelloAgentsLLM
from core.config import settings


llm = HelloAgentsLLM(model=settings.llm.model, api_key=settings.llm.api_key, base_url=settings.llm.base_url,
                     timeout=settings.llm.timeout)

# 創建SimpleAgent
agent = SimpleAgent(
    name="AI助理",
    llm=llm,
    system_prompt="你是一個有用的AI助手"
)

# 基础对话
response = agent.run("你好！請介紹一下自己")
print(response)

# 查看对话历史
print(f"歷史消息數: {len(agent.get_history())}")
