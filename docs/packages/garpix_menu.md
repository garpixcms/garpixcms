# Меню

Customizable menus for [garpix_page](https://github.com/garpixcms/garpix_page).

## Quickstart

First, install and set up [garpix_page](https://github.com/garpixcms/garpix_page).

---

Install with pip:

```bash
pip install garpix_menu
```

Add the `garpix_menu` and dependency packages to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'garpix_menu',
]

```

Package not included migrations, set path to migration directory. Don't forget create this directory (`app/migrations/garpix_page/`) and place empty `__init__.py`:

```
app/migrations/
app/migrations/__init__.py  # empty file
app/migrations/garpix_menu/__init__.py  # empty file
```

Add path and other settings:

```python
# settings.py

MIGRATION_MODULES = {
    'garpix_menu': 'app.migrations.garpix_menu',
}

TEMPLATES = [
    {
        # ...
        'OPTIONS': {
            'context_processors': [
                # ...
                'garpix_menu.context_processors.menu_processor',
            ],
        },
    },
]
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

Set up your custom menus in `settings.py`, for example:

```python
# settings.py

MENU_TYPE_HEADER_MENU = 'header_menu'
MENU_TYPE_FOOTER_MENU = 'footer_menu'

MENU_TYPES = {
    MENU_TYPE_HEADER_MENU: {
        'title': 'Header menu',
    },
    MENU_TYPE_FOOTER_MENU: {
        'title': 'Footer menu',
    },
}

CHOICE_MENU_TYPES = [(k, v['title']) for k, v in MENU_TYPES.items()]
```

Example template for default menu:

```html
# templates/menus/default.html

{% for menu_item in menu %}
<a {% if menu_item.target_blank %}target="_blank" {% endif %}
   href="{{ menu_item.get_link }}">{{ menu_item.title }}</a>
{% if not forloop.last %}|{% endif %}
{% endfor %}
```

Example with all templates:

```html
# templates/base.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {% include 'garpix_page/seo.html' %}
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet"
          crossorigin="anonymous">
</head>
<body>
{% include 'include/header.html' %}

<main class="container">
    {% block content %}
    {% endblock %}
</main>

{% include 'include/footer.html' %}
</body>
</html>

# templates/pages/default.html

{% extends 'base.html' %}

{% block content %}
<h1>{{object.title}}</h1>
<div>
    {{object.content|safe}}
</div>
{% endblock %}

# templates/include/header.html

<nav class="navbar navbar-expand-md navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">My Site</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExampleDefault"
                aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarsExampleDefault">
            {% include 'menus/header_menu.html' with menu=menus.header_menu %}
        </div>
    </div>
</nav>

# templates/include/footer.html

<style>
    /* Sticky footer styles
    -------------------------------------------------- */
    html {
        position: relative;
        min-height: 100%;
    }

    body {
        margin-bottom: 60px; /* Margin bottom by footer height */
    }

    .footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 60px; /* Set the fixed height of the footer here */
        line-height: 60px; /* Vertically center the text there */
        background-color: #f5f5f5;
    }

</style>

<footer class="footer">
    <div class="container">
        <span class="text-muted">
            {% include 'menus/footer_menu.html' with menu=menus.footer_menu %}
        </span>
    </div>
</footer>

# templates/menus/header_menu.html

<ul class="navbar-nav me-auto mb-2 mb-md-0">
    {% for menu_item in menu %}
    <li class="nav-item">
        <a class="nav-link {% if menu_item.is_current %}active{% endif %}" aria-current="page"
           {% if menu_item.target_blank %}target="_blank" {% endif %}
           href="{{ menu_item.get_link }}">{{ menu_item.title }}</a>
    </li>
    {% endfor %}
</ul>

# templates/menus/footer_menu.html

{% for menu_item in menu %}
<a {% if menu_item.target_blank %}target="_blank" {% endif %}
   href="{{ menu_item.get_link }}">{{ menu_item.title }}</a>
{% if not forloop.last %}|{% endif %}
{% endfor %}

```

Now you can auth in admin panel and starting add menus and pages.
