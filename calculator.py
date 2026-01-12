# calculator_pro.py - Продвинутый калькулятор
import os
import json
from datetime import datetime
import sys

# ============================================
# КОНСТАНТЫ И НАСТРОЙКИ
# ============================================
HISTORY_FILE = "calculator_history.json"
VERSION = "2.0"
AUTHOR = "Кристина"  # Замени на своё имя

# Цвета для терминала (ANSI коды)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ============================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ИСТОРИЕЙ
# ============================================
def load_history():
    """Загружаем историю из файла"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняем историю в файл"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(operation, result):
    """Добавляем запись в историю"""
    history = load_history()
    
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": operation,
        "result": result
    }
    
    history.append(record)
    
    # Храним только последние 50 записей
    if len(history) > 50:
        history = history[-50:]
    
    save_history(history)
    return record

def show_history():
    """Показываем историю вычислений"""
    history = load_history()
    
    if not history:
        print(f"\n{Colors.YELLOW}📭 История пуста{Colors.END}")
        return
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}📜 ИСТОРИЯ ВЫЧИСЛЕНИЙ ({len(history)} записей):{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    for i, record in enumerate(reversed(history[-10:]), 1):  # Показываем последние 10
        print(f"{Colors.YELLOW}{i}.{Colors.END} [{record['timestamp']}]")
        print(f"   {record['operation']}")
        print(f"   {Colors.GREEN}Результат: {record['result']}{Colors.END}")
        print(f"{Colors.CYAN}{'-'*40}{Colors.END}")

# ============================================
# МАТЕМАТИЧЕСКИЕ ФУНКЦИИ
# ============================================
def calculate(choice, num1, num2):
    """Выполняет математическую операцию"""
    operations = {
        '1': ('+', lambda a, b: a + b),
        '2': ('-', lambda a, b: a - b),
        '3': ('*', lambda a, b: a * b),
        '4': ('/', lambda a, b: a / b if b != 0 else "Ошибка: деление на ноль"),
        '5': ('**', lambda a, b: a ** b),  # Возведение в степень
        '6': ('%', lambda a, b: a % b),    # Остаток от деления
        '7': ('//', lambda a, b: a // b if b != 0 else "Ошибка: деление на ноль")  # Целочисленное деление
    }
    
    if choice not in operations:
        return None, "Неизвестная операция"
    
    operation_symbol, func = operations[choice]
    
    try:
        result = func(num1, num2)
        if "Ошибка" in str(result):
            return operation_symbol, result
        return operation_symbol, result
    except Exception as e:
        return operation_symbol, f"Ошибка: {str(e)}"

# ============================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================
def clear_screen():
    """Очищает экран терминала"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Печатает красивый заголовок"""
    clear_screen()
    print(f"\n{Colors.PURPLE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}🎯 ПРОДВИНУТЫЙ КАЛЬКУЛЯТОР v{VERSION}{Colors.END}")
    print(f"{Colors.BLUE}👩‍💻 Автор: {AUTHOR}{Colors.END}")
    print(f"{Colors.PURPLE}{'='*60}{Colors.END}")

def print_menu():
    """Печатает меню операций"""
    print(f"\n{Colors.BOLD}📋 ВЫБЕРИ ОПЕРАЦИЮ:{Colors.END}")
    print(f"{Colors.CYAN}1.{Colors.END} Сложение (+)")
    print(f"{Colors.CYAN}2.{Colors.END} Вычитание (-)")
    print(f"{Colors.CYAN}3.{Colors.END} Умножение (*)")
    print(f"{Colors.CYAN}4.{Colors.END} Деление (/)")
    print(f"{Colors.CYAN}5.{Colors.END} Возведение в степень (**)")
    print(f"{Colors.CYAN}6.{Colors.END} Остаток от деления (%)")
    print(f"{Colors.CYAN}7.{Colors.END} Целочисленное деление (//)")
    print(f"{Colors.YELLOW}8.{Colors.END} 📜 Показать историю")
    print(f"{Colors.YELLOW}9.{Colors.END} 🗑️  Очистить историю")
    print(f"{Colors.RED}0.{Colors.END} 🚪 Выход")
    print(f"{Colors.PURPLE}{'-'*40}{Colors.END}")

