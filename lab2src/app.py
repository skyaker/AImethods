import streamlit as st
from utils.model_utils import load_model, generate_text
from utils.config_loader import load_generation_params
from typing import Optional

# Загрузка конфигурации и модели
generation_params: dict = load_generation_params('config.yaml')
model, tokenizer, device = load_model()

st.title("Генератор текста")

topic: Optional[str] = st.text_area("Введите тему для КНИР", "")

# Проверка, что тема не пуста
if topic:
    # Кнопка для генерации аннотации
    if st.button("Сгенерировать аннотацию"):
        prompt: str = f"Аннотация на тему: {topic}"
        st.write("Генерация аннотации...")
        annotation: str = generate_text(prompt, model, tokenizer, device, generation_params, text_length=200)
        st.subheader("Аннотация:")
        st.write(annotation)

    # Кнопка для генерации введения
    if st.button("Сгенерировать введение"):
        prompt: str = f"Введение на тему: {topic}"
        st.write("Генерация введения...")
        introduction: str = generate_text(prompt, model, tokenizer, device, generation_params, text_length=400)
        st.subheader("Введение:")
        st.write(introduction)
