from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from aiogram import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from motor import motor_asyncio

# from bot import select_users

TOKEN = 'TOKEN'
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

# Database


# buttons
in_user_types = types.InlineKeyboardMarkup(row_width=1)
indl1 = types.InlineKeyboardButton(text='Учитель', callback_data='type_teacher')
indl2 = types.InlineKeyboardButton(text='Студент', callback_data='type_student')
indl3 = types.InlineKeyboardButton(text='Тьютор', callback_data='type_tutor')
in_user_types.add(indl1).add(indl2).add(indl3)

keyb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button1 = types.KeyboardButton(text='Перейти к поиску')
keyb.add(button1)

keyb2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button2 = types.KeyboardButton(text='Попробовать еще раз')
keyb2.add(button2)



class User(StatesGroup):
    teachers_name = State()
    students_name = State()
    tutors_name = State()
    repeat = State()

    teachers_username = State()
    students_username = State()
    tutors_username = State()

    teachers_delete_name = State()
    students_delete_name = State()
    tutors_delete_name = State()

    teachers_phone = State()
    students_phone = State()
    tutors_phone = State()
    
    teachers_surname = State()
    students_surname = State()
    tutors_surname = State()
    
    teachers_telegram = State()
    students_telegram = State()
    tutors_telegram = State()
    students_orda = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Приветствую! Я бот, который поможет вам найти контакты нужного пользователя. ',
                         reply_markup=keyb)


@dp.message_handler(text='Перейти к поиску')
async def com(message: types.Message):
    await message.answer('Кого вы хотите найти?', reply_markup=in_user_types)



@dp.callback_query_handler(lambda c: c.data.startswith('type'))
async def call_back(call: types.CallbackQuery):
    if call.data == 'type_teacher':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [types.InlineKeyboardButton(text='Найти преподавателя', callback_data='find_teachers'),
                   types.InlineKeyboardButton(text='Добавить преподавателя', callback_data='add_teachers'),
                   types.InlineKeyboardButton(text='Удалить преподавателя', callback_data='delete_teachers'),
                   types.InlineKeyboardButton(text='Показать список всех преподавателей', callback_data='get_teachers'),
                   types.InlineKeyboardButton(text='Назад', callback_data='back')]
        keyboard.add(*buttons)

        await bot.edit_message_text('Выберите подходящее действие:', call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)

    elif call.data == 'type_student':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [types.InlineKeyboardButton(text='Найти студента', callback_data='find_students'),
                   types.InlineKeyboardButton(text='Добавить студента', callback_data='fff_students'),
                   types.InlineKeyboardButton(text='Удалить студента', callback_data='delete_students'),
                   types.InlineKeyboardButton(text='Назад', callback_data='back')]
        keyboard.add(*buttons)

        await bot.edit_message_text('Выберите подходящее действие:', call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)

    elif call.data == 'type_tutor':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [types.InlineKeyboardButton(text='Найти тьютора', callback_data='find_tutors'),
                   types.InlineKeyboardButton(text='Добавить тьютора', callback_data='add_tutors'),
                   types.InlineKeyboardButton(text='Удалить тьютора', callback_data='delete_tutors'),
                   types.InlineKeyboardButton(text='Показать список всех тьюторов', callback_data='get_tutors'),
                   types.InlineKeyboardButton(text='Назад', callback_data='back')]
        keyboard.add(*buttons)

        await bot.edit_message_text('Выберите подходящее действие:', call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        

@dp.callback_query_handler(lambda c: c.data.startswith('add'))
async def call_back(call: types.CallbackQuery):
    collection = call.data.split('_')[1]
    print(collection)
    await bot.edit_message_text('Введите имя для добавления:', call.message.chat.id, call.message.message_id)

    if collection == 'teachers':
        await User.teachers_username.set()
    if collection == 'tutors':
        await User.tutors_username.set()

@dp.message_handler(state=[User.teachers_username, User.tutors_username])
async def add(message: types.Message, state: FSMContext):
    name = message.text.capitalize()
    collection = await state.get_state()
    print(collection)
    if 'teachers' in collection:
        await message.answer('Введите фамилию преподавателя:')
        await User.teachers_surname.set()
    if collection == 'tutors':
        await message.answer('Введите фамилию тьютора:')
        await User.tutors_surname.set()
    await state.update_data(name=name)
    
@dp.message_handler(state=[User.teachers_surname, User.tutors_surname])
async def add(message: types.Message, state: FSMContext):
    surname = message.text.capitalize()
    collection = await state.get_state()
    print(collection)
    if 'teachers' in collection:
        await message.answer('Введите телефон преподавателя:')
        await User.teachers_phone.set()
    if collection == 'tutors':
        await message.answer('Введите телефон тьютора:')
        await User.tutors_phone.set()
    await state.update_data(surname=surname)


@dp.message_handler(state=[User.teachers_phone, User.tutors_phone])
async def add(message: types.Message, state: FSMContext):
    phone = message.text
    collection = await state.get_state()
    print(collection)
    if 'teachers' in collection:
        await message.answer('Введите телеграм преподавателя:')
        await User.teachers_telegram.set()
    if collection == 'tutors':
        await message.answer('Введите телеграм тьютора:')
        await User.tutors_telegram.set()
    await state.update_data(phone=phone)


@dp.message_handler(state=[User.teachers_telegram, User.tutors_telegram])
async def add(message: types.Message, state: FSMContext):
    telegram = message.text
    collection = await state.get_state()
    print(collection)
    data = await state.get_data()
    print(data)
    if 'teachers' in collection:
        await db.teachers.insert_one({'name': data['name'], 'surname': data['surname'], 'phone': data['phone'], 'telegram': telegram})
        await message.answer('Преподаватель добавлен в базу.')
    if collection == 'tutors':
        await db.tutors.insert_one({'name': data['name'], 'surname': data['surname'], 'phone': data['phone'], 'telegram': telegram})
        await message.answer('Тьютор добавлен в базу.')
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('fff'))
async def call_back(call: types.CallbackQuery):
    collection = call.data.split('_')[1]
    print(collection)
    await bot.edit_message_text('Введите имя для добавления:', call.message.chat.id, call.message.message_id)

    if collection == 'students':
        await User.students_username.set()

