# Интеграция Firebase и FCM Django в проект Django

  

##  1. Создание проекта в Firebase

  

##### Шаг 1: Создание проекта в Firebase

  

1. **Откройте Firebase Console:**

- Перейдите на [Firebase Console](https://console.firebase.google.com/).

  

2. **Создайте новый проект:**

- Нажмите на кнопку "Add project" или выберите существующий проект, если он уже есть.

  

3. **Укажите имя проекта:**

- Введите имя проекта (например, "MyDjangoApp").

- Нажмите "Create project".

  

##### Шаг 2: Добавление вашего веб-приложения в проект Firebase

  

1. **Добавление приложения:**

- В консоли Firebase выберите ваш только что созданный проект.

  

2. **Выберите веб (Web):**

- Нажмите на значок "</>" для добавления веб-приложения в Firebase.

  

3. **Настройте ваше веб-приложение:**

- Введите название вашего приложения (например, "MyApp").

- Опционально можно включить публичный хостинг, если нужно.

- Нажмите "Register app".

  

4. **Скопируйте конфигурацию SDK:**

- После регистрации приложения Firebase, скопируйте объект конфигурации Firebase SDK, который выглядит примерно так:

```javascript

var firebaseConfig = {

apiKey: "YOUR_API_KEY",

authDomain: "YOUR_AUTH_DOMAIN",

projectId: "YOUR_PROJECT_ID",

storageBucket: "YOUR_STORAGE_BUCKET",

messagingSenderId: "YOUR_MESSAGING_SENDER_ID",

appId: "YOUR_APP_ID"

};

```

- Этот конфигурационный объект понадобится для инициализации Firebase в вашем веб-приложении Django.

  

##  2. Интеграция Firebase в проект Django


  

1. **Установите Firebase Admin SDK:**

- Установите Firebase Admin SDK для Python с помощью pip:

```bash

pip install firebase-admin

```

  

2. **Настройка учетных данных:**

  

Для настройки аутентификации с Firebase Admin SDK:

  

- Перейдите в [Firebase Console](https://console.firebase.google.com/).

- Выберите ваш проект Firebase.

- Перейдите в раздел "Настройки проекта" (Project Settings).

- Перейдите на вкладку "Service accounts".

- Нажмите на кнопку "Generate new private key", чтобы скачать JSON-файл с учетными данными.

- Сохраните этот файл в безопасном месте на вашем сервере.

  

3. **Установка переменной окружения:**

- Установите переменную окружения `GOOGLE_APPLICATION_CREDENTIALS`, указывающую на путь к скачанному JSON-файлу с учетными данными сервисного аккаунта:

```bash

export GOOGLE_APPLICATION_CREDENTIALS="/путь/к/вашему/service-account-file.json"

```

- Это необходимо для авторизации вашего приложения Django при работе с Firebase Admin SDK.

  

## 3. Интеграция FCM Django в проект Django

FCM Django — это Django-приложение, специально разработанное для интеграции с Firebase Cloud Messaging (FCM), обеспечивающее отправку push-уведомлений на мобильные устройства и браузеры (Android, iOS, Chrome, Firefox и другие) через HTTP v1 API Firebase. Если требуется поддержка устаревшего API, рекомендуется использовать версию fcm-django меньше 1.

  

1. **Модель данных FCMDevice**


  

 Основная модель данных в FCM Django:

  

- **registration_id**: токен FCM устройства (обязательное поле).

- **name**: имя устройства (необязательное поле).

- **active**: статус активности устройства (по умолчанию True).

- **user**: связь с пользователем Django (необязательное поле).

- **device_id**: уникальный идентификатор устройства (необязательное поле).

- **type**: тип устройства ('android', 'web', 'ios').

  

2. **Функциональность**

  

FCM Django предоставляет множество функций:

  

- **Администрирование устройств**:

- Интеграция с Django Admin для управления устройствами.

- Административные действия для тестирования отправки уведомлений в одиночном и массовом режиме.

- Автоматическое удаление неактивных устройств из базы данных при неудачной отправке уведомлений.

  

- **Интеграция с Django REST Framework**:

- Поддержка `viewsets` для работы с устройствами через REST API.

  

- **Демонстрационный клиент на JavaScript**:

- Пример клиентского проекта для демонстрации возможностей библиотеки.

  

- **Обновление до версии 1.0**:

- Замена пакета `pyfcm` на официальный пакет `firebase-admin`.

- Использование переменной `GOOGLE_APPLICATION_CREDENTIALS` для хранения учетных данных.

  

2. **Работа с устройствами (FCMDevice)**

  

Основные шаги по работе с устройствами в FCM Django:

  

- **Создание устройства**:

  

```python

from fcm_django.models import FCMDevice

  

device = FCMDevice.objects.create(

registration_id="device_registration_token",

name="Device Name",

type="android",

active=True,

)

```

  

- **Отправка уведомления на устройство**:

  

```python

from firebase_admin.messaging import Message

  

message = Message(

notification={

'title': 'Hello',

'body': 'This is a test notification'

}

)

  

device.send_message(message)

```

  

- **Работа с темами (Topics)**:

  

```python

# Подписка на тему

device.handle_topic_subscription(True, topic="news_updates")

  

# Отправка сообщения по теме

from firebase_admin.messaging import Message

  

message = Message(

notification={

'title': 'News Update',

'body': 'New articles available'

},

topic="news_updates"

)

  

FCMDevice.send_topic_message(message, "news_updates")

```

  

## 4. Состояния и условия перехода FCM Django

  

Модель `FCMDevice` в FCM Django имеет следующие состояния:

  

- **Активное состояние (`active=True`)**: устройство активно и готово к получению уведомлений.

- **Неактивное состояние (`active=False`)**: устройство помечено как неактивное, если отправка уведомлений на него завершилась неудачно или из-за других причин.

  

Условия перехода между состояниями:

  

- **Активация устройства**: устройство становится активным при создании или обновлении записи.

- **Деактивация устройства**: устройство автоматически становится неактивным при неудачной отправке уведомлений или если было принято решение пометить его как неактивное.

  

FCM Django представляет собой мощный инструмент для интеграции push-уведомлений в ваши Django-приложения, обеспечивая надежную и гибкую отправку сообщений на различные платформы.

  

##### Шаг 1: Установка и настройка FCM Django

  

1. **Установите FCM Django:**

- Установите библиотеку FCM Django с помощью pip:

```bash

pip install fcm-django

```

  

2. **Настройте ваше приложение Django:**

- В файле `settings.py` вашего проекта Django добавьте следующие настройки:

```python

# Импортируйте Firebase Admin SDK

from firebase_admin import initialize_app

  

# Инициализируйте приложение Firebase Admin SDK

initialize_app()

  

# Настройки FCM Django

FCM_DJANGO_SETTINGS = {

"DEFAULT_FIREBASE_APP": None, # Используйте None для использования основного приложения Firebase Admin SDK

"APP_VERBOSE_NAME": "FCM Django", # Название вашего приложения в админке Django

"ONE_DEVICE_PER_USER": False, # Опционально, только одно активное устройство на пользователя

"DELETE_INACTIVE_DEVICES": False, # Опционально, удаление неактивных устройств

}

  

INSTALLED_APPS = [

# Другие установленные приложения

'fcm_django',

]

```

  

3. **Примените миграции:**

- Выполните миграции Django для установки моделей FCM Django:

```bash

python manage.py migrate

```

  

## 5.Связь Firebase и FCM Django

- **Регистрация устройств и отправка уведомлений:**

В вашем Django приложении используйте модель FCMDevice из `fcm_django.models` для регистрации устройств и отправки уведомлений:

  

```python

from firebase_admin.messaging import Message

from fcm_django.models import FCMDevice

  

# Регистрация устройства

device = FCMDevice()

device.registration_id = "регистрационный_идентификатор_устройства"

device.type = "android" # или "web", "ios" в зависимости от типа устройства

device.save()

  

# Отправка уведомления

device.send_message(Message(data={"key": "value"}))

```

  

- **Управление подпиской на темы:**

Подписывайте устройства на темы и отправляйте уведомления группам устройств:

  

```python

topic = "название_темы"

FCMDevice.objects.handle_subscription(True, topic)

FCMDevice.send_topic_message(Message(data={"key": "value"}), topic)

```
Вы правы, у нас не только письма, но и push-уведомления через Firebase и FCM Django. SMTP-аккаунты нужны только для отправки email-уведомлений. Теперь добавим пункт про админку, который будет охватывать настройки для работы с Firebase и FCM Django.

## 6. Работа с админкой в проекте

### Настройка админки для работы с Firebase и FCM Django

Админка Django позволяет удобно управлять различными аспектами вашего приложения, включая устройства, зарегистрированные для получения push-уведомлений.

### Основные разделы админки

#### 1. Устройства (Devices)

В этом разделе вы можете управлять устройствами, зарегистрированными для получения push-уведомлений.

1. **Добавление устройства:**
   - Перейдите в раздел "Devices" -> "FCM Devices".
   - Нажмите "Add FCM Device".
   - Заполните поля:
     - **Registration ID:** Уникальный идентификатор устройства.
     - **Name:** Имя устройства (опционально).
     - **Active:** Статус активности устройства.
     - **User:** Пользователь, связанный с устройством (если есть).
     - **Type:** Тип устройства (`android`, `web`, `ios`).

2. **Редактирование устройства:**
   - Выберите устройство из списка и нажмите на его имя.
   - Обновите необходимые поля и сохраните изменения.

#### 2. Категории уведомлений (Notification Categories)

Категории помогают организовать уведомления по типам (например, информационные, маркетинговые).

1. **Добавление категории:**
   - Перейдите в раздел "Notifications" -> "Categories".
   - Нажмите "Add Category".
   - Заполните поля:
     - **Name:** Название категории.
     - **Description:** Описание категории (опционально).

#### 3. Шаблоны уведомлений (Notification Templates)

Шаблоны используются для создания содержимого уведомлений, отправляемых пользователям.

1. **Добавление шаблона:**
   - Перейдите в раздел "Notifications" -> "Templates".
   - Нажмите "Add Template".
   - Заполните поля:
     - **Event:** Событие, для которого создается шаблон.
     - **Category:** Категория уведомления.
     - **Title:** Заголовок уведомления.
     - **Body:** Тело уведомления.
     - **Platform:** Платформа (например, `email`, `push`).

#### 4. Управление подписками на темы (Topics)

Темы позволяют группировать устройства для отправки уведомлений определенной группе пользователей.

1. **Подписка на тему:**
   - Выберите устройство или несколько устройств.
   - Выберите действие "Subscribe to topic" и укажите тему.

### Параметры для файла `.env`

Для удобного управления настройками и повышения безопасности, некоторые параметры нужно вынести в файл `.env`.

#### Пример файла `.env`:

```env
# Firebase Admin SDK
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json

# FCM Django settings
FCM_SERVER_KEY=your_fcm_server_key

# SMTP settings (если нужны для email-уведомлений)
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
```

