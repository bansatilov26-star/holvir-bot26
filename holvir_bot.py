# -*- coding: utf-8 -*-
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# ============================================================
# НАСТРОЙКИ
# ============================================================

API_TOKEN = os.environ.get("API_TOKEN", "ВСТАВЬ_ТОКЕН_СЮДА")
ADMIN_ID = 7875472491

PAYMENT_LINK = "https://yookassa.ru/my/i/aqJyfcDnZHSX/l"
SUPPORT_USERNAME = "@holvir_creator"
TG_CHANNEL = "https://t.me/holvir_ai_lab"
EMAIL = "holvir.ai.lab@gmail.com"

# ============================================================
# ЛОГИРОВАНИЕ
# ============================================================

logging.basicConfig(level=logging.INFO)

# ============================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ============================================================
# СЧЁТЧИК КЛИЕНТОВ
# ============================================================

def load_counter():
    try:
        with open("counter.txt", "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_counter(counter):
    with open("counter.txt", "w", encoding="utf-8") as f:
        f.write(str(counter))


def get_price():
    counter = load_counter()

    if counter < 3:
        return 990, "🥇 Вы попали в число первых 3 клиентов!"
    elif counter < 8:
        return 1390, "🥈 Вы попали в число следующих 5 клиентов!"
    elif counter < 13:
        return 1890, "🥉 Вы попали в число следующих 5 клиентов!"
    else:
        return 2390, "💎 Основная стоимость"

# ============================================================
# СОСТОЯНИЯ АНКЕТЫ
# ============================================================

class ProjectForm(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()
    question7 = State()
    question8 = State()
    username = State()

# ============================================================
# КЛАВИАТУРЫ
# ============================================================

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🚀 Начать проект"))
    keyboard.add(KeyboardButton("💼 Чем мы можем помочь"))
    keyboard.add(KeyboardButton("💎 Тарифы"))
    keyboard.add(KeyboardButton("⭐ Отзывы"), KeyboardButton("📞 Связаться"))
    return keyboard


def help_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🚀 Запуск проекта"))
    keyboard.add(KeyboardButton("🤖 AI и автоматизация"))
    keyboard.add(KeyboardButton("📈 Развитие и стратегия"))
    keyboard.add(KeyboardButton("🔙 Главное меню"))
    return keyboard


def next_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("➡️ Продолжить"))
    return keyboard


def back_to_help_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔙 Назад"))
    return keyboard


def q2_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("📢 Telegram-канал"))
    keyboard.add(KeyboardButton("🛍️ Интернет-магазин"))
    keyboard.add(KeyboardButton("🎓 Онлайн-курс или обучение"))
    keyboard.add(KeyboardButton("🤖 AI-сервис или приложение"))
    keyboard.add(KeyboardButton("💼 Услуги или консалтинг"))
    keyboard.add(KeyboardButton("🎨 Личный бренд"))
    keyboard.add(KeyboardButton("✍️ Другое"))
    return keyboard


def q3_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("🌱 Новички в вашей нише"))
    keyboard.add(KeyboardButton("💪 Опытные пользователи"))
    keyboard.add(KeyboardButton("💼 Бизнес и предприниматели"))
    keyboard.add(KeyboardButton("🎯 Узкая специализированная аудитория"))
    keyboard.add(KeyboardButton("🌎 Широкая аудитория"))
    keyboard.add(KeyboardButton("✍️ Другое"))
    return keyboard


def q4_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("💰 Зарабатывать на рекламе"))
    keyboard.add(KeyboardButton("📦 Продавать товары или услуги"))
    keyboard.add(KeyboardButton("🤝 Создать сильное сообщество"))
    keyboard.add(KeyboardButton("🌎 Стать экспертом в своей нише"))
    keyboard.add(KeyboardButton("🚀 Развить личный бренд"))
    keyboard.add(KeyboardButton("📈 Построить пассивный доход"))
    keyboard.add(KeyboardButton("✍️ Другое"))
    return keyboard


def q5_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("💳 Подписка на закрытый контент"))
    keyboard.add(KeyboardButton("📢 Реклама и спонсорство"))
    keyboard.add(KeyboardButton("🎓 Продажа курсов или гайдов"))
    keyboard.add(KeyboardButton("💼 Услуги и консультации"))
    keyboard.add(KeyboardButton("🤝 Партнерские программы"))
    keyboard.add(KeyboardButton("🛍️ Продажа товаров"))
    keyboard.add(KeyboardButton("✍️ Другое"))
    return keyboard