def get_number(prompt):
    """Получает число от пользователя с проверкой"""
    while True:
        try:
            value = input(f"{Colors.BLUE}{prompt}{Colors.END}")
            # Позволяем вводить простые выражения типа "2*3" или "5+10"
            if any(op in value for op in '+-*/'):
                return eval(value)
            return float(value)
        except ValueError:
            print(f"{Colors.RED}❌ Ошибка! Введи число.{Colors.END}")
        except:
            print(f"{Colors.RED}❌ Ошибка в выражении!{Colors.END}")

# ============================================
# ОСНОВНАЯ ПРОГРАММА
# ============================================
def main():
    """Главная функция программы"""
    print_header()
    
    # Загрузка истории при старте
    history_count = len(load_history())
    print(f"{Colors.GREEN}📊 Загружено записей в истории: {history_count}{Colors.END}")
    
    name = input(f"\n{Colors.YELLOW}👋 Как тебя зовут? {Colors.END}")
    
    while True:
        print_menu()
        
        choice = input(f"\n{Colors.BOLD}🎯 {name}, выбери операцию (0-9): {Colors.END}").strip()
        
        # Выход из программы
        if choice == '0':
            print(f"\n{Colors.GREEN}👋 Пока, {name}! Хорошего дня!{Colors.END}")
            print(f"{Colors.PURPLE}{'='*60}{Colors.END}")
            break
        
        # Показать историю
        elif choice == '8':
            show_history()
            input(f"\n{Colors.CYAN}Нажми Enter чтобы продолжить...{Colors.END}")
            print_header()
            continue
        
        # Очистить историю
        elif choice == '9':
            confirm = input(f"{Colors.RED}⚠️  Ты уверена? Это удалит всю историю! (да/нет): {Colors.END}")
            if confirm.lower() in ['да', 'yes', 'y', 'д']:
                save_history([])
                print(f"{Colors.GREEN}✅ История очищена!{Colors.END}")
                input(f"\n{Colors.CYAN}Нажми Enter чтобы продолжить...{Colors.END}")
                print_header()
            continue
        
        # Проверка валидности выбора
        if choice not in ['1', '2', '3', '4', '5', '6', '7']:
            print(f"{Colors.RED}❌ Ошибка! Выбери число от 0 до 9{Colors.END}")
            continue
        
        # Ввод чисел
        print()
        num1 = get_number("Введи первое число (можно выражение, например 2*3): ")
        num2 = get_number("Введи второе число: ")
        
        # Вычисление
        operation_symbol, result = calculate(choice, num1, num2)
        
        # Вывод результата
        print(f"\n{Colors.GREEN}{'='*40}{Colors.END}")
        print(f"{Colors.BOLD}🧮 РЕЗУЛЬТАТ:{Colors.END}")
        print(f"{Colors.CYAN}{num1} {operation_symbol} {num2} = {result}{Colors.END}")
        print(f"{Colors.GREEN}{'='*40}{Colors.END}")
        
        # Сохранение в историю (если не ошибка)
        if "Ошибка" not in str(result):
            operation_str = f"{num1} {operation_symbol} {num2}"
            record = add_to_history(operation_str, result)
            print(f"{Colors.YELLOW}💾 Сохранено в историю: [{record['timestamp']}]{Colors.END}")
        
        # Продолжить или выйти
        print(f"\n{Colors.PURPLE}{'-'*40}{Colors.END}")
        continue_choice = input(f"{Colors.YELLOW}➡️  Продолжить? (да/нет): {Colors.END}")
        
        if continue_choice.lower() in ['нет', 'no', 'n', 'н']:
            print(f"\n{Colors.GREEN}👋 Пока, {name}! Возвращайся ещё!{Colors.END}")
            print(f"{Colors.PURPLE}{'='*60}{Colors.END}")
            break
        
        print_header()

# ============================================
# ЗАПУСК ПРОГРАММЫ
# ============================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Программа прервана пользователем.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}💥 Критическая ошибка: {e}{Colors.END}")
        sys.exit(1)