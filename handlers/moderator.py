from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import commands as cmd
import common_functions
from keyboards import ReplyStartupKeyboard, ReplyConfirmKeyboard, ReplyDontUpload, ReplyKeyboardRemove, \
    create_dynamic_inline_keyboard, InlineMonthKeyboard, InlineConfirmKeyboard
from keyboards.confirm_keyboard import buttons as conf_btns
from common_functions import lower_list
from models import Courses, Webinars


class FDMModerator(StatesGroup):
    waiting_for_subject = State()
    waiting_for_school = State()
    waiting_for_shedule = State()
    waiting_for_course = State()
    waiting_for_month = State()
    waiting_for_confirmation = State()
    waiting_for_course_upload = State()
    upload_again = State()


# TODO: выбор парамтров inline для загрузки курсов
async def subjects_start(callback: types.CallbackQuery):
    keyboard = create_dynamic_inline_keyboard(
        [x[0] for x in await Courses.all().order_by('subject').distinct().values_list('subject')])
    if isinstance(callback, types.Message):
        await callback.answer("Выберите название предмета или введите новое:", reply_markup=keyboard)
    else:
        await callback.message.answer("Выберите название предмета или введите новое:", reply_markup=keyboard)
    await FDMModerator.waiting_for_subject.set()


async def subjects_chosen(callback: types.CallbackQuery, state: FSMContext):
    keyboard = create_dynamic_inline_keyboard(
        [x[0] for x in await Courses.all().order_by('school').distinct().values_list('school')])
    if isinstance(callback, types.Message):
        await callback.answer("Выберите название школы или введите новое:", reply_markup=keyboard)
        await state.update_data(chosen_subject=callback.html_text)

    else:
        await callback.message.answer("Выберите название школы или введите новое:", reply_markup=keyboard)
        await state.update_data(chosen_subject=callback.data)

    await FDMModerator.next()


async def schools_chosen(callback: types.CallbackQuery, state: FSMContext):
    if isinstance(callback, types.Message):
        await callback.answer("Пришлите расписание:")
        await state.update_data(chosen_school=callback.html_text)

    else:
        await callback.message.answer("Пришлите расписание:")
        await state.update_data(chosen_school=callback.data)

    await FDMModerator.next()


async def shedule_load(message: types.Message, state: FSMContext):
    await state.update_data(shedule_id=message.photo[0].file_id)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await FDMModerator.next()
    await message.answer("Введите название курса:")


async def course_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_course=message.html_text)
    await FDMModerator.next()
    await message.answer("Выберите месяц:", reply_markup=InlineMonthKeyboard)


async def month_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(month=callback.data)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await FDMModerator.next()
    user_data = await state.get_data()
    await callback.message.answer(f"Вы загружаете {user_data['chosen_course']} от школы {user_data['chosen_school']}"
                                  f" по {user_data['chosen_subject']}.\n Все верно?", reply_markup=InlineConfirmKeyboard)


async def confirm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.lower() == 'NO':
        await state.reset_state()
        await callback.message.answer("Хорошо.")
        await subjects_start(callback)
    else:
        await FDMModerator.next()
        # Для последовательных шагов можно не указывать название состояния, обходясь next()
        await callback.message.answer("Перешлите курс сюда. Нажмите /stop, когда закончите",
                             reply_markup=ReplyDontUpload)
        await state.update_data(course=[])


async def course_upload(message: types.Message, state: FSMContext):
    if message.text.lower() != '/stop':
        async with state.proxy() as data:
            data['course'].append(message.html_text)
        return
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    data = await state.get_data()
    webs = data['course']
    course = await Courses.create(subject=data['chosen_subject'],
                                  school=data['chosen_school'],
                                  name=data['chosen_course'],
                                  month=data['month'],
                                  schedule_img_id=data['shedule_id'])
    for web in webs: await course.webinars.add(await Webinars.create(text=web))
    await message.answer("Курс успешно загружен. Хотите загрузить еще?", reply_markup=InlineConfirmKeyboard)
    await FDMModerator.next()


async def confirm_upload_again(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'YES':
        await state.reset_state()
        await callback.message.answer("Хорошо.")
        await subjects_start(callback)
    else:
        # Для последовательных шагов можно не указывать название состояния, обходясь next()
        await callback.message.answer("Окей", reply_markup=ReplyStartupKeyboard)
        await state.finish()


def register_handlers_upload_course(dp: Dispatcher):
    dp.register_callback_query_handler(subjects_start,
                                       (lambda cb: cb.data == cmd.upload_course_cmd),
                                       is_admin=True,
                                       state="*")
    dp.register_message_handler(subjects_chosen, state=FDMModerator.waiting_for_subject)
    dp.register_callback_query_handler(subjects_chosen, state=FDMModerator.waiting_for_subject)
    dp.register_message_handler(schools_chosen, state=FDMModerator.waiting_for_school)
    dp.register_callback_query_handler(schools_chosen, state=FDMModerator.waiting_for_school)
    dp.register_message_handler(shedule_load, content_types=['photo'], state=FDMModerator.waiting_for_shedule)
    dp.register_message_handler(course_chosen, state=FDMModerator.waiting_for_course)
    dp.register_callback_query_handler(month_chosen,
                                       state=FDMModerator.waiting_for_month)
    dp.register_message_handler(confirm, state=FDMModerator.waiting_for_confirmation)
    dp.register_callback_query_handler(confirm, state=FDMModerator.waiting_for_confirmation)
    dp.register_message_handler(course_upload, state=FDMModerator.waiting_for_course_upload)
    dp.register_message_handler(confirm_upload_again, state=FDMModerator.upload_again)
    dp.register_callback_query_handler(confirm_upload_again, state=FDMModerator.upload_again)

