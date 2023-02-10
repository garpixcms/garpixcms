from django.conf import settings
from garpix_menu.models import MenuItem
from garpix_menu.serializers import MenuItemSerializer


def global_context(request, page):

    current_path = page.get_absolute_url() if page else request.path

    menus = {}
    menu_items = MenuItem.objects.filter(is_active=True, parent=None).order_by('sort', 'title')
    for menu_type_arr in settings.CHOICE_MENU_TYPES:
        menu_type = menu_type_arr[0]
        menu = list(filter(lambda item: item.menu_type == menu_type, menu_items))
        menus[menu_type] = MenuItemSerializer(menu, context={'request': request, 'current_path': current_path}, many=True).data

    return {
        'menus': menus,
    }
