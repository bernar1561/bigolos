from .models import *
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist


class IndexView(TemplateView):
    template_name = 'golos/main.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['shows'] = Show.objects.all()
        return context


class VotesView(View):
    model = Nominees  # Модель данных - Статьи или Комментарии
    vote_type = None

    def post(self, request, pk, key_b):
        obj = Nominees.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            if key_b not in UserGolos:
                key_b = UserGolos.objects.create(key=key_b)
                key_b.save()
            key_b = UserGolos.objects.get(key=key_b)
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=key_b)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )

    # def index(request):
#     q = Show.objects.all()
#     for i in q:
#         for t in i.like_set.all():
#             print(t.nominants.title)
#         print(i)
#     return HttpResponse([i for i in q])
