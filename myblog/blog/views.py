from django.shortcuts import render,get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Create your views here.

def post_list(request):
	posts=Post.objects.order_by('-created_date')
	return render(request, 'blog/post_list.html', {'posts':posts})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save()
			post.save()
			return redirect('blog.views.post_list')
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('blog.views.post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('blog.views.post_detail', pk=post_pk)