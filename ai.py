from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import db
from ai import ask_ai, summarize_text
from pdf_ai import read_pdf
import os

# 🔑 من Environment Variables (Render / Railway)
TOKEN = os.environ.get("TOKEN")

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    db.add_user(user_id)

    await update.message.reply_text(
        "🎓 أهلاً بك في Study Bot الحقيقي\n\n"
        "/ai + السؤال → ذكاء اصطناعي\n"
        "/materials → المواد\n"
        "/points → نقاطك\n"
        "📎 أرسل PDF ليتم تلخيصه"
    )

# ================= AI COMMAND =================
async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب السؤال بعد /ai")
        return

    question = " ".join(context.args)

    await update.message.reply_text("🤖 جاري التفكير...")

    answer = ask_ai(question)

    await update.message.reply_text(f"📘 الإجابة:\n\n{answer}")

# ================= POINTS =================
async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    p = db.get_points(user_id)

    await update.message.reply_text(f"🏆 نقاطك: {p}")

# ================= MATERIALS =================
async def materials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = db.get_materials()

    if not data:
        await update.message.reply_text("لا توجد مواد")
        return

    msg = "📚 المواد:\n\n"
    for t, c in data:
        msg += f"📌 {t}\n{c}\n\n"

    await update.message.reply_text(msg)

# ================= PDF HANDLER =================
async def handle_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    file_obj = await file.get_file()

    path = f"files/{file.file_name}"
    await file_obj.download_to_drive(path)

    await update.message.reply_text("📥 تم استلام الملف... جاري التحليل")

    text = read_pdf(path)
    summary = summarize_text(text)

    await update.message.reply_text(f"📘 ملخص الملف:\n\n{summary}")

# ================= MAIN =================
def main():
    db.init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ai", ai))
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CommandHandler("materials", materials))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_doc))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
