from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from database.models import Obj
from .models import CollectionItem

@login_required
def add_to_collection(request):
    """Добавить предмет в коллекцию"""
    obj_id = request.GET.get('obj_id')
    color = request.GET.get('color', 'Default')
    
    if not obj_id:
        return JsonResponse({'status': 'error', 'message': 'Не указан ID предмета'})
    
    obj = get_object_or_404(Obj, id=obj_id)
    
    collection_item, created = CollectionItem.objects.get_or_create(
        user=request.user,
        obj=obj,
        color=color,
        defaults={'quantity': 1}
    )
    
    if not created:
        collection_item.quantity += 1
        collection_item.save()
    
    return JsonResponse({
        'status': 'added',
        'user_quantity': collection_item.quantity,
        'color': color,
        'total_count': CollectionItem.objects.filter(obj=obj).count()
    })

@login_required
def remove_from_collection(request):
    """Удалить предмет из коллекции"""
    obj_id = request.GET.get('obj_id')
    color = request.GET.get('color', 'Default')
    
    if not obj_id:
        return JsonResponse({'status': 'error', 'message': 'Не указан ID предмета'})
    
    obj = get_object_or_404(Obj, id=obj_id)
    
    try:
        collection_item = CollectionItem.objects.get(
            user=request.user,
            obj=obj,
            color=color
        )
        
        collection_item.quantity -= 1
        
        if collection_item.quantity > 0:
            collection_item.save()
            status = 'removed'
            user_quantity = collection_item.quantity
        else:
            collection_item.delete()
            status = 'removed'
            user_quantity = 0
            
        return JsonResponse({
            'status': status,
            'user_quantity': user_quantity,
            'color': color,
            'total_count': CollectionItem.objects.filter(obj=obj).count()
        })
        
    except CollectionItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Предмет не найден в коллекции',
            'color': color
        })

@login_required
def collection_view(request):
    """Страница коллекции"""
    collection_items = CollectionItem.objects.filter(user=request.user).select_related('obj')
    total_items = sum(item.quantity for item in collection_items)
    
    return render(request, "users/collection.html", {
        "collection_items": collection_items,
        "total_items": total_items
    }) 