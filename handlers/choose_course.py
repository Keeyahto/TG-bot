from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import commands as cmd
from keyboards import startup_keyboard, confirm_keyboard
from keyboards.confirm_keyboard import buttons
# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_subjects = ["Химия", "Биология", "Информатика", 'Математика']
available_schools = ["Школа 1", "Школа 2", "Школа 3"]
available_courses = ["Курс 1", "Курс 2", "Покупка отдельных занятий"]


class CourseOrder(StatesGroup):
    waiting_for_subject = State()
    waiting_for_school = State()
    waiting_for_course = State()
    waiting_for_confirmation = State()


async def subjects_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in available_subjects:
        keyboard.add(subject)
    await message.answer("Выберите предмет:", reply_markup=keyboard)
    await CourseOrder.waiting_for_subject.set()


async def subjects_chosen(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    if message.text.lower() not in lower_list(available_subjects):
        await message.answer("Пожалуйста, выберите предмет, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_subject=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for school in available_schools:
        keyboard.add(school)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await CourseOrder.next()
    await message.answer("Теперь выберите школу:", reply_markup=keyboard)


async def schools_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in lower_list(available_schools):
        await message.answer("Пожалуйста, выберите школу, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_school=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for course in available_courses:
        keyboard.add(course)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await CourseOrder.next()
    await message.answer("Пора выбрать интересующий Вас курс:", reply_markup=keyboard)


async def course_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in lower_list(available_courses):
        await message.answer("Пожалуйста, выберите курс, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_course=message.text.lower())

    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await CourseOrder.next()
    user_data = await state.get_data()
    await message.answer(f"Вы покупаете {user_data['chosen_course']} от школы {user_data['chosen_school']}"
                         f" по {user_data['chosen_subject']}.\n Все верно?", reply_markup=confirm_keyboard)


async def confirm(message: types.Message, state: FSMContext):
    if message.text.lower() not in lower_list(buttons):
        await message.answer("Пожалуйста, используйте клавиатуру ниже.")
        return
    if message.text.lower() == 'нет':
        await state.reset_state()
        await message.answer("Хорошо.")
        await subjects_start(message)
    else:
        # Для последовательных шагов можно не указывать название состояния, обходясь next()
        await message.answer("Принято.", reply_markup=startup_keyboard)
        print_dict(await state.get_data())
        await state.finish()


def register_handlers_course(dp: Dispatcher):
    dp.register_message_handler(subjects_start, lambda msg: msg.text.lower() == cmd.buy_course_cmd, state="*")
    dp.register_message_handler(subjects_chosen, state=CourseOrder.waiting_for_subject)
    dp.register_message_handler(schools_chosen, state=CourseOrder.waiting_for_school)
    dp.register_message_handler(course_chosen, state=CourseOrder.waiting_for_course)
    dp.register_message_handler(confirm, state=CourseOrder.waiting_for_confirmation)


def lower_list(items: list):
    for i in range(len(items)):
        items[i] = items[i].lower()
    return items


def print_dict(dct):
    for key, value in dct.items():
        print(key, ':', value)