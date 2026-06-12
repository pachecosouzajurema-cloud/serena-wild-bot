import os
import logging
import random
import hmac
import hashlib
from datetime import datetime
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# =============================================
# CONFIGURAÇÕES
# =============================================
TOKEN = os.environ.get("TOKEN")
LINK_GRUPO = "https://t.me/+w_Tb4mgp9hQyN2Mx"
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")  # Chave secreta da Sharkbot (opcional)
PORT = int(os.environ.get("PORT", 8080))

# =============================================
# PERSONA: SERENA WILD
# =============================================
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

Para adquirir, entre em contato comigo diretamente. 😏"""

RESPOSTAS_COMPRAR = [
    "Ansioso? Isso é bom sinal. Me chama no privado para fechar. 🖤",
    "Paciente... eu gosto. Me chama no privado e a gente resolve. 😏",
]

lista_vip = []

logging.basicConfig(level=logging.INFO)

# =============================================
# HANDLERS DO BOT
# =============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id not in lista_vip:
        lista_vip.append(user_id)
    texto = random.choice(RESPOSTAS_INICIO)
    keyboard = [
        [InlineKeyboardButton("📂 Ver Catálogo", callback_data="catalogo")],
        [InlineKeyboardButton("💳 Quero comprar", callback_data="comprar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode="Markdown")


async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Quero comprar", callback_data="comprar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(RESPOSTAS_CATALOGO, reply_markup=reply_markup, parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "catalogo":
        keyboard = [[InlineKeyboardButton("💳 Quero comprar", callback_data="comprar")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(RESPOSTAS_CATALOGO, reply_markup=reply_markup, parse_mode="Markdown")
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
    palavras_compra = ["comprar", "quero", "preco", "valor", "quanto", "pagar", "link", "grupo"]
    if any(p in texto for p in palavras_compra):
        await update.message.reply_text(random.choice(RESPOSTAS_COMPRAR))
        return
    await update.message.reply_text(random.choice(RESPOSTAS_CONVERSA))


# =============================================
# WEBHOOK DA SHARKBOT
# =============================================

async def sharkbot_webhook(request):
    try:
        # Valida assinatura HMAC se a chave estiver configurada
        if WEBHOOK_SECRET:
            signature = request.headers.get("X-Signature", "")
            body = await request.read()
            expected = hmac.new(
                WEBHOOK_SECRET.encode(),
                body,
                hashlib.sha256
            ).hexdigest()
            if not hmac.compare_digest(signature, expected):
                return web.Response(status=401, text="Assinatura inválida")
            data = __import__("json").loads(body)
        else:
            data = await request.json()

        event = data.get("event")
        logging.info(f"Webhook recebido: {event}")

        # Pagamento aprovado
        if event == "payment_approved":
            customer = data.get("customer", {})
            telegram_id = customer.get("telegram_id")
            first_name = customer.get("first_name", "")

            if telegram_id:
                mensagem = (
                    f"✅ Pagamento confirmado! Obrigada, {first_name}! 🖤\n\n"
                    f"Aqui está o link exclusivo do meu grupo:\n"
                    f"👇👇👇\n"
                    f"{LINK_GRUPO}\n\n"
                    f"Seja bem-vindo. Eu estava te esperando. 😏"
                )
                bot = request.app["bot"]
                await bot.send_message(chat_id=telegram_id, text=mensagem)
                logging.info(f"Link enviado para {telegram_id}")

        return web.Response(status=200, text="OK")

    except Exception as e:
        logging.error(f"Erro no webhook: {e}")
        return web.Response(status=500, text="Erro interno")


# =============================================
# MAIN
# =============================================

def main():
    app_telegram = Application.builder().token(TOKEN).build()

    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("catalogo", catalogo))
    app_telegram.add_handler(CallbackQueryHandler(button_callback))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # Servidor web para receber webhooks da Sharkbot
    web_app = web.Application()
    web_app["bot"] = app_telegram.bot
    web_app.router.add_post("/webhook", sharkbot_webhook)

    async def run_both():
        await app_telegram.initialize()
        await app_telegram.start()
        await app_telegram.updater.start_polling()

        runner = web.AppRunner(web_app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()

        print(f"🖤 Serena Wild está online! Webhook em 0.0.0.0:{PORT}/webhook")

        await app_telegram.updater.idle()
        await app_telegram.stop()
        await runner.cleanup()

    import asyncio
    asyncio.run(run_both())


if __name__ == "__main__":
    main()
