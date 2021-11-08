# Пример входа через Google (SPA)

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

#### Шаг 3. Настраиваем со стороны Google

3.1. Перейдите на страницу Google Console Credentials https://console.cloud.google.com/apis/credentials

3.2. Нажмите "Create Credentaials" и выберите "OAuth client ID"

3.3. В "Application type" выберите "Web application".

3.4. В появившейся форме заполните поля:

* Name: любое название проекта
* Authorized JavaScript origins: Добавить новый и ввести адрес сайта, например "https://mysite.com"
* Нажмите "Create"

3.5. Скачайте файл (желательно) и сохраните ключи "Client ID" и "Client Secret". Они пригодятся на следующем шаге.

#### Шаг 4. Настраиваем со стороны бэкенда

Добавляем в `backend/app/settings.py`:

```python
# ...

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',  # for client backend: google-oauth2
] + AUTHENTICATION_BACKENDS

# social - google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
```

И в файл `.env`:

```dotenv
# Client ID от Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=999999999999-A99AAAAAAAAAA652f6hlem2q5rfvnel4.apps.googleusercontent.com
# Client Secret от Google
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=AAAAAA-Jt8qTX3Nw8_mXW2dxnpiDM-AAAA9A
```

#### Шаг 5. Настраиваем со стороны административной панели

Заходим в на страницу `/admin/oauth2_provider/application/` (DJANGO OAUTH TOOLKIT -> Applications) и добавляем новый:

* Client type: Confidential
* Authorization grant type: Client credentials
* Name: google-oauth2

Остальное оставляем как есть и сохраняем.

Также, строки "Client id" и "Client secret" необходимы на фронтенде.

#### Шаг 6. Настраиваем со стороны фронтенда (React)

6.1. Устанавливаем зависимости:

```bash
yarn add react-social-login
```

6.2. Добавляем компоненты:

Файл `SocialButton.js`:

```jsx
import React from "react";
import SocialLogin from "react-social-login";

class SocialButton extends React.Component {
  render() {
    const { children, triggerLogin, ...props } = this.props;
    return (
      <button onClick={triggerLogin} {...props}>
        {children}
      </button>
    );
  }
}

export default SocialLogin(SocialButton);
```

Файл `LoginWithGoogle.js`:

```jsx
import React from "react";
import SocialButton from "../SocialButton";

export default class LoginWithGoogle extends React.Component {

    handleSocialLogin = async (user) => {
        console.log(user);
        // convert token
        // POST /api/social-auth/convert-token/
        // Payload:
        /*
        {
            grant_type: 'convert_token',
            // Client id из п. 5
            client_id: '999999999999-A99AAAAAAAAAA652f6hlem2q5rfvnel4.apps.googleusercontent.com',
            // Client secret из п. 5
            client_secret: 'AAAAAA-Jt8qTX3Nw8_mXW2dxnpiDM-AAAA9A',
            backend: 'google-oauth2',
            token: user._token.accessToken,
        }
        */
        // В ответ вернется стандартный ответ как при получении токена.
    };

    handleSocialLoginFailure = (err) => {
        console.error(err);
    };

    render() {
        return (
            <div>
                <SocialButton
                    provider="google"
                    // Client ID от Google
                    appId="999999999999-A99AAAAAAAAAA652f6hlem2q5rfvnel4.apps.googleusercontent.com"
                    onLoginSuccess={
                        this.handleSocialLogin
                    }
                    onLoginFailure={
                        this.handleSocialLoginFailure
                    }
                >
                    Login with Google
                </SocialButton>
            </div>
        )
    }
}
```

#### Шаг 7. Тестируем

Вход работает только по https, обязательно потестируйте с нескольких аккаунтов.
