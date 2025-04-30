# NeoNeon DDoS Manager by NeoDelux

🔥 Мощный CLI-инструмент для нагрузочного тестирования ваших серверов.  
Позволяет имитировать трафик через Tor, выбирать страну и автоматически находить самые быстрые выходные ноды.

> ⚠️ Этот инструмент предназначен исключительно для тестирования производительности и устойчивости ваших собственных или разрешённых систем. Не используйте его для атак без явного разрешения владельца.

---

## 📦 Функционал

✅ Поддержка методов: GET / POST / HEAD  
✅ Поддержка Tor через SOCKS5  
✅ Автоподбор самых быстрых выходных нод Tor  
✅ Указание желаемой страны (`--country`)  
✅ Цветной интерфейс терминала  
✅ Логирование запросов  

---

## 📦 Установка (Ubuntu/Debian/Mint)
sudo apt update
sudo apt install tor python3 python3-pip -y
git clone https://github.com/NeoDelux/neoddosman
cd neoddosman
pip install -r requirements.txt

## 📦 Установка (Arch/Kali/Manjaro)
sudo pacman -Sy tor python python-pip git --noconfirm
pip install -r requirements.txt

---

## 🐍 Требования

```bash
pip install requests colorama fake-useragent argparse tqdm stem lxml


