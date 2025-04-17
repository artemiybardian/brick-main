from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from brick_main.models import (
    Alternate, Images, Links, Obj, Theme, ThemeLinks, ThemeObjLinks,
    Color, KnownColor, Currency, ObjProduct, ObjProductPrice, WantedList,
    WantedListProduct, Deliverys, Shops
)

admin.site.register(Deliverys)
admin.site.register(Shops)
admin.site.register(Alternate)
admin.site.register(Images)
admin.site.register(Links)
admin.site.register(Obj)
admin.site.register(Theme)
admin.site.register(ThemeLinks)
admin.site.register(ThemeObjLinks)
admin.site.register(Color)
admin.site.register(KnownColor)
admin.site.register(Currency)


class LimitObjProductPrice(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # count all forms that have not been marked for deletion
        count = sum(1 for form in self.forms if not self._should_delete_form(form))
        max_num = 20  # specify your max number of images here
        if count > max_num:
            raise ValidationError(f'You can only associate up to {max_num} images with this product.')


class AdminObjProductPrice(admin.TabularInline):
    model = ObjProductPrice
    formset = LimitObjProductPrice
    extra = 1
    min_num = 1
    max_num = 20


class ObjProductAdmin(admin.ModelAdmin):
    inlines = [
        AdminObjProductPrice,
    ]
    list_display = ['id', 'name']
    search_fields = ['name']

admin.site.register(ObjProduct, ObjProductAdmin)


admin.site.register(WantedList)
admin.site.register(WantedListProduct)