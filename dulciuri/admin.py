from django.contrib import admin
from .models import Produs, Brand, Categorie, Stoc_Produs, Eveniment, Oferta


class ProdusAdmin(admin.ModelAdmin):
    list_display = ('id_produs', 'nume','pret', 'brand', 'categorie')


admin.site.register(Produs, ProdusAdmin)
admin.site.register(Brand)
admin.site.register(Categorie)
admin.site.register(Stoc_Produs)
admin.site.register(Eveniment)
admin.site.register(Oferta)