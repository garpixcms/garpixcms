import pytest
from django.conf import settings
from django.test import RequestFactory
from garpix_menu.models import MenuItem
from garpixcms.contexts import global_context
from garpix_menu.serializers import MenuItemSerializer


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def menu_items():
    items = [
        MenuItem.objects.create(title='Home', menu_type='main', is_active=True, sort=1),
        MenuItem.objects.create(title='About', menu_type='main', is_active=True, sort=2),
        MenuItem.objects.create(title='Contact', menu_type='footer', is_active=True, sort=3),
        MenuItem.objects.create(title='Blog', menu_type='main', is_active=False, sort=4),
    ]
    return items


@pytest.fixture
def settings_choice_menu_types():
    original_choice_menu_types = settings.CHOICE_MENU_TYPES
    settings.CHOICE_MENU_TYPES = [
        ('main', 'Main Menu'),
        ('footer', 'Footer Menu'),
    ]
    yield
    settings.CHOICE_MENU_TYPES = original_choice_menu_types


def test_global_context_no_page(request_factory, menu_items, settings_choice_menu_types):
    request = request_factory.get('/some-path/')
    context = global_context(request, None)

    assert 'menus' in context
    assert 'main' in context['menus']
    assert 'footer' in context['menus']

    main_menu = [item for item in menu_items if item.menu_type == 'main' and item.is_active]
    footer_menu = [item for item in menu_items if item.menu_type == 'footer' and item.is_active]

    assert context['menus']['main'] == MenuItemSerializer(
        main_menu, context={'request': request, 'current_path': '/some-path/'}, many=True).data
    assert context['menus']['footer'] == MenuItemSerializer(
        footer_menu, context={'request': request, 'current_path': '/some-path/'}, many=True).data


def test_global_context_with_page(request_factory, menu_items, settings_choice_menu_types):
    class MockPage:
        def get_absolute_url(self):
            return '/mock-page/'
    mock_page = MockPage()
    request = request_factory.get('/another-path/')
    context = global_context(request, mock_page)
    assert 'menus' in context
    assert 'main' in context['menus']
    assert 'footer' in context['menus']
    main_menu = [item for item in menu_items if item.menu_type == 'main' and item.is_active]
    footer_menu = [item for item in menu_items if item.menu_type == 'footer' and item.is_active]

    assert context['menus']['main'] == MenuItemSerializer(
        main_menu, context={'request': request, 'current_path': '/mock-page/'}, many=True).data
    assert context['menus']['footer'] == MenuItemSerializer(
        footer_menu, context={'request': request, 'current_path': '/mock-page/'}, many=True).data
    