from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import database


start_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary_or_grade = State()
    test = State()

@start_router.message(Command("stop"))
@start_router.message(F.text.lower() == "стоп")
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за прохождение опроса!")

@start_router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    # await message.answer()
    await state.set_state(BookSurvey.name)
    await message.answer('кто вы?')

@start_router.message(BookSurvey.name)
async def upp12(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.age)
    await state.update_data(name=message.text)
    await message.answer(f'скок лет?')

@start_router.message(BookSurvey.age)
async def upp123(message: types.Message, state: FSMContext):
    cyfr = int(message.text)
    if cyfr < 10 or cyfr > 100:
        await state.clear()
        await message.answer('вы малолетка или умер.'
                             '\nвы не имеете доступ.')
    else:
        await state.set_state(BookSurvey.occupation)
        await state.update_data(age=cyfr)
        await message.answer('чем увлекаетесь?')
    # if cyfr <= 18:
    #     await message.answer('оцените что-то (от 1 до 10).')
    # await message.answer('укажите сколько зарабатываете (доллары).')


@start_router.message(BookSurvey.occupation)
async def upp1234(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cyfr = data['age']
    await state.set_state(BookSurvey.salary_or_grade)
    await state.update_data(occupation=message.text)
    if cyfr <= 18:
        await message.answer('какой средний бал , школота?')
    else:
        await message.answer(f'сколько зарабатываете господин?')

@start_router.message(BookSurvey.salary_or_grade)
async def upp1243(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.test)
    await state.update_data(salary_or_grade=message.text)
    await message.answer('опрос окончен.')
    data = await state.get_data()
    await message.answer(f'Отправил.'
                         f'\nИмя - {data['name']}'
                         f'\nВозраст - {data['age']}'
                         f'\nУвлечение - {data['occupation']}'
                         f'\nЗп или Средний - {data['salary_or_grade']}')

    await database.execute('INSERT INTO survey ('
                           'name, age, occupation, salary_or_grade) VALUES ('
                           '?, ?, ?, ?)',
                           (data["name"], data["age"], data['occupation'], data['salary_or_grade']))
    # await message.answer('Отправлено')
    await state.clear()