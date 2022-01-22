from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import IDFilter, Text
import commands as cmd
from keyboards import Startup_keyboard, Confirm_keyboard, Dont_upload, ReplyKeyboardRemove
from keyboards.confirm_keyboard import buttons as conf_btns
from common_functions import lower_list, print_dict
from config import config


class FDMModerator(StatesGroup):
    waiting_for_subject = State()
    waiting_for_school = State()
    waiting_for_course = State()
    waiting_for_confirmation = State()
    waiting_for_course_upload = State()
    upload_again = State()


# TODO: выбор парамтров inline для загрузки курсов
async def subjects_start(message: types.Message):
    await message.answer("Выберите название предмета или введите новое:", reply_markup=ReplyKeyboardRemove())
    await FDMModerator.waiting_for_subject.set()


async def subjects_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_subject=message.html_text)
    await FDMModerator.next()
    await message.answer("Выберите название школы или введите новое:")


async def schools_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_school=message.html_text)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await FDMModerator.next()
    await message.answer("Выберите название курса или введите новое:")


# TODO: возможно стоит сделать confirm inline?
async def course_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_course=message.html_text)
    await FDMModerator.next()
    user_data = await state.get_data()
    await message.answer(f"Вы загружаете {user_data['chosen_course']} от школы {user_data['chosen_school']}"
                         f" по {user_data['chosen_subject']}.\n Все верно?", reply_markup=Confirm_keyboard)


async def confirm(message: types.Message, state: FSMContext):
    if message.text.lower() not in lower_list(conf_btns):
        await message.answer("Пожалуйста, используйте клавиатуру ниже.")
        return
    if message.text.lower() == 'нет':
        await state.reset_state()
        await message.answer("Хорошо.")
        await subjects_start(message)
    else:
        await FDMModerator.next()
        # Для последовательных шагов можно не указывать название состояния, обходясь next()
        await message.answer("Перешлите курс сюда. Нажмите /stop, когда закончите",
                             reply_markup=Dont_upload)
        await state.update_data(course=[])


async def course_upload(message: types.Message, state: FSMContext):
    if message.text.lower() != '/stop':
        async with state.proxy() as data:
            data['course'].append(message.html_text)
        return
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    print_dict(await state.get_data())
    # await state.finish()
    await message.answer("Курс успешно загружен. Хотите загрузить еще?", reply_markup=Confirm_keyboard)
    await FDMModerator.next()


async def confirm_upload_again(message: types.Message, state: FSMContext):
    if message.text.lower() not in lower_list(conf_btns):
        await message.answer("Пожалуйста, используйте клавиатуру ниже.")
        return
    if message.text.lower() == 'да':
        await state.reset_state()
        await state.reset_state()
        await message.answer("Хорошо.", reply_markup=ReplyKeyboardRemove())
        await subjects_start(message)
    else:
        # Для последовательных шагов можно не указывать название состояния, обходясь next()
        await message.answer("Окей", reply_markup=Startup_keyboard)
        await state.finish()


def register_handlers_upload_course(dp: Dispatcher):
    dp.register_message_handler(subjects_start, Text(equals=cmd.upload_course_cmd, ignore_case=True), is_admin=True,
                                state="*")
    dp.register_message_handler(subjects_chosen, state=FDMModerator.waiting_for_subject)
    dp.register_message_handler(schools_chosen, state=FDMModerator.waiting_for_school)
    dp.register_message_handler(course_chosen, state=FDMModerator.waiting_for_course)
    dp.register_message_handler(confirm, state=FDMModerator.waiting_for_confirmation)
    dp.register_message_handler(course_upload, state=FDMModerator.waiting_for_course_upload)
    dp.register_message_handler(confirm_upload_again, state=FDMModerator.upload_again)
