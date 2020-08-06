from django.shortcuts import render, get_object_or_404
from .models import Category, Post, Comment
from .forms import CommentForms
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    """Displays the home page."""
    template_name = 'blog_app/index.html'
    posts = Post.objects.filter(status=1).order_by('-created_on')
    category = Category.objects.all()
    context = {'posts':posts, 'category':category}

    return render(request, template_name, context)

@login_required
def post_detail(request, slug):
    """Resolves a post to a slug and displays it."""
    template_name = 'blog_app/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    # new_comment = None
    # Comment Posted
    if request.method == 'POST':
        comment_form = CommentForms(data=request.POST)
        if comment_form.is_valid():
            
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForms()

    return render(request, template_name, {'post':post, 'comments':comments, 'comment_form':comment_form})

@login_required
def blog_category(request, slug):
    category = Category.objects.get(slug=slug)
    context = {'category': category}
    
    return render(request, 'blog_app/blog_category.html', context)

def search(request):
    posts = Post.objects.filter(status=1)
    query = request.GET.get('q')
    queries = query.split() # pthon install 2020 = [python, install, 2020]
    for q in queries:
        search_results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q),
            ).distinct()

    return render(request, 'blog_app/search.html', {'search_results':search_results, 'posts':posts})