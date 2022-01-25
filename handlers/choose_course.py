from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import commands as cmd
from keyboards import ReplyStartupKeyboard, create_dynamic_inline_keyboard, InlineConfirmKeyboard
from models import Courses

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
    keyboard = create_dynamic_inline_keyboard(
        [x[0] for x in await Courses.filter().distinct().values_list('subject')])
    await message.answer("Выберите предмет:", reply_markup=keyboard)
    await CourseOrder.waiting_for_subject.set()


async def subjects_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    await state.update_data(chosen_subject=callback.data)

    async with state.proxy() as data:
        keyboard = create_dynamic_inline_keyboard(
            [x[0] for x in
             await Courses.filter(subject=data['chosen_subject']).values_list('school')])

        # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await CourseOrder.next()
    await callback.message.answer("Теперь выберите школу:", reply_markup=keyboard)


async def schools_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_school=callback.data)
    async with state.proxy() as data:
        keyboard = create_dynamic_inline_keyboard(
            [x[0] for x in
             await Courses.filter(subject=data['chosen_subject'], school=data['chosen_school']).values_list('name')])

    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await CourseOrder.next()
    await callback.message.answer("Пора выбрать интересующий Вас курс:", reply_markup=keyboard)


async def course_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_course=callback.data)

    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await CourseOrder.next()
    user_data = await state.get_data()
    await callback.message.answer(f"Вы покупаете {user_data['chosen_course']} от школы {user_data['chosen_school']}"
                                  f" по {user_data['chosen_subject']}.\n Все верно?", reply_markup=InlineConfirmKeyboard)


async def confirm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'NO':
        await state.reset_state()
        await callback.message.answer("Хорошо.")
        await subjects_start(callback.message)
    else:
        # Для последовательных шагов можно не указывать название состояния, обходясь next()
        await callback.message.answer("Принято.", reply_markup=ReplyStartupKeyboard)
        async with state.proxy() as data:
            school = data['chosen_school']
            subject = data['chosen_subject']
            name = data['chosen_course']

        current_course = await Courses.get(school=school, subject=subject, name=name).prefetch_related('webinars')
        webinars = await current_course.webinars.limit(1)
        await callback.message.answer(webinars[0].text, parse_mode='HTML')
        await state.finish()


def register_handlers_course(dp: Dispatcher):
    dp.register_message_handler(subjects_start, Text(cmd.buy_course_cmd, ignore_case=True), state="*")
    dp.register_callback_query_handler(subjects_chosen, state=CourseOrder.waiting_for_subject)
    dp.register_callback_query_handler(schools_chosen, state=CourseOrder.waiting_for_school)
    dp.register_callback_query_handler(course_chosen, state=CourseOrder.waiting_for_course)
    dp.register_callback_query_handler(confirm, state=CourseOrder.waiting_for_confirmation)


def lower_list(items: list):
    for i in range(len(items)):
        items[i] = items[i].lower()
    return items


def print_dict(dct):
    for key, value in dct.items():
        print(key, ':', value)
