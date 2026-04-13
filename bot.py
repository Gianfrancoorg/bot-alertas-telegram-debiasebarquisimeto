import os
import asyncio
import calendar
from datetime import datetime, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

TOKEN   = "8734954604:AAGgd6mfgpHWrJCglHTt9apO1diHIkGEk6w"
CHAT_ID = "-5138910545"

bot = Bot(token=TOKEN)

MESES = [
    "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

def es_ultimo_dia_del_mes() -> bool:
    hoy = date.today()
    ultimo = calendar.monthrange(hoy.year, hoy.month)[1]
    return hoy.day == ultimo

def es_primer_dia_del_mes() -> bool:
    return date.today().day == 1

async def verificar_y_enviar():
    hoy = date.today()
    mes_actual   = MESES[hoy.month]
    mes_anterior = MESES[hoy.month - 1] if hoy.month > 1 else MESES[12]

    if es_ultimo_dia_del_mes():
        mensaje = (
            f"⚠️ *¡Último día de {mes_actual}!*\n\n"
            f"📋 Por favor, enviar la información del mes de *{mes_actual}* "
            f"antes de que termine el día.\n\n"
            f"_Gracias a todos_ 🙏"
        )
        await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
        print(f"[{datetime.now()}] ✅ Alerta de fin de mes enviada.")

    elif es_primer_dia_del_mes():
        mensaje = (
            f"📅 *¡Inicio de {mes_actual}!*\n\n"
            f"📋 Recuerden enviar la información pendiente del mes de "
            f"*{mes_anterior}* si aún no lo han hecho.\n\n"
            f"_Gracias a todos_ 🙏"
        )
        await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
        print(f"[{datetime.now()}] ✅ Alerta de inicio de mes enviada.")

    else:
        print(f"[{datetime.now()}] ℹ️ Hoy no es día de alerta.")

async def main():
    print("🤖 Bot iniciado. Esperando horario de alertas...")
    scheduler = AsyncIOScheduler(timezone="America/Caracas")
    scheduler.add_job(verificar_y_enviar, "cron", hour=8, minute=0)
    scheduler.start()
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
