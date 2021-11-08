# Пример входа через AppleId (SPA)

Пример также можно увидеть здесь: https://example.cms.garpix.com/kontakty (см. консоль браузера)

Репозиторий здесь: https://github.com/garpixcms/example-corp-spa

#### Шаг 1. Создание нового проекта

Для начала, создайте новый проект по [документации](install_new_project.md).

#### Шаг 2. Включаем вход

Необходимо включить вход в `.env`:

```bash
# ...
ENABLE_GARPIX_AUTH=True
```

#### Шаг 3. Настраиваем со стороны Developer Apple

3.1. Вам нужен аккаунт разработчика Apple.

3.2. Добавляем новый идентификатор на странице https://developer.apple.com/account/resources/identifiers/list

3.2.1. На экране "Register a new identifier" выбираем "App IDs" и жмем "Continue".
3.2.2. На экране "Select a type" выбираем "App" и жмем "Continue".
3.2.3. На экране "Register an App ID" заполняем данные (пример):

* Description: MyApplication
* Bundle ID: com.mycompany.MyApplication
* Capabilities: ставим галку "Sign In with Apple", выбираем "Enable as a primary App ID" и в "Server to Server Notification Endpoint" пишем
адрес сервера, например, "https://mysite.com"
* Жмем "Continue"

3.2.4. На экране "Confirm your App ID" жмем "Register".

Также, сверху этой страницы есть Team ID (например, "XXAAAA99A9"), запишите его, он пригодится в дальнейшем.

3.3. Добавляем новый ключ на странице https://developer.apple.com/account/resources/authkeys/list

3.3.1. На экране "Register a New Key" заполняем данные:

* Key Name: MyApplication
* Ставим галку на "Sign in with Apple", жмем "Configure" и в "Primary App ID" выбираем идентификатор, введенный выше. Жмем "Save"

3.3.2. На следующем экране "Register a New Key" жмем "Register".

3.3.3. На следующем экране жмем "Download" и скачиваем приватный ключ. Сохраняем в надежное место, чтобы не потерять. Также, он нам пригодится в дальнейшем.

3.3.4. Запишите "Key ID", он пригодится нам в дальнейшем.

3.4. Добавляем новый сервис на странице https://developer.apple.com/account/resources/identifiers/list/serviceId

3.4.1. На странице "Register a new identifier" выбираем "Services IDs" и жмем "Continue".

3.4.2. На экране "Register a Services ID" заполняем данные (пример):

* Description: MyApplicationService
* Identifier: com.mycompany.MyApplicationService

3.4.3. Жмем "Register".

#### Шаг 4. Настраиваем со стороны бэкенда

Добавляем в `backend/app/settings.py`:

```python
# ...

AUTHENTICATION_BACKENDS = [
    'social_core.backends.apple.AppleIdAuth',  # for client backend: apple-id
] + AUTHENTICATION_BACKENDS

# social - apple
SOCIAL_AUTH_APPLE_ID_CLIENT = env('SOCIAL_AUTH_APPLE_ID_CLIENT')  # Your client_id com.application.your, aka "Service ID"
SOCIAL_AUTH_APPLE_ID_TEAM = env('SOCIAL_AUTH_APPLE_ID_TEAM')  # Your Team ID, ie K2232113
SOCIAL_AUTH_APPLE_ID_KEY = env('SOCIAL_AUTH_APPLE_ID_KEY')  # Your Key ID, ie Y2P99J3N81K
SOCIAL_AUTH_APPLE_ID_SECRET = env('SOCIAL_AUTH_APPLE_ID_SECRET')  # SOCIAL_AUTH_APPLE_ID_SECRET="-----BEGIN PRIVATE KEY-----\nMIGTAgE.....\n-----END PRIVATE KEY-----"
SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True
```

И в файл `.env`:

```dotenv
# Идентификатор сервиса
SOCIAL_AUTH_APPLE_ID_CLIENT=com.mycompany.MyApplicationService
# Team ID
SOCIAL_AUTH_APPLE_ID_TEAM=XXAAAA99A9
# Key ID
SOCIAL_AUTH_APPLE_ID_KEY=NYAAAAAA9A
# Содержимое приватного ключа, заменить переносы строк на \n
SOCIAL_AUTH_APPLE_ID_SECRET="-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGB...\n...\n-----END PRIVATE KEY-----"
```

#### Шаг 5. Настраиваем со стороны административной панели

Заходим в на страницу `/admin/oauth2_provider/application/` (DJANGO OAUTH TOOLKIT -> Applications) и добавляем новый:

* Client type: Confidential
* Authorization grant type: Client credentials
* Name: apple-id

Остальное оставляем как есть и сохраняем.

Также, строки "Client id" и "Client secret" необходимы на фронтенде.

#### Шаг 6. Настраиваем со стороны фронтенда (React)

6.1. Устанавливаем модуль "react-apple-signin-auth":

```bash
yarn add react-apple-signin-auth
```

6.2. Добавляем компонент:

```jsx
import React from "react";
import AppleSignin from 'react-apple-signin-auth';

export default class LoginWithAppleId extends React.Component {

    handleSocialLogin = async (data) => {
        console.log(data);
        // convert token
        // POST /api/social-auth/convert-token/
        // Payload:
        /*
        {
            grant_type: 'convert_token',
            // Client id из п. 5
            client_id: 'CSDuH8UgHDTFue2GbjZbYJmaRm7VY70QVEFj6A4T',
            // Client secret из п. 5
            client_secret: 'ic0GJAhwLUF12hvrQugXueplPvvtkkXQS6Yno6fYKiWl7wPE5VNmvvxAWvnBPMIirjtuMds9RQ8oT0U7wSpAqmLrI9fnmX1Ft1NYNW9oybo5ECbAwOZUTEV3b1NZlrRb',
            backend: 'apple-id',
            token: data.authorization.id_token,
        }
        */
        // В ответ вернется стандартный ответ как при получении токена.
    };

    render() {
        return (
            <div>
                <AppleSignin
                    authOptions={{
                      // SOCIAL_AUTH_APPLE_ID_CLIENT 
                      clientId: 'com.mycompany.MyApplicationService',
                      scope: 'email name',
                      redirectURI: 'https://mysite.com',
                      state: '',
                      nonce: 'nonce',
                      usePopup: true,
                    }}
                    uiType="dark"
                    className="apple-auth-btn"
                    buttonExtraChildren="Continue with Apple ID"
                    onSuccess={this.handleSocialLogin}
                    onError={(error) => console.error(error)}
                  />
            </div>
        )
    }
}
```

#### Шаг 7. Тестируем

Вход работает только по https, обязательно потестируйте с нескольких аккаунтов.
