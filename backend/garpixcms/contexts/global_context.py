def global_context(request, page):
    from garpix_menu.utils import get_menus
    menus = get_menus(page.get_absolute_url())
    return {
        'menus': menus,
    }
