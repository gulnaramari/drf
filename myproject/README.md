EduMaterials API Сервис
EduMaterials  - это веб-приложение, позволяющее пользователям размещать свои полезные материалы или курсы.

Описание
Приложение позволяет создавать и управлять курсами, добавлять материалы, а также предоставляет функционал для управления пользователями и их доступами.

Авторы
Имя: Михайлова Гульнара
Email: gulnaramari@yandex.ru
GitHub: https://github.com/gulnaramari/drf.git
Требования к проекту
Python: версия 3.8 или выше
Django: версия 3.2 или выше
PostgreSQL: версия 12 или выше
Инструкции по установке и запуску проекта
Клонировать репозиторий: git clone git@github.com:gulnaramari/drf.git
Перейти в папку проекта: cd myproject
Установить зависимости: pip install -r requirements.txt
Создайте файл .env в корневой папке проекта и заполните его по шаблону .env.sample переменными:
SECRET_KEY: секретный ключ проекта (например, случайная строка из 50 символов)
NAME: имя базы данных
DBUSER: имя пользователя базы данных
PASSWORD: пароль пользователя базы данных
HOST: адрес хоста базы данных (например, localhost)
PORT: порт базы данных (например, 5432)
Создать базу данных: python manage.py migrate
Запустить сервер: python manage.py runserver

Тестирование кода:
Name                                                                            Stmts   Miss  Cover
---------------------------------------------------------------------------------------------------
config\__init__.py                                                                  0      0   100%
config\asgi.py                                                                      4      4     0%
config\settings.py                                                                 30      0   100%
config\urls.py                                                                      7      1    86%
config\wsgi.py                                                                      4      4     0%
edu_materials\__init__.py                                                           0      0   100%
edu_materials\admin.py                                                             10      0   100%
edu_materials\apps.py                                                               4      0   100%
edu_materials\migrations\0001_initial.py                                            6      0   100%
edu_materials\migrations\0002_course_owner_lesson_owner.py                          6      0   100%
edu_materials\migrations\0003_subscription.py                                       6      0   100%
edu_materials\migrations\0004_alter_lesson_course.py                                5      0   100%
edu_materials\migrations\0005_alter_lesson_course.py                                5      0   100%
edu_materials\migrations\__init__.py                                                0      0   100%
edu_materials\models.py                                                            27      2    93%
edu_materials\paginators.py                                                         5      0   100%
edu_materials\serializers.py                                                       20      0   100%
edu_materials\tests.py                                                            150     45    70%
edu_materials\urls.py                                                               9      0   100%
edu_materials\validators.py                                                        13      3    77%
edu_materials\views.py                                                             64      1    98%
manage.py                                                                          11      2    82%
users\__init__.py                                                                   0      0   100%
users\admin.py                                                                      8      0   100%
users\apps.py                                                                       4      0   100%
users\management\__init__.py                                                        0      0   100%
users\management\commands\__init__.py                                               0      0   100%
users\management\commands\csu.py                                                   11     11     0%
users\migrations\0001_initial.py                                                    7      0   100%
users\migrations\0002_payment.py                                                    7      0   100%
users\migrations\0003_alter_user_date_joined_alter_user_is_active_and_more.py       5      0   100%
users\migrations\__init__.py                                                        0      0   100%
users\models.py                                                                    50     16    68%
users\permissions.py                                                               10      1    90%
users\serializers.py                                                               15      0   100%
users\tests.py                                                                      0      0   100%
users\urls.py                                                                       7      0   100%
users\views.py                                                                     37      6    84%
---------------------------------------------------------------------------------------------------
TOTAL                                                                             547     96    82%
