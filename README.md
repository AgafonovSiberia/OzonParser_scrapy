
## Парсер маркетплейса Ozon на <a href="https://scrapy.org/">Scrapy</a>
В данной конкретной конфигурации парсит операционные системы 100 первых смартфонов, отсортированных по рейтингу. Возвращает распределение по версиям ОС.<br><br>
Результат выводится в терминал, а так же сохраняется в файле **result.json.**<br>
Для обхода **CloudFlare** используется web-driver <a href="https://pypi.org/project/selenium-stealth/">selenium_stealth</a>, незаметно вызываемый в промежуточном ПО Scrapy.


## Запуск
<ol>
  <li>Клонировать репозиторий <code>https://github.com/AgafonovSiberia/OzonParser_scrapy.git</code>
  <li>Перейти в рабочий каталог <code>cd OzonParser_scrapy</code>
  <li>Создать виртуальное окружение <code>python3.10 -m venv venv</code>
  <li>Активировать виртуальное окружение <code>source venv/bin/activate</code>
  <li>Установить зависимости <code>pip install -r requirements.txt</code>
  <li>Запустить парсер <code>python main.py</code>
</ol>


