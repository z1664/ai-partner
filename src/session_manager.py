#会话、压缩、消息重组
from config import MAX_CHAT_TOKENS,KEEP_RECENT_ROUNDS
from src.token_counter import count_message_tokens
from src.summarizer import summarizxer_history

def process_session_context(messages:list[dict],current_summary:str):  #接受消息列表和已有摘要
    token_num = count_message_tokens(messages)
    if token_num <= MAX_CHAT_TOKENS:                           #判断token是否超
        return messages,current_summary
    #保留最近N轮对话
    keep = messages[-KEEP_RECENT_ROUNDS:]                      #切分
    to_summarize = messages[:-KEEP_RECENT_ROUNDS]
    if not to_summarize:
        return messages,current_summary
    new_summary = summarizxer_history(to_summarize)
    return keep,new_summary

