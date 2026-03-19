import time

import streamlit as st
from agent.react_agent import ReactAgent

# 标题
st.title("智扫通机器人智能客服")
# 分隔符
st.divider()

# 把 ReactAgent 的对象保存在session_state字典中
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

# 构建历史的消息记录
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

# 把历史消息从缓存列表中取出
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input("请输入你的问题：")

if prompt:
    # 显示用户输入的提示词
    st.chat_message("user").write(prompt)
    # 把用户的提问也保存到聊天历史中
    st.session_state["messages"].append({"role": "user", "content": prompt})
    # 定义缓存消息的存入列表
    response_messages = []
    # agent 的回复，给一个可以转圈的框提升用户的体验
    with st.spinner("智能客服思考中..."):
        # 这里使返回一个迭代器
        res_stream = st.session_state["agent"].execute_stream(prompt)

        # 定义函数捕获数据记录历史中
        # generator--迭代器，cache_list--缓存列表
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["messages"].append({"role": "assistant", "content": response_messages[-1]})

        # 在AI思考完准备回复的时候刷新页面，只保留最后一条信息，不要思考过程
        st.rerun()





















