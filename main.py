import re
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import get_current_date, calculator
# Загружаем переменные из файла .env
load_dotenv()

# Теперь ключ берется из системы, а не прописан в коде!
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools_map = {
    "get_current_date": get_current_date,
    "calculator": calculator
}

SYSTEM_PROMPT = """
Ты — агент ReAct. Твой цикл: Мысль, Действие, Наблюдение.
Инструменты:
- get_current_date(): текущая дата.
- calculator("выражение"): математика (sqrt, pow).

Формат:
Мысль: [твои рассуждения]
Действие: имя_инструмента("аргумент")
(Жди Наблюдение)

Финальный ответ: [ответ]
"""

def run_agent(user_query):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    print(f"--- Старт: {user_query} ---\n")

    for i in range(5):
        # Запрос к модели
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0
        )
        
        content = response.choices[0].message.content
        print(content)
        messages.append({"role": "assistant", "content": content})

        if "Финальный ответ:" in content:
            break

        # Поиск действия
        action_match = re.search(r"Действие:\s*(\w+)\((.*)\)", content)
        
        if action_match:
            tool_name = action_match.group(1).strip()
            # Убираем кавычки из аргументов, если они есть
            tool_arg = action_match.group(2).strip().replace('"', '').replace("'", "")

            if tool_name in tools_map:
                # Вызываем инструмент
                if tool_name == "get_current_date":
                    observation = tools_map[tool_name]()
                else:
                    observation = tools_map[tool_name](tool_arg)
                
                obs_str = f"Наблюдение: {observation}"
                print(f"🔍 {obs_str}\n")
                messages.append({"role": "user", "content": obs_str})

if __name__ == "__main__":
    query = "Сколько дней осталось до Нового года (2027) и каков квадратный корень из этого числа?"
    run_agent(query)