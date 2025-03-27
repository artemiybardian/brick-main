from django.core.management.base import BaseCommand
from database.models import Obj, Images
import requests
import random
import concurrent.futures
import time
from pathlib import Path
from threading import Lock

class Command(BaseCommand):
    help = 'Generate images for objects'

    def __init__(self):
        super().__init__()
        self.colors = [
            "Red", "Blue", "Yellow", "Green", "Black", "White", "Orange", 
            "Brown", "Gray", "Dark Blue", "Dark Green", "Purple", "Pink",
            "Gold", "Silver", "Bronze", "Copper", "Metallic", "Chrome",
            "Trans-Clear", "Trans-Red", "Trans-Blue", "Trans-Yellow", "Trans-Green",
            "Pearl Gold", "Pearl Silver", "Sand Blue", "Sand Green", "Sand Red",
            "Dark Red", "Dark Gray", "Light Gray", "Tan", "Lime", "Magenta",
            "Azure", "Coral", "Lavender", "Olive", "Teal"
        ]
        self.created_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.processed_objects = 0
        self.lock = Lock()
        # Создаем директорию для сохранения изображений
        self.media_dir = Path('media/generated_images')
        self.media_dir.mkdir(parents=True, exist_ok=True)

    def update_progress(self, total_objects):
        """Обновляет и выводит прогресс"""
        with self.lock:
            self.processed_objects += 1
            if self.processed_objects % 1 == 0:  # Выводим каждый объект
                self.stdout.write(
                    f'Progress: {self.processed_objects}/{total_objects} objects '
                    f'({(self.processed_objects/total_objects*100):.1f}%) | '
                    f'Images created: {self.created_count} | '
                    f'Errors: {self.error_count}\r'
                )
                self.stdout.flush()

    def download_image(self, obj, total_objects):
        try:
            # Выбираем случайное количество цветов для объекта (от 1 до 5)
            num_colors = random.randint(1, 5)
            selected_colors = random.sample(self.colors, num_colors)
            
            for color in selected_colors:
                # Получаем изображение с thispersondoesnotexist.com
                response = requests.get('https://thispersondoesnotexist.com')
                if response.status_code == 200:
                    # Генерируем уникальное имя файла
                    filename = f'person_{obj.id}_{color}_{int(time.time())}.jpg'
                    file_path = self.media_dir / filename
                    
                    # Сохраняем изображение
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    # Создаем запись в базе данных
                    Images.objects.create(
                        item=obj,
                        color=color,
                        address=f'/media/generated_images/{filename}'
                    )
                    with self.lock:
                        self.created_count += 1
                else:
                    with self.lock:
                        self.error_count += 1
                
                # Небольшая задержка между запросами (0.2 секунды)
                time.sleep(0.2)
                
        except Exception as e:
            with self.lock:
                self.error_count += 1
            self.stdout.write(self.style.ERROR(f'\nError processing object {obj.id}: {str(e)}'))
        
        finally:
            self.update_progress(total_objects)

    def handle(self, *args, **options):
        # Очищаем существующие изображения
        Images.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Existing images deleted'))

        # Получаем все объекты
        objects = Obj.objects.all()
        total_objects = objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'Starting image generation for {total_objects} objects'))
        
        # Используем пул потоков для параллельной обработки
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Запускаем задачи
            futures = [executor.submit(self.download_image, obj, total_objects) for obj in objects]
            
            # Ждем завершения всех задач
            concurrent.futures.wait(futures)
        
        # Выводим финальную статистику
        self.stdout.write('\n' + '='*50 + '\n')
        self.stdout.write(self.style.SUCCESS(
            f'Image generation completed:\n'
            f'Objects processed: {self.processed_objects}/{total_objects}\n'
            f'Images created: {self.created_count}\n'
            f'Skipped: {self.skipped_count}\n'
            f'Errors: {self.error_count}'
        )) 