@dp.message_handler(state=[User.students_username])
async def add(message: types.Message, state: FSMContext):
    name = message.text.capitalize()
    collection = await state.get_state()
    print(collection)
    if 'students' in collection:
        await message.answer('Введите фамилию студента:')
        await User.students_surname.set()

    await state.update_data(name=name)
        
@dp.message_handler(state=[User.students_surname])
async def add(message: types.Message, state: FSMContext):
    surname = message.text.capitalize()
    collection = await state.get_state()
    print(collection)
    if 'students' in collection:
        await message.answer('Введите орду студента:')
        await User.students_orda.set()

    await state.update_data(surname=surname)

@dp.message_handler(state=[User.students_orda])
async def add(message: types.Message, state: FSMContext):
    orda = message.text
    collection = await state.get_state()
    print(collection)
    if 'students' in collection:
        await message.answer('Введите телефон студента:')
        await User.students_phone.set()

    await state.update_data(orda=orda)


@dp.message_handler(state=[User.students_phone])
async def add(message: types.Message, state: FSMContext):
    phone = message.text
    collection = await state.get_state()
    print(collection)
    if 'students' in collection:
        await message.answer('Введите телеграм студента:')
        await User.students_telegram.set()
    await state.update_data(phone=phone)


@dp.message_handler(state=[User.students_telegram])
async def add(message: types.Message, state: FSMContext):
    telegram = message.text
    collection = await state.get_state()
    print(collection)
    data = await state.get_data()
    print(data)
    if 'students' in collection:
        await db.students.insert_one({'name': data['name'], 'surname': data['surname'], 'orda': data['orda'], 'phone': data['phone'], 'telegram': telegram})
        await message.answer('Студент добавлен в базу.')
    await state.finish()

@dp.message_handler(text='Попробовать еще раз')
async def com(message: types.Message):
    await bot.edit_message_text('hello')
    
@dp.callback_query_handler(lambda c: c.data.startswith('find'))
async def call_back(call: types.CallbackQuery):
    collection = call.data.split('_')[1]
    print(collection)
    await bot.edit_message_text('Введите имя для поиска:', call.message.chat.id, call.message.message_id)

    if collection == 'teachers':
        await User.teachers_name.set()
    elif collection == 'students':
        await User.students_name.set()
    elif collection == 'tutors':
        await User.tutors_name.set()


@dp.message_handler(state=[User.teachers_name, User.students_name, User.tutors_name])
async def find(message: types.Message, state: FSMContext):
    name = message.text.capitalize() 
    collection = await state.get_state()
    print(collection)
    if 'teachers' in collection:
        name_count = await db.teachers.count_documents({"name": name})
        if name_count > 1:
            await another_function(message)
        elif name_count == 1:
            await message.answer('Ищем преподавателя...')
            teacher = await db.teachers.find_one({'name': name})
            if teacher:
                await message.answer(f'Имя: {teacher["name"]}\nНомер: {teacher["phone"]}\nТелеграм: {teacher["telegram"]}')
        else:
            await message.answer('Такого преподавателя нет в базе.')
    elif 'students' in collection:
        name_count = await db.students.count_documents({"name": name})
        if name_count > 1:
            await baska_function(message)
        elif name_count == 1:
            await message.answer('Ищем студента...')
            student = await db.students.find_one({'name': name})
            if student:
                await message.answer(
                    f'Имя: {student["name"]}\nОрда: {student["orda"]}\nТелефон: {student["phone"]}\nТелеграм: {student["telegram"]}')
        else:
            await message.answer('Такого студента нет в базе.')
    elif 'tutors' in collection:
        name_count = await db.tutors.count_documents({"name": name})
        if name_count > 1:
            await another_function(message)
        elif name_count == 1:
            await message.answer('Ищем тьютора...')
            tutor = await db.tutors.find_one({'name': name})
            if tutor:
                await message.answer(f'Имя: {tutor["name"]}\nТелефон: {tutor["phone"]}\nТелеграм: {tutor["telegram"]}')
            else:
                await message.answer('Такого тьютора нет в базе.')
    await state.finish()


