from django.shortcuts import render,get_object_or_404
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect


# Create your views here.
def post_list(request):
	posts=Post.objects.order_by('-created_date')
	return render(request, 'blog/post_list.html', {'posts':posts})

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