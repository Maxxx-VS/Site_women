from django.contrib import admin, messages
from .models import Women, Category

class MarriedFilter(admin.SimpleListFilter): # свой дополнительный фильт в панели фильтров
    title = "Статус женщин"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужен'),
            ('single', 'Не замужен'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info') # содержит список всех полей для отображения в админ панели
    list_display_links = ('title',) # указывются поля, которые стаут кликабельными в админ панели
    ordering = ['-time_create', 'title'] # порядок сортировки для админ панели
    list_editable = ('is_published',) # какое поле можно редактировать в админ панели
    list_per_page = 5 # пагинация списка в админ панели
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name'] # список полей по которому будет оуществлятся поиск
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] # панель для ильтрации (фильтр)

    @admin.display(description="Краткое описание", ordering='content') # ordering='content' добавляет сортировку пользовательских полей
    def brief_info(self, women: Women): # добавили поле в админ панели
        return f"Описание {len(women.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset): # добавили в поле Действия: действие
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset): # добавили в поле Действия: действие
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


# admin.site.register(Women, WomenAdmin)