from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, PostComment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out

# Create your views here.
@login_required(redirect_field_name='login')
def post_list(request):

	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

	return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def post_detail(request, pk):

	post = get_object_or_404(Post, pk=pk)


	comments = Comment.objects.filter(comment=pk).order_by('created_date')


	if request.method == 'POST':

		form = PostComment(request.POST)

		if form.is_valid():

			comment = form.save(commit=False)
			comment.author = request.user
			comment.comment = post
			comment.created_date = timezone.now()
			comment.save()
			return (redirect('post_detail', pk=pk))

	else:

		form = PostComment()




	return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form })


@login_required
def post_new(request):

	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():

			post= form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
			form =PostForm()

	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def logout(request):

	log_out(request)

	return render(request, 'blog/logout.html', {})