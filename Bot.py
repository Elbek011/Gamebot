import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@playgameuzz"
CHANNEL_URL = "https://t.me/playgameuzz"
SITE_URL = "https://mygameuz.netlify.app"


async def is_member(bot, user_id: int) -> bool:
    try:
        m = await bot.get_chat_member(CHANNEL, user_id)
    except Exception:
        return False
    return m.status in ("member", "administrator", "creator") or (
        m.status == "restricted" and m.is_member
    )


def play_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎮 O‘yinlarni ochish", web_app=WebAppInfo(url=SITE_URL))]]
    )


def subscribe_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check")],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await is_member(context.bot, user.id):
        await update.message.reply_text("Xush kelibsiz! O‘yinni tanlang:", reply_markup=play_markup())
    else:
        await update.message.reply_text(
            "Botdan foydalanish uchun avval kanalimizga obuna bo‘ling, so‘ng «Tekshirish» tugmasini bosing.",
            reply_markup=subscribe_markup(),
        )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if await is_member(context.bot, q.from_user.id):
        await q.answer()
        await q.edit_message_text("Rahmat! O‘yinni tanlang:", reply_markup=play_markup())
    else:
        await q.answer("Siz hali obuna bo‘lmagansiz.", show_alert=True)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check, pattern="^check$"))
    app.run_polling()


if __name__ == "__main__":
    main()
