import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

from config import SESSION_DATA_DIR
from src.session_manager import process_session_context
from src.session_store import list_all_session_ids,save_file,load_file,delete_file
from src.llm_client import get_llm_client
from src.ui import render_chat

#dotenv.

st.title("AI partner")
st.logo("assets/2.jpg") 
def make_new_sid():#生成会话标识

    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

#初始化聊天信息---------------------
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #昵称
    if "nick_name" not in st.session_state:
        st.session_state.nick_name = "小可爱"

    #性格
    if "nature" not in st.session_state:
        st.session_state.nature = "活泼开朗"

    if "datetime_id" not in st.session_state:
        st.session_state.datetime_id = make_new_sid()
    #
    if "summary" not in st.session_state:
        st.session_state.summary = ""
init_state()



#胶水----------------------------------------------
def save_session_data():
       sid = st.session_state.datetime_id
       #构建新的会话对象
       session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "session_id": st.session_state.datetime_id,
            "messages": st.session_state.messages,
            "summary":st.session_state.get("summary","")
        }
       save_file(sid,session_data)

def load_session(sid:str):
    data = load_file(sid)
    if data is None:
        st.error("加载会话失败！")
        return
    st.session_state.messages = data["messages"]
    st.session_state.nick_name = data["nick_name"]
    st.session_state.nature = data["nature"]
    st.session_state.datetime_id = sid
    st.session_state["summary"] = data.get("summary","")
        
def delete_session(sid:str):
    success = delete_file(sid)
    if not success:
        st.error("删除会话失败！")
        return
    if sid == st.session_state.datetime_id:
        st.session_state.messages = []
        st.session_state.summary = ""
        st.session_state.datetime_id = make_new_sid()

#LLM调用------------------------------------
def chat_call(messages,nick,nature):
           system_prompt ="你叫%s,你是一个%s的朋友"%(nick,nature)
           req_messages = [ {"role": "system", "content": system_prompt }]+messages
           client = get_llm_client()
           resp = client.chat.completions.create(
            model="deepseek-flash",
            messages=req_messages,
            temperature=0.2,
           )
           return resp.choices[0].message.content.strip()
           

#主入口---------------------
def main():
    st.set_page_config(
               page_title="AI partner",
               page_icon="🌸",
               #布局
               layout="wide",#铺满整个屏幕
               initial_sidebar_state="expanded",#控制侧边栏的状态
               menu_items={}
            )
    init_state()
     
    session_list = list_all_session_ids()


#侧边栏-with:streamlit中上下文管理器----------------------
with st.sidebar:
    #会话信息
    st.subheader("会话管理")
    #新建会话
    if st.button("新建会话",width="stretch",icon="🖌️"): #按钮
        #保存当前会话信息
        save_session_data()

        #创建新会话
        if st.session_state.messages: #判断是否有会话信息,会话是否为空
            st.session_state.messages = []
            st.session_state.datetime_id = make_new_sid()
            save_session_data()
            st.rerun()#重新运行当前页面
 #会话历史
    st.text("会话历史")
    session_list = list_all_session_ids()
    for session_id in session_list: #遍历会话列表
        col1,col2 =st.columns([4,1])
        with col1:
            #三元运算符-> a if 条件 else b

            if st.button(session_id,width="stretch",icon="📄",key=f"load_{session_id}",type="primary" if session_id == st.session_state.datetime_id else "secondary"):
                load_session(session_id)                                                
                st.rerun()
        with col2:  
            if st.button("",width="stretch",icon="❌️",key=f"delete_{session_id}"):
                delete_session(session_id)
                st.rerun()
    #分割线
    st.divider()
    st.subheader("角色设定")
    nick_name = st.text_input("昵称",placeholder="请输入partner的昵称",value=st.session_state.nick_name)
    if nick_name: 
        st.session_state.nick_name = nick_name
    nature = st.text_area("性格",height=100,placeholder="请输入partner性格",value=st.session_state.nature)
    if nature: 
        st.session_state.nature = nature


#渲染聊天-------------------placeholder="请输入.....
render_chat(st.session_state.messages,st.session_state.summary)
user_input = st.chat_input("请输入.....",key="user_input")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"),st.spinner("思考中..."):
        reply = chat_call(st.session_state.messages,st.session_state.nick_name,st.session_state.nature)
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        new_msg,new_sum = process_session_context(st.session_state.messages,st.session_state.summary)
        st.session_state.messages = new_msg
        st.session_state.summary = new_sum
        save_session_data()
        st.rerun()

if __name__ == "__main__":
    main()

# #页面配置





# #大标题
# st.title("AI_partner")
# st.logo("assets/2.jpg")





# #展示聊天信息
# st.text(f"会话名称：{st.session_state.datetime_id}")
# for message in st.session_state.messages:
#     st.chat_message(message["role"]).write(message["content"])


# client = OpenAI(
#     api_key=os.environ.get('DEEPSEEK_API_KEY'),
#     base_url="https://api.deepseek.com")





# promt=st.chat_input("请输入你的问题")

# if promt:#字符串会自动转化布尔值
#     st.chat_message("user").write(promt)
#     print("---------->调用AI大模型,提示词:",promt)

#     #保存用户提示词
#     st.session_state.messages.append({"role": "user", "content": promt})

#     #调用大模型
#     print([
#         {"role": "system", "content":system_prompt },
#         *st.session_state.messages
#     ])
#     #与ai大模型进行交互（）
#     response = client.chat.completions.create(
#         model="deepseek-flash",
#         messages=[
#             {"role": "system", "content":system_prompt % (st.session_state.nick_name,st.session_state.nature) },
#             #{"role": "user", "content": promt},
#             *st.session_state.messages
#         ],
#         stream=True,#是否流式输出
#         reasoning_effort="high",
#         extra_body={"thinking": {"type": "enabled"}}
#     )
#     #输出大模型返回的结果（非流式输出）
#     # print("----------->大模型返回的结果:",response.choices[0].message.content)
#     # st.chat_message("assistant").write(response.choices[0].message.content)
    

#     #流式输出
#     response_message =st.empty()#创建一个空的组件，用于展示模型返回的结果
#     full_response = ""
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             content = chunk.choices[0].delta.content
#             full_response += content
#             response_message.chat_message("assistant").write(full_response)

    

#     #保存大模型返回的结果
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
#     save_session_data()
