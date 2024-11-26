from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from src.bot.bot import bot
from src.bot.keyboards import *
from src.model.model import generate_training_program, generate_diet_program, load_model

router = Router()

loaded_models = {}

class TrainingProgramStates(StatesGroup):
  return_to_menu_state = State()
  choose_model_state = State()
  choose_service_state = State()
  choose_goal_state = State()
  user_parameters_state = State()
  generate_train_state = State()
  confirm_train_state = State()
  generate_diet_state = State()
  confirm_diet_state = State()
  ending_state = State()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
  await message.answer("Здравствуйте! Выберите языковую модель для работы:", reply_markup=get_model_keyboard())
  await state.set_state(TrainingProgramStates.choose_model_state)


@router.message(F.text == "Вернуться в главное меню")
async def return_to_main_menu(message: types.Message, state: FSMContext):
  await state.clear()
  await message.answer("Выберите языковую модель для работы:", reply_markup=get_model_keyboard())
  await state.set_state(TrainingProgramStates.choose_model_state)


@router.message(TrainingProgramStates.return_to_menu_state)
async def return_to_main_menu_through_state(message: types.Message, state: FSMContext):
  await state.clear()
  await message.answer("Выберите языковую модель для работы:", reply_markup=get_model_keyboard())
  await state.set_state(TrainingProgramStates.choose_model_state)


@router.message(TrainingProgramStates.choose_model_state)
async def choose_model(message: types.Message, state: FSMContext):
  model = message.text
  if model not in ["GPT", "LLaMA"]:
    await message.answer("Пожалуйста, выберите модель из предложенных.", reply_markup=get_model_keyboard())
    return

  await state.update_data(model=model)

  if model not in loaded_models and model == "LLaMA":
    print("\ncheck pipeline llama\n")
    model_pipeline = await load_model(model)
    loaded_models[model] = model_pipeline

  await message.answer("Чем могу помочь?", reply_markup=get_greeting_keyboard())
  await state.set_state(TrainingProgramStates.choose_service_state)


@router.message(TrainingProgramStates.choose_service_state)
async def choose_service(message: types.Message, state: FSMContext):
  if message.text == "Подобрать тренировочную программу":
    await message.answer("Какая у вас цель?", reply_markup=get_goal_keyboard())
    await state.set_state(TrainingProgramStates.choose_goal_state)
  elif message.text == "Узнать советы по здоровому образу жизни": # TODO: generate tip
    await message.answer("Совет: Пейте достаточно воды и занимайтесь физической активностью каждый день!")


async def retry_parameters(message: types.Message, state: FSMContext):
  await message.answer("Какая у вас цель?", reply_markup=get_goal_keyboard())
  await state.set_state(TrainingProgramStates.choose_goal_state)


@router.message(TrainingProgramStates.choose_goal_state)
async def choose_goal(message: types.Message, state: FSMContext):
  goal = message.text
  if message.text not in ["Похудение", "Набор мышечной массы", "Поддержание формы"]:
    await message.answer("Пожалуйста, выберите цель из предложенных.", reply_markup=get_goal_keyboard())
    return

  await state.update_data(goal=goal)
  await message.answer("Укажите ваш возраст, вес и уровень физической подготовки (Новичок, Средний, Продвинутый). Вводите данные в формате: возраст, вес, уровень.",
                        reply_markup=ReplyKeyboardRemove()) 
  await state.set_state(TrainingProgramStates.user_parameters_state)


