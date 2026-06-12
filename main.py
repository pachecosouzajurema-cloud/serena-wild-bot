import os
import logging
import random
import json
from datetime import datetime, timedelta
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
GRUPO_ID = -1003860216725
PORT = int(os.environ.get("PORT", 8080))

# Arquivo para salvar assinantes
ASSINANTES_FILE = "assinantes.json"

# =============================================
# GERENCIAMENTO DE ASSINANTES
# =============================================

def carregar_assinantes():
    try:
        with open(ASSINANTES_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def salvar_assinantes(assinantes):
    with open(ASSINANTES_FILE, "w") as f:
        json.dump(assinantes, f)

def adicionar_assinante(telegram_id, plano, dias):
    assinantes = carregar_assinantes()
    expiracao = (datetime.now() + timedelta(days=dias)).isoformat()
    assinantes[str(telegram_id)] = {
        "plano": plano,
        "expiracao": expiracao
    }
    salvar_assinantes(assinantes)

def remover_assinante(telegram_id):
    assinantes = carregar_assinantes()
    if str(telegram_id) in assinantes:
        del assinantes[str(telegram_id)]
        salvar_assinantes(assinantes)

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

logging.basicConfig(level=logging.INFO)


# =============================================
# HANDLERS DO BOT
# =============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = random.choice(RESPOSTAS_INICIO)
    keyboard = [[InlineKeyboardButton("💎 Ver Planos VIP", callback_data="planos")]]
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
    texto = update.message.text.lower()
    palavras_elogio = ["linda", "gostosa", "perfeita", "incrivel", "maravilhosa", "top", "boa", "bonita", "sexy"]
    if any(p in texto for p in palavras_elogio):
        await update.message.reply_text(random.choice(RESPOSTAS_ELOGIO))
        return
    palavras_compra = ["comprar", "quero", "preco", "valor", "quanto", "pagar", "link", "grupo", "vip", "plano", "assinar"]
    if any(p in texto for p in palavras_compra):
        keyboard = [[InlineKeyboardButton("💎 Ver Planos VIP", callback_data="planos")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(random.choice(RESPOSTAS_INDUZIR), reply_markup=reply_markup)
        return
    await update.message.reply_text(random.choice(RESPOSTAS_CONVERSA))


# =============================================
# VERIFICAÇÃO DIÁRIA DE ASSINATURAS
# =============================================

async def verificar_assinaturas(context: ContextTypes.DEFAULT_TYPE):
    assinantes = carregar_assinantes()
    agora = datetime.now()
    para_remover = []

    for telegram_id, dados in assinantes.items():
        expiracao = datetime.fromisoformat(dados["expiracao"])
        dias_restantes = (expiracao - agora).days

        # Avisa 1 dia antes de expirar
        if dias_restantes == 1:
            try:
                await context.bot.send_message(
                    chat_id=int(telegram_id),
                    text="⚠️ Sua assinatura VIP expira amanhã!\n\nRenove agora para não perder o acesso. 🖤\n\nUse /planos para renovar."
                )
            except Exception as e:
                logging.error(f"Erro ao avisar {telegram_id}: {e}")

        # Remove se expirou
        if agora >= expiracao:
            try:
                await context.bot.ban_chat_member(chat_id=GRUPO_ID, user_id=int(telegram_id))
                await context.bot.unban_chat_member(chat_id=GRUPO_ID, user_id=int(telegram_id))
                await context.bot.send_message(
                    chat_id=int(telegram_id),
                    text="😔 Sua assinatura VIP expirou e você foi removido do grupo.\n\nMas a porta continua aberta... 🖤\n\nUse /planos para renovar e voltar."
                )
                para_remover.append(telegram_id)
                logging.info(f"Removido do grupo: {telegram_id}")
            except Exception as e:
                logging.error(f"Erro ao remover {telegram_id}: {e}")

    for telegram_id in para_remover:
        remover_assinante(telegram_id)


# =============================================
# WEBHOOK DA SHARKBOT
# =============================================

PLANOS_DIAS = {
    "semanal": 7,
    "mensal": 30,
    "anual": 365,
}

async def sharkbot_webhook(request):
    try:
        data = await request.json()
        event = data.get("event")
        logging.info(f"Webhook recebido: {event}")

        if event == "payment_approved":
            customer = data.get("customer", {})
            telegram_id = customer.get("telegram_id")
            first_name = customer.get("first_name", "")
            transaction = data.get("transaction", {})
            plan_name = transaction.get("plan_name", "").lower()

            # Descobre quantos dias pelo plano
            dias = 30  # padrão mensal
            if "semanal" in plan_name or "semana" in plan_name:
                dias = 7
                plano = "Semanal"
            elif "anual" in plan_name or "ano" in plan_name:
                dias = 365
                plano = "Anual"
            else:
                plano = "Mensal"

            if telegram_id:
                bot = request.app["bot"]

                # Adiciona no grupo
                try:
                    await bot.unban_chat_member(chat_id=GRUPO_ID, user_id=int(telegram_id))
                    link = await bot.create_chat_invite_link(
                        chat_id=GRUPO_ID,
                        member_limit=1,
                        expire_date=datetime.now() + timedelta(minutes=10)
                    )
                    adicionar_assinante(telegram_id, plano, dias)

                    await bot.send_message(
                        chat_id=int(telegram_id),
                        text=f"✅ Pagamento confirmado! Bem-vindo ao VIP, {first_name}! 🖤\n\n"
                             f"Plano: *{plano}*\n\n"
                             f"Clique no link abaixo para entrar no grupo exclusivo:\n"
                             f"👇👇👇\n{link.invite_link}\n\n"
                             f"_O link expira em 10 minutos. Use logo!_ 😏",
                        parse_mode="Markdown"
                    )
                    logging.info(f"Usuário {telegram_id} adicionado ao grupo.")
                except Exception as e:
                    logging.error(f"Erro ao adicionar {telegram_id}: {e}")

        return web.Response(status=200, text="OK")

    except Exception as e:
        logging.error(f"Erro no webhook: {e}")
        return web.Response(status=500, text="Erro interno")


# =============================================
# MAIN
# =============================================

def main():
    import asyncio

    app_telegram = Application.builder().token(TOKEN).build()

    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("planos", planos))
    app_telegram.add_handler(CallbackQueryHandler(button_callback))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # Verificação diária de assinaturas
    job_queue = app_telegram.job_queue
    job_queue.run_repeating(verificar_assinaturas, interval=3600, first=10)

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

    asyncio.run(run_both())


if __name__ == "__main__":
    main()
