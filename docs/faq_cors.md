# FAQ - Вопросы и ответы

#### Есть ли защита от кроссдоменных запросов (CORS)?

Да, используется модуль [django-cors-headers](https://github.com/adamchainz/django-cors-headers).
При параметре `DEBUG` равном `True`, доступны все кроссдоменные запросы (`CORS_ALLOW_ALL_ORIGINS = True`).
