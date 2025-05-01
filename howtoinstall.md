🔧 1. Установка зависимостей
Перед запуском нужно установить Python и системные библиотеки.

1.1. Установи Python 3 и pip
bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
1.2. Установи системные зависимости (для lxml и других модулей)
bash
sudo apt install libxml2-dev libxslt1-dev
🚀 2. Настройка виртуального окружения
(Чтобы изолировать зависимости проекта от системы)

2.1. Клонируй репозиторий (если есть GitHub)
bash
git clone https://github.com/твой-юзернейм/neoddosman.git
cd neoddosman
(Если скрипт лежит локально, просто открой папку в терминале.)

2.2. Создай виртуальное окружение
bash
python3 -m venv venv
2.3. Активируй его
bash
source venv/bin/activate  # Linux/macOS
(Для Windows: venv\Scripts\activate)

🔹 Теперь в начале строки терминала будет (venv) — значит, окружение активно.

📦 3. Установка Python-зависимостей
В папке проекта должен быть файл requirements.txt (если нет, создай его).

3.1. Установи все зависимости одной командой
bash
pip install -r requirements.txt
(Если requirements.txt нет, установи модули вручную:)

bash
pip install requests colorama fake-useragent tqdm stem lxml
🖥 4. Запуск скрипта
Теперь можно запускать программу:

bash
python3 neoneon.py
🔹 Если скрипт требует аргументов:
bash
python3 neoneon.py --аргумент1 значение --аргумент2 значение
(Проверь, какие аргументы поддерживает скрипт, через --help.)

❌ Возможные ошибки и решения
➊ ModuleNotFoundError даже после установки
Убедись, что виртуальное окружение активно ((venv) в терминале).

Попробуй переустановить модуль:

bash
pip install --force-reinstall имя_модуля
➋ Ошибки с lxml или другими бинарными модулями
Установи недостающие системные библиотеки:

bash
sudo apt install build-essential python3-dev
Затем переустанови модуль:

bash
pip install --no-cache-dir lxml
➌ Permission denied при запуске
Дай файлу права на выполнение:

bash
chmod +x neoneon.py
Или явно укажи Python:

bash
python3 neoneon.py
