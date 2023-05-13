from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
OPENAI_API_KEY = "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"
chat = ChatAnthropic()
query = "Hi!"
messages = [
    HumanMessage(content=query)
]
print(chat(messages))