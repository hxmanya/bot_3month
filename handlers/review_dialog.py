from Tools.scripts.findlinksto import visit
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_config import RATINGS, users_reviewed

from bot_config import database


review_router = Router()

def validate_day(day):
    try:
        rating = int(day)
        return 1 <= rating <= 31
    except ValueError:
        return False

ratings_kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text=f"1 - {RATINGS['1']}", callback_data='1')
        ],
        [
            types.InlineKeyboardButton(text=f"2 - {RATINGS['2']}", callback_data='2')
        ],
        [
            types.InlineKeyboardButton(text=f"3 - {RATINGS['3']}", callback_data='3')
        ],
        [
            types.InlineKeyboardButton(text=f"4 - {RATINGS['4']}", callback_data='4')
        ],
        [
            types.InlineKeyboardButton(text=f"5 - {RATINGS['5']}", callback_data='5')
        ]
    ]
)

months_kb = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Январь"),
            types.KeyboardButton(text="Февраль")
        ],
        [
            types.KeyboardButton(text="Март"),
            types.KeyboardButton(text="Апрель")
        ],
        [
            types.KeyboardButton(text="Май"),
            types.KeyboardButton(text="Июнь")
        ],
        [
            types.KeyboardButton(text="Июль"),
            types.KeyboardButton(text="Август")
        ],
        [
            types.KeyboardButton(text="Сентябрь"),
            types.KeyboardButton(text="Октябрь")
        ],
        [
            types.KeyboardButton(text="Ноябрь"),
            types.KeyboardButton(text="Декабрь")
        ]
    ],
    resize_keyboard=True
)

class RestaurantReview(StatesGroup):
    name = State()
    contact = State()
    visit_date_day = State()
    visit_date_month = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    confirm = State()

@review_router.message(Command("stop"))
@review_router.message(F.text == "стоп")
async def stop_opros(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос остановлен")


@review_router.callback_query(F.data.in_(RATINGS.keys()))
async def process_rating(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    rating_value = RATINGS[callback.data]

    if current_state == RestaurantReview.food_rating.state:
        await state.update_data(food_rating=rating_value)
        await callback.message.answer("Как вы оцениваете чистоту заведения? (от 1 до 5)", reply_markup=ratings_kb)
        await state.set_state(RestaurantReview.cleanliness_rating)

    elif current_state == RestaurantReview.cleanliness_rating.state:
        await state.update_data(cleanliness_rating=rating_value)
        await callback.message.answer("Пожалуйста, оставьте ваши дополнительные комментарии или жалобы (если есть):")
        await state.set_state(RestaurantReview.extra_comments)

    await callback.answer()




@review_router.callback_query(F.data == "review")
async def start_review(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if user_id in users_reviewed:
        await callback.message.answer("Извините, вы уже оставляли отзыв. Нельзя оставить более одного отзыва.")
        await state.clear()
        await callback.answer()
        return

    await callback.message.answer("Пожалуйста, введите ваше имя:")
    await state.set_state(RestaurantReview.name)
    await callback.answer()

@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Введите ваше имя без различный символов и цифр.")
        return
    name = name.capitalize()
    await state.update_data(name=name)
    await state.set_state(RestaurantReview.contact)
    await message.answer("Введите ваш номер телефона или имя пользователя в Instagram:")


@review_router.message(RestaurantReview.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(RestaurantReview.visit_date_day)
    await message.answer("Введите день вашего посещения: ")

@review_router.message(RestaurantReview.visit_date_day)
async def process_visit_date_day(message: types.Message, state: FSMContext):
    day_number = message.text
    if validate_day(day_number):
        await state.update_data(visit_date_day=day_number)
        await message.answer("Введите месяц:", reply_markup=months_kb)
        await state.set_state(RestaurantReview.visit_date_month)
    else:
        await message.answer("Пожалуйста, введите день от 1 до 31.")

@review_router.message(RestaurantReview.visit_date_month)
async def process_visit_date_month(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.update_data(visit_date_month=message.text)
    await message.answer("Готово!", reply_markup=kb)
    await message.answer("Как вы оцениваете качество еды? (от 1 до 5)", reply_markup=ratings_kb)
    await state.set_state(RestaurantReview.food_rating)

@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите оценку от 1 до 5 с помощью кнопок!", reply_markup=ratings_kb)

@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите оценку от 1 до 5 с помощью кнопок!", reply_markup=ratings_kb)


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await message.answer("confirm?(yes/no)")
    await state.set_state(RestaurantReview.confirm)

@review_router.message(RestaurantReview.confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text == "yes":
        data = await state.get_data()

        visit_date = data["visit_date_day"] + " " + data["visit_date_month"]

        review_text = (
            "Спасибо за ваш отзыв!\n\n"
            f"Имя: {data['name']}\n"
            f"Контакт: {data['contact']}\n"
            f"Дата посещения: {visit_date}\n"
            f"Оценка еды: {data['food_rating']}\n"
            f"Оценка чистоты: {data['cleanliness_rating']}\n"
            f"Комментарии: {data['extra_comments']}"
        )


        await message.answer(review_text)

        database.execute(
            query="""
                 INSERT INTO reviews (name, phone_number, visit_date, food_rating, cleanliness_rating, extra_comments)
                 VALUES (?,?,?,?,?,?)      
               """,
            params=(data["name"], data["contact"], visit_date,
                    data["food_rating"], data["cleanliness_rating"], data["extra_comments"])
        )

        users_reviewed.add(message.from_user.id)

        await state.clear()
    elif message.text == "no":
        await message.answer("okokok")
        await state.clear()
    else:
        await message.answer("write only 'yes' or 'no'")


    # data = await state.get_data()
    #
    # review_text = (
    #     "Спасибо за ваш отзыв!\n\n"
    #     f"Имя: {data['name']}\n"
    #     f"Контакт: {data['contact']}\n"
    #     f"Дата посещения: {data['visit_date_day']} {data['visit_date_month']}\n"
    #     f"Оценка еды: {data['food_rating']}\n"
    #     f"Оценка чистоты: {data['cleanliness_rating']}\n"
    #     f"Комментарии: {data['extra_comments']}"
    # )
    #
    # await message.answer(review_text)
    #
    # users_reviewed.add(message.from_user.id)
    #
    # await state.clear()