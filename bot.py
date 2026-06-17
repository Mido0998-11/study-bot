from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import db
from ai import ask_ai, summarize_text     # ✅ التعديل هنا: سحبنا دالة التلخيص من ملف ai.py الصح
from pdf_ai import read_pdf               # ✅ التعديل هنا: سحبنا دالة القراءة فقط من ملف pdf_ai.py
import os

TOKEN = "8375721826:AAGuPfFzyxTMxKrJ43R7uWKrMddDJjk_o78"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    db.add_user(user_id)

    await update.message.reply_text(
        "🎓 أهلاً بك في Study Bot الحقيقي\n\n"
        "/materials - عرض المواد\n"
        "/points - نقاطك\n"
        "/ai - اسأل الذكاء الاصطناعي\n"
        "📎 أرسل PDF ليتم تلخيصه"
    )

# ================= POINTS =================
async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    p = db.get_points(user_id)
    await update.message.reply_text(f"🏆 نقاطك: {p}")

# ================= AI =================
async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب السؤال بعد /ai")
        return

    question = " ".join(context.args)
    answer = ask_ai(question)

    await update.message.reply_text(f"🤖:\n{answer}")

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
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CommandHandler("ai", ai))
    app.add_handler(CommandHandler("materials", materials))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_doc))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
