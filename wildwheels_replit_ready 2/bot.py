from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = "7671147312:AAFySpZoV3njldLyeqjg7S5P3IlO9I-vUdA"
PHOTO_PATH = os.path.expanduser("~/Documents/telega")

pickup_buttons = [
    ["Toyota Hilux", "Toyota Tundra", "Toyota Tacoma"],
    ["Mitsubishi L200", "Isuzu D-Max", "Nissan Navara (NP300)"],
    ["Nissan Titan / Titan XD", "Ford Ranger", "Ford F-150 / F-250 / F-350"],
    ["Volkswagen Amarok", "Mazda BT-50", "SsangYong Actyon Sports"],
    ["UAZ Pickup", "Great Wall Wingle 5 / Wingle 7", "Great Wall Poer (GWM Poer)"],
    ["JAC T6 / T8 / T9", "Foton Tunland V9 / G7", "Sollers ST8"],
    ["Chevrolet Colorado / Silverado", "GMC Sierra / Canyon", "RAM 1500 / 2500 / 3500"],
    ["Jeep Gladiator", "Honda Ridgeline", "Rivian R1T"],
    ["Changan Hunter", "JMC Vigus / Baodian", "Dongfeng DF6"],
    ["TLC79", "Rambox"]
]

next_step_buttons = [["Кунг", "Автодом"], ["Крышка", "Другое"], ["⬅️ Назад", "🏠 Главное меню"]]
kung_options = [["Стандарт", "Про"], ["По индивидуальному заказу"], ["⬅️ Назад", "🏠 Главное меню"]]
ADMIN_CHAT_ID = 7702769974
user_states = {}
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_CHAT_ID:
        return
    reply_markup = ReplyKeyboardMarkup(pickup_buttons, resize_keyboard=True)
    await update.message.reply_text("Здравствуйте, выберите вашу марку пикапа:", reply_markup=reply_markup)
    user_states[user_id] = "awaiting_pickup"
    user_data[user_id] = {}

