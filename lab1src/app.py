import requests
import streamlit as st
from langdetect import detect
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('RAPIDAPI_KEY_RESERVE')
URL_GPT = os.getenv('URL_GPT')
URL_LLAMA = os.getenv('URL_LLAMA')

CONSIDER_CHAT_HISTORY = False
WEB_ACCESS = False
MAX_TOKENS = 700

# Максимальная свобода
# TEMPERATURE = 0.9 # Степень креативности, где 0.1 - самые предсказуемые ответы
# TOP_K = 9 # Количество вариантов для последующего ответа (сорт по вероятности)
# TOP_P = 1.0 # Сумма вероятностей первых вариантов

# Средняя свобода
TEMPERATURE = 0.5
TOP_K = 5
TOP_P = 0.7

# Минимальная свобода
# TEMPERATURE = 0.1
# TOP_K = 1
# TOP_P = 0.1

def summarize_with_chatgpt42(text):
    url = URL_GPT

    language = detect(text)
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following text in {language}, reducing its length by 75%, but keeping all key points and main information:\n\n{text}"

            }
        ],
        "system_prompt": "",
        "temperature": TEMPERATURE,
        "top_k": TOP_K,
        "top_p": TOP_P,
        "max_tokens": len(text) / 2,
        "web_access": WEB_ACCESS
    }
    
    headers = {
        "x-rapidapi-key": API_KEY,
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
    url = URL_LLAMA

    language = detect(text)

    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following text in {language}, reducing its length by 75%, but keeping all key points and main information:\n\n{text}"
            }
        ],
        "web_access": WEB_ACCESS,
        "temperature": TEMPERATURE,
        "top_k": TOP_K,
        "top_p": TOP_P,
        "max_tokens": len(text) / 2,
        "consider_chat_history": CONSIDER_CHAT_HISTORY,
        "system_prompt": "",
        "conversation_id": ""
    }
    headers = {
        "x-rapidapi-key": API_KEY,
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

        st.subheader("Результат от Llama API:")
        summary_cohere = summarize_with_llama(text)
        st.write(summary_cohere)
    else:
        st.warning("Введите текст для суммаризации.")
 