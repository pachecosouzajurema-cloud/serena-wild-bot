import os
import logging
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

TOKEN = os.environ.get("TOKEN", "8799350801:AAEsmD30Awq1Iw-r3NJ3XjMQ_u8C5qdEdcw")

DIA_ENVIO = 1
HORA_ENVIO = 20
MINUTO_ENVIO = 0

NOME = "Serena Wild"

RESPOSTAS_INICIO = [
    "Hmm... então você finalmente apareceu. Eu sou Serena Wild, e aqui as regras são minhas. 😏\n\nUse /catalogo para ver o que está disponível.",
    "Olha quem chegou... 👁️ Eu sou Serena Wild. Não sou qualquer uma — sou exatamente o que você estava precisando.\n\nDigite /catalogo e me prove que merece.",
    "Você bateu na porta certa, mas aqui quem decide os próximos passos sou eu. 🖤\n\nUse /catalogo se tiver coragem.",
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

RESPOSTAS_CATALOGO = """🖤 *Catálogo da Serena Wild* 🖤

Aqui você encontra o que há de mais exclusivo.
Conteúdo premium, feito pra quem sabe o que quer.

📦 *Pacote Básico* — Primeiros passos
📦 *Pacote VIP* — Acesso especial
📦 *Pacote Black* — Tudo. Sem filtros.

Quando meu link de pagamento estiver disponível, você será o primeiro a saber. 😏

Digite /avisar para entrar na lista VIP de notificações."""

RESPOSTAS_COMPRAR = [
    "Paciente... eu gosto. Em breve meu conteúdo estará disponível. Use /avisar para não perder. 🖤",
    "Ansioso? Isso é bom sinal. Use /avisar e eu te chamo pessoalmente quando abrir. 😏",
]

lista_vip = []

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id not in lista_vip:
        lista_vip.append(user_id)
    texto = random.choice(RESPOSTAS_INICIO)
    keyboard = [
        [InlineKeyboardButton("📂 Ver Catálogo", callback_data="catalogo")],
        [InlineKeyboardButton("🔔 Me avise quando abrir", callback_data="avisar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode="Markdown")


async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Quero comprar", callback_data="comprar")],
        [InlineKeyboardButton("🔔 Me avise quando abrir", callback_data="avisar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(RESPOSTAS_CATALOGO, reply_markup=reply_markup, parse_mode="Markdown")


async def avisar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id not in lista_vip:
        lista_vip.append(user_id)
        await update.message.reply_text(
            "✅ Perfeito. Você está na minha lista VIP.\nQuando eu abrir, você será um dos primeiros a saber. 🖤\n\nNão me decepcione quando chegar a hora. 😏"
        )
    else:
        await update.message.reply_text("Você já está na minha lista, amor. Seja paciente. 😏")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "catalogo":
        keyboard = [
            [InlineKeyboardButton("💳 Quero comprar", callback_data="comprar")],
            [InlineKeyboardButton("🔔 Me avise quando abrir", callback_data="avisar")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(RESPOSTAS_CATALOGO, reply_markup=reply_markup, parse_mode="Markdown")
    elif query.data == "avisar":
        user_id = query.message.chat_id
        if user_id not in lista_vip:
            lista_vip.append(user_id)
        await query.message.reply_text(
            "✅ Anotado. Você está na lista VIP da Serena Wild.\nFique de olho no seu Telegram. 🖤"
        )
    elif query.data == "comprar":
        await query.message.reply_text(random.choice(RESPOSTAS_COMPRAR))


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id not in lista_vip:
        lista_vip.append(user_id)
    texto = update.message.text.lower()
    palavras_elogio = ["linda", "gostosa", "perfeita", "incrivel", "maravilhosa", "top", "boa"]
    if any(p in texto for p in palavras_elogio):
        await update.message.reply_text(random.choice(RESPOSTAS_ELOGIO))
        return
    palavras_compra = ["comprar", "quero", "preco", "valor", "quanto", "pagar", "link"]
    if any(p in texto for p in palavras_compra):
        await update.message.reply_text(random.choice(RESPOSTAS_COMPRAR))
        return
    await update.message.reply_text(random.choice(RESPOSTAS_CONVERSA))


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalogo", catalogo))
    app.add_handler(CommandHandler("avisar", avisar))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("🖤 Serena Wild está online...")
    app.run_polling(stop_signals=None)


if __name__ == "__main__":
    main()
