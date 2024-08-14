#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/15 00:13
@Author  : claudexie
@File    : settings.py
@Software: PyCharm
"""
import streamlit as st


def common_settings_init():
    # Force responsive layout for columns also on mobile
    st.write(
        """<style>
        [data-testid="column"] {
            width: calc(50% - 1rem);
            flex: 1 1 calc(50% - 1rem);
            min-width: calc(50% - 1rem);
        }
        </style>""",
        unsafe_allow_html=True,
    )

    # Hide Streamlit elements
    hide_streamlit_style = """
                <style>
                .stDeployButton {visibility: hidden;}
                [data-testid="stToolbar"] {visibility: hidden !important;}
                footer {visibility: hidden !important;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)