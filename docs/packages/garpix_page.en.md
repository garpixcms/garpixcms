# Page

Convenient page structure with any context and template.
It is suitable not only for a blog, but also for large sites with a complex presentation.
Supports SEO.

## Quickstart

Install with pip:

```bash
pip install garpix_page
```

Add the `garpix_page` and dependency packages to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
    'modeltranslation',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    # ... django.contrib.*
    'django.contrib.sites',
    'tabbed_admin',
    'garpix_page',
    # third-party and your apps
]

SITE_ID=1

LANGUAGE_CODE = 'en'
USE_DEFAULT_LANGUAGE_PREFIX = False

LANGUAGES = (
    ('en', 'English'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware'
]

```

Package not included migrations, set path to migration directory. Don't forget create this directory (`app/migrations/garpix_page/`) and place empty `__init__.py`:

```
app/migrations/
app/migrations/__init__.py  # empty file
app/migrations/garpix_page/__init__.py  # empty file
```

Add path to settings:

```python
# settings.py

MIGRATION_MODULES = {
    'garpix_page': 'app.migrations.garpix_page',
}
```

Run make migrations:

```bash
python manage.py makemigrations
```

Migrate:

```bash
python manage.py migrate
```

Add celery settings path to `settings.py`:

```python
GARPIXCMS_CELERY_SETTINGS = 'app.celery.app'
```

Now, you can create your models from `BasePage` and set template and context. See example below.

### Important

**Page (Model Page)** - model, subclass from `BasePage`. You create it yourself. There must be at least 1 descendant from BasePage.

**Context** - includes `object` and `request`. It is a function that returns a dictionary from model instance. Values from the key dictionary can be used in the template.

**Template** - standard Django template.

### Example

Urls:

```python
# app/urls.py

from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.i18n import i18n_patterns
from garpix_page.views.page import PageView
from multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings
from garpix_page.views.index import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)$', PageView.as_view(), name='page'),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        path('', IndexView.as_view()),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)

```

Models:

```python
# app/models/page.py

from django.db import models
from garpix_page.models import BasePage


class Page(BasePage):
    content = models.TextField(verbose_name='Content', blank=True, default='')

    template = 'pages/default.html'

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ('-created_at',)


# app/models/category.py

from garpix_page.models import BasePage


