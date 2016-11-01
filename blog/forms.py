from django import forms

from.models import Post, Comment

class PostForm (forms.ModelForm):


	class Meta:

		model =Post
		fields = ('title', 'text',)




class PostComment (forms.ModelForm):

	text = forms.CharField(widget=forms.Textarea, label='')

	class Meta:

		model = Comment
		fields = ('text',)
