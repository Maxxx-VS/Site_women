from django.contrib import admin
from .models import Women, Category


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat') # содержит список всех полей для отображения в админ панели
    list_display_links = ('id', 'title') # указывются поля, которые стаут кликабельными в админ панели
    ordering = ['-time_create', 'title'] # порядок сортировки для админ панели
    list_editable = ('is_published',) # какое поле можно редактировать в админ панели
    list_per_page = 5 # пагинация списка в админ панели


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


# admin.site.register(Women, WomenAdmin)