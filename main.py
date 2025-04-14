import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

auto_models = [
    "Toyota Hilux", "Toyota Tundra", "Toyota Tacoma", "Mitsubishi L200", "Isuzu D-Max",
    "Nissan Navara (NP300)", "Nissan Titan / Titan XD", "Ford Ranger", "Ford F-150 / F-250 / F-350",
    "Volkswagen Amarok", "Mazda BT-50", "SsangYong Actyon Sports", "UAZ Pickup",
    "Great Wall Wingle 5 / Wingle 7", "Great Wall Poer (GWM Poer)", "JAC T6 / T8 / T9",
    "Foton Tunland V9 / G7", "Sollers ST8", "Chevrolet Colorado / Silverado", "GMC Sierra / Canyon",
    "RAM 1500 / 2500 / 3500", "Jeep Gladiator", "Honda Ridgeline", "Rivian R1T",
    "Changan Hunter / F70", "JMC Vigus / Baodian", "Dongfeng DF6"
]

kunq_types = ["Кунг Стандарт", "Кунг Pro", "Кунг по индивидуальному заказу", "Другое"]

kunq_texts = {
    "Кунг Стандарт": "✅ Базовая комплектация кунга Wild Wheels\n🔩 Алюминиевый сварной каркас\n🚪 Задняя дверь на газ-лифтах\n🪟 Глухие боковины или открывающиеся люки\n🎨 Порошковая покраска\nНадёжно, практично, доступно.\nОтличный выбор для повседневных задач.",
    "Кунг Pro": "🛠 Расширенная комплектация Pro\n💡 Внутренний свет, вентиляция\n🪟 Боковые окна с москитными сетками\n⚙️ Утеплённые панели, усиленный каркас\n🎨 Премиум-отделка, спеццвета\nДля тех, кто уходит за горизонт.",
    "Кунг по индивидуальному заказу": "🔧 Хочешь свой уникальный кунг?\nМы делаем: спальники, ящики, кухни, душ, освещение, окна, автономку и всё, что нужно.\nНапиши, что хочешь — подберём решение и сделаем проект.",
    "Другое": "🚙 Интересует не кунг, а: крышка кузова, багажник, экспедиционник и т.д.\nНапиши в свободной форме, мы поможем."
}

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(text=model, callback_data=model)] for model in auto_models[:5]]
    await update.message.reply_text("Выберите вашу модель пикапа:", reply_markup=InlineKeyboardMarkup(buttons))

async def model_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_states[query.from_user.id] = query.data
    buttons = [[InlineKeyboardButton(text=qt, callback_data=qt)] for qt in kunq_types]
    await query.edit_message_text(f"Вы выбрали {query.data}. Теперь выберите тип кунга:", reply_markup=InlineKeyboardMarkup(buttons))

async def kunq_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    kunq = query.data
    text = kunq_texts.get(kunq, "Описание временно недоступно.")
    buttons = [[InlineKeyboardButton(text="📲 Оставить номер для связи", callback_data="leave_contact")]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))

async def request_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✍️ Введите номер телефона или способ связи — мы свяжемся с вами.")

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 Новый контакт с бота:
{user_msg}")
    await update.message.reply_text("✅ Спасибо! Мы получили ваши данные.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(model_selected, pattern='^(' + '|'.join(auto_models) + ')$'))
    app.add_handler(CallbackQueryHandler(kunq_selected, pattern='^(' + '|'.join(kunq_types) + ')$'))
    app.add_handler(CallbackQueryHandler(request_contact, pattern='^leave_contact$'))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_contact))
    app.run_polling()

if __name__ == "__main__":
    main()
