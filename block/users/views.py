from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
import string
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import CustomUser, WishlistItem, LoginVerificationCode, CollectionItem
from database.models import Obj, Links
from .forms import CustomUserCreationForm, AvatarUploadForm
from django.contrib import messages

@login_required
def add_to_wishlist(request):
    """Добавление объекта в вишлист (увеличивает количество)"""
    obj_id = request.GET.get("obj_id")
    color = request.GET.get("color", "Default")  # Получаем цвет из запроса
    add_parts = request.GET.get("add_parts", "false") == "true"  # Получаем флаг добавления деталей
    obj = get_object_or_404(Obj, id=obj_id)
    
    wishlist_item = None
    created = False
    
    # Добавляем основной объект только если не добавляются детали набора
    if not add_parts:
        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user, 
            obj=obj,
            color=color,  # Добавляем цвет в get_or_create
            defaults={'quantity': 1}
        )

        if not created:  # Увеличиваем количество только если элемент уже существовал
            wishlist_item.quantity += 1
            wishlist_item.save()

    # Если это набор и нужно добавить все детали
    added_parts = []
    if add_parts and obj.item_class == 0:  # 0 - это класс для наборов
        # Получаем все детали набора из связей
        parts = Links.objects.filter(set=obj)
        for part_link in parts:
            # Создаем запись в вишлисте для каждой детали с её цветом и количеством
            part_item, part_created = WishlistItem.objects.get_or_create(
                user=request.user,
                obj=part_link.part,
                color=part_link.color,
                defaults={'quantity': part_link.part_count}
            )
            if not part_created:
                # Если деталь уже была в вишлисте, увеличиваем количество на количество из набора
                part_item.quantity += part_link.part_count
                part_item.save()
            added_parts.append({
                'id': part_link.part.id,
                'name': part_link.part.item_name,
                'color': part_link.color,
                'quantity': part_link.part_count
            })

    # Подсчитываем общее количество пользователей с этим предметом
    total_users = WishlistItem.objects.filter(obj=obj).count()

    return JsonResponse({
        "status": "added",
        "total_users": total_users,
        "user_quantity": wishlist_item.quantity if wishlist_item else 0,
        "color": color,
        "is_new": created,
        "added_parts": added_parts if add_parts else []
    })

@login_required
def remove_from_wishlist(request):
    """Удаление объекта из вишлиста (уменьшает количество или удаляет)"""
    obj_id = request.GET.get("obj_id")
    color = request.GET.get("color", "Default")  # Получаем цвет из запроса
    obj = get_object_or_404(Obj, id=obj_id)
    
    try:
        wishlist_item = WishlistItem.objects.get(
            user=request.user, 
            obj=obj,
            color=color  # Добавляем цвет в фильтр
        )
        
        wishlist_item.quantity -= 1
        
        if wishlist_item.quantity > 0:
            wishlist_item.save()
            status = 'removed'
            user_quantity = wishlist_item.quantity
        else:
            wishlist_item.delete()
            status = 'removed'
            user_quantity = 0
            
        return JsonResponse({
            'status': status,
            'total_users': WishlistItem.objects.filter(obj=obj).count(),
            'user_quantity': user_quantity,
            'color': color
        })
        
    except WishlistItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Предмет не найден в вишлисте',
            'color': color
        })

@login_required
def wishlist_view(request):
    """Страница вишлиста"""
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('obj')
    total_items = sum(item.quantity for item in wishlist_items)
    
    return render(request, "users/wishlist.html", {
        "wishlist_items": wishlist_items,
        "total_items": total_items
    })

@login_required
def add_to_collection(request):
    """Добавление объекта в коллекцию (увеличивает количество)"""
    obj_id = request.GET.get("obj_id")
    color = request.GET.get("color", "Default")  # Получаем цвет из запроса
    add_parts = request.GET.get("add_parts", "false") == "true"  # Получаем флаг добавления деталей
    obj = get_object_or_404(Obj, id=obj_id)
    
    collection_item = None
    created = False
    
    # Добавляем основной объект только если не добавляются детали набора
    if not add_parts:
        collection_item, created = CollectionItem.objects.get_or_create(
            user=request.user, 
            obj=obj,
            color=color,  # Добавляем цвет в get_or_create
            defaults={'quantity': 1}
        )

        if not created:  # Увеличиваем количество только если элемент уже существовал
            collection_item.quantity += 1
            collection_item.save()

    # Если это набор и нужно добавить все детали
    added_parts = []
    if add_parts and obj.item_class == 0:  # 0 - это класс для наборов
        # Получаем все детали набора из связей
        parts = Links.objects.filter(set=obj)
        for part_link in parts:
            # Создаем запись в коллекции для каждой детали с её цветом и количеством
            part_item, part_created = CollectionItem.objects.get_or_create(
                user=request.user,
                obj=part_link.part,
                color=part_link.color,
                defaults={'quantity': part_link.part_count}
            )
            if not part_created:
                # Если деталь уже была в коллекции, увеличиваем количество на количество из набора
                part_item.quantity += part_link.part_count
                part_item.save()
            added_parts.append({
                'id': part_link.part.id,
                'name': part_link.part.item_name,
                'color': part_link.color,
                'quantity': part_link.part_count
            })

    # Подсчитываем общее количество пользователей с этим предметом
    total_users = CollectionItem.objects.filter(obj=obj).count()

    return JsonResponse({
        "status": "added",
        "total_users": total_users,
        "user_quantity": collection_item.quantity if collection_item else 0,
        "color": color,
        "is_new": created,
        "added_parts": added_parts if add_parts else []
    })

