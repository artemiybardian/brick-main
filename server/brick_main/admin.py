from django.contrib import admin
from brick_main.models import (
    Alternate, Images, Links, Obj,
    Theme, ThemeLinks, ThemeObjLinks,
    Color, KnownColor
)


admin.site.register(Alternate)
admin.site.register(Images)
admin.site.register(Links)
admin.site.register(Obj)
admin.site.register(Theme)
admin.site.register(ThemeLinks)
admin.site.register(ThemeObjLinks)
admin.site.register(Color)
admin.site.register(KnownColor)