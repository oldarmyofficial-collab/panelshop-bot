from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8894345960:AAE6iepstgfDnhMQlLKe-_L5y-aMXD84BoA"
ADMIN_USERNAME = "nageshsahoo01"

# Product List
PRODUCTS = {
    "1h": {"name": "1 Hour Key", "price": "33.00"},
    "1d": {"name": "1 Day Key", "price": "432.00"},
}

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"🏢 — BALA MOD PRO SHOP — 🏢\n\n"
        f"👋 Welcome, {user.first_name}!\n\n"
        f"⭐ — SHOP FEATURES — ⭐\n"
        f"├ 🔑 Premium Bala Keys\n"
        f"├ ⚡ Instant Delivery 24/7\n"
        f"├ 🔒 100% Secure Payment\n"
        f"└ 🏆 Professional Support\n\n"
        f"🚀 Click Shop Now to Start!"
    )
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop Now", callback_data="shop")],
        [InlineKeyboardButton("📦 My Orders", callback_data="orders"), InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("💰 Add Balance", callback_data="add_balance"), InlineKeyboardButton("🎁 Referral", callback_data="referral")],
        [InlineKeyboardButton("📺 Tutorials", callback_data="tutorials"), InlineKeyboardButton("💬 Support", callback_data="support")]
    ]
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "shop":
        keyboard = [[InlineKeyboardButton(f"🛒 {v['name']} - ₹{v['price']}", callback_data=f"buy_{k}")] for k, v in PRODUCTS.items()]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="main")])
        await query.edit_message_text("📦 **Select a product below:**", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "profile":
        text = f"👤 — YOUR PROFILE — 👤\n\n🆔 User ID: `{query.from_user.id}`\n📛 Name: {query.from_user.first_name}\n💰 Balance: ₹0.00"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "add_balance":
        text = "💰 **ADD BALANCE**\n\nUPI: `nageshsahoo01@upi`\nScreenshot admin ko bhejen."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "support":
        text = "🎫 — SUPPORT CENTER — 🎫\n\nNeed help? Contact Admin directly!"
        keyboard = [[InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")], [InlineKeyboardButton("🔙 Back", callback_data="main")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "main":
        await main_menu(update, context)

    elif data.startswith("buy_"):
        await query.edit_message_text("✅ Payment request received. Admin will verify shortly.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", main_menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()

