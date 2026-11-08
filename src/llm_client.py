#LLM SDK封装、重试、异常、超时
import os 
from openai import OpenAI

#延迟初始化
_CLIENT = None
def get_llm_client():#按需创建客户端
    global _CLIENT
    if _CLIENT is None:
        key = os.environ.get("DEEPSEEK_API_KEY")
        _CLIENT = OpenAI(api_key=key,base_url = "https://api.deepseek.com")
    return _CLIENT
