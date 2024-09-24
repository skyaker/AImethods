import requests
import streamlit as st
from langdetect import detect

def summarize_with_chatgpt42(text):
    url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"

    language = detect(text)
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following text in {language}:\n\n{text}"
            }
        ],
        "system_prompt": "",
        "temperature": 0.7,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 100,
        "web_access": False
    }
    
    headers = {
        "x-rapidapi-key": "api-key",
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    try:
        data = response.json()
        if 'result' in data:
            return data['result']
        else:
            return f"Unexpected response structure: {data}"
    except Exception as e:
        return f"Ошибка: {str(e)}, Ответ от API: {response.text}"

def summarize_with_llama(text):
    url = "https://llama-ai-mixtral-cohere-gpt-api.p.rapidapi.com/nllama3"

    language = detect(text)
    
    prompt = f"Summarize the following text in {language}:\n\n{text}"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "web_access": False,
        "consider_chat_history": False,
        "system_prompt": "",
        "conversation_id": ""
    }
    headers = {
        "x-rapidapi-key": "api-key",
        "x-rapidapi-host": "llama-ai-mixtral-cohere-gpt-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()

        if 'result' in result:
            summary = result['result']

            summary_lines = summary.split('\n')
            if len(summary_lines) > 1:
                return '\n'.join(summary_lines[1:])
            else:
                return summary
        else:
            return "Ошибка: ключ 'result' не найден в ответе"
    else:
        return f"Ошибка: {response.status_code} - {response.text}"

st.title("Суммаризация текста")

text = st.text_area("Введите текст:", height=200)

if st.button("Суммаризировать"):
    if text:
        st.subheader("Результат от OpenAI API:")
        summary_gpt = summarize_with_chatgpt42(text)
        st.write(summary_gpt)

        st.subheader("Результат от Cohere API:")
        summary_cohere = summarize_with_llama(text)
        st.write(summary_cohere)
    else:
        st.warning("Введите текст для суммаризации.")
 