async def another_function(message: types.Message):
    # Этап 1: Найти повторяющиеся имена
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    repeating_names = await db.teachers.aggregate(pipeline).to_list(length=100)

    # Этап 2: Для каждого имени найти соответствующие фамилии
    buttons = []
    for name in repeating_names:
        teachers = await db.teachers.find({'name': name['_id']}).to_list(length=100)
        for teacher in teachers:
            button_text = f"{teacher['name']} {teacher['surname']}"
            callback_data = f'db_teachers_get_{teacher["name"]}_{teacher["surname"]}'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*buttons)
    await bot.send_message(message.chat.id, 'Какой из этих?', reply_markup=inline_kb)


async def drugoi_function(message: types.Message):
    # Этап 1: Найти повторяющиеся имена
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    repeating_names = await db.tutors.aggregate(pipeline).to_list(length=100)

    # Этап 2: Для каждого имени найти соответствующие фамилии
    buttons = []
    for name in repeating_names:
        tutors = await db.tutors.find({'name': name['_id']}).to_list(length=100)
        for tutor in tutors:
            button_text = f"{tutor['name']} {tutor['surname']}"
            callback_data = f'bd_tutors_get_{tutor["name"]}_{tutor["surname"]}'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*buttons)
    await bot.send_message(message.chat.id, 'Какой из этих?', reply_markup=inline_kb)
    
async def baska_function(message: types.Message):
    # Этап 1: Найти повторяющиеся имена
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    repeating_names = await db.students.aggregate(pipeline).to_list(length=100)

    # Этап 2: Для каждого имени найти соответствующие фамилии
    buttons = []
    for name in repeating_names:
        students = await db.students.find({'name': name['_id']}).to_list(length=100)
        for student in students:
            button_text = f"{student['name']} {student['surname']}"
            callback_data = f'bd_students_get_{student["name"]}_{student["surname"]}'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*buttons)
    await bot.send_message(message.chat.id, 'Какой из этих?', reply_markup=inline_kb)

    

@dp.callback_query_handler(lambda c: c.data.startswith('get'))
async def call_back(call: types.CallbackQuery):
    collection = call.data.split('_')[1]
    print(collection)

    if collection == 'teachers':
        teachers = await db.teachers.find().to_list(length=100)
        buttons = [types.InlineKeyboardButton(text=teacher['name'], callback_data=f'db_teachers_get_{teacher["name"]}_{teacher["surname"]}')
                   for teacher in teachers]
        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        inline_kb.add(*buttons)
        await bot.edit_message_text('Список всех преподавателей:', call.message.chat.id, call.message.message_id,
                                    reply_markup=inline_kb)
    elif collection == 'tutors':
        tutors = await db.tutors.find().to_list(length=100)
        buttons = [types.InlineKeyboardButton(text=tutor['name'], callback_data=f'db_tutors_get_{tutor["name"]}_{tutor["surname"]}') for
                   tutor in tutors]
        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        inline_kb.add(*buttons)
        await bot.edit_message_text('Список всех тьюторов:', call.message.chat.id, call.message.message_id,
                                    reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data.startswith('db'))
