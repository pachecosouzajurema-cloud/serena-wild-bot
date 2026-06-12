import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# =============================================
# CONFIGURAÇÕES
# =============================================
TOKEN = os.environ.get("TOKEN")

# =============================================
# PERSONA: SERENA WILD
# =============================================
RESPOSTAS_INICIO = [
    "Hmm... então você finalmente apareceu. Eu sou Serena Wild, e aqui as regras são minhas. 😏\n\nSe quer ver o que eu tenho pra oferecer, use /planos para ver as opções.",
    "Olha quem chegou... 👁️ Eu sou Serena Wild. Não sou qualquer uma — sou exatamente o que você estava precisando.\n\nDigite /planos e me prove que merece.",
    "Você bateu na porta certa, mas aqui quem decide os próximos passos sou eu. 🖤\n\nUse /planos se tiver coragem.",
]

RESPOSTAS_CONVERSA = [
    "Interessante... mas vai ter que fazer melhor do que isso pra me impressionar. 😏",
    "Você acha que é tão fácil assim? Eu gosto de quem tem um pouco de... persistência. 🖤",
    "Hm. Você tem potencial. Mas ainda precisa me provar muita coisa.",
    "Não seja ansioso. As melhores coisas são para quem sabe esperar — e obedecer. 😈",
    "Você está me deixando curiosa. Continue assim.",
    "Cuidado com o que deseja... porque eu entrego de verdade. 🔥",
    "Eu gosto quando me desafiam. Mas no fim, eu sempre ganho. 😏",
    "Pensa bem antes de responder. Cada palavra sua me diz muito sobre você.",
]

RESPOSTAS_ELOGIO = [
    "Claro que sou. Você esperava menos? 😏",
    "Isso eu já sei, amor. A pergunta é: o que você vai fazer com isso? 🖤",
    "Hm... gosto quando percebem o óbvio. Continue assim.",
]

RESPOSTAS_INDUZIR = [
    "Você ainda não entrou no meu grupo VIP? 😏 Tá perdendo muito...\n\nUse /planos e veja o que te espera. 🔥",
    "Tem certeza que quer ficar de fora? Meus VIPs estão muito satisfeitos... 🖤\n\nDá uma olhada em /planos.",
    "Eu sei que você quer. Só falta dar o próximo passo. 😈\n\nUse /planos — você não vai se arrepender.",
    "Todo dia que passa é conteúdo novo que você está perdendo... 😏\n\nVeja /planos e entre agora.",
]

MENSAGEM_PLANOS = """🖤 *Planos VIP da Serena Wild* 🖤

Acesso exclusivo ao meu grupo com conteúdo sem censura. 🔥

━━━━━━━━━━━━━━━━
📅 *VIP Semanal* — R$ 10,90
Acesso por 7 dias

📆 *VIP Mensal* — R$ 19,90
Acesso por 30 dias ⭐ Mais popular

🗓️ *VIP Anual* — R$ 79,90
Acesso por 365 dias 💎 Melhor custo-benefício
━━━━━━━━━━━━━━━━

Escolha seu plano abaixo e entre agora. 😏"""

lista_usuarios = []

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id not in lista_usuarios:
        lista_usuarios.append(user_id)
    texto = random.choice(RESPOSTAS_INICIO)
    keyboard = [
        [InlineKeyboardButton("💎 Ver Planos VIP", callback_data="planos")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode="Markdown")


async def planos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Semanal — R$ 10,90", callback_data="semanal")],
        [InlineKeyboardButton("📆 Mensal — R$ 19,90 ⭐", callback_data="mensal")],
        [InlineKeyboardButton("🗓️ Anual — R$ 79,90 💎", callback_data="anual")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(MENSAGEM_PLANOS, reply_markup=reply_markup, parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "planos":
        keyboard = [
            [InlineKeyboardButton("📅 Semanal — R$ 10,90", callback_data="semanal")],
            [InlineKeyboardButton("📆 Mensal — R$ 19,90 ⭐", callback_data="mensal")],
            [InlineKeyboardButton("🗓️ Anual — R$ 79,90 💎", callback_data="anual")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(MENSAGEM_PLANOS, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "semanal":
        await query.message.reply_text(
            "📅 *VIP Semanal — R$ 10,90*\n\n"
            "Acesso por 7 dias ao meu grupo exclusivo. 🔥\n\n"
            "Boa escolha para começar... mas aviso: você vai querer mais. 😏\n\n"
            "Finalize seu pagamento pelo link abaixo:",
            parse_mode="Markdown"
        )

    elif query.data == "mensal":
        await query.message.reply_text(
            "📆 *VIP Mensal — R$ 19,90*\n\n"
            "Acesso por 30 dias ao meu grupo exclusivo. ⭐\n\n"
            "Esse é o favorito dos meus VIPs. Você tem bom gosto. 🖤\n\n"
            "Finalize seu pagamento pelo link abaixo:",
            parse_mode="Markdown"
        )

    elif query.data == "anual":
        await query.message.reply_text(
            "🗓️ *VIP Anual — R$ 79,90*\n\n"
            "Acesso por 365 dias ao meu grupo exclusivo. 💎\n\n"
            "Você sabe o que quer e não brinca em serviço. Eu gosto. 😏🔥\n\n"
            "Finalize seu pagamento pelo link abaixo:",
            parse_mode="Markdown"
        )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id not in lista_usuarios:
        lista_usuarios.append(user_id)

    texto = update.message.text.lower()

    palavras_elogio = ["linda", "gostosa", "perfeita", "incrivel", "maravilhosa", "top", "boa", "bonita", "sexy"]
    if any(p in texto for p in palavras_elogio):
        await update.message.reply_text(random.choice(RESPOSTAS_ELOGIO))
        return

    palavras_compra = ["comprar", "quero", "preco", "valor", "quanto", "pagar", "link", "grupo", "vip", "plano", "assinar"]
    if any(p in texto for p in palavras_compra):
        keyboard = [
            [InlineKeyboardButton("💎 Ver Planos VIP", callback_data="planos")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            random.choice(RESPOSTAS_INDUZIR),
            reply_markup=reply_markup
        )
        return

    await update.message.reply_text(random.choice(RESPOSTAS_CONVERSA))


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("planos", planos))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("🖤 Serena Wild está online...")
    app.run_polling(stop_signals=None)


if __name__ == "__main__":
    main()
