import streamlit as st
import os
import json
from io import BytesIO
from PIL import Image
from common.log_config import setup_logger
from common.settings import common_settings_init
from sidebar import sidebar

# Configure logger
logger = setup_logger(__name__)

# Configure Streamlit pages and state
st.set_page_config(page_title="网球馆", page_icon="🎾", layout="wide")

# Init settings for ui
common_settings_init()

# Init sidebar
sidebar()

# Define the directory to store the tennis court info and photos
info_dir = "practice_tennis_court_infos"
photos_dir = os.path.join(info_dir, "photos")
if not os.path.exists(info_dir):
    os.makedirs(info_dir)
if not os.path.exists(photos_dir):
    os.makedirs(photos_dir)

def save_court_info(info):
    filename = os.path.join(info_dir, f"{info['name']}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

def save_photos(files):
    photo_paths = []
    for file in files:
        file_path = os.path.join(photos_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        photo_paths.append(file.name)
    return photo_paths

def delete_court_info(name):
    file_path = os.path.join(info_dir, f"{name}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        # Also delete associated photos
        for photo in os.listdir(photos_dir):
            if photo.startswith(name):
                os.remove(os.path.join(photos_dir, photo))

def get_court_info(name):
    file_path = os.path.join(info_dir, f"{name}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Render Streamlit pages
st.title("网球馆信息管理系统")

# Create tabs
tab1, tab2 = st.tabs(["网球馆信息", "录入信息"])

# Tab 1: 录入网球场信息
with tab2:
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
                photo_paths = []
                if photos:
                    photo_paths = save_photos(photos)
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
                    "photos": photo_paths
                }
                save_court_info(court_info)
                st.success("信息已保存！")
            else:
                st.error("请填写网球场名称。")

# Tab 2: 展示网球场信息
with tab1:
    st.markdown("**已录入的网球场信息**")

    # Display saved information with collapsible sections
    files = os.listdir(info_dir)
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(info_dir, file), "r", encoding="utf-8") as f:
                court_info = json.load(f)
                with st.expander(f"{court_info['name']} - {court_info['address']}", expanded=False):
                    st.write(f"预定方式: {court_info['booking_method']}")
                    st.write(f"开放预定时间: {court_info['open_booking_time']}")
                    st.write(f"可提前多少天预定: {court_info['advance_booking_days']}")
                    st.write(f"价格范围: {court_info['price_range']}")
                    st.write(f"类型: {court_info['court_type']}")
                    st.write(f"联系电话: {court_info['contact']}")
                    st.write(f"备注: {court_info['notes']}")
                    if court_info["photos"]:
                        for photo in court_info["photos"]:
                            photo_path = os.path.join(photos_dir, photo)
                            if os.path.exists(photo_path):
                                st.image(photo_path)
                            else:
                                st.error(f"无法找到图片: {photo}")

                    # Buttons for editing and deleting
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("编辑", key=f"edit_{court_info['name']}"):
                            st.session_state.editing = court_info['name']
                    with col2:
                        if st.button("删除", key=f"delete_{court_info['name']}"):
                            delete_court_info(court_info['name'])
                            st.rerun()

if 'editing' in st.session_state:
    name_to_edit = st.session_state.editing
    court_info = get_court_info(name_to_edit)
    if court_info:
        with st.form(key="edit_court_form"):
            st.text_input("网球场名称", value=court_info['name'], key="edit_name", disabled=True)
            address = st.text_input("地址", value=court_info['address'])
            booking_method = st.text_input("预定方式", value=court_info['booking_method'])
            open_booking_time = st.text_input("开放预定时间", value=court_info['open_booking_time'])
            advance_booking_days = st.number_input("可提前多少天预定", value=court_info['advance_booking_days'], min_value=0, step=1)
            price_range = st.text_input("价格范围", value=court_info['price_range'])
            court_type = st.selectbox("类型", ["室内", "室外", "风雨"], index=["室内", "室外", "风雨"].index(court_info['court_type']))
            photos = st.file_uploader("照片", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            contact = st.text_input("联系电话", value=court_info['contact'])
            notes = st.text_area("备注", value=court_info['notes'])
            update_button = st.form_submit_button(label="更新")

            if update_button:
                photo_paths = []
                if photos:
                    photo_paths = save_photos(photos)
                updated_court_info = {
                    "name": name_to_edit,
                    "address": address,
                    "booking_method": booking_method,
                    "open_booking_time": open_booking_time,
                    "advance_booking_days": advance_booking_days,
                    "price_range": price_range,
                    "court_type": court_type,
                    "contact": contact,
                    "notes": notes,
                    "photos": photo_paths + court_info['photos']  # Keep old photos and add new ones
                }
                save_court_info(updated_court_info)
                st.session_state.editing = None
                st.success("信息已更新！")
                st.rerun()
