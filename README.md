Вариант №14 - Транслятор конфигурационного языка в XML
1. Общее описание
Инструмент командной строки преобразует файлы на учебном конфигурационном языке в XML-формат. Реализован синтаксический разбор с помощью специализированной библиотеки Lark. Поддерживаются все конструкции языка: комментарии, константы, массивы, строки, вычисления на этапе трансляции с операциями сложения, pow() и ord(). Синтаксические ошибки выявляются с диагностическими сообщениями.

2. Описание всех функций и настроек
Используемые технологии
Язык: Python
Специализированный парсер: Lark (grammar.lark)
Генерация XML: xml.etree.ElementTree
Тестирование: pytest

Ключи командной строки
-i, --input (обязательный) - путь к входному файлу конфигурации (.cfg)
-o, --output (обязательный) - путь к выходному XML файлу

Поддерживаемый синтаксис

Комментарии:
REM однострочный комментарий
(comment
многострочный
комментарий
)

Числа: 3.14, -10.5, +99.99
Строки: @"текст строки"
Массивы: [1.0 @"text" [вложенный]]
Константы: const имя = значение;
Выражения: !{имя + 1}, !{pow(2.0, 3.0)}, !{ord(@"A")}

3. Команды для сборки проекта и запуска тестов
Установка зависимостей
pip install -r requirements.txt

Запуск утилиты
python cli.py -i examples/database_config.cfg -o output_db.xml
python cli.py -i examples/server_config.cfg -o output_server.xml

Запуск тестов
pip install pytest
pytest

4. Примеры использования
Пример 1: Конфигурация базы данных PostgreSQL
Входной файл: examples/database_config.cfg

REM Конфигурация базы данных PostgreSQL
const pool_size = 10.0;
const retry_count = 3.0;
const timeout = 60.0;
const max_retries = !{pow(retry_count, 2.0)};
[@"postgresql://localhost:5432/mydb"]
[ @"users" @"orders" @"products" ]
!{ord(@"P")}

Команда запуска:
python cli.py -i examples/database_config.cfg -o output_db.xml
Результат: XML файл output_db.xml

Пример 2: Конфигурация веб-сервера
Входной файл: examples/server_config.cfg

REM Конфигурация веб-сервера
const port = 8080.0;
const timeout = 30.0;
const max_workers = 4.0;
const connections = !{port + 10.0};
[@"localhost"]
[ @"GET" @"POST" @"PUT" @"DELETE" ]
!{pow(max_workers, 2.0)}

Команда запуска:
python cli.py -i examples/server_config.cfg -o output_server.xml
Результат: XML файл output_server.xml

Структура проекта
CONFIG-HW14/
├── README.md
├── requirements.txt
├── grammar.lark
├── cli.py
├── parser.py
├── transformer.py
├── examples/
│   ├── database_config.cfg
│   └── server_config.cfg
└── tests/
    └── test_parser.py

Покрытие тестами
Тесты tests/test_parser.py проверяют все конструкции языка:
- комментарии (одно- и многострочные)
- числа (+/- и без знака)
- строки и массивы (пустые, вложенные)
- константы (числа, строки, массивы)
- выражения: сложение, pow(), ord()
- синтаксические ошибки
- неопределенные константы
- полный сценарий конфигурации