#全局配置
import os
from dotenv import load_dotenv
load_dotenv()
#路径
SESSION_DATA_DIR = os.path.join(os.path.dirname(__file__), "session_data")
#LLM配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY","")
MODEL_NAME = "deepseek-flash"
DEEPSEEK_BASE_URL ="https://api.deepseek.com"
#压缩
MAX_CHAT_TOKENS = 3000  #阈值
KEEP_RECENT_ROUNDS = 6  #保留最近几轮
SUMMARY_TEMPERATURE = 0.2  #摘要温度
CHAT_TEMPERATURE = 0.7     #聊天温度
#LLM请求参数
STREAM = True #是否流式返回
TIMEOUT = 60  #请求超时时间
MAX_RETRY = 3 #最大重试次数