def q6_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("⏰ До 30 минут в день"))
    keyboard.add(KeyboardButton("🕐 1-2 часа в день"))
    keyboard.add(KeyboardButton("💼 3-5 часов в день"))
    keyboard.add(KeyboardButton("🚀 Полный рабочий день"))
    keyboard.add(KeyboardButton("📆 Пока не определился"))
    return keyboard


def q7_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("💰 Бюджет на развитие"))
    keyboard.add(KeyboardButton("📱 Телефон или компьютер"))
    keyboard.add(KeyboardButton("📸 Опыт создания контента"))
    keyboard.add(KeyboardButton("👥 Первая аудитория или база клиентов"))
    keyboard.add(KeyboardButton("🤖 Навыки работы с AI"))
    keyboard.add(KeyboardButton("🛠️ Технические навыки"))
    keyboard.add(KeyboardButton("✍️ Другое"))
    return keyboard


def q8_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("💰 Недостаточно бюджета"))
    keyboard.add(KeyboardButton("🕐 Не хватает времени"))
    keyboard.add(KeyboardButton("📈 Не знаю, как привлекать клиентов"))
    keyboard.add(KeyboardButton("✍️ Не понимаю, какой контент создавать"))
    keyboard.add(KeyboardButton("🤔 Не знаю, с чего начать"))
    keyboard.add(KeyboardButton("😧 Страх, что не получится"))
    keyboard.add(KeyboardButton("🚀 Другое"))
    return keyboard


def payment_result_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            "📞 Написать менеджеру",
            url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}",
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            "📢 Перейти в Telegram-канал",
            url=TG_CHANNEL,
        )
    )
    return keyboard

# ============================================================
# КОМАНДЫ
# ============================================================

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer(
        "👋 Здравствуйте!\n\n"
        "Добро пожаловать в Holvir — мы помогаем запускать проекты с нуля.\n\n"
        "Выберите интересующий раздел:",
        reply_markup=main_keyboard(),
    )


@dp.message_handler(commands=["create"])
async def create_command(message: types.Message):
    await start_project(message)


@dp.message_handler(commands=["develop"])
async def develop_command(message: types.Message):
    await message.answer(
        "📈 Развитие и стратегия\n\n"
        "Уже есть проект, но не знаете, куда двигаться дальше?\n\n"
        "Мы поможем определить:\n"
        "• Целевую аудиторию\n"
        "• Дальнейшие шаги развития\n"
        "• Способы монетизации\n"
        "• Стратегию продвижения\n\n"
        "Наша команда проанализирует ваш текущий проект и предложит план действий для роста.\n\n"
        "Holvir AI помогает превращать идеи в понятные и структурированные проекты.",
        reply_markup=main_keyboard(),
    )


@dp.message_handler(commands=["support"])
async def support_command(message: types.Message):
    await message.answer(
        "📞 Поддержка Holvir\n\n"
        "Если у вас возникли вопросы или проблемы, напишите нам:\n\n"
        f"👨‍💻 Менеджер: {SUPPORT_USERNAME}\n"
        f"📧 Email: {EMAIL}\n\n"
        "Мы ответим в ближайшее время!",
        reply_markup=main_keyboard(),
    )

# ============================================================
# НАЧАТЬ ПРОЕКТ
# ============================================================

@dp.message_handler(lambda message: message.text == "🚀 Начать проект")
async def start_project(message: types.Message):
    await message.answer(
        "🎉 Добро пожаловать в Holvir!\n\n"
        "Мы помогаем запускать проекты с нуля.\n\n"
        "Наша команда поможет вам:\n"
        "✅ Определить концепцию\n"
        "✅ Разработать стратегию\n"
        "✅ Настроить монетизацию\n"
        "✅ Привлечь первых клиентов\n\n"
        "Для начала нам нужно познакомиться с вашей идеей.\n"
        "Заполните анкету из 8 вопросов — это займет не более 5 минут.",
        reply_markup=next_keyboard(),
    )

# ============================================================
# АНКЕТА
# ============================================================

@dp.message_handler(
    lambda message: message.text == "➡️ Продолжить",
    state=None,
)
async def start_questions(message: types.Message):
    await ProjectForm.question1.set()
    await message.answer(
        "📝 Вопрос 1 из 8\n\n"
        "Какую идею или проект вы хотите создать?\n\n"
        "Напишите несколькими предложениями. Не переживайте, если идея еще не до конца сформирована."
    )


@dp.message_handler(state=ProjectForm.question1)
async def process_q1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q1"] = message.text
    await ProjectForm.question2.set()
    await message.answer("✅ Записал! Идем дальше.", reply_markup=next_keyboard())


