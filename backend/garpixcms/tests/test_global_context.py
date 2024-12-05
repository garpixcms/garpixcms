import pytest
from unittest.mock import patch
from django.test import RequestFactory
from garpix_menu.models import MenuItem
from garpixcms.contexts.global_context import global_context


@pytest.fixture
def create_request():
    def _create_request(path):
        return RequestFactory().get(path)

    return _create_request


@pytest.fixture
def setup_menu_items():
    items = [
        MenuItem.objects.create(title='Test1', menu_type='header', is_active=True, sort=1),
        MenuItem.objects.create(title='Test2', menu_type='header', is_active=True, sort=2),
        MenuItem.objects.create(title='Test3', menu_type='header', is_active=False, sort=3),
        MenuItem.objects.create(title='Test4', menu_type='footer', is_active=True, sort=4),
        MenuItem.objects.create(title='Test5', menu_type='footer', is_active=True, sort=5),
    ]
    return items


@pytest.fixture
def mock_page():
    class get_absolute_url:
        def get_absolute_url(self):
            return '/test/'

    return get_absolute_url()


@pytest.mark.django_db
def test_global_context_page1(create_request, setup_menu_items, mock_page):
    request = create_request('/home/')

    mock_page.get_absolute_url = lambda: '/testing'

    with patch('django.conf.settings.CHOICE_MENU_TYPES', [
        ('header', 'Header Menu'),
        ('footer', 'Footer Menu'),
    ]):
        context = global_context(request, None)

    assert 'menus' in context
    assert isinstance(context['menus'], dict)

    assert 'header' in context['menus']
    assert 'footer' in context['menus']

    header_menu = context['menus']['header']
    footer_menu = context['menus']['footer']

    assert len(header_menu) == 2
    assert len(footer_menu) == 2

    assert all(item['title'] != 'Test3' for item in header_menu)


@pytest.mark.django_db
def test_global_context_no_page(create_request, setup_menu_items):
    request = create_request('/home/')

    with patch('django.conf.settings.CHOICE_MENU_TYPES', [
        ('header', 'Header Menu'),
        ('footer', 'Footer Menu'),
    ]):
        context = global_context(request, None)

    assert 'menus' in context
    assert isinstance(context['menus'], dict)

    assert 'header' in context['menus']
    assert 'footer' in context['menus']

    header_menu = context['menus']['header']
    footer_menu = context['menus']['footer']

    assert len(header_menu) == 2
    assert len(footer_menu) == 2


@pytest.mark.django_db
def test_global_context_with_no_active_menu_items(create_request):
    request = create_request('/home/')

    MenuItem.objects.create(title='Inactive1', menu_type='header', is_active=False)
    MenuItem.objects.create(title='Inactive2', menu_type='footer', is_active=False)

    with patch('django.conf.settings.CHOICE_MENU_TYPES', [
        ('header', 'Header Menu'),
        ('footer', 'Footer Menu'),
    ]):
        context = global_context(request, None)

    assert 'menus' in context
    assert context['menus'] == {'header': [], 'footer': []}


@pytest.mark.django_db
def test_global_context_with_invalid_menu_type(create_request, mock_page):
    request = create_request('/home/')

    with patch('django.conf.settings.CHOICE_MENU_TYPES', [
        ('header', 'Header Menu'),
        ('footer', 'Footer Menu'),
    ]):
        with patch('garpix_menu.serializers.MenuItemSerializer') as mock_serializer:
            invalid_menu_data = {
                'header': [{'title': 'Menu1', 'is_active': True, 'menu_type': 'header', 'sort': 1}],
                'footer': [{'title': 'Menu2', 'is_active': True, 'menu_type': 'footer', 'sort': 2}],
                'invalid_type': [{'title': 'Menu3', 'is_active': True, 'menu_type': 'invalid_type', 'sort': 3}]
            }
            mock_serializer.return_value.data = invalid_menu_data
            context = global_context(request, mock_page)

            assert 'menus' in context
            assert context['menus'] == {'header': [], 'footer': []}


@pytest.mark.django_db
def test_global_context_empty_menu_type(create_request, mock_page):
    request = create_request('/home/')

    with patch('django.conf.settings.CHOICE_MENU_TYPES', []):
        with patch('garpix_menu.serializers.MenuItemSerializer') as mock_serializer:
            mock_serializer.return_value.data = {}
            context = global_context(request, mock_page)

            assert 'menus' in context
            assert context['menus'] == {}
