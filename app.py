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

# 让历史消息从历史消息列表中拿出并显示
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input("请输入你的问题：")

# 用户输入了提示词
if prompt:
    # 显示用户输入的提示词
    st.chat_message("user").write(prompt)
    # 把用户的提问也保存到聊天历史中
    st.session_state["messages"].append({"role": "user", "content": prompt})
    # agent 的回复，给一个可以转圈的框提升用户的体验
    with st.spinner("智能客服思考中..."):
        # 这里使返回一个迭代器
        res_stream = st.session_state["agent"].execute_stream(prompt)

        # 定义函数捕获数据
        # generator--迭代器
        def capture(generator):
            for chunk in generator:
                for char in chunk:
                    yield char
        # 在AI回复中显示内容
        with st.chat_message("assistant"):
            response = st.write_stream(capture(res_stream))

    # 保存完整回复到历史记录
    if response:
        st.session_state["messages"].append({"role": "assistant", "content": response})
