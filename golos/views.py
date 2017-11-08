from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
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

    def post(self, request):
        if request.method == 'POST':
            kwargs = request.POST
            if User.objects.all().filter(username=kwargs['username']).count() == 0:
                user = User.objects.create(username=kwargs['username'], password=kwargs['username'])
                user.save()
                user = auth.authenticate(username=kwargs['username'], password=kwargs['username'])
                auth.login(request, user)
            else:
                user = auth.authenticate(username=kwargs['username'], password=kwargs['username'])
                auth.login(request, user)
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['shows'] = Show.objects.all()
        return context


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
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




# class VotesView(View):
#     model = Nominees  # Модель данных - Статьи или Комментарии
#     vote_type = None
#
#     def post(self, request, pk):
#         obj = Nominees.objects.get(pk=pk)
#
#         # GenericForignKey не поддерживает метод get_or_create
#         if request.method == "POST":
#             kwargs = request.POST
#             if UserGolos.objects.all().filter(key=kwargs['key_b']).count() == 0:
#                 key_b = UserGolos.objects.create(key=kwargs['key_b'])
#                 key_b.save()
#             try:
#                 key = UserGolos.objects.get(key=kwargs['key_b'])
#                 likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=key)
#                 if likedislike.vote is not self.vote_type:
#                     likedislike.vote = self.vote_type
#                     likedislike.save(update_fields=['vote'])
#                     result = True
#                 else:
#                     likedislike.delete()
#                     result = False
#             except LikeDislike.DoesNotExist:
#                 obj.votes.create(user=request.user, vote=self.vote_type)
#                 result = True
#
#             return HttpResponse(
#                 json.dumps({
#                     "result": result,
#                     "like_count": obj.votes.likes().count(),
#                     "dislike_count": obj.votes.dislikes().count(),
#                     "sum_rating": obj.votes.sum_rating()
#                 }),
#                 content_type="application/json"
#             )
#
#     # def index(request):
