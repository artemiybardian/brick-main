from rest_framework import serializers

from brick_main.models import Obj, Images, ThemeObjLinks, Links
from brick_main.category.serializers import ThemesSerializer


class ThemeObjLinkSerializer(serializers.ModelSerializer):
    high = ThemesSerializer()

    class Meta:
        model = ThemeObjLinks
        fields = ['high']


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['id', 'item', 'color', 'address']


class LinksSerializer(serializers.ModelSerializer):
    part_images = serializers.SerializerMethodField()

    class Meta:
        model = Links
        fields = ['id', 'set', 'part', 'set_class', 'part_class', 'part_count', 'color', 'part_images']

    def get_part_images(self, obj):
        images = Images.objects.filter(item=obj.part)
        return ImagesSerializer(images, many=True).data


class ProductsSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True)

    class Meta:
        model = Obj
        fields = ['id',
                'item_name',
                'item_class',
                'year_first_release',
                'year_last_release',
                'weight',
                'item_dim',
                'pack_dim',
                'flat_dim',
                'stud_dim',
                'instructions',
                'images'
                ]


class ProductDetaileSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True)
    theme_obj_links = ThemeObjLinkSerializer(many=True)

    class Meta:
        model = Obj
        fields = ['id',
                'item_name',
                'item_class',
                'year_first_release',
                'year_last_release',
                'weight',
                'item_dim',
                'pack_dim',
                'flat_dim',
                'stud_dim',
                'instructions',
                'images',
                'theme_obj_links'
                ]
