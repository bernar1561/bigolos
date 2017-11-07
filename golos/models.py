from django.db import models
from .manager import LikeDislikeManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.functional import cached_property


# Create your models here.
class UserGolos(models.Model):
    key = models.CharField(verbose_name='отпечаток пальца', max_length=500)


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(UserGolos, verbose_name="Пользователь")
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
    votes = GenericRelation(LikeDislike, related_query_name='articles')

    class Meta:
        verbose_name = "Номинант"
        verbose_name_plural = "Номинанты"
        ordering = ['title']

    def __str__(self):
        return self.title


# class Like(models.Model):
#     show = models.ForeignKey(Show, verbose_name='название шоу')
#     nominants = models.ForeignKey(Nominees, verbose_name='Номинанты')
#     like = models.IntegerField(verbose_name='количество лайков', default=0, blank=True)
#
#     class Meta:
#         verbose_name = "лайк"
#         verbose_name_plural = "лайки"
#         ordering = ['show']
#
#     def __str__(self):
#         return '%s - %s' % (self.show.title, self.nominants.title)