@router.message(TrainingProgramStates.user_parameters_state)
async def user_parameters(message: types.Message, state: FSMContext):
  params = message.text

  try:
    parts = [part.strip() for part in params.split(",")]

    age = int(parts[0].split()[0])
    if age <= 0:
      raise ValueError("Возраст вне допустимого диапазона.")

    weight = int(parts[1].split()[0])
    if weight <= 0:
      raise ValueError("Вес вне допустимого диапазона.")

    level = parts[2].capitalize() 
    if level not in ["Новичок", "Средний", "Продвинутый"]:
      raise ValueError("Некорректный уровень подготовки, выберите из предложенных.")

    await state.update_data(age=age, weight=weight, level=level)

    data = await state.get_data()
    goal = data.get("goal")
    await message.answer(
      f"Ваши данные:\nВозраст: {age}\nВес: {weight}\nУровень подготовки: {level}\nЦель: {goal}\nВсе верно?",
      reply_markup=get_yes_or_no_keyboard()
    )
    await state.set_state(TrainingProgramStates.generate_train_state)

  except ValueError as e:
    await message.answer(
      "Некорректный ввод. Пожалуйста, введите данные в формате: возраст, вес, уровень. Например: 25, 70, Новичок.",
      reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(TrainingProgramStates.choose_goal_state)
    return


async def retry_generate(message: types.Message, state: FSMContext, generator_function, state_to_set):
  data = await state.get_data()
  model = data.get("model")
  goal = data.get("goal")
  age = data.get("age")
  weight = data.get("weight")
  level = data.get("level")
  parameters = f"Возраст: {age}, Вес: {weight}, Уровень: {level}"

  await message.answer(f"Подождите пожалуйста...", reply_markup=ReplyKeyboardRemove())

  response = await generator_function(loaded_models, model, goal, parameters)
  await message.answer(f"Новый результат:\n{response}\n\n Устраивает ли вас ответ?", reply_markup=get_yes_or_no_keyboard())
  await state.set_state(state_to_set)


@router.message(TrainingProgramStates.generate_train_state)
async def generate_train(message: types.Message, state: FSMContext):
  if message.text == "Да":
    data = await state.get_data()
    model = data.get("model")
    goal = data.get("goal")
    age = data.get("age")
    weight = data.get("weight")
    level = data.get("level")

    parameters = f"Возраст: {age}, Вес: {weight}, Уровень: {level}"

    await message.answer(f"Подождите пожалуйста...", reply_markup=ReplyKeyboardRemove())
    response = await generate_training_program(loaded_models, model, goal, parameters)

    await message.answer(f"Сгенерированная тренировка:\n{response}\n\n Устраивает ли вас ответ?", reply_markup=get_yes_or_no_keyboard())
    await state.set_state(TrainingProgramStates.confirm_train_state)
  elif message.text == "Нет":
    await retry_parameters(message, state)


@router.message(TrainingProgramStates.confirm_train_state)
async def confirm_train(message: types.message, state: FSMContext):
  if message.text == "Да":
    await message.answer("Хотите ли составить диету?", reply_markup=get_yes_or_no_keyboard())
    await state.set_state(TrainingProgramStates.generate_diet_state)
  elif message.text == "Нет":
    await retry_generate(message, state, generate_training_program, TrainingProgramStates.confirm_train_state)


@router.message(TrainingProgramStates.generate_diet_state)
async def generate_diet(message: types.Message, state: FSMContext):
  if message.text == "Да":
    data = await state.get_data()
    model = data.get("model")
    goal = data.get("goal")
    age = data.get("age")
    weight = data.get("weight")
    level = data.get("level")

    parameters = f"Возраст: {age}, Вес: {weight}, Уровень: {level}"

    await message.answer(f"Подождите пожалуйста...", reply_markup=ReplyKeyboardRemove())
    response = await generate_diet_program(loaded_models, model, goal, parameters)

    await message.answer(f"Сгенерированный план питания: {response}\n\n Устраивает ли вас ответ?", reply_markup=get_yes_or_no_keyboard())

    await state.set_state(TrainingProgramStates.confirm_diet_state)
  elif message.text == "Нет":
    await message.answer("Рад был помочь!", reply_markup=get_menu_keyboard())
    await state.clear()
    

@router.message(TrainingProgramStates.confirm_diet_state)
async def confirm_diet(message: types.Message, state: FSMContext):
  if message.text == "Да":
    await message.answer("Отлично, был рад помочь!", reply_markup=get_menu_keyboard())
    await state.clear()
  elif message.text == "Нет":
    await retry_generate(message, state, generate_diet_program, TrainingProgramStates.confirm_diet_state)


def register_handlers(dp):
  dp.include_router(router)