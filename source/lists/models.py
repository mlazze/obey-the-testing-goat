from django.core.urlresolvers import reverse
from django.db import models


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @staticmethod
    def create_new():
        pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
