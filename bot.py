from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)
import os

NAME, NATIONAL_ID, BIRTHDATE, PHONE = range(4)
CHANNEL_ID = os.getenv("CHANNEL_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً نام و نام خانوادگی خود را وارد کنید:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("کد ملی خود را وارد کنید:")
    return NATIONAL_ID

async def get_national_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["national_id"] = update.message.text
    await update.message.reply_text("تاریخ تولد خود را وارد کنید (مثلاً: 1380/01/12):")
    return BIRTHDATE

async def get_birthdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["birthdate"] = update.message.text
    await update.message.reply_text("شماره موبایل خود را وارد کنید:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    user_data = context.user_data

    msg = (
        f"📥 ثبت‌نام جدید:\n\n"
        f"👤 نام: {user_data['name']}\n"
        f"🆔 کد ملی: {user_data['national_id']}\n"
        f"🎂 تولد: {user_data['birthdate']}\n"
        f"📞 موبایل: {user_data['phone']}"
    )

    await update.message.reply_text("✅ مشخصات شما دریافت شد. تیم پشتیبانی با شما تماس خواهند گرفت.")
    await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⛔️ ثبت‌نام لغو شد.")
    return ConversationHandler.END

def main():
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            NATIONAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_national_id)],
            BIRTHDATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birthdate)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
