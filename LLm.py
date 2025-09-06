from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    api_version="2025-01-01-preview",  # or your api version
    temperature=0,
)