@dp.message_handler(lambda message: message.text == "➡️ Продолжить", state=ProjectForm.question2)
async def continue_to_q2(message: types.Message):
    await message.answer(
        "📝 Вопрос 2 из 8\n\n"
        "Что именно вы хотите создать?\n\n"
        "Выберите один вариант:",
        reply_markup=q2_keyboard(),
    )


@dp.message_handler(state=ProjectForm.question2)
async def process_q2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q2"] = message.text
    await ProjectForm.question3.set()
    await message.answer("✅ Принято! Идем дальше.", reply_markup=next_keyboard())


@dp.message_handler(lambda message: message.text == "➡️ Продолжить", state=ProjectForm.question3)
async def continue_to_q3(message: types.Message):
    await message.answer(
        "📝 Вопрос 3 из 8\n\n"
        "Для кого вы создаете этот проект?\n\n"
        "Выберите один или несколько вариантов:",
        reply_markup=q3_keyboard(),
    )


@dp.message_handler(state=ProjectForm.question3)
async def process_q3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q3"] = message.text
    await ProjectForm.question4.set()
    await message.answer("✅ Отлично! Идем дальше.", reply_markup=next_keyboard())


@dp.message_handler(lambda message: message.text == "➡️ Продолжить", state=ProjectForm.question4)
async def continue_to_q4(message: types.Message):
    await message.answer(
        "📝 Вопрос 4 из 8\n\n"
        "Какую главную цель вы ставите перед проектом?\n\n"
        "Выберите один или несколько вариантов:",
        reply_markup=q4_keyboard(),
    )


@dp.message_handler(state=ProjectForm.question4)
async def process_q4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q4"] = message.text
    await ProjectForm.question5.set()
    await message.answer("✅ Записал! Идем дальше.", reply_markup=next_keyboard())


@dp.message_handler(lambda message: message.text == "➡️ Продолжить", state=ProjectForm.question5)
async def continue_to_q5(message: types.Message):
    await message.answer(
        "📝 Вопрос 5 из 8\n\n"
        "Какая модель монетизации вам ближе?\n\n"
        "Выберите один или несколько вариантов:",
        reply_markup=q5_keyboard(),
    )


@dp.message_handler(state=ProjectForm.question5)
async def process_q5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q5"] = message.text
    await ProjectForm.question6.set()
    await message.answer("✅ Принято! Идем дальше.", reply_markup=next_keyboard())


@dp.message_handler(lambda message: message.text == "➡️ Продолжить", state=ProjectForm.question6)
async def continue_to_q6(message: types.Message):
    await message.answer(
        "📝 Вопрос 6 из 8\n\n"
        "Сколько времени вы готовы уделять развитию проекта?\n\n"
        "Выберите один вариант:",
        reply_markup=q6_keyboard(),
    )


@dp.message_handler(state=ProjectForm.question6)
async def process_q6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q6"] = message.text
    await ProjectForm.question7.set()
    await message.answer("✅ Отлично! Идем дальше.", reply_markup=next_keyboard())


@dp.message_handler(lambda message: message.text == "➡️ Продолжить", state=ProjectForm.question7)
async def continue_to_q7(message: types.Message):
    await message.answer(
        "📝 Вопрос 7 из 8\n\n"
        "Какие ресурсы у вас уже есть для запуска?\n\n"
        "Выберите один или несколько вариантов:",
        reply_markup=q7_keyboard(),
    )


