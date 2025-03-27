from django.core.management.base import BaseCommand
from database.models import Theme, ThemeLinks, Obj, ThemeObjLinks, Links, Images
from django.db import transaction
import requests
import random
import concurrent.futures
import time
from pathlib import Path
from threading import Lock
from django.db.models import F

class Command(BaseCommand):
    help = 'Generates test data and images for the database'

    def __init__(self):
        super().__init__()
        self.created_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.processed_objects = 0
        self.lock = Lock()
        self.media_dir = Path('media/generated_images')
        self.media_dir.mkdir(parents=True, exist_ok=True)
        
        # Кэш для цветов
        self.color_cache = {}

    def print_progress(self, current, total, prefix='', suffix=''):
        """Выводит прогресс-бар"""
        bar_length = 50
        filled_length = int(round(bar_length * current / float(total)))
        percents = round(100.0 * current / float(total), 1)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        self.stdout.write(f'\r{prefix} [{bar}] {percents}% {suffix}', ending='')
        self.stdout.flush()
        if current == total:
            self.stdout.write('\n')

    def get_existing_colors(self, part_id):
        """Получает список существующих цветов для детали из кэша или базы данных"""
        if part_id in self.color_cache:
            return self.color_cache[part_id]
            
        colors = list(Links.objects.filter(part_id=part_id).values_list('color', flat=True).distinct())
        self.color_cache[part_id] = colors
        return colors

    def update_progress(self, total_objects):
        """Обновляет и выводит прогресс генерации изображений"""
        with self.lock:
            self.processed_objects += 1
            if self.processed_objects % 5 == 0 or self.processed_objects == total_objects:  # Чаще обновляем
                self.print_progress(
                    self.processed_objects,
                    total_objects,
                    prefix='Generating images:',
                    suffix=f'({self.created_count} created, {self.error_count} errors)'
                )

    def download_images_batch(self, objects_batch):
        """Загружает изображения для группы объектов"""
        images_to_create = []
        
        for obj in objects_batch:
            try:
                existing_colors = self.get_existing_colors(obj.id) or ['Default']
                
                for color in existing_colors:
                    response = requests.get('https://thispersondoesnotexist.com')
                    if response.status_code == 200:
                        filename = f'person_{obj.id}_{color}_{int(time.time())}.jpg'
                        file_path = self.media_dir / filename
                        
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        
                        images_to_create.append(Images(
                            item=obj,
                            color=color,
                            address=f'/media/generated_images/{filename}'
                        ))
                        
                        with self.lock:
                            self.created_count += 1
                    else:
                        with self.lock:
                            self.error_count += 1
                    
                    time.sleep(0.1)  # Уменьшенная задержка
                    
            except Exception as e:
                with self.lock:
                    self.error_count += 1
                self.stdout.write(self.style.ERROR(f'\nError processing object {obj.id}: {str(e)}'))
            
            finally:
                self.update_progress(len(objects_batch))
        
        # Bulk create images
        if images_to_create:
            Images.objects.bulk_create(images_to_create, batch_size=100)

    def create_objects_for_category(self, category_name, base_id, count=5, total_categories=8):
        """Создает объекты для категории с выводом прогресса"""
        self.stdout.write(f'\nGenerating objects for category: {category_name}')
        
        category = Theme.objects.get(collection_name=category_name)
        
        objects_to_create = []
        theme_obj_links_to_create = []
        links_to_create = []
        
        for i in range(count):
            # Создаем набор
            obj = Obj(
                id=base_id + i,
                item_name=f"{category_name} Set {i+1}",
                item_class=0,
                year_first_release=2020 + i,
                weight=500 + i*100,
                pack_dim=f"{30+i}x{20+i}x{10+i} cm",
                stud_dim=f"{32+i}x{16+i}",
                instructions=True
            )
            objects_to_create.append(obj)
            
            theme_obj_links_to_create.append(ThemeObjLinks(
                high=category,
                obj=obj
            ))
            
            # Создаем детали
            for j in range(3):
                part = Obj(
                    id=base_id + count + i*3 + j,
                    item_name=f"Part {j+1} for {category_name} Set {i+1}",
                    item_class=1,
                    year_first_release=2020 + i
                )
                objects_to_create.append(part)
                
                existing_colors = self.get_existing_colors(part.id)
                if existing_colors:
                    for color in existing_colors:
                        links_to_create.append(Links(
                            set=obj,
                            part=part,
                            part_count=random.randint(1, 5),
                            part_class=1,
                            set_class=0,
                            color=color
                        ))
                else:
                    links_to_create.append(Links(
                        set=obj,
                        part=part,
                        part_count=random.randint(1, 5),
                        part_class=1,
                        set_class=0,
                        color="Default"
                    ))
            
            # Создаем минифигурку
            minifig = Obj(
                id=base_id + count*4 + i,
                item_name=f"Minifigure for {category_name} Set {i+1}",
                item_class=2,
                year_first_release=2020 + i
            )
            objects_to_create.append(minifig)
            
            existing_colors = self.get_existing_colors(minifig.id)
            color = existing_colors[0] if existing_colors else "Default"
            links_to_create.append(Links(
                set=obj,
                part=minifig,
                part_count=1,
                part_class=2,
                set_class=0,
                color=color
            ))
            
            # Создаем инструкцию
            instruction = Obj(
                id=base_id + count*5 + i,
                item_name=f"Instructions for {category_name} Set {i+1}",
                item_class=6,
                year_first_release=2020 + i
            )
            objects_to_create.append(instruction)
            
            links_to_create.append(Links(
                set=obj,
                part=instruction,
                part_count=1,
                part_class=6,
                set_class=0,
                color="Default"
            ))
            
            # Показываем прогресс создания объектов
            self.print_progress(
                i + 1,
                count,
                prefix=f'Creating objects ({len(objects_to_create)} total):',
                suffix=f'Set {i+1}/{count}'
            )
        
        # Bulk create all objects
        self.stdout.write('\nSaving objects to database...')
        Obj.objects.bulk_create(objects_to_create)
        ThemeObjLinks.objects.bulk_create(theme_obj_links_to_create)
        Links.objects.bulk_create(links_to_create)
        self.stdout.write(self.style.SUCCESS('Done!'))

    def generate_data(self):
        """Генерирует тестовые данные для базы данных"""
        self.stdout.write(self.style.SUCCESS('\nStarting data generation...'))
        
        with transaction.atomic():
            # Clear existing data
            self.stdout.write('Clearing existing data...')
            Links.objects.all().delete()
            ThemeObjLinks.objects.all().delete()
            ThemeLinks.objects.all().delete()
            Theme.objects.all().delete()
            Obj.objects.all().delete()
            Images.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Database cleared!'))

            self.stdout.write('\nCreating root category...')
            theme_id_counter = 1
            root = Theme.objects.create(
                id=theme_id_counter,
                collection_name="BRICK Database"
            )
            theme_id_counter += 1
            self.stdout.write(self.style.SUCCESS('Root category created!'))

            # Основные категории (без изменений)
            categories = {
                "Star Wars": {
                    "subcategories": {
                        "Ultimate Collector Series": {"subcategories": {}},
                        "Vehicles": {
                            "subcategories": {
                                "Star Wars Starfighters": {"subcategories": {}},
                                "Star Wars Capital Ships": {"subcategories": {}},
                                "Star Wars Ground Vehicles": {"subcategories": {}}
                            }
                        },
                        "Star Wars Locations": {"subcategories": {}},
                        "Star Wars Minifigures": {"subcategories": {}}
                    }
                },
                "Technic": {
                    "subcategories": {
                        "Vehicles": {
                            "subcategories": {
                                "Technic Cars": {"subcategories": {}},
                                "Technic Trucks": {"subcategories": {}},
                                "Technic Construction": {"subcategories": {}}
                            }
                        },
                        "Technic Machines": {"subcategories": {}},
                        "Technic Robotics": {"subcategories": {}}
                    }
                },
                "City": {
                    "subcategories": {
                        "City Police": {"subcategories": {}},
                        "City Fire": {"subcategories": {}},
                        "Transport": {
                            "subcategories": {
                                "City Cars": {"subcategories": {}},
                                "City Trains": {"subcategories": {}},
                                "City Aircraft": {"subcategories": {}}
                            }
                        },
                        "City Buildings": {"subcategories": {}}
                    }
                }
            }

            self.stdout.write('\nCreating category hierarchy...')
            def create_categories(parent_id, categories_dict, prefix=""):
                nonlocal theme_id_counter
                themes_to_create = []
                theme_links_to_create = []
                
                for name, data in categories_dict.items():
                    category = Theme(
                        id=theme_id_counter,
                        collection_name=name
                    )
                    themes_to_create.append(category)
                    
                    theme_links_to_create.append(ThemeLinks(
                        high_id=parent_id,
                        low_id=theme_id_counter
                    ))
                    
                    current_id = theme_id_counter
                    theme_id_counter += 1
                    
                    if data["subcategories"]:
                        sub_themes, sub_links = create_categories(current_id, data["subcategories"], prefix + "  ")
                        themes_to_create.extend(sub_themes)
                        theme_links_to_create.extend(sub_links)
                
                return themes_to_create, theme_links_to_create

            themes, theme_links = create_categories(root.id, categories)
            Theme.objects.bulk_create(themes)
            ThemeLinks.objects.bulk_create(theme_links)
            self.stdout.write(self.style.SUCCESS('Category hierarchy created!'))

            # Генерируем объекты для категорий
            self.stdout.write('\nGenerating objects for categories...')
            categories_to_generate = [
                ("Ultimate Collector Series", 1000),
                ("Star Wars Starfighters", 2000),
                ("Star Wars Capital Ships", 3000),
                ("Technic Cars", 4000),
                ("Technic Trucks", 5000),
                ("City Police", 6000),
                ("City Fire", 7000),
                ("City Buildings", 8000)
            ]
            
            total_categories = len(categories_to_generate)
            for i, (category_name, base_id) in enumerate(categories_to_generate, 1):
                self.stdout.write(f'\nProcessing category {i}/{total_categories}:')
                self.create_objects_for_category(category_name, base_id, total_categories=total_categories)

            self.stdout.write(self.style.SUCCESS('\nAll test data generated successfully!'))

    def generate_images(self):
        """Генерирует изображения для объектов"""
        self.stdout.write(self.style.SUCCESS('\nStarting image generation'))
        
        objects = list(Obj.objects.all())
        total_objects = len(objects)
        
        self.stdout.write(f'Found {total_objects} objects to process')
        
        # Разбиваем объекты на батчи по 10
        batch_size = 10
        object_batches = [objects[i:i + batch_size] for i in range(0, len(objects), batch_size)]
        total_batches = len(object_batches)
        
        self.stdout.write(f'Split into {total_batches} batches of {batch_size} objects each')
        
        # Используем пул потоков для параллельной обработки батчей
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.download_images_batch, batch) for batch in object_batches]
            concurrent.futures.wait(futures)
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(
            f'\nImage generation completed:\n'
            f'Objects processed: {self.processed_objects}/{total_objects}\n'
            f'Images created: {self.created_count}\n'
            f'Skipped: {self.skipped_count}\n'
            f'Errors: {self.error_count}'
        ))

    def handle(self, *args, **options):
        """Основной метод команды"""
        start_time = time.time()
        
        try:
            self.stdout.write(self.style.SUCCESS('\n=== Starting BRICK Database Generation ===\n'))
            
            self.generate_data()
            self.generate_images()
            
            end_time = time.time()
            duration = end_time - start_time
            
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS(
                f'\nGeneration completed successfully!\n'
                f'Total time: {duration:.2f} seconds\n'
                f'Images created: {self.created_count}\n'
                f'Errors: {self.error_count}'
            ))
            self.stdout.write('='*50 + '\n')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during generation: {str(e)}'))