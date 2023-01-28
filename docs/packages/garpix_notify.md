# Notify


## Quickstart

Install with pip:

```bash
pip install garpix_notify
```

Add the `garpix_notify` and dependencies to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'fcm_django',
    'garpix_notify',
]

FCM_DJANGO_SETTINGS = {
        "APP_VERBOSE_NAME": "Firebase Cloud Messaging",
        "FCM_SERVER_KEY": "[your api key]",
        "ONE_DEVICE_PER_USER": False,
        "DELETE_INACTIVE_DEVICES": False,
}

```

Package not included migrations, set path to migration directory. Don't forget create this directory (`app/migrations/garpix_notify/`) and place empty `__init__.py`:

```
app/migrations/
app/migrations/__init__.py  # empty file
app/migrations/garpix_notify/__init__.py  # empty file
```

Add path to settings:

```python
# settings.py

MIGRATION_MODULES = {
    'garpix_notify': 'app.migrations.garpix_notify',
}
```

Add mixin to settings:

```python

# settings.py
   
GARPIX_NOTIFY_MIXIN = 'app.models.notify_mixin.NotifyMixin'
```

Create your custom user model and add `AUTH_USER_MODEL` to `app/settings.py`:

```
AUTH_USER_MODEL = 'user.User'

```

Run make migrations:

```bash
python manage.py makemigrations
```

Migrate:

```bash
python manage.py migrate
```

### Example

#### Step 1. Set notify types in `app/settings.py`, for example:

```python
REGISTRATION_EVENT = 1
FEEDBACK_EVENT = 2
EXAMPLE_EVENT_1 = 3
EXAMPLE_EVENT_2 = 4


NOTIFY_EVENTS = {
    REGISTRATION_EVENT: {
        'title': 'Register',
    },
    FEEDBACK_EVENT: {
        'title': 'Feeback',
    },
    EXAMPLE_EVENT_1: {
        'title': 'Example 1',
    },
    EXAMPLE_EVENT_2: {
        'title': 'Example 2',
    },
}

CHOICES_NOTIFY_EVENT = [(k, v['title']) for k, v in NOTIFY_EVENTS.items()]

```
#### Step 2. Import default settings in your ``app/settings.py``
```python

    from garpix_notify.settings import *
```
or copy from here if you want more customization
```python
PERIODIC_SENDING = 60
EMAIL_MAX_DAY_LIMIT = 240
EMAIL_MAX_HOUR_LIMIT = 240
# SMS
SMS_URL_TYPE = 0
SMS_API_ID = 1234567890
SMS_LOGIN = ''
SMS_PASSWORD = ''
SMS_FROM = ''
# CALL
CALL_URL_TYPE = 0
CALL_API_ID = 1234567890
CALL_LOGIN = ''
CALL_PASSWORD = ''
# TELEGRAM
TELEGRAM_API_KEY = '000000000:AAAAAAAAAA-AAAAAAAA-_AAAAAAAAAAAAAA'
TELEGRAM_BOT_NAME = 'MySuperBot'
TELEGRAM_WELCOME_TEXT = 'Hello'
TELEGRAM_HELP_TEXT = '/set !help for HELP'
TELEGRAM_BAD_COMMAND_TEXT = 'Incorrect command format'
TELEGRAM_SUCCESS_ADDED_TEXT = 'Success'
TELEGRAM_FAILED_ADDED_TEXT = 'Failed'
TELEGRAM_PARSE_MODE = None
TELEGRAM_DISABLE_NOTIFICATION = False
TELEGRAM_DISABLE_PAGE_PREVIEW = False
TELEGRAM_SENDING_WITHOUT_REPLY = False
TELEGRAM_TIMEOUT = None
# VIBER
VIBER_API_KEY = '000000000:AAAAAAAAAA-AAAAAAAA-_AAAAAAAAAAAAAA'
VIBER_BOT_NAME = 'MySuperViberBot'
VIBER_WELCOME_TEXT = 'Hello'
VIBER_SUCCESS_ADDED_TEXT = 'Success'
VIBER_FAILED_ADDED_TEXT = 'Failed'
VIBER_TEXT_FOR_NEW_SUB = 'HI!'
# WHATSAPP
IS_WHATS_APP_ENABLED = True
WHATS_APP_AUTH_TOKEN = None
WHATS_APP_ACCOUNT_SID = None
WHATS_APP_NUMBER_SENDER = None
# SETTINGS
EMAIL_MALLING = 1
GARPIX_NOTIFY_MIXIN = 'garpix_notify.mixins.notify_mixin.NotifyMixin'
NOTIFY_USER_WANT_MESSAGE_CHECK = None
NOTIFY_CALL_CODE_CHECK = None
GARPIX_NOTIFY_CELERY_SETTINGS = 'app.celery.app'
DEFAULT_SYSTEM_NOTIFY_TYPE = 'system'

