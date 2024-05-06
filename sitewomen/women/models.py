from django.db import models

class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True) # blank позволяет не передавать в content записи
    time_create = models.DateTimeField(auto_now_add=True) # auto_now_add автоматически заполняет поле в момент появления записи
    time_update = models.DateTimeField(auto_now=True) # auto_now каждый раз меняется в момент записи
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title