import streamlit as st
import os
import json
from common.log_config import setup_logger
from common.settings import common_settings_init
from sidebar import sidebar

# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="预定方式", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# Define the directory to store the tennis court info
info_dir = "tennis_court_infos"
if not os.path.exists(info_dir):
    os.makedirs(info_dir)

def save_court_info(info):
    filename = os.path.join(info_dir, f"{info['name']}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

# Render Streamlit pages
st.title("网球场信息")

st.markdown("**录入网球场信息**")

with st.form(key="court_form"):
    name = st.text_input("网球场名称")
    address = st.text_input("地址")
    booking_method = st.text_input("预定方式")
    open_booking_time = st.text_input("开放预定时间")
    advance_booking_days = st.number_input("可提前多少天预定", min_value=0, step=1)
    price_range = st.text_input("价格范围")
    court_type = st.selectbox("类型", ["室内", "室外", "风雨"])
    photos = st.file_uploader("照片", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    contact = st.text_input("联系电话")
    notes = st.text_area("备注")

    submit_button = st.form_submit_button(label="提交")

    if submit_button:
        if name:
            court_info = {
                "name": name,
                "address": address,
                "booking_method": booking_method,
                "open_booking_time": open_booking_time,
                "advance_booking_days": advance_booking_days,
                "price_range": price_range,
                "court_type": court_type,
                "contact": contact,
                "notes": notes,
                "photos": [photo.name for photo in photos]
            }
            save_court_info(court_info)
            st.success("信息已保存！")
        else:
            st.error("请填写网球场名称。")

st.markdown("**已录入的网球场信息**")

# Display saved information
files = os.listdir(info_dir)
for file in files:
    if file.endswith(".json"):
        with open(os.path.join(info_dir, file), "r", encoding="utf-8") as f:
            court_info = json.load(f)
            st.subheader(court_info["name"])
            st.write(f"地址: {court_info['address']}")
            st.write(f"预定方式: {court_info['booking_method']}")
            st.write(f"开放预定时间: {court_info['open_booking_time']}")
            st.write(f"可提前多少天预定: {court_info['advance_booking_days']}")
            st.write(f"价格范围: {court_info['price_range']}")
            st.write(f"类型: {court_info['court_type']}")
            st.write(f"联系电话: {court_info['contact']}")
            st.write(f"备注: {court_info['notes']}")
            if court_info["photos"]:
                for photo in court_info["photos"]:
                    st.image(os.path.join(info_dir, photo))
