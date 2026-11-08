# AI Partner：基于大模型的对话智能体
个人独立项目，持续迭代开发，面向大模型应用实践。

## 当前已实现功能
- 模块化分层设计，代码解耦：模型调用、会话管理、持久存储、UI 逻辑分离
- LLM 客户端封装，对接 DeepSeek API，方便无缝切换底层大模型
- 会话持久化：对话历史落地存储，重启应用后恢复完整聊天上下文
- 对话摘要机制：长会话自动摘要，控制上下文窗口，降低 token 开销与接口成本
- Token 计数模块：实时统计对话消耗 token，辅助控制上下文长度
- 使用 Streamlit 快速搭建交互式前端
- 工程化规范：使用 `.env` 管理密钥、独立配置文件、依赖清单、gitignore

## 技术栈
Python | Streamlit | DeepSeek LLM API | python-dotenv | Git

## 目录说明
ai_partner/
├── assets/            # 静态资源
├── session_data/      # 本地会话存储（gitignore，不上传）
├── src/
│   ├── llm_client.py      # 大模型接口封装
│   ├── session_manager.py # 会话业务逻辑
│   ├── session_store.py   # 会话持久读写
│   ├── summarizer.py      # 对话摘要
│   ├── token_counter.py   # token 统计
│   └── ui.py              # 页面渲染
├── .env.example       # 环境变量模板
├── .gitignore
├── config.py          # 全局配置
├── main.py            # 程序入口
├── requirements.txt
└── README.md
##  快速启动
1, 安装依赖
```bash
pip install -r requirements.txt
2,复制。env.example 文件并命名为 .env，并填写对应的密钥。
3,启动项目
streamlit run main.py

迭代计划（Roadmap）
 
- 接入 RAG：向量库 + BM25 混合检索，支持私有文档知识库问答

- 实现 Agent 工具调用能力

- 存储迁移至 SQLite，替代本地 JSON 文件

- 增加日志、异常捕获、参数可调面板


## 三、requirements.txt（配套，直接复制）
根目录新建 `requirements.txt`
```txt
streamlit
python-dotenv
requests
