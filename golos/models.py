from django.db import models
from .manager import LikeDislikeManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.functional import cached_property
from django.contrib.auth.models import User


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(User, verbose_name="голосующий")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class Show(models.Model):
    title = models.CharField(verbose_name='название шоу', max_length=300)
    image = models.ImageField(verbose_name='изображение', upload_to="show/photos")

    class Meta:
        verbose_name = "Шоу"
        verbose_name_plural = "Все Шоу"
        ordering = ['title']

    def __str__(self):
        return self.title

    # тут хотел Nominees отсортировать по лайкам или что то вроде того пока еще додумал
    @cached_property
    def offer(self):
        return self.nominees_set.all()


class Nominees(models.Model):
    title = models.CharField(verbose_name='имя номинанта', max_length=300)
    image = models.ImageField(verbose_name='изображение', upload_to="nominees/photos")
    show = models.ForeignKey(Show, verbose_name='название шоу')
    votes = GenericRelation(LikeDislike, related_query_name='nominees')

    class Meta:
        verbose_name = "Номинант"
        verbose_name_plural = "Номинанты"
        ordering = ['title']

    def __str__(self):
        return self.title

