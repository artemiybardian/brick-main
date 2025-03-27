from django.core.management.base import BaseCommand
from database.models import Theme, ThemeLinks, Obj, ThemeObjLinks, Links, Images
from django.db import transaction

class Command(BaseCommand):
    help = 'Generates test data for the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data generation...')
        
        with transaction.atomic():
            # Clear existing data
            self.stdout.write('Clearing existing data...')
            Links.objects.all().delete()
            ThemeObjLinks.objects.all().delete()
            ThemeLinks.objects.all().delete()
            Theme.objects.all().delete()
            Obj.objects.all().delete()
            Images.objects.all().delete()

            # Counter for Theme IDs
            theme_id_counter = 1

            # Создаем корневую категорию
            root = Theme.objects.create(
                id=theme_id_counter,
                collection_name="BRICK Database"
            )
            theme_id_counter += 1

            # Основные категории
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

            # Создаем категории и связи
            def create_categories(parent_id, categories_dict, prefix=""):
                nonlocal theme_id_counter
                for name, data in categories_dict.items():
                    category = Theme.objects.create(
                        id=theme_id_counter,
                        collection_name=name
                    )
                    theme_id_counter += 1
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
                        weight=500 + i*100,
                        pack_dim=f"{30+i}x{20+i}x{10+i} cm",
                        stud_dim=f"{32+i}x{16+i}",
                        instructions=True  # Set to True since we're creating an instruction object for each set
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
                            part_class=1,
                            set_class=0,  # Since obj.item_class is 0 (set)
                            color="Default"  # Adding default color
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
                        part_class=2,
                        set_class=0,  # Since obj.item_class is 0 (set)
                        color="Default"  # Adding default color
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
                        part_class=6,
                        set_class=0,  # Since obj.item_class is 0 (set)
                        color="Default"  # Adding default color
                    )

            # Генерируем объекты для некоторых категорий
            create_objects_for_category("Ultimate Collector Series", 1000)
            create_objects_for_category("Star Wars Starfighters", 2000)
            create_objects_for_category("Star Wars Capital Ships", 3000)
            create_objects_for_category("Technic Cars", 4000)
            create_objects_for_category("Technic Trucks", 5000)
            create_objects_for_category("City Police", 6000)
            create_objects_for_category("City Fire", 7000)
            create_objects_for_category("City Buildings", 8000)

            self.stdout.write(self.style.SUCCESS('Successfully generated test data')) 