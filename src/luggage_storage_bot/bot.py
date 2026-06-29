import os

from telegram.ext import Updater

from luggage_storage_bot.promotec import get_lockers_amount, get_lockers_state

TOKEN = os.getenv("TOKEN")
MAX_ID = os.getenv("MAX_ID")
ANNA_ID = os.getenv("ANNA_ID")

last_lockers_state: dict[int, bool] = {}
last_lockers_amount = None


def check_lockers_state(bot, job):
    global last_lockers_state
    current_lockers_state = get_lockers_state()
    if len(current_lockers_state) == 20 and current_lockers_state != last_lockers_state:
        current_used_lockers = [
            num
            for num, is_available in current_lockers_state.items()
            if not is_available
        ]
        current_unused_lockers = [
            num for num, is_available in current_lockers_state.items() if is_available
        ]

        locker_rows = sorted(
            current_lockers_state.items(),
            key=lambda item: (str(item[0]).isdigit(), str(item[0])),
        )
        locker_list = "\n".join(
            f"{locker_num} {'🟢' if is_available else '🔴'}"
            for locker_num, is_available in locker_rows
        )

        if last_lockers_state:
            delta_lockers = sum(not v for v in current_lockers_state.values()) - sum(
                not v for v in last_lockers_state.values()
            )
            locker_list += f"\nVariazione: {'📈' if delta_lockers > 0 else '📉' if delta_lockers < 0 else '➖'} {delta_lockers:+d}"

        message = (
            "Stato locker aggiornato\n"
            f"🔴 Usati: {len(current_used_lockers)} | 🟢 Liberi: {len(current_unused_lockers)}\n"
            f"{locker_list}"
        )
        bot.send_message(chat_id=ANNA_ID, text=message)
        bot.send_message(chat_id=MAX_ID, text=message)

        last_lockers_state = current_lockers_state


def check_lockers_amount(bot, job):
    global last_lockers_amount
    current_lockers_amount = get_lockers_amount()
    if current_lockers_amount and current_lockers_amount != last_lockers_amount:
        amount_line = f"💰 Totale incassi: {current_lockers_amount:.2f} €"

        if last_lockers_amount is not None:
            delta = current_lockers_amount - last_lockers_amount
            trend_emoji = "📈" if delta > 0 else "📉" if delta < 0 else "➖"
            trend_line = f"\n{trend_emoji} Variazione: {delta:.2f} €"
            amount_line += trend_line

        message = f"Incassi aggiornati\n{amount_line}"
        bot.send_message(chat_id=ANNA_ID, text=message)
        bot.send_message(chat_id=MAX_ID, text=message)

        last_lockers_amount = current_lockers_amount


def main():
    updater = Updater(TOKEN)

    job_queue = updater.job_queue
    job_queue.run_repeating(check_lockers_state, interval=60 * 5, first=0)
    job_queue.run_repeating(check_lockers_amount, interval=60 * 5, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
