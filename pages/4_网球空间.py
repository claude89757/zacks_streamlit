import streamlit as st
import random
import string
import uuid
from common.redis_client import RedisClient
from PIL import Image
import io
from datetime import datetime
import base64

# 初始化RedisClient实例
redis_client = RedisClient(db=1)

# 随机生成英文代号
def generate_random_alias():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# 页面标题
st.title("🎾 网球聊天室")

# 实时更新消息
def load_messages():
    comments = redis_client.get_json_data_by_prefix("chat:")
    if comments:
        sorted_comments = sorted(comments.values(), key=lambda x: x['timestamp'], reverse=True)
        return sorted_comments
    return []

# 显示消息
def display_messages(messages):
    columns = st.columns(3)  # 创建三列布局
    for index, message in enumerate(messages):
        col = columns[index % 3]  # 根据列数分配消息
        with col:
            st.markdown(f"**{message['nickname']}**")
            st.markdown(f"*{message['timestamp']}*")
            st.markdown(f"> {message['message']}")
            if message['image_url']:
                st.image(message['image_url'], use_column_width=True)
            st.markdown("---")

# 加载并显示消息
messages = load_messages()
display_messages(messages)

# 消息输入框
st.subheader("发送消息")
nickname = st.text_input("输入昵称（可选）：", max_chars=20)
if not nickname:
    nickname = generate_random_alias()

message = st.text_area("输入你的消息：", max_chars=500)
uploaded_file = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])

# 处理上传的图片
image_url = None
if uploaded_file:
    image = Image.open(uploaded_file)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_data = image_bytes.getvalue()
    image_url = f"data:image/png;base64,{base64.b64encode(image_data).decode()}"

# 提交消息
if st.button("发送"):
    if message or image_url:
        # 构建消息数据
        chat_message = {
            "nickname": nickname,
            "message": message,
            "image_url": image_url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        redis_client.set_json_data(f"chat:{uuid.uuid4()}", chat_message, timeout=86400 * 7)  # 保持消息7天
        st.success("消息发送成功！")
        # 清空输入框和图片上传
        st.text_area("输入你的消息：", max_chars=500, value="", key="message")
        st.file_uploader("上传图片", type=["png", "jpg", "jpeg"], key="file_uploader", label_visibility="hidden")
        st.experimental_rerun()
    else:
        st.warning("请输入消息或上传图片！")

# 设置页面布局为适合手机端使用
st.markdown(
    """
    <style>
    .main {
        max-width: 400px;
        margin: auto;
    }
    .column {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 使用卡片样式
for i in range(3):
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
