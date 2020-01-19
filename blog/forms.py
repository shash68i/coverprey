from .models import Post, Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class MyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'placeholder': 'title',
            'id' : 'title-create'
        }
        self.fields['body'].widget.attrs = {
            'placeholder': 'write something',
            'id' : 'body-create'
        }
        self.fields['book_name'].widget.attrs = {
            'placeholder': 'book name',
            'id' : 'book-create'
        }     
        self.fields['author_name'].widget.attrs = {
            'placeholder': 'author name',
            'id' : 'author-create'
        }     
        self.fields['tags'].widget.attrs = {
            'placeholder': 'tags (A comma seperated list of tags)',
            'id' : 'tags-create'
        }     

    class Meta:
        model = Post
        fields = ['title', 'body', 'book_name', 'author_name', 'tags']