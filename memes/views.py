from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Meme, Comment, Like
from .forms import CommentForm


def welcome_view(request):
    newest_meme = Meme.objects.all().order_by("-pub_date")
    if newest_meme:
        meme_id = newest_meme[0].id
    else:
        meme_id = -1
    return render(request, "memes/welcome.html", {"newest_meme": meme_id})


class MainView(ListView):
    queryset = Meme.objects.all().order_by("-pub_date")
    template_name = 'memes/main.html'
    context_object_name = 'memes_list'
    paginate_by = 10


def top_view(request):
    unsorted_memes = Meme.objects.all()
    sorted_memes = sorted(unsorted_memes,
                          reverse=True,
                          key=lambda meme: meme.get_rating())
    memes_list = sorted_memes[:10]
    context = {'memes_list': memes_list}
    return render(request, "memes/top.html", context)


def user_memes_view(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    memes_list = Meme.objects.filter(author=user).order_by("-pub_date")
    context = {
        "memes_list": memes_list,
        "author": user,
    }
    return render(request, "memes/user_memes.html", context)


def get_thumb_up(is_authenticated, user, meme):
    if is_authenticated:
        try:
            like = Like.objects.get(user=user, meme=meme)
        except (Like.DoesNotExist):
            return -1
        else:
            if like.thumb_up:
                return 1
            else:
                return 0
    else:
        return -1


def meme_details_view(request, meme_id):
    form = CommentForm(request.POST or None)
    meme = Meme.objects.get(pk=meme_id)
    comments = Comment.objects.filter(meme=meme).order_by("-pub_date")
    thumb_up = get_thumb_up(request.user.is_authenticated, request.user, meme)
    next_meme_id = meme_id - 1
    if meme_id <= 1:
        next_meme_id = Meme.objects.latest('id').id

    context = {
        "form": form,
        "meme": meme,
        "comments": comments,
        "thumb_up": thumb_up,
        'next_meme_id': next_meme_id,
    }

    if form.is_valid() and request.user.is_authenticated:
        comment = form.save(commit=False)
        comment.author = request.user
        comment.meme = meme
        comment.save()
        return HttpResponseRedirect(request.path_info)

    return render(request, 'memes/detail.html', context)


class AddMemeView(CreateView):
    model = Meme
    fields = ['title', 'image']

    def form_valid(self, form):
        meme = form.save(commit=False)
        meme.author = self.request.user
        meme.save()
        return redirect(meme.get_absolute_url())


@login_required
def like_view(request, meme_id, thumb_up):
    meme = Meme.objects.get(pk=meme_id)

    try:
        like = Like.objects.get(user=request.user, meme=meme)

    except Like.DoesNotExist:
        if thumb_up == 1:
            like = Like(user=request.user, meme_id=meme_id, thumb_up=True)
        else:
            like = Like(user=request.user, meme_id=meme_id, thumb_up=False)

        like.save()
        return redirect(reverse('memes:detail', kwargs={'meme_id': meme_id}))

    if like.thumb_up:
        if thumb_up == 1:
            like.delete()
        else:
            like.thumb_up = False
            like.save()
    else:
        if thumb_up == 1:
            like.thumb_up = True
            like.save()
        else:
            like.delete()

    return redirect(reverse('memes:detail', kwargs={'meme_id': meme_id}))