@dp.message_handler(state=ProjectForm.question7)
async def process_q7(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q7"] = message.text
    await ProjectForm.question8.set()
    await message.answer("✅ Записал! Идем дальше.", reply_markup=next_keyboard())


@dp.message_handler(lambda message: message.text == "➡️ Продолжить", state=ProjectForm.question8)
async def continue_to_q8(message: types.Message):
    await message.answer(
        "📝 Вопрос 8 из 8\n\n"
        "Что сейчас больше всего мешает вам начать или развивать проект?\n\n"
        "Выберите один или несколько вариантов:",
        reply_markup=q8_keyboard(),
    )


@dp.message_handler(state=ProjectForm.question8)
async def process_q8(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["q8"] = message.text

    await ProjectForm.username.set()

    await message.answer(
        "🙏 Спасибо, что ответили на все вопросы!\n\n"
        "Остался последний шаг — оставьте ваш username в Telegram,\n"
        "чтобы мы могли с вами связаться.\n\n"
        "Например: @your_username"
    )


@dp.message_handler(state=ProjectForm.username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text.strip()

    if not username.startswith("@"):
        username = "@" + username

    async with state.proxy() as data:
        data["username"] = username

        price, discount_text = get_price()

        application_text = (
            "📋 Новая заявка!\n\n"
            f"1️⃣ Идея: {data['q1']}\n"
            f"2️⃣ Тип проекта: {data['q2']}\n"
            f"3️⃣ Целевая аудитория: {data['q3']}\n"
            f"4️⃣ Цели: {data['q4']}\n"
            f"5️⃣ Монетизация: {data['q5']}\n"
            f"6️⃣ Время: {data['q6']}\n"
            f"7️⃣ Ресурсы: {data['q7']}\n"
            f"8️⃣ Препятствия: {data['q8']}\n\n"
            f"👤 Username: {data['username']}\n"
            f"🆔 Telegram ID: {message.from_user.id}\n"
            f"💰 Цена: {price} ₽"
        )

    await bot.send_message(ADMIN_ID, application_text)
    await state.finish()

    payment_keyboard = InlineKeyboardMarkup(row_width=1)
    payment_keyboard.add(
        InlineKeyboardButton("💳 Оплатить заказ", url=PAYMENT_LINK)
    )
    payment_keyboard.add(
        InlineKeyboardButton("✅ Я оплатил", callback_data="paid")
    )

    await message.answer(
        "✅ Ваша заявка создана!\n\n"
        f"{discount_text}\n\n"
        f"💳 Стоимость: {price} ₽\n\n"
        "Чтобы мы начали работать над вашим проектом,\n"
        "необходимо оплатить заказ.\n\n"
        f"💳 Ссылка на оплату:\n{PAYMENT_LINK}\n\n"
        "❗️ В комментарии к платежу укажите ваш username в Telegram.\n\n"
        "После оплаты нажмите кнопку «✅ Я оплатил».",
        reply_markup=payment_keyboard,
    )

# ============================================================
# ПОСЛЕ НАЖАТИЯ «Я ОПЛАТИЛ»
# ============================================================

@dp.callback_query_handler(lambda c: c.data == "paid")
async def process_payment(callback_query: types.CallbackQuery):
    await callback_query.answer("Заявка на проверку отправлена.")

    counter = load_counter()
    counter += 1
    save_counter(counter)

    await callback_query.message.answer(
        "🔎 Проверяем оплату!\n\n"
        "⏱ В течение 1 часа с вами свяжется наш менеджер.\n\n"
        "📸 Пожалуйста, напишите менеджеру и отправьте ему "
        "скриншот оплаты — это поможет быстрее подтвердить платеж.\n\n"
        f"👨‍💻 Менеджер: {SUPPORT_USERNAME}\n\n"
        "После проверки мы приступим к работе над вашим проектом.\n\n"
        "Спасибо, что выбрали Holvir! 💜",
        reply_markup=payment_result_keyboard(),
    )

# ============================================================
# ЧЕМ МЫ МОЖЕМ ПОМОЧЬ
# ============================================================

@dp.message_handler(lambda message: message.text == "💼 Чем мы можем помочь")
async def help_menu(message: types.Message):
    await message.answer(
        "💼 Чем мы можем помочь\n\n"
        "Holvir AI помогает превращать идеи в понятные и структурированные проекты.\n\n"
        "Мы можем помочь с запуском проекта, его развитием, стратегией и использованием современных AI-инструментов.\n\n"
        "Выберите интересующее направление:",
        reply_markup=help_keyboard(),
    )


@dp.message_handler(lambda message: message.text == "🚀 Запуск проекта")
async def launch_project(message: types.Message):
    await start_project(message)


@dp.message_handler(lambda message: message.text == "🤖 AI и автоматизация")
async def ai_info(message: types.Message):
    await message.answer(
        "🤖 AI и автоматизация\n\n"
        "В дальнейшем Holvir сможет помогать внедрять AI и автоматизацию в проекты.\n\n"
        "Мы работаем над инструментами, которые позволят:\n"
        "• Автоматизировать рутинные задачи\n"
        "• Создавать контент с помощью AI\n"
        "• Анализировать данные\n"
        "• Оптимизировать процессы\n\n"
        "Следите за обновлениями!",
        reply_markup=back_to_help_keyboard(),
    )


@dp.message_handler(lambda message: message.text == "📈 Развитие и стратегия")
async def strategy_info(message: types.Message):
    await message.answer(
        "📈 Развитие и стратегия\n\n"
        "Мы можем помочь определить дальнейшие шаги, аудиторию, способы развития и монетизации.\n\n"
        "Наша команда поможет:\n"
        "• Определить целевую аудиторию\n"
        "• Выстроить стратегию развития\n"
        "• Найти способы монетизации\n"
        "• Составить план действий",
        reply_markup=back_to_help_keyboard(),
    )


@dp.message_handler(lambda message: message.text == "🔙 Назад")
async def back_to_help(message: types.Message):
    await help_menu(message)

# ============================================================
# ТАРИФЫ
# ============================================================

@dp.message_handler(lambda message: message.text == "💎 Тарифы")
async def tariffs(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🛒 Оформить заказ"))
    keyboard.add(KeyboardButton("💬 Связаться с нами"))
    keyboard.add(KeyboardButton("🔙 Главное меню"))

    await message.answer(
        "💎 ТАРИФЫ\n\n"
        "Holvir AI развивается и постепенно создает новые решения для запуска, развития и масштабирования проектов.\n\n"
        "На данный момент доступен первый проект нашей экосистемы:\n\n"
        "⸻\n\n"
        "💎 HOLVIR START\n\n"
        "Персональная стратегия запуска проекта\n\n"
        "Если у вас есть идея, но вы не знаете, с чего начать, "
        "Holvir Start поможет превратить ее в понятный план действий.\n\n"
        "Мы изучим ваш проект, проведем анализ и подготовим персональный отчет с рекомендациями под вашу задачу.\n\n"
        "⸻\n\n"
        "💰 Стоимость\n\n"
        "🚀 Специальная цена на этапе запуска\n\n"
        "🥇 Первые 3 клиентов — 990 ₽\n"
        "🥈 Следующие 5 клиентов — 1390 ₽\n"
        "🥉 Следующие 5 клиентов — 1890 ₽\n"
        "💎 Далее основная стоимость — 2390 ₽\n\n"
        "⸻\n\n"
        "📦 Что входит\n\n"
        "• Анализ идеи проекта\n"
        "• Определение целевой аудитории\n"
        "• Анализ потенциала\n"
        "• SWOT-анализ\n"
        "• Контент-стратегия\n"
        "• Возможные способы монетизации\n"
        "• Пошаговый план запуска\n"
        "• Индивидуальные рекомендации\n"
        "• Персональный Holvir Report\n\n"
        "⸻\n\n"
        "🚀 Это только начало\n\n"
        "Holvir AI — развивающийся проект, и Holvir Start является первым этапом нашей экосистемы.\n\n"
        "Следить за обновлениями можно в нашем Telegram-канале.\n\n"
        f"📢 {TG_CHANNEL}",
        reply_markup=keyboard,
    )


@dp.message_handler(lambda message: message.text == "🛒 Оформить заказ")
async def order_tariff(message: types.Message):
    await start_project(message)


@dp.message_handler(lambda message: message.text == "💬 Связаться с нами")
async def contact_from_tariff(message: types.Message):
    await message.answer(
        "📞 Свяжитесь с нами:\n\n"
        f"👨‍💻 Менеджер: {SUPPORT_USERNAME}\n"
        f"📧 Email: {EMAIL}\n\n"
        "Мы ответим в ближайшее время!",
        reply_markup=back_to_help_keyboard(),
    )

# ============================================================
# ОТЗЫВЫ
# ============================================================

@dp.message_handler(lambda message: message.text == "⭐ Отзывы")
async def reviews(message: types.Message):
    await message.answer(
        "⭐ Отзывы\n\n"
        "Мы запускаемся и будем рады поделиться результатами первых проектов!\n\n"
        "Отзывы наших клиентов вы можете найти в нашем Telegram-канале — "
        "в закрепленных сообщениях и описании канала.\n\n"
        f"📢 Подписаться на Telegram-канал:\n{TG_CHANNEL}",
        reply_markup=main_keyboard(),
    )

# ============================================================
# СВЯЗАТЬСЯ
# ============================================================

@dp.message_handler(lambda message: message.text == "📞 Связаться")
async def contact(message: types.Message):
    await message.answer(
        "📞 Связаться с нами\n\n"
        "Если у вас есть вопросы или предложения, напишите нам:\n\n"
        f"👨‍💻 Менеджер: {SUPPORT_USERNAME}\n"
        f"📧 Email: {EMAIL}\n"
        f"📢 Telegram-канал: {TG_CHANNEL}\n\n"
        "Мы ответим в ближайшее время!",
        reply_markup=main_keyboard(),
    )

# ============================================================
# ГЛАВНОЕ МЕНЮ
# ============================================================

@dp.message_handler(lambda message: message.text == "🔙 Главное меню")
async def back_to_main(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_keyboard())

# ============================================================
# НЕИЗВЕСТНЫЕ СООБЩЕНИЯ
# ============================================================

@dp.message_handler()
async def unknown_message(message: types.Message):
    await message.answer(
        "Пожалуйста, используйте кнопки меню для навигации.",
        reply_markup=main_keyboard(),
    )

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)