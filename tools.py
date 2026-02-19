import datetime
import math

def get_current_date():
    # Мы используем 19 февраля 2026 года, как в системном времени
    now = datetime.date(2026, 2, 19)
    return f"Сегодня {now.strftime('%d %B %Y')}, четверг."

def calculator(expression):
    try:
        # Разрешаем только безопасные математические операции
        allowed_names = {"sqrt": math.sqrt, "pow": math.pow, "abs": abs}
        # Очищаем строку от лишних символов
        expression = expression.strip("'\"")
        return eval(expression, {"__builtins__": None}, allowed_names)
    except Exception as e:
        return f"Ошибка расчетов: {e}"
        