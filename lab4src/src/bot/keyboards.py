from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_model_keyboard():
  """Greetings keyboard"""
  keyboard = [
    [KeyboardButton(text = "GPT")],
    [KeyboardButton(text = "LLaMA")]
  ]
  return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_greeting_keyboard():
  """Greetings keyboard"""
  keyboard = [
    [KeyboardButton(text = "Подобрать тренировочную программу")],
    [KeyboardButton(text = "Узнать советы по здоровому образу жизни")],
    [KeyboardButton(text = "Вернуться в главное меню")],
  ]
  return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_goal_keyboard():
  """Goal keyboard"""
  keyboard = [
    [KeyboardButton(text = "Похудение")],
    [KeyboardButton(text = "Набор мышечной массы")],
    [KeyboardButton(text = "Поддержание формы")],
    [KeyboardButton(text = "Вернуться в главное меню")],
  ]
  keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
  return keyboard

def get_yes_or_no_keyboard():
  "User ecision"
  keyboard = [
    [KeyboardButton(text = "Да")],
    [KeyboardButton(text = "Нет")],
    [KeyboardButton(text = "Вернуться в главное меню")],
  ]
  keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
  return keyboard

def get_menu_previous_section():
  """Goal keyboard"""
  keyboard = [
    [KeyboardButton(text = "Вернуться в главное меню")],
    [KeyboardButton(text = "Перейти к предыдущему вопросу")]
  ]
  keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
  return keyboard

def get_menu_keyboard():
  keyboard = [
    [KeyboardButton(text = "Вернуться в главное меню")]
  ]
  keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
  return keyboard