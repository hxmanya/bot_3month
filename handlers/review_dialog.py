from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_config import RATINGS, users_reviewed


review_router = Router()


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

class RestaurantReview(StatesGroup):
    name = State()
    contact = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

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
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.contact)
    await message.answer("Введите ваш номер телефона или имя пользователя в Instagram:")


@review_router.message(RestaurantReview.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer("Введите дату вашего посещения: ")

@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await message.answer("Как вы оцениваете качество еды? (от 1 до 5)", reply_markup=ratings_kb)
    await state.set_state(RestaurantReview.food_rating)

@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await message.answer("Как вы оцениваете чистоту заведения? (от 1 до 5)", reply_markup=ratings_kb)
    await state.set_state(RestaurantReview.cleanliness_rating)


@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await message.answer("Пожалуйста, оставьте ваши дополнительные комментарии или жалобы (если есть):")
    await state.set_state(RestaurantReview.extra_comments)


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()

    review_text = (
        "Спасибо за ваш отзыв!\n\n"
        f"Имя: {data['name']}\n"
        f"Контакт: {data['contact']}\n"
        f"Дата посещения: {data['visit_date']}\n"
        f"Оценка еды: {data['food_rating']}\n"
        f"Оценка чистоты: {data['cleanliness_rating']}\n"
        f"Комментарии: {data['extra_comments']}"
    )

    await message.answer(review_text)

    users_reviewed.add(message.from_user.id)

    await state.clear()