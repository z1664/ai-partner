from src.llm_client import get_llm_client  #摘要生成+清洗思考
from config import MODEL_NAME,SUMMARY_TEMPERATURE
import re

#第一次调用才创建客户端
_client = None
def _get_client():
    global _client
    if _client is None:
        _client = get_llm_client()
    return _client

def strip_thinking(text:str)->str: #清除deepseek-flash的思考过程
    return re.sub(r"[\s\S]*?","",text,flags=re.DOTALL).strip()

def summarizxer_history(old_messages:list)->str:
    prompt = """请精简总结一下对话历史，保留：用户性格、偏好、关键信息、重复对话内容。
                删除重复、无意义、琐碎闲聊。输出干净简短摘要。只返回摘要内容，，不要解释。历史对话："""
    +str(old_messages)
    client = _get_client()
    resp=client.chat_completion.create(model=MODEL_NAME,messages=[{"role": "user", "content": prompt}],temperature=SUMMARY_TEMPERATURE)
    raw_result = resp.choices[0].message.content
    return strip_thinking(raw_result)