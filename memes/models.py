from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


def upload_location(meme, filename):
    extension = filename.split(".")[-1]
    if meme.id:
        name = meme.id
    else:
        name = Meme.objects.count() + 1
    return "%s.%s" % (name, extension)


class Meme(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_location,
                              blank=False,
                              height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField(verbose_name='image height', default=0)
    width_field = models.IntegerField(verbose_name='image width', default=0)
    pub_date = models.DateTimeField(verbose_name='date published', auto_now_add=True)

    def get_absolute_url(self):
        return reverse('memes:detail', kwargs={'meme_id': self.pk})

    def get_number_of_likes(self):
        likes = Like.objects.filter(meme=self)
        number_of_likes = 0
        for like in likes:
            if like.thumb_up:
                number_of_likes += 1
        return number_of_likes

    def get_number_of_dislikes(self):
        likes = Like.objects.filter(meme=self)
        number_of_dislikes = 0
        for like in likes:
            if not like.thumb_up:
                number_of_dislikes += 1
        return number_of_dislikes

    def get_rating(self):
        return self.get_number_of_likes() - self.get_number_of_dislikes()

    def __str__(self):
        return self.title

    get_number_of_likes.short_description = 'likes'
    get_number_of_dislikes.short_description = 'dislikes'


class Comment(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment_text = models.CharField(verbose_name='comment', max_length=300)
    pub_date = models.DateTimeField(verbose_name='date published', auto_now_add=True)

    def __str__(self):
        return self.comment_text


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    thumb_up = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.user, self.meme, self.thumb_up)