async def handle_pickup_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if user_id == ADMIN_CHAT_ID:
        return
    state = user_states.get(user_id)

    if text == "⬅️ Назад":
        if state == "awaiting_kung_type":
            user_states[user_id] = "awaiting_addon"
            reply_markup = ReplyKeyboardMarkup(next_step_buttons, resize_keyboard=True)
            await update.message.reply_text("Вы вернулись к выбору типа надстройки:", reply_markup=reply_markup)
            return
        elif state == "awaiting_addon":
            user_states[user_id] = "awaiting_pickup"
            reply_markup = ReplyKeyboardMarkup(pickup_buttons, resize_keyboard=True)
            await update.message.reply_text("Вы вернулись к выбору марки пикапа:", reply_markup=reply_markup)
            return
        elif state == "awaiting_final_contact":
            user_states[user_id] = "awaiting_kung_type"
            reply_markup = ReplyKeyboardMarkup(kung_options, resize_keyboard=True)
            await update.message.reply_text("Вы вернулись к выбору типа кунга:", reply_markup=reply_markup)
            return

    if text == "🏠 Главное меню":
        reply_markup = ReplyKeyboardMarkup(pickup_buttons, resize_keyboard=True)
        await update.message.reply_text("Вы вернулись в главное меню:", reply_markup=reply_markup)
        user_states[user_id] = "awaiting_pickup"
        user_data[user_id] = {}
        return

    if state == "awaiting_pickup" and text in sum(pickup_buttons, []):
        user_data[user_id]["пикап"] = text
        reply_markup = ReplyKeyboardMarkup(next_step_buttons, resize_keyboard=True)
        await update.message.reply_text(f"Вы выбрали: {text}\nТеперь выберите тип надстройки:", reply_markup=reply_markup)
        user_states[user_id] = "awaiting_addon"
        return

    if state == "awaiting_addon" and text == "Кунг":
        user_states[user_id] = "awaiting_kung_type"
        reply_markup = ReplyKeyboardMarkup(kung_options, resize_keyboard=True)
        await update.message.reply_text("Вы выбрали: Кунг. Уточните тип:", reply_markup=reply_markup)
        return

    if state == "awaiting_addon" and text == "Автодом":
        user_states[user_id] = "awaiting_contact_info"
        await update.message.reply_text("Спасибо за ваше обращение! Напишите, как с вами связаться, и мы ответим в течение 1 часа.")
        return

    if state == "awaiting_kung_type":
        user_data[user_id]["кунговый_тип"] = text
        pickup = user_data[user_id].get("пикап")

        # загрузка фотографий по пикапу
        filename_map = {
            "Changan Hunter": {"Стандарт": "ch.st.JPG", "Про": "ch.pro.jpeg"},
            "Dongfeng DF6": {"Стандарт": "df6.st.JPG"},
            "RAM 1500 / 2500 / 3500": {"Стандарт": "dr.st.JPG", "Про": "dr.pro.JPG"},
            "Rambox": {"Стандарт": "drb.HEIC", "Про": "drb.HEIC"},
            "Ford F-150 / F-250 / F-350": {"Стандарт": "ford.mov", "Про": "ford.mov"},
            "Foton Tunland V9 / G7": {"Стандарт": "FT.st.JPG", "Про": "FT.st.JPG"},
            "Great Wall Poer (GWM Poer)": {"Стандарт": "GW.st.JPG", "Про": "GW.pro.JPG"},
            "Great Wall Wingle 5 / Wingle 7": {"Стандарт": "GWW7.st.JPG", "Про": "GWW7.pro.JPG"},
            "Isuzu D-Max": {"Стандарт": "IDM.st.JPG", "Про": "IDM.st.JPG"},
            "Jeep Gladiator": {"Стандарт": "JG.o.JPG", "Про": "JG.o.JPG"},
            "JMC Vigus / Baodian": {"Стандарт": "JMC.vig.heic", "Про": "JMC.vig.heic"},
            "Mitsubishi L200": {"Стандарт": "ML200.st.JPG", "Про": "ML200.st.JPG"},
            "Nissan Navara (NP300)": {"Стандарт": "NN.st.heic", "Про": "NN.pro.HEIC"},
            "Nissan Titan / Titan XD": {"Стандарт": "NT.pro.JPG", "Про": "NT.pro.JPG"},
            "Sollers ST8": {"Стандарт": "ST6.JPG", "Про": "ST6.JPG"},
            "SsangYong Actyon Sports": {"Стандарт": "SY.JPG", "Про": "SY.JPG"},
            "TLC79": {"Стандарт": "TLS.st.PNG", "Про": "TLS.pro.JPG"},
            "Toyota Hilux": {"Стандарт": "TH.st.jpeg", "Про": "TH.pro.jpg"},
            "Toyota Tacoma": {"Стандарт": "TT..JPG", "Про": "TT..JPG"},
            "Toyota Tundra": {"Стандарт": "TTU.st.jpeg", "Про": "TTU.pro.JPG"},
            "UAZ Pickup": {"Стандарт": "UAZ.PNG", "Про": "UAZ.PNG"},
            "Volkswagen Amarok": {"Стандарт": "VW.JPG", "Про": "VW.JPG"}
        }

        if pickup in filename_map and text in filename_map[pickup]:
            file_name = filename_map[pickup][text]
            file_path = os.path.join(PHOTO_PATH, file_name)
            if os.path.exists(file_path):
                with open(file_path, "rb") as photo:
                    if file_name.endswith(".mov"):
                        await update.message.reply_document(photo)
                    else:
                        await update.message.reply_photo(photo)

        if text == "Стандарт":
            await update.message.reply_text(
                "🔹 Кунг “Стандарт” — базовая, но прочная надстройка, идеально подходящая для ежедневной работы и перевозки.\n"
                "📦 Выполнен из алюминиевого каркаса , защищает груз от осадков и постороннего доступа.\n"
                "⚙️ Устанавливается без доработки кузова.\n"
                "🛠 Внутри — чистое пространство, которое можно доработать под задачу: полки, ящики, освещение, утепление.\n"
                "✅ Отличный выбор, если нужен практичный и бюджетный вариант."
            )
        elif text == "Про":
            await update.message.reply_text(
                "🔹 Кунг “Про” — это версия, созданная для тех, кто требует больше: больше прочности, больше функциональности, больше стиля.\n"
                "🛡 Изготовлен из алюминиевого каркаса, выдерживает тяжёлую эксплуатацию в любое время года.\n"
                "⚙️ Возможна установка: освещения, розеток, автономного отопления, крепежей, полок и других модулей.\n"
                "💼 Отличный выбор для коммерческого использования, экспедиций, охоты или путешествий."
            )
        elif text == "По индивидуальному заказу":
            await update.message.reply_text(
                "🎯 Кунг по индивидуальному заказу — это история, которую мы создаём вместе с вами.\n"
                "🔧 Хотите кунг под экспедиции, выставки, охоту, стройку или просто с душой — мы воплотим всё, что вы задумали.\n"
                "🛠 Проекты под ключ: с окнами, освещением, отоплением, отделкой и любыми модулями.\n"
                "💬 Напишите, как с вами связаться — мы перезвоним в течение часа и вместе создадим ваш идеальный кунг."
            )

        await update.message.reply_text("✍️ Напишите, как с вами связаться, и мы ответим в течение 1 часа:")
        user_states[user_id] = "awaiting_final_contact"
        return

    if state == "awaiting_final_contact":
        contact_info = update.message.text
        summary = user_data.get(user_id, {})
        pickup = summary.get("пикап", "[не указано]")
        kung_type = summary.get("кунговый_тип", text)
        await update.message.reply_text("Спасибо! Мы свяжемся с вами в течение часа. ☎️")
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Новая заявка:\nПикап: {pickup}\nКунг: {kung_type}\nКонтакт: {contact_info}"
        )
        user_states.pop(user_id)
        user_data.pop(user_id, None)
        return

    if state == "awaiting_contact_info":
        contact_info = update.message.text
        await update.message.reply_text("Спасибо, мы скоро свяжемся с вами! 📞")
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Новая заявка:\n{contact_info}"
        )
        user_states.pop(user_id)
        user_data.pop(user_id, None)
        return

    await update.message.reply_text(f"Вы выбрали: {text}. Спасибо! 🛠")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_pickup_choice))

print("Бот запущен...")
app.run_polling()