@login_required
def remove_from_collection(request):
    """Удаление объекта из коллекции (уменьшает количество или удаляет)"""
    obj_id = request.GET.get("obj_id")
    color = request.GET.get("color", "Default")  # Получаем цвет из запроса
    obj = get_object_or_404(Obj, id=obj_id)
    
    try:
        collection_item = CollectionItem.objects.get(
            user=request.user, 
            obj=obj,
            color=color  # Добавляем цвет в фильтр
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
            'total_users': CollectionItem.objects.filter(obj=obj).count(),
            'user_quantity': user_quantity,
            'color': color
        })
        
    except CollectionItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Предмет не найден в коллекции',
            'color': color
        })

@login_required
def add_set_to_collection(request):
    """Добавление всех объектов из obj_consists_of в коллекцию"""
    obj_id = request.GET.get("obj_id")
    obj = get_object_or_404(Obj, id=obj_id)
    user = request.user
    for item in obj.obj_consists_of.all():
        user.collection.add(item)
    return JsonResponse({"status": "set_added"})

@login_required
def collection_view(request):
    """Страница коллекции"""
    collection_items = CollectionItem.objects.filter(user=request.user).select_related('obj')
    total_items = sum(item.quantity for item in collection_items)
    
    return render(request, "users/collection.html", {
        "collection_items": collection_items,
        "total_items": total_items
    })

@login_required
def profile_view(request):
    """Страница профиля пользователя"""
    if request.method == 'POST':
        avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if avatar_form.is_valid():
            # Удаляем старый аватар, если он существует
            if request.user.avatar:
                request.user.avatar.delete(save=False)
            avatar_form.save()
            return redirect('profile')
    else:
        avatar_form = AvatarUploadForm(instance=request.user)

    # Получаем количество предметов в вишлисте и коллекции
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    collection_count = CollectionItem.objects.filter(user=request.user).count()
    
    # Получаем последние добавленные предметы (из обоих списков)
    wishlist_items = WishlistItem.objects.filter(user=request.user).order_by('-added_at')[:5]
    collection_items = CollectionItem.objects.filter(user=request.user).order_by('-added_at')[:5]
    
    # Объединяем и сортируем по дате добавления
    recent_items = list(wishlist_items) + list(collection_items)
    recent_items.sort(key=lambda x: x.added_at, reverse=True)
    recent_items = recent_items[:5]  # Оставляем только 5 последних
    
    context = {
        'avatar_form': avatar_form,
        'wishlist_count': wishlist_count,
        'collection_count': collection_count,
        'recent_items': recent_items,
    }
    
    return render(request, "users/profile.html", context)

@login_required
def change_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        request.user.avatar = request.FILES['avatar']
        request.user.save(skip_clean = True)
        messages.success(request, 'Avatar updated successfully!')
        return redirect('profile')
    messages.error(request, 'Please select an image file.')
    return redirect('profile')

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    
    verification_link = f"http://{current_site.domain}{reverse('verify_email', kwargs={'uidb64': uid, 'token': token})}"
    
    subject = "Подтверждение почты"
    message = f"Привет, {user.username}! Подтвердите свою почту: {verification_link}"
    
    send_mail(subject, message, "your-email@gmail.com", [user.email])

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.clean()
            user.is_active = False  # Делаем аккаунт неактивным
            user.save()
            send_verification_email(user, request)  # Отправляем письмо
            return render(request, "users/registration_pending.html")  # Ожидание подтверждения

    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def send_login_verification_email(user, code):
    subject = 'Код подтверждения для входа в BRICK'
    message = f'''Здравствуйте, {user.username}!

Для входа в аккаунт введите следующий код подтверждения:

{code}

Если вы не пытались войти в аккаунт, проигнорируйте это письмо.

С уважением,
Команда BRICK'''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Генерируем и отправляем код подтверждения
            code = generate_verification_code()
            expires_at = timezone.now() + timedelta(minutes=10)
            
            # Создаем новый код подтверждения
            LoginVerificationCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )
            
            # Отправляем код на почту
            send_login_verification_email(user, code)
            
            # Перенаправляем на страницу ввода кода
            return render(request, 'users/verify_login.html', {
                'user_id': user.id,
                'email': user.email
            })
        else:
            return render(request, 'users/login.html', {
                'error': 'Неверное имя пользователя или пароль'
            })
    
    return render(request, 'users/login.html')

def verify_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        verification_code = request.POST.get('verification_code')
        
        try:
            user = CustomUser.objects.get(id=user_id)
            verification = LoginVerificationCode.objects.filter(
                user=user,
                code=verification_code,
                is_used=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
            
            # Код верный, отмечаем его как использованный
            verification.is_used = True
            verification.save()
            print("dd")
            # Выполняем вход с указанием бэкенда
            user.save(skip_clean=True)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
            
        except (CustomUser.DoesNotExist, LoginVerificationCode.DoesNotExist):
            return render(request, 'users/verify_login.html', {
                'user_id': user_id,
                'email': user.email if 'user' in locals() else '',
                'error': 'Неверный или устаревший код подтверждения'
            })
    
    return redirect('login')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, "users/email_confirmed.html")  # Страница успешного подтверждения
        else:
            return render(request, "users/email_invalid.html")  # Ошибка токена

    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, "users/email_invalid.html")
    
def logout_view(request):
    logout(request)
    return redirect('login')  # Перенаправляем на страницу входа

@login_required
def clear_wishlist(request):
    """Очистка всего вишлиста"""
    if request.method == 'POST':
        WishlistItem.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'cleared'})
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})

@login_required
def clear_collection(request):
    """Очистка всей коллекции"""
    if request.method == 'POST':
        CollectionItem.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'cleared'})
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})