import requests
import json
import streamlit as st
from bs4 import BeautifulSoup

# http://www.qstheory.cn/qshyjx/2024-05/31/c_1130154865.htm

API_KEY = "YA8hC3AGFvkEhSmZrgjTD7em"
SECRET_KEY = "QDepxih6vfsocMe4gpjLO9YNCzoTgbHU"

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def main():
    #st.title("新闻摘要")
    
    # 用户输入网址
    url = st.text_input("请输入新闻网址:")

    if url:
        try:
            # 获取网页内容
            response = requests.get(url)
            response.raise_for_status()  # 确保请求成功
            html_content = response.content  # 使用 response.content 获取二进制内容
            text_content = extract_text(html_content)
            
            # 获取 access token
            access_token = get_access_token()
            if access_token:
                # 百度API的URL
                api_url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary?charset=UTF-8&access_token={access_token}"
                
                # 准备payload
                payload = {
                    "content": text_content,
                    "max_summary_len": 300
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                
                # 发送请求并获取响应
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()  # 确保请求成功
                summary = response.json()  # 直接解析 JSON 响应
                
                # 检查摘要是否存在并正确解码
                if 'summary' in summary:
                    # 确保摘要文本使用 UTF-8 解码
                    summary_text = summary["summary"].encode('utf-8').decode('utf-8')
                    st.write("### 新闻摘要")
                    st.write(summary_text)
                else:
                    st.error("无法获取新闻摘要，请检查API响应内容。")
            else:
                st.error("无法获取有效的 access token")
        except requests.RequestException as e:
            st.error(f"请求错误: {e}")

if __name__ == "__main__":
    main()
