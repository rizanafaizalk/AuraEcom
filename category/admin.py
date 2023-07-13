from django.contrib import admin
from.models import Brand,Category
# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}

admin.site.register(Brand,BrandAdmin)
admin.site.register(Category,CategoryAdmin)