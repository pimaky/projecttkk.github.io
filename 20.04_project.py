from aiogram import Bot, types
import random
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import filters
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, WebAppInfo
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

a = ['лазанья',
     'Грибной жульен - Ингредиенты (на 3 порции): шампиньоны — 350 г; лук репчатый — 1 шт.;  сливки 20% — 200 мл; сыр — 150 г; мука — 1 ч. л.; масло сливочное — 25 г;',
     'карбонара', 'сырный суп', 'пирог']
fh = ['Минтай, тушенный в сметане', 'Уха', 'Рыба, запеченная с картошкой в духовке', 'Рыбное филе в сырном кляре', 'Стейки из красной рыбы', 'Жаренная рыба в сырном кляре', 'Селедка под шубой', 'Биточки из рыбы']
mt = ['Жульен с курицей и грибами', 'Жаркое по-деревенски', 'Куриное филе в кисло-сладком соусе', 'Куриные рулетики с сыром', 'Мясо по-французски с запеченным картофелем', 'Куриная отбивная', 'Котлета по-киевски']
ft = ['Шарлотка', 'Компот', 'Банановые панкейки', 'Салат Изумрудная россыпь', 'Печеные яблоки', 'Пастила из сливы', 'Фруктовое желе']
ve = ['Оладьи из кабачков', 'Рататуй', 'Овощное рагу', 'Цветная капуста, запеченная в сметанно-чесночном соусе под сыром', 'Паприкаш из кабачков с помидорами', 'Рис с овощами']

kbd = ReplyKeyboardMarkup()
btn1 = KeyboardButton("рыба")
btn2 = KeyboardButton("мясо")
btn3 = KeyboardButton("фрукты")
btn4 = KeyboardButton("овощи")
kbd.row(btn1, btn2, btn3, btn4)

web_app = WebAppInfo(url="https://maximilian13.github.io/Maximilian13071999.github.io/")
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton(text="site", web_app=web_app))

bot = Bot(token="7548509146:AAHS7ZZWslpNfN44YrZ13U5oN95HPbQuCO4")
dp = Dispatcher(bot)

buy_kb = ReplyKeyboardMarkup(resize_keyboard=True)
buy_kb.add(KeyboardButton("Оплатить"))

price = 0


@dp.message_handler(commands=['start'])
async def start(mes: types.Message):
    await mes.answer("Хай, это бот кулинар. \n"
                     "Чтобы выдать любой рецепт введите /random_dish \n"
                     "Чтобы посмотреть возможные блюда с вашими продуктами введите /products и выберите из панели нужный продукт")

@dp.message_handler(commands=['random_dish'])
async def random_dish(mes: types.Message):
    await mes.answer(random.choice(a))

@dp.message_handler(commands=['products'])
async def products(mes: types.Message):
    await mes.answer('выбери продукт', reply_markup=kbd)

@dp.message_handler(filters.Text(contains=['мясо'], ignore_case = True))
async def meat(mes: types.Message):
    await mes.answer(random.choice(mt))

@dp.message_handler(filters.Text(contains=['рыба'], ignore_case = True))
async def fish(mes: types.Message):
    await mes.answer(random.choice(fh))

@dp.message_handler(filters.Text(contains=['фрукты'], ignore_case = True))
async def fruit(mes: types.Message):
    await mes.answer(random.choice(ft))

@dp.message_handler(filters.Text(contains=['овощи'], ignore_case = True))
async def vegetable(mes: types.Message):
    await mes.answer(random.choice(ve))

@dp.message_handler(content_types=["web_app_data"])  # ✅ исправлено
async def get_data(web_app_message: types.Message):
    global price
    text = web_app_message.web_app_data.data
    match = re.search(r"С вас (\d+)\$", text)
    if match:
        price = match.group(1)
    else:
        price = "неизвестна"

    await bot.send_message(web_app_message.chat.id, text, reply_markup=buy_kb)

@dp.message_handler(filters.Text(contains="Оплатить"))
async def buy(message: types.Message):
    await message.answer(f"Спасибо за покупку на {price}$")

executor.start_polling(dp, skip_updates=True)