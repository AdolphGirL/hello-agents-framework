"""消息類系統"""
from typing import Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field

# 定義角色，限制存取
MessageRole = Literal["user", "assistant", "system", "tool"]


class Message(BaseModel):
    """消息類"""

    content: str
    role: MessageRole
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """轉換為 OpenAI API 格式"""
        return {
            "role": self.role,
            "content": self.content
        }

    def __str__(self) -> str:
        return f"[{self.role}] {self.content}"


def main():
    # 1️⃣ 建立單一 message
    msg1 = Message(
        content="你好，這是一個測試訊息",
        role="user"
    )

    print("=== 單一 Message ===")
    print(msg1)
    print(msg1.to_dict())
    print(msg1.timestamp)
    print(msg1.metadata)

    # 2️⃣ 建立 assistant 回覆
    msg2 = Message(
        content="你好！有什麼可以幫你？",
        role="assistant",
        metadata={"model": "gpt-5.3"}
    )

    print("\n=== Assistant Message ===")
    print(msg2)
    print(msg2.to_dict())

    # 3️⃣ 模擬對話列表
    conversation: List[Message] = [msg1, msg2]

    print("\n=== 對話紀錄 ===")
    for msg in conversation:
        print(msg)

    # 4️⃣ 轉換為 OpenAI API 格式
    api_messages = [msg.to_dict() for msg in conversation]

    print("\n=== API Messages ===")
    for m in api_messages:
        print(m)

    # 5️⃣ 新增 tool / system message
    system_msg = Message(
        content="你是一個專業助理",
        role="system"
    )

    tool_msg = Message(
        content="查詢完成",
        role="tool",
        metadata={"tool_name": "search"}
    )

    conversation.extend([system_msg, tool_msg])

    print("\n=== 加入 system / tool 後 ===")
    for msg in conversation:
        print(msg)

    # 6️⃣ 篩選特定角色
    user_messages = [m for m in conversation if m.role == "user"]

    print("\n=== 只看 user 訊息 ===")
    for msg in user_messages:
        print(msg)


if __name__ == "__main__":
    main()
