# GarpixCMS

<p align="center">
    <a href="https://t.me/garpixcmsnews">Telegram channels</a> •
    <a href="https://t.me/garpixcms">Telegram chat</a> •
    <a href="https://garpixcms.github.io/garpixcms/">Docs</a>
</p>

# 💪 Features

- Project structure management from the admin panel
- Navigation control from the admin panel
- Code quality check
- Backward compatible with Django
- Front-end Agnostic: Use any front-end framework (React, Vue, Angular, etc.), mobile apps.

# 📕 Documentation

For complete documentation [https://garpixcms.github.io/garpixcms/](https://garpixcms.github.io/garpixcms/)


# 🚀 Getting Started

```bash
cookiecutter https://github.com/garpixcms/garpixcms-empty-template
cd website
cp example.env .env
pipenv install
pipenv shell
docker-compose up -d
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate
python3 backend/manage.py createsuperuser
python3 backend/manage.py runserver
```

# 👷‍♀️ Changelog

See [CHANGELOG.md](backend/garpixcms/CHANGELOG.md).

# 🧡 Contributing

See [CONTRIBUTING.md](backend/garpixcms/CONTRIBUTING.md).

# 📝 License

[MIT](LICENSE)