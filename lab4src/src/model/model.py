from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from gpt4all import GPT4All
from huggingface_hub import InferenceClient
from googletrans import Translator
from dotenv import load_dotenv
import os
import sys
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "gguf_models/")

sys.path.append(os.path.dirname(__file__))
from config_loader import load_config

config = load_config()
translator = Translator()
load_dotenv()

HF_TOKEN: str = os.getenv('HUGGING_FACE_SECOND_TOKEN')


async def translate_result_to_ru(result: str):
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


async def generate_by_falcon(prompt: str):
  """
  Start answer generation with falcon

  :param prompt: request to model
  """
  MODEL_NAME = config["model"]["falcon"]["full_name"]

  model = GPT4All(MODEL_NAME, model_path=model_path)

  prompt_en = translator.translate(prompt, src='ru', dest='en').text

  with model.chat_session():
    print("\nFALCON GENERATION STARTED\n")

    result = str(model.generate(
      prompt_en,
      max_tokens=config["falcon_config"]["max_tokens"],
      temp=config["falcon_config"]["temperature"],
      top_p=config["falcon_config"]["top_p"],
      top_k=config["falcon_config"]["top_k"],
      repeat_penalty=config["falcon_config"]["repetition_penalty"]
    ))

    print("\nFALCON GENERATION COMPLETED\n")

    result_ru: str = await translate_result_to_ru(result)
    return result_ru


async def generate_by_llama(prompt: str):
  """
  Start answer generation with llama

  :param prompt: request to model
  """
  client = InferenceClient(api_key=HF_TOKEN)

  MODEL_PATH = config["model"]["llama"]["model_path"]

  prompt_en = translator.translate(prompt, src='ru', dest='en').text

  messages = [
    {
      "role": "user",
      "content": prompt_en
    }
  ]

  print("\nLLAMA GENERATION STARTED\n")

  completion = client.chat.completions.create(
    model=MODEL_PATH, 
    messages=messages, 
    max_tokens=config["llama_config"]["max_tokens"],
    temperature=config["llama_config"]["temperature"],
    top_p=config["llama_config"]["top_p"],
    frequency_penalty=config["llama_config"]["frequency_penalty"],
    presence_penalty=config["llama_config"]["presence_penalty"]
  )

  print("\nLLAMA GENERATION COMPLETED\n")

  result = completion.choices[0].message["content"]

  cleaned_result = result.strip()

  formatted_result = cleaned_result.replace("\\n", "\n")

  result_ru: str = await translate_result_to_ru(formatted_result)
  return result_ru


async def generate_training_program(model: str, goal: str, parameters: str) -> str:
  """
  Getting training program

  :param model: the name of model
  :param goal: the goal user training for
  :param parameters: user's age, weight, experience
  """
  prompt = f"Составь тренировочную программу для {goal}.\nПараметры пользователя: {parameters}\n"
  if model == "FALCON": 
    result = await generate_by_falcon(prompt)

    return result
  elif model == "LLaMA":
    result = await generate_by_llama(prompt)

    return result
    

async def generate_diet_program(model: str, goal: str, parameters: str) -> str:
  """
  Getting diet program

  :param model: the name of model
  :param goal: the goal user training for
  :param parameters: user's age, weight, experience
  """
  prompt: str = f"Составь рацион для {goal}.\nПараметры пользователя: {parameters}\n"

  if model == "FALCON": 
    result = await generate_by_falcon(prompt)

    return result
    
  elif model == "LLaMA":
    result = await generate_by_llama(prompt)

    return result