import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv

load_dotenv()

def load_model():
    """
    Загрузка модели и токенизатора из переменной окружения URL_RUGPT_3_LARGE.
    """
    GPT_URL: str = os.getenv('URL_RUGPT_3_LARGE')
    
    tokenizer = AutoTokenizer.from_pretrained(GPT_URL)
    model = AutoModelForCausalLM.from_pretrained(GPT_URL)

    # Определение устройства (MPS или CPU)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device)

    return model, tokenizer, device


def generate_text(prompt: str, model, tokenizer, device, generation_params: dict, text_length: int) -> str:
    """
    Функция генерации текста.

    :param prompt: Начальная строка для генерации
    :param model: Загруженная модель
    :param tokenizer: Токенизатор для модели
    :param device: Устройство для модели (CPU или MPS)
    :param generation_params: Параметры генерации (temperature, top_k, и т.д.)
    :param text_length: Максимальная длина текста
    :return: Сгенерированный текст
    """
    encoded_input = tokenizer(prompt, return_tensors='pt', add_special_tokens=False).to(device)
    
    output = model.generate(
        **encoded_input,
        repetition_penalty=generation_params['repetition_penalty'],
        max_length=text_length,
        num_beams=generation_params['num_beams'],
        do_sample=generation_params['do_sample'],
        temperature=generation_params['temperature'],
        top_k=generation_params['top_k'],
        top_p=generation_params['top_p'],
    )
    
    return tokenizer.decode(output[0], skip_special_tokens=True)
