from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(max_length=300,
                                   label="Add a comment",
                                   widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))

    class Meta:
        model = Comment
        fields = ['comment_text']