```
#### Step 3. Go to the admin panel and go to the "Notifications" section - "SMTP accounts"

Add an SMTP account to send Email notifications. These will be the senders of Email notifications.

#### Step 4. Also go to "Notifications" - "Categories"

Create a category that will be used to send emails. Usually one category is enough. The ability to enter several categories
is necessary to divide them into informational and marketing notifications.

#### Step 4. Go to "Notifications" - "Templates"

Create a template for a specific event (when you added them to `settings.py`).

#### Step 5. Call Notify.send()

In the code where it is necessary to work out sending a notification, we perform the following actions:

```python
import datetime
from django.conf import settings
from garpix_notify.models import Notify

# Syntax
# Notify.send(<event>, <context>[, <user=None>, <email=None>, <phone=None>, <files=None>, <data_json=None>])
# That is, we specify the event ID as the first parameter,
# create variables for the template,
# third - the user to send it to (it is not necessary to specify his email, phone number, etc.,
# because this will be determined automatically depending on the type of template)   

# Example
user = request.user  # this will be the recipient of the notification.

Notify.send(settings.REGISTRATION_EVENT, {
    'confirmation_code': 'abcdef12345',
}, user=user)

# If we do not have a user in the system, but we need to send an email, we can do the following

Notify.send(settings.EXAMPLE_EVENT_1, {
    'confirmation_code': 'abcdef12345',
}, email='example@mail.ru')

# If you need more detailed time settings, add send_at

Notify.send(settings.EXAMPLE_EVENT_1, {
    'confirmation_code': 'abcdef12345',
}, email='example@mail.ru', send_at=(datetime.datetime.now() + datetime.timedelta(days=1)))

# If you need to send a code by phone call
Notify.send(settings.EXAMPLE_EVENT_2, phone='79998881122', context={})

# or if you need to get the code directly
Notify.call(phone=79998881122)


```

#### Mass email and sms mailing:
To perform a mass mailing, you need to add user lists to the template.
Or directly in the notification.

#### New system Notifications:
Now system notifications are placed in an independent model. 
It is not necessary to create templates for them. 
Mass mailing is also available.

```python
from django.conf import settings
from garpix_notify.models import SystemNotify
from django.contrib.auth import get_user_model

# 1. Example of use without templates
User = get_user_model()
user = User.objects.filter().first()
SystemNotify.send({'test': 'data'}, user)

# 2. Example of using a template
SystemNotify.send({'test': 'data'}, event=settings.EXAMPLE_EVENT_2)
```

#### Do not forget run celery:

```
celery -A app worker --loglevel=info -B
```

# Telegram Notify

Register you bot [https://t.me/BotFather](https://t.me/BotFather)

Go to [http://localhost:8000/admin/garpix_notify/notifyconfig/](https://t.me/BotFather) and fill "Telegram" section (`API key` and `Bot name`).

Run daemon:

```bash
python3 backend/manage.py garpix_notify_telegram
```

Go to your bot and send `/start` command.

Also, see `user/admin.py` file (see instructions):

```python
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        ('Telegram', {
            'fields': ('telegram_chat_id', 'telegram_secret', 'get_telegram_connect_user_help'),
        })
    ) + UserAdmin.fieldsets
    readonly_fields = ['telegram_secret', 'get_telegram_connect_user_help'] + list(UserAdmin.readonly_fields)
```

# System ws Notify

Add the `channels` to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'channels',
]
```

Add the `REDIS_HOST` and `REDIS_PORT` variables and `asgi` and `channels` configurations:

```python
# settings.py

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

...

ASGI_APPLICATION = 'app.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}
```

Edit your `asgi.py` file

```python
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from garpix_notify import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
```

Socket notification example

```python
group_name = f'workflow-{user.pk}'
Notify.send(settings.MY_NOTIFY, {
        'message': 'my message',
    }, room_name=group_name, user=user)
```

For notifications of the SYSTEM type, a separate non-periodic task is used that works instantly, if room_name is missing system messages will be sent in `'room_{id}'` where `'id'` is user id
