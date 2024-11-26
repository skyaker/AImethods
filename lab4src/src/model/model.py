from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from gpt4all import GPT4All
from huggingface_hub import InferenceClient
from googletrans import Translator
from dotenv import load_dotenv
import torch
import os
import sys
import re

sys.path.append(os.path.dirname(__file__))
from config_loader import load_config

config = load_config()

translator = Translator()

load_dotenv()

token: str = os.getenv('HUGGING_FACE_SECOND_TOKEN')


async def load_model(model_name: str):
  if model_name == "GPT":
    model_path = "EleutherAI/gpt-neo-125M"
  elif model_name == "LLaMA":
    model_path = "meta-llama/Llama-3.1-8B-Instruct"
  else:
    raise ValueError("Неизвестная модель")

  print(f"Загружаем модель {model_name}...")
  
  tokenizer = AutoTokenizer.from_pretrained(model_path, token=token)

  if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

  device = config["model"]["use_resource"]

  model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map=device,
    torch_dtype=torch.float16,
    token=token
  )
  
  return pipeline("text-generation", model=model, device_map="auto")


async def generate_training_program(loaded_models: dict, model: str, goal: str, parameters: str) -> str:
  if model == "GPT": 
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    prompt = f"Составь тренировочную программу для {goal}.\nПараметры пользователя: {parameters}\n"
    prompt_en = translator.translate(prompt, src='ru', dest='en').text
    print(f"\n{prompt_en}\n\n")

    with model.chat_session():
      print("Генерация началась\n")

      result = str(model.generate(prompt_en, max_tokens=1024))

      sentences = re.split(r'(?<=[.!?])\s+', result)
      translated_sentences = []

      for sentence in sentences:
        try:
          if sentence.strip():
            translated_sentence = translator.translate(sentence, src='en', dest='ru').text
            translated_sentences.append(translated_sentence)
        except Exception as e:
          translated_sentences.append("")

      result_ru = " ".join(translated_sentences)
      return result_ru

  elif model == "LLaMA":
    model_pipeline = loaded_models[model]
    prompt = f"Составь тренировочную программу для {goal}.\nПараметры пользователя: {parameters}\n"
    
    model_pipeline.tokenizer.pad_token_id = model_pipeline.tokenizer.eos_token_id

    result = model_pipeline(
      prompt, 
      max_length=500, 
      truncation=True, 
      num_return_sequences=1)

    sentences = re.split(r'(?<=[.!?])\s+', result[0]["generated_text"])
    translated_sentences = []

    for sentence in sentences:
      try:
        if sentence.strip():
          translated_sentence = translator.translate(sentence, src='en', dest='ru').text
          translated_sentences.append(translated_sentence)
      except Exception as e:
        translated_sentences.append("[Ошибка перевода]")

    result_ru = " ".join(translated_sentences)
    return result_ru
  

async def generate_diet_program(loaded_models: dict, model: str, goal: str, parameters: str) -> str:
  prompt: str = f"Составь рацион для {goal}.\nПараметры пользователя: {parameters}\n"

  if model == "GPT": 
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

    prompt_en = translator.translate(prompt, src='ru', dest='en').text

    with model.chat_session():
      print("Генерация началась\n")

      result = str(model.generate(prompt_en, max_tokens=1024))

      sentences = re.split(r'(?<=[.!?])\s+', result)
      translated_sentences = []

      for sentence in sentences:
        try:
          if sentence.strip():
            translated_sentence = translator.translate(sentence, src='en', dest='ru').text
            translated_sentences.append(translated_sentence)
        except Exception as e:
          translated_sentences.append("")

      result_ru = " ".join(translated_sentences)
      return result_ru
    
  elif model == "LLaMA":
    model_pipeline = loaded_models[model]
    
    model_pipeline.tokenizer.pad_token_id = model_pipeline.tokenizer.eos_token_id

    result = model_pipeline(
      prompt, 
      max_length=500, 
      truncation=True, 
      num_return_sequences=1)

    return result[0]["generated_text"]