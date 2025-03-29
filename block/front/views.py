from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from database.models import Obj, Theme, ThemeLinks
from users.models import CustomUser, WishlistItem, CollectionItem

def home(request):
    """Главная страница"""
    return render(request, "front/home.html")

def categories(request):
    """Страница категорий"""
    root_categories = Theme.objects.exclude(
        id__in=ThemeLinks.objects.values('low')
    )
    return render(request, "front/categories.html", {'categories': root_categories})

def category_detail(request, category_id):
    """Страница конкретной категории"""
    category = get_object_or_404(Theme, id=category_id)
    subcategories = Theme.objects.filter(
        id__in=ThemeLinks.objects.filter(high=category).values('low')
    )
    # Получаем все объекты категории и подкатегорий
    objects = category.get_all_objects().order_by('item_name')
    return render(request, "front/categories.html", {
        'categories': subcategories,
        'current_category': category,
        'objects': objects
    })

def object_list(request):
    """Список объектов"""
    objects = Obj.objects.all()
    return render(request, "front/object_list.html", {"objects": objects})

def object_search(request):
    """Поиск объектов"""
    query = request.GET.get("q", "")
    results = Obj.objects.filter(item_name__icontains=query) if query else []
    return render(request, "front/search_results.html", {"query": query, "results": results})

def api_object_list(request):
    """API: JSON-ответ со списком объектов"""
    objects = list(Obj.objects.values("id", "item_name"))
    return JsonResponse({"objects": objects})

def object_detail(request):
    """Рендер страницы объекта"""
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Obj, id=obj_id)
    wishlist_count = WishlistItem.objects.filter(obj=obj).count()
    collection_count = CollectionItem.objects.filter(obj=obj).count()
    
    # Получаем все объекты, входящие в состав данного набора
    obj_consists_of = Obj.objects.filter(
        links_as_part__set=obj
    ).select_related().distinct()

    # Получаем все наборы, в которые входит данный объект
    appears_in = Obj.objects.filter(
        links_as_set__part=obj
    ).select_related().distinct()
    
    # Проверяем, есть ли объект в вишлисте и коллекции пользователя
    is_in_wishlist = False
    is_in_collection = False
    user_wishlist_items = []
    user_collection_items = []
    
    if request.user.is_authenticated:
        # Получаем все элементы вишлиста для данного объекта
        user_wishlist_items = WishlistItem.objects.filter(
            user=request.user,
            obj=obj
        ).order_by('color')
        
        # Получаем все элементы коллекции для данного объекта
        user_collection_items = CollectionItem.objects.filter(
            user=request.user,
            obj=obj
        ).order_by('color')
        
        is_in_wishlist = user_wishlist_items.exists()
        is_in_collection = user_collection_items.exists()
    
    return render(request, "front/details.html", {
        "obj": obj,
        "obj_consists_of": obj_consists_of,
        "appears_in": appears_in,
        "wishlist_count": wishlist_count,
        "collection_count": collection_count,
        "is_in_wishlist": is_in_wishlist,
        "is_in_collection": is_in_collection,
        "user_wishlist_items": user_wishlist_items,
        "user_collection_items": user_collection_items
    })
