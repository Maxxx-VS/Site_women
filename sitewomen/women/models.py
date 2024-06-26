from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class PublishedManager(models.Manager): # класс для отображения только опубликованных женщин
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

def translit_to_eng(s: str) -> str: # костыль для формирования слага на английском при русском заголовке
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликованно'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug', # unique делает поле уникальным, db_index делает поле индексируемым
                            validators=[
                                MinLengthValidator(5, message="Минимум 5 символов"),
                                MaxLengthValidator(100, message="Максимум 100 символов"),
                            ])

    content = models.TextField(blank=True, verbose_name='Текст статьи') # blank позволяет не передавать в content записи
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания') # auto_now_add автоматически заполняет поле в момент появления записи
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения') # auto_now каждый раз меняется в момент записи
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts', verbose_name='Категории') # формируем свзь многие-к-одному
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Тэги') # формируем свзь многие-к-многим
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='woman', verbose_name='Муж')

    objects = models.Manager() # менеджер по умолчанию
    published = PublishedManager() # менеджер собственный

    def __str__(self):
        return self.title

    class Meta: # класс для сортировки
        verbose_name = "Изестные женщины"
        verbose_name_plural = "Изестные женщины"
        ordering = ['-time_create'] # метод сортировки
        indexes = [ # метод индексации
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self): # формирует url адрес для каждой записи
        return reverse('post', kwargs={'post_slug':self.slug})

    # def save(self, *args, **kwargs): # формирование автоматического slug
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self): # формирует url адрес для каждой записи
        return reverse('tag', kwargs={'tag_slug':self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')