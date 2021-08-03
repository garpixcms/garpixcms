# FAQ - Вопросы и ответы

#### Как изменить количество выводимых записей в Структуре страниц?

Используйте в `app/settings.py` переменную `GARPIX_PAGE_ADMIN_LIST_PER_PAGE`.

По умолчанию ее значение равно 25.

Можно изменить следующим образом:

```
# app/settings.py

GARPIX_PAGE_ADMIN_LIST_PER_PAGE = 50

```