async def call_back(call: types.CallbackQuery):
    surname = call.data.split('_')[4]
    collection = call.data.split('_')[1]
    db_collection = await db[collection].find_one({'surname': surname})
    await bot.edit_message_text(
        f'Имя: {db_collection["name"]}\nНомер: {db_collection["phone"]}\nТелеграм: {db_collection["telegram"]}',
        call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(lambda c: c.data.startswith('bd'))
async def call_back(call: types.CallbackQuery):
    surname = call.data.split('_')[4]
    collection = call.data.split('_')[1]
    db_collection = await db[collection].find_one({'surname': surname})
    await bot.edit_message_text(
        f'Имя: {db_collection["name"]}\nОрда: {db_collection["orda"]}\nНомер: {db_collection["phone"]}\nТелеграм: {db_collection["telegram"]}',
        call.message.chat.id, call.message.message_id)



@dp.callback_query_handler(lambda c: c.data.startswith('delete'))
async def call_back(call: types.CallbackQuery):
    collection = call.data.split('_')[1]
    print(collection)
    await bot.edit_message_text('Введите имя для удаления:', call.message.chat.id, call.message.message_id)

    if collection == 'teachers':
        await User.teachers_delete_name.set()
    elif collection == 'students':
        await User.students_delete_name.set()
    elif collection == 'tutors':
        await User.tutors_delete_name.set()


@dp.message_handler(state=[User.teachers_delete_name, User.students_delete_name, User.tutors_delete_name])
async def delete(message: types.Message, state: FSMContext):
    collection = await state.get_state()
    name = message.text.capitalize() 
    print(collection)
    if 'teachers' in collection:
        name_count = await db.teachers.count_documents({"name": name})
        if name_count > 1:
            await kkk_function(message)
        elif name_count ==1:
            db['teachers'].delete_one({'name': message.text})
            await message.answer('Преподаватель удален из базы.')
        else:
            await message.answer('Такого преподавателя нет в списке')
    elif 'students' in collection:
        name_count = await db.students.count_documents({"name": name})
        if name_count > 1:
            await ddd_function(message)
        elif name_count==1:
            db['students'].delete_one({'name': message.text})
            await message.answer('Студент удален из базы.')
        else:
            await message.answer('Такого Студент нет в списке')
    elif 'tutors' in collection:
        name_count = await db.tutors.count_documents({"name": name})
        if name_count > 1:
            await ggg_function(message)
        elif name_count==1:
            db['tutors'].delete_one({'name': message.text})
            await message.answer('Тьютор удален из базы.')
        else:
            await message.answer('Такого Тьютор нет в списке')

    await state.finish()

async def kkk_function(message: types.Message):
    # Этап 1: Найти повторяющиеся имена
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    repeating_names = await db.teachers.aggregate(pipeline).to_list(length=100)

    # Этап 2: Для каждого имени найти соответствующие фамилии
    buttons = []
    for name in repeating_names:
        teachers = await db.teachers.find({'name': name['_id']}).to_list(length=100)
        for teacher in teachers:
            button_text = f"{teacher['name']} {teacher['surname']}"
            callback_data = f'database_teachers_get_{teacher["name"]}_{teacher["surname"]}'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*buttons)
    await bot.send_message(message.chat.id, 'Какой из этих?', reply_markup=inline_kb)

async def ggg_function(message: types.Message):
    # Этап 1: Найти повторяющиеся имена
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    repeating_names = await db.tutors.aggregate(pipeline).to_list(length=100)

    # Этап 2: Для каждого имени найти соответствующие фамилии
    buttons = []
    for name in repeating_names:
        tutors = await db.tutors.find({'name': name['_id']}).to_list(length=100)
        for tutor in tutors:
            button_text = f"{tutor['name']} {tutor['surname']}"
            callback_data = f'database_tutors_get_{tutor["name"]}_{tutor["surname"]}'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*buttons)
    await bot.send_message(message.chat.id, 'Какой из этих?', reply_markup=inline_kb)
    
async def ddd_function(message: types.Message):
    # Этап 1: Найти повторяющиеся имена
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    repeating_names = await db.students.aggregate(pipeline).to_list(length=100)

    # Этап 2: Для каждого имени найти соответствующие фамилии
    buttons = []
    for name in repeating_names:
        students = await db.students.find({'name': name['_id']}).to_list(length=100)
        for student in students:
            button_text = f"{student['name']} {student['surname']}"
            callback_data = f'database_students_get_{student["name"]}_{student["surname"]}'
            buttons.append(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(*buttons)
    await bot.send_message(message.chat.id, 'Какой из этих?', reply_markup=inline_kb)
 
@dp.callback_query_handler(lambda c: c.data.startswith('database'))
async def call_back(call: types.CallbackQuery):
    name = call.data.split('_')[3]
    collection = call.data.split('_')[1]
    db_collection = await db[collection].find_one({'name': name})
    db[collection].delete_one({'name': name})
    if collection=='teachers':
        await bot.edit_message_text('Преподаватель удален из базы.', call.message.chat.id, call.message.message_id)
    elif collection=='students':
        await bot.edit_message_text('Студент удален из базы.', call.message.chat.id, call.message.message_id)
    elif collection == 'tutors':
        await bot.edit_message_text('Тьютор удален из базы.', call.message.chat.id, call.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('back'))
async def call_back(call: types.CallbackQuery):
    await bot.edit_message_text('Кого вы хотите найти?', call.message.chat.id, call.message.message_id,
                                reply_markup=in_user_types)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
