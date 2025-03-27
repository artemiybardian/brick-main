from django.core.management.base import BaseCommand
from database.models import Theme, ThemeLinks, Obj, ThemeObjLinks, Links, Images
from django.db import transaction

class Command(BaseCommand):
    help = 'Generates test data for the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data generation...')
        
        with transaction.atomic():
            # Создаем корневую категорию
            root = Theme.objects.create(
                id=1,
                collection_name="BRICK Database",
                collection_type="root"
            )

            # Основные категории
            categories = {
                "Star Wars": {
                    "subcategories": {
                        "Ultimate Collector Series": {"subcategories": {}},
                        "Vehicles": {
                            "subcategories": {
                                "Starfighters": {"subcategories": {}},
                                "Capital Ships": {"subcategories": {}},
                                "Ground Vehicles": {"subcategories": {}}
                            }
                        },
                        "Locations": {"subcategories": {}},
                        "Minifigures": {"subcategories": {}}
                    }
                },
                "Technic": {
                    "subcategories": {
                        "Vehicles": {
                            "subcategories": {
                                "Cars": {"subcategories": {}},
                                "Trucks": {"subcategories": {}},
                                "Construction": {"subcategories": {}}
                            }
                        },
                        "Machines": {"subcategories": {}},
                        "Robotics": {"subcategories": {}}
                    }
                },
                "City": {
                    "subcategories": {
                        "Police": {"subcategories": {}},
                        "Fire": {"subcategories": {}},
                        "Transport": {
                            "subcategories": {
                                "Cars": {"subcategories": {}},
                                "Trains": {"subcategories": {}},
                                "Aircraft": {"subcategories": {}}
                            }
                        },
                        "Buildings": {"subcategories": {}}
                    }
                }
            }

            # Создаем категории и связи
            def create_categories(parent_id, categories_dict, prefix=""):
                for name, data in categories_dict.items():
                    category = Theme.objects.create(
                        collection_name=name,
                        collection_type="category"
                    )
                    ThemeLinks.objects.create(
                        high_id=parent_id,
                        low_id=category.id
                    )
                    if data["subcategories"]:
                        create_categories(category.id, data["subcategories"], prefix + "  ")

            create_categories(root.id, categories)

            # Создаем объекты для каждой категории
            def create_objects_for_category(category_name, base_id, count=5):
                category = Theme.objects.get(collection_name=category_name)
                
                # Создаем наборы (item_class=0)
                for i in range(count):
                    obj = Obj.objects.create(
                        id=base_id + i,
                        item_name=f"{category_name} Set {i+1}",
                        item_class=0,
                        year_first_release=2020 + i,
                        weight=f"{500 + i*100}g",
                        pack_dim=f"{30+i}x{20+i}x{10+i} cm",
                        stud_dim=f"{32+i}x{16+i}",
                        instructions=f"Instructions for {category_name} Set {i+1}"
                    )
                    ThemeObjLinks.objects.create(
                        high=category,
                        obj=obj
                    )
                    
                    # Создаем детали для набора (item_class=1)
                    for j in range(3):
                        part = Obj.objects.create(
                            id=base_id + count + i*3 + j,
                            item_name=f"Part {j+1} for {category_name} Set {i+1}",
                            item_class=1,
                            year_first_release=2020 + i
                        )
                        Links.objects.create(
                            set=obj,
                            part=part,
                            part_count=j+1,
                            part_class=1
                        )
                    
                    # Создаем минифигурки для набора (item_class=2)
                    minifig = Obj.objects.create(
                        id=base_id + count*4 + i,
                        item_name=f"Minifigure for {category_name} Set {i+1}",
                        item_class=2,
                        year_first_release=2020 + i
                    )
                    Links.objects.create(
                        set=obj,
                        part=minifig,
                        part_count=1,
                        part_class=2
                    )
                    
                    # Создаем инструкцию (item_class=6)
                    instruction = Obj.objects.create(
                        id=base_id + count*5 + i,
                        item_name=f"Instructions for {category_name} Set {i+1}",
                        item_class=6,
                        year_first_release=2020 + i
                    )
                    Links.objects.create(
                        set=obj,
                        part=instruction,
                        part_count=1,
                        part_class=6
                    )

            # Генерируем объекты для некоторых категорий
            create_objects_for_category("Ultimate Collector Series", 1000)
            create_objects_for_category("Starfighters", 2000)
            create_objects_for_category("Capital Ships", 3000)
            create_objects_for_category("Cars", 4000)
            create_objects_for_category("Trucks", 5000)
            create_objects_for_category("Police", 6000)
            create_objects_for_category("Fire", 7000)
            create_objects_for_category("Buildings", 8000)

            self.stdout.write(self.style.SUCCESS('Successfully generated test data')) 