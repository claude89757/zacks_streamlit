#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/16 20:23
@Author  : claude
@File    : 4_网球空间.py
@Software: PyCharm
"""

import datetime
import streamlit as st
import random
import string
from common.redis_client import RedisClient
from PIL import Image
import io

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
st.title("🎾 网球空间")

# 留言输入区
nickname = st.text_input("输入昵称（可选）：", max_chars=20)
message = st.text_area("你的留言", max_chars=500)
uploaded_file = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])

# 如果未输入昵称，则生成随机代号
if not nickname:
    nickname = generate_random_alias()

# 处理上传的图片
image_url = None
if uploaded_file:
    image = Image.open(uploaded_file)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_data = image_bytes.getvalue()
    image_url = f"data:image/png;base64,{base64.b64encode(image_data).decode()}"

# 留言提交
if st.button("发布留言"):
    if message or image_url:
        # 构建留言数据
        comment = {
            "nickname": nickname,
            "message": message,
            "image_url": image_url,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        redis_client.set_json_data(f"comment:{uuid.uuid4()}", comment, timeout=86400 * 7)  # 保持留言7天
        st.success("留言发布成功！")
    else:
        st.warning("请先输入留言或上传图片！")

# 显示留言板
st.subheader("🎾 留言板")
comments = redis_client.get_json_data_by_prefix("comment:")
if comments:
    sorted_comments = sorted(comments.values(), key=lambda x: x['timestamp'], reverse=True)
    for comment in sorted_comments:
        st.markdown(f"**{comment['nickname']}** 于 *{comment['timestamp']}* 留言：")
        st.markdown(f"> {comment['message']}")
        if comment['image_url']:
            st.image(comment['image_url'])
        st.markdown("---")
else:
    st.info("暂无留言，快来抢沙发吧！")

# 设置页面布局为适合手机端使用
st.markdown(
    """
    <style>
    .main {
        max-width: 400px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
