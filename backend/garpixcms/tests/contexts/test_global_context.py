import pytest
from unittest.mock import patch
from django.test import RequestFactory
from garpix_menu.models import MenuItem
from garpix_menu.serializers import MenuItemSerializer
from garpixcms.contexts.global_context import global_context


@pytest.fixture
def create_request():
    def _create_request(path):
        return RequestFactory().get(path)

    return _create_request


@pytest.fixture
def setup_menu_items():
    items = [
        MenuItem.objects.create(title='Test1', menu_type='test', is_active=True, sort=1),
        MenuItem.objects.create(title='Test2', menu_type='test', is_active=True, sort=2),
        MenuItem.objects.create(title='Test3', menu_type='test', is_active=False, sort=3),
        MenuItem.objects.create(title='Test4', menu_type='test1', is_active=True, sort=4),
        MenuItem.objects.create(title='Test5', menu_type='test1', is_active=True, sort=5),
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
        ('test', 'Test'),
        ('test1', 'Test1'),
    ]):
        context = global_context(request, None)

    menu_types = ['test', 'test1']
    filtered_menus = {
        menu_type: list(filter(lambda item: item.menu_type == menu_type and item.is_active, setup_menu_items))
        for menu_type in menu_types
    }

    serialized_menus = {}
    for menu_type, menu_items in filtered_menus.items():
        serialized_menus[menu_type] = MenuItemSerializer(
            menu_items,
            context={'request': request, 'current_path': '/testing'},
            many=True
        ).data

    # Проверки assert
    assert 'menus' in context
    for menu_type in menu_types:
        assert menu_type in context['menus']
        assert context['menus'][menu_type] == serialized_menus[menu_type]


@pytest.mark.django_db
def test_global_context_no_page(create_request, setup_menu_items):
    request = create_request('/home/')

    with patch('django.conf.settings.CHOICE_MENU_TYPES', [
        ('test', 'Test'),
        ('test1', 'Test1'),
    ]):
        context = global_context(request, None)

    menu_types = ['test', 'test1']
    filtered_menus = {
        menu_type: list(filter(lambda item: item.menu_type == menu_type and item.is_active, setup_menu_items))
        for menu_type in menu_types
    }

    serialized_menus = {}
    for menu_type, menu_items in filtered_menus.items():
        serialized_menus[menu_type] = MenuItemSerializer(
            menu_items,
            context={'request': request, 'current_path': '/home/'},
            many=True
        ).data

    assert 'menus' in context
    for menu_type in menu_types:
        assert menu_type in context['menus']
        assert context['menus'][menu_type] == serialized_menus[menu_type]


@pytest.mark.django_db
def test_global_context_with_no_active_menu_items(create_request, mock_page):
    request = create_request('/home/')

    with patch('django.conf.settings.CHOICE_MENU_TYPES', [
        ('test', 'Test'),
        ('test1', 'Test1'),
    ]):
        with patch('garpix_menu.serializers.MenuItemSerializer') as mock_serializer:
            mock_serializer.return_value.data = {'test': [], 'test1': []}
            context = global_context(request, mock_page)

            assert 'menus' in context
            assert context['menus'] == {'test': [], 'test1': []}


@pytest.mark.django_db
def test_global_context_with_invalid_menu_type(create_request, mock_page):
    request = create_request('/home/')

    with patch('django.conf.settings.CHOICE_MENU_TYPES', [
        ('test', 'Test'),
        ('test1', 'Test1'),
    ]):
        with patch('garpix_menu.serializers.MenuItemSerializer') as mock_serializer:
            invalid_menu_data = {
                'test': [{'title': 'Menu1', 'is_active': True, 'menu_type': 'test', 'sort': 1}],
                'test1': [{'title': 'Menu2', 'is_active': True, 'menu_type': 'test1', 'sort': 2}],
                'invalid_type': [{'title': 'Menu3', 'is_active': True, 'menu_type': 'invalid_type', 'sort': 3}]
            }
            mock_serializer.return_value.data = invalid_menu_data
            context = global_context(request, mock_page)

            assert 'menus' in context
            assert context['menus'] == {'test': [], 'test1': []}


@pytest.mark.django_db
def test_global_context_empty_menu_type(create_request, mock_page):
    request = create_request('/home/')

    with patch('django.conf.settings.CHOICE_MENU_TYPES', []):
        with patch('garpix_menu.serializers.MenuItemSerializer') as mock_serializer:
            mock_serializer.return_value.data = {}
            context = global_context(request, mock_page)

            assert 'menus' in context
            assert context['menus'] == {}