class Category(BasePage):
    template = 'pages/category.html'

    def get_context(self, request=None, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = Post.on_site.filter(is_active=True, parent=kwargs['object'])
        context.update({
            'posts': posts
        })
        return context

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ('-created_at',)


# app/models/post.py

from django.db import models
from garpix_page.models import BasePage


class Post(BasePage):
    content = models.TextField(verbose_name='Content', blank=True, default='')

    template = 'pages/post.html'

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ('-created_at',)
```

Admins:

```python
# app/admin/__init__.py

from .page import PageAdmin
from .category import CategoryAdmin
from .post import PostAdmin


# app/admin/page.py

from ..models.page import Page
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(Page)
class PageAdmin(BasePageAdmin):
    pass

# app/admin/category.py

from ..models.category import Category
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(Category)
class CategoryAdmin(BasePageAdmin):
    pass

# app/admin/post.py

from ..models.post import Post
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(Post)
class PostAdmin(BasePageAdmin):
    pass

```

Translations:

```python
# app/translation/__init__.py

from .page import PageTranslationOptions
from .category import CategoryTranslationOptions
from .post import PostTranslationOptions

# app/translation/page.py

from modeltranslation.translator import TranslationOptions, register
from ..models import Page


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('content',)


# app/translation/category.py

from modeltranslation.translator import TranslationOptions, register
from ..models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = []

# app/translation/post.py

from modeltranslation.translator import TranslationOptions, register
from ..models import Post


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('content',)

```

Templates:

```html
# templates/base.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {% include 'garpix_page/seo.html' %}
</head>
<body>
{% include 'garpix_page/admin_toolbar.html' %}
<main>
    {% block content %}404{% endblock %}
    {% block components %}
        {% for component in components %}
        {{ component.template }}
        {% include component.template %}
        {% endfor %}
    {% endblock %}
</main>
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



# templates/pages/category.html

{% extends 'base.html' %}

{% block content %}
<h1>{{object.title}}</h1>
{% for post in posts %}
    <div>
        <h3><a href="{{post.get_absolute_url}}">{{post.title}}</a></h3>
    </div>
{% endfor %}

{% endblock %}



# templates/pages/post.html

{% extends 'base.html' %}

{% block content %}
<h1>{{object.title}}</h1>
<div>
    {{object.content|safe}}
</div>
{% endblock %}

```

Now you can auth in admin panel and starting add pages.

If you need to use a serializer whose model is this page, use the get_serializer() method to avoid circular imports.

## Page permissions


If you need to add login access to your model pages, add login_required static field to your model.

To add some user permissions to page, add permissions  static field to your page model:

```python
class Post(BasePage):
    content = models.TextField(verbose_name='Content', blank=True, default='')

    template = 'pages/post.html'

    login_required = True
    permissions = [IsAdminUser,]

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ('-created_at',)

```

# API

You can use garpix_page with SPA sites.

Add to settings API_URL parameter:

```python
API_URL = 'api'
```

Add to `urls.py` this:

```python
urlpatterns += [
    re_path(r'{}/page_models_list/$'.format(settings.API_URL), PageApiListView.as_view()),
    re_path(r'{}/page/(?P<slugs>.*)$'.format(settings.API_URL), PageApiView.as_view()),
]
```

And you can test it:

`http://localhost:8000/api/page/` - home page (empty slug)
`http://localhost:8000/api/page/another_page` - another page (slug)
`http://localhost:8000/api/page/kategoriya/post-1` - sub page (slug)

Example answer:

```json
{
    "page_model": "Post",
    "init_state": {
        "object": {
            "id": 4,
            "title": "post 1",
            "title_en": "post 1",
            "is_active": true,
            "display_on_sitemap": true,
            "slug": "post-1",
            "created_at": "2021-06-21T19:39:49.749460Z",
            "updated_at": "2021-06-21T19:39:49.749488Z",
            "seo_title": "",
            "seo_title_en": null,
            "seo_keywords": "",
            "seo_keywords_en": null,
            "seo_description": "",
            "seo_description_en": "",
            "seo_author": "",
            "seo_author_en": null,
            "seo_og_type": "website",
            "seo_image": null,
            "lft": 2,
            "rght": 3,
            "tree_id": 3,
            "level": 1,
            "content": "example",
            "content_en": "example",
            "polymorphic_ctype": 11,
            "parent": 3,
            "sites": [
                1
            ]
        }
    }
}
```

## Error contexts

Module consists of 3 reserved names for page models: `Page404`, `Page403` and `Page401`. These names are used for responses when corresponding error statuses are caught.
Example answer on not found error:

```json
{
    "page_model": "Page404",
    "init_state": {
        "object": null,
        "global": {}
    }
}
```

To add drf paginated list of objects to your page context use `GarpixPagePagination` class:

```python
     # example
from garpix_page.models import BasePage
from garpix_page.pagination import GarpixPagePagination

class Post(BasePage):
    ...

    def get_context(self, request=None, *args, **kwargs):

        ...
        # get your_objects_list
        # import objects serializer class YourObjectsSerializer
        ...

        paginator = GarpixPagePagination()

        paginated_list = paginator.get_paginated_data(queryset=your_objects_list, serializer=YourObjectsSerializer,
                                                       request=request)
        context = {
            'paginated_list': paginated_list
        }
 ```

# Components

It is possible to compose a page from components. You can do this in the same way as creating pages.

Model

```python
# app/models/components.py
from django.db import models

from garpix_page.models import BaseComponent

class TextComponent(BaseComponent):
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Текстовый компонент'
        verbose_name_plural = 'Текстовые компоненты'

    def get_context_data(self, request):  # add overriding this method to customize component's context
        context = super().get_context_data(request)
        return context

```
Admin

```python
# app/admin/components.py
from django.contrib import admin

from garpix_page.admin.components.base_component import BaseComponentAdmin
from app.models import TextComponent


@admin.register(TextComponent)
class TextComponentAdmin(BaseComponentAdmin):
    pass

```

Translations:

```python
# app/translation/components.py

from modeltranslation.translator import TranslationOptions, register
from app.models import TextComponent


@register(TextComponent)
class TextComponentTranslationOptions(TranslationOptions):
    fields = ('text',)


```

BaseComponent has m2m field `pages` to specify on which pages the component should be displayed. Through table also has `view_order` field to specify the ordering of components at the page (ascending order).
You can override `get_context_data` method to add some info to component context.

Example answer with some components:

```json
{
    "page_model": "Page",
    "init_state": {
        "object": {
            "id": 1,
            "title": "page",
            "title_en": "page",
            "is_active": true,
            "display_on_sitemap": true,
            "slug": "page",
            "created_at": "2022-02-28T15:33:26.083166Z",
            "updated_at": "2022-04-12T07:45:34.695803Z",
            "seo_title": "",
            "seo_title_en": null,
            "seo_keywords": "",
            "seo_keywords_en": null,
            "seo_description": "",
            "seo_description_en": "",
            "seo_author": "",
            "seo_author_en": null,
            "seo_og_type": "website",
            "seo_image": null,
            "lft": 1,
            "rght": 2,
            "tree_id": 1,
            "level": 0,
            "content": "",
            "content_en": "",
            "polymorphic_ctype": 10,
            "parent": null,
            "sites": [
                1
            ],
            "components": [
                {
                    "component_model": "TextComponent",
                    "object": {
                        "id": 1,
                        "title": "Текстовый блок",
                        "title_en": "Text block",
                        "created_at": "2022-04-11T15:35:24.829579Z",
                        "updated_at": "2022-04-11T15:37:09.898287Z",
                        "text_title": "",
                        "text": "Текст",
                        "text_en": "Text",
                        "polymorphic_ctype": 22,
                        "pages": [
                            1
                        ]
                    }
                },
                {
                    "component_model": "TextDescriptionComponent",
                    "object": {
                        "id": 2,
                        "title": "Описание рубрики",
                        "created_at": "2022-04-12T07:45:15.341862Z",
                        "updated_at": "2022-04-12T07:45:15.341886Z",
                        "text_title": "",
                        "text": "Текст",
                        "description": "Описание",
                        "polymorphic_ctype": 21,
                        "pages": [
                            1
                        ]
                    }
                }
            ]
        },
        "global": {}
    }
}
```

Templates:

If you want to override the base component template, add `template` parameter to component class:

```python
# app/models/components.py

from garpix_page.models import BaseComponent

class TextComponent(BaseComponent):
    # ...
    template = 'text_component.html'
    # ...

```

In html you can use `component` object:
```html
# templates/pages/components/default.html

<h1>{{ component.title }}</h1>
```

You can use `gx_component` tag in section with the component to add edit functionality for admin in template:
```html
{% load gx_component %}
<section class="text-component" {% gx_component component %}>
    ...
</section>
```

# Seo-templates

You can create seo-template from admin panel. 
If you set `field` value to `Model title`, the template will be used for pages only for those model.
In other cases the template will be used for pages with the `value` of the `field`.

You can also specify the sites the template will be used on.

You can add fields which will be used for template keys, using `get_seo_template_keys` method and `seo_template_keys_list` class method.

```python
class Page(BasePage):
    #...
    def get_seo_template_keys(self):
        seo_keys = super().get_seo_template_keys()
        seo_keys.update({
            'yourfield': self.yourfield
        })
        return seo_keys

    @classmethod
    def seo_template_keys_list(cls):
        return [('yourfield', 'your field title')]
```

## Grapesjs

Grapesjs component implementation example:

```js
const Grapesjs = ({ data }): React.ReactElement => {
  const {css, js, object} = data;
  useEffect(() => {
    const jsId = `js_${object.id}`
    const nodeScript = document.getElementById(jsId)
    if(nodeScript === null) {
      const script = document.createElement('script')
      script.id = jsId
      script.type = 'text/javascript'
      script.src = js
      document.body.appendChild(script)
    }

    const cssId = `css_${object.id}`
    const nodeStyle = document.getElementById(cssId)
    if(nodeStyle === null) {
      const link = document.createElement('link')
      link.id = cssId
      link.rel = 'stylesheet'
      link.href = css
      document.body.appendChild(link)
    }
  }, [css, js])
  const html = data.object.html
  return (
    <div dangerouslySetInnerHTML={{__html: html}}></div>
  )
}
```

Сomponent usage
```js
{components.map((component) => {
    return (
        <Grapesjs data={component} key={component.object.id} />
    )
})}
```

## Important!

Also, see this project for additional features (`BaseListPage`, `BaseSearchPage`, `sitemap.xml`, etc).
