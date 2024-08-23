#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/8/23 12:07
@Author  : claude
@File    : bing_news.py
@Software: PyCharm
"""
import requests
import os


def get_bing_news_msg(query: str) -> list:
    """
    get data from bing
    This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
    Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    """
    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    bing_subscription_key = os.environ.get("BING_KEY")
    if not bing_subscription_key:
        raise Exception("no BING_KEY!!!")

    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    # Construct a request
    mkt = 'zh-HK'
    params = {'q': query, 'mkt': mkt, 'answerCount': 5, 'promote': 'News', 'freshness': 'Day'}
    headers = {'Ocp-Apim-Subscription-Key': bing_subscription_key}

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        return response.json()['news']['value']
    except Exception as error:
        return [{"name": f"Ops, 我崩溃了: {error}", "url": "？"}]
