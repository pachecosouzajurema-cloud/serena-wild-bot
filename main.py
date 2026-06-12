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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# =============================================
# CONFIGURAÇÕES
# =============================================
TOKEN = os.environ.get("TOKEN")
GRUPO_ID = -1003860216725
PORT = int(os.environ.get("PORT", 8080))
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
    assinantes[str(telegram_id)] = {"plano": plano, "expiracao": expiracao}
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
    "Hmm... então você finalmente apareceu. Eu sou Serena Wild, e aqui as regras são minhas. 😏\n\nUse /planos para ver o que está disponível.",
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
# HANDLERS
# =============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = random.choice(RESPOSTAS_INICIO)
    keyboard = [[InlineKeyboardButton("💎 Ver Planos VIP", callback_data="planos")]]
    await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def planos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Semanal — R$ 10,90", callback_data="semanal")],
        [InlineKeyboardButton("📆 Mensal — R$ 19,90 ⭐", callback_data="mensal")],
        [InlineKeyboardButton("🗓️ Anual — R$ 79,90 💎", callback_data="anual")],
    ]
    await update.message.reply_text(MENSAGEM_PLANOS, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "planos":
        keyboard = [
            [InlineKeyboardButton("📅 Semanal — R$ 10,90", callback_data="semanal")],
            [InlineKeyboardButton("📆 Mensal — R$ 19,90 ⭐", callback_data="mensal")],
            [InlineKeyboardButton("🗓️ Anual — R$ 79,90 💎", callback_data="anual")],
        ]
        await query.message.reply_text(MENSAGEM_PLANOS, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif query.data == "semanal":
        await query.message.reply_text("📅 *VIP Semanal — R$ 10,90*\n\nAcesso por 7 dias ao meu grupo exclusivo. 🔥\n\nBoa escolha para começar... mas aviso: você vai querer mais. 😏\n\nFinalize seu pagamento pelo link abaixo:", parse_mode="Markdown")
    elif query.data == "mensal":
        await query.message.reply_text("📆 *VIP Mensal — R$ 19,90*\n\nAcesso por 30 dias ao meu grupo exclusivo. ⭐\n\nEsse é o favorito dos meus VIPs. Você tem bom gosto. 🖤\n\nFinalize seu pagamento pelo link abaixo:", parse_mode="Markdown")
    elif query.data == "anual":
        await query.message.reply_text("🗓️ *VIP Anual — R$ 79,90*\n\nAcesso por 365 dias ao meu grupo exclusivo. 💎\n\nVocê sabe o que quer e não brinca em serviço. Eu gosto. 😏🔥\n\nFinalize seu pagamento pelo link abaixo:", parse_mode="Markdown")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    palavras_elogio = ["linda", "gostosa", "perfeita", "incrivel", "maravilhosa", "top", "boa", "bonita", "sexy"]
    if any(p in texto for p in palavras_elogio):
        await update.message.reply_text(random.choice(RESPOSTAS_ELOGIO))
        return
    palavras_compra = ["comprar", "quero", "preco", "valor", "quanto", "pagar", "link", "grupo", "vip", "plano", "assinar"]
    if any(p in texto for p in palavras_compra):
        keyboard = [[InlineKeyboardButton("💎 Ver Planos VIP", callback_data="planos")]]
        await update.message.reply_text(random.choice(RESPOSTAS_INDUZIR), reply_markup=InlineKeyboardMarkup(keyboard))
        return
    await update.message.reply_text(random.choice(RESPOSTAS_CONVERSA))

# =============================================
# VERIFICAÇÃO DE ASSINATURAS
# =============================================

async def verificar_assinaturas(bot):
    assinantes = carregar_assinantes()
    agora = datetime.now()
    para_remover = []
    for telegram_id, dados in assinantes.items():
        expiracao = datetime.fromisoformat(dados["expiracao"])
        dias_restantes = (expiracao - agora).days
        if dias_restantes == 1:
            try:
                await bot.send_message(chat_id=int(telegram_id), text="⚠️ Sua assinatura VIP expira amanhã!\n\nRenove agora para não perder o acesso. 🖤\n\nUse /planos para renovar.")
            except Exception as e:
                logging.error(f"Erro ao avisar {telegram_id}: {e}")
        if agora >= expiracao:
            try:
                await bot.ban_chat_member(chat_id=GRUPO_ID, user_id=int(telegram_id))
                await bot.unban_chat_member(chat_id=GRUPO_ID, user_id=int(telegram_id))
                await bot.send_message(chat_id=int(telegram_id), text="😔 Sua assinatura VIP expirou e você foi removido do grupo.\n\nMas a porta continua aberta... 🖤\n\nUse /planos para renovar e voltar.")
                para_remover.append(telegram_id)
            except Exception as e:
                logging.error(f"Erro ao remover {telegram_id}: {e}")
    for telegram_id in para_remover:
        remover_assinante(telegram_id)

# =============================================
# WEBHOOK DA SHARKBOT
# =============================================

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
            if "semanal" in plan_name or "semana" in plan_name:
                dias, plano = 7, "Semanal"
            elif "anual" in plan_name or "ano" in plan_name:
                dias, plano = 365, "Anual"
            else:
                dias, plano = 30, "Mensal"
            if telegram_id:
                bot = request.app["bot"]
                try:
                    await bot.unban_chat_member(chat_id=GRUPO_ID, user_id=int(telegram_id))
                    link = await bot.create_chat_invite_link(chat_id=GRUPO_ID, member_limit=1, expire_date=datetime.now() + timedelta(minutes=10))
                    adicionar_assinante(telegram_id, plano, dias)
                    await bot.send_message(
                        chat_id=int(telegram_id),
                        text=f"✅ Pagamento confirmado! Bem-vindo ao VIP, {first_name}! 🖤\n\nPlano: *{plano}*\n\nClique no link abaixo para entrar no grupo exclusivo:\n👇👇👇\n{link.invite_link}\n\n_O link expira em 10 minutos. Use logo!_ 😏",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logging.error(f"Erro ao adicionar {telegram_id}: {e}")
        return web.Response(status=200, text="OK")
    except Exception as e:
        logging.error(f"Erro no webhook: {e}")
        return web.Response(status=500, text="Erro interno")

# =============================================
# MAIN
# =============================================

async def main():
    app_telegram = Application.builder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("planos", planos))
    app_telegram.add_handler(CallbackQueryHandler(button_callback))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # Scheduler separado
    scheduler = AsyncIOScheduler()
    scheduler.add_job(verificar_assinaturas, "interval", hours=1, args=[app_telegram.bot])
    scheduler.start()

    # Servidor web para webhook
    web_app = web.Application()
    web_app["bot"] = app_telegram.bot
    web_app.router.add_post("/webhook", sharkbot_webhook)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    # Inicia o bot com polling
    await app_telegram.initialize()
    await app_telegram.start()
    await app_telegram.updater.start_polling(drop_pending_updates=True)

    print(f"🖤 Serena Wild está online! Webhook em 0.0.0.0:{PORT}/webhook")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
