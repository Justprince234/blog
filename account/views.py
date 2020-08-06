from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def login(request):
    """Renders the login page"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('blog_app:home')
        messages.info(request, 'Invalid Login Credentials')
        redirect('account:login')
    return render(request, 'blog_app/login.html')

def register(request):
    """Renders the home register page."""
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist.')
                return redirect('account:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'E-mail already exist.')
                return redirect('account:register')
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.save()
        return redirect('account:login')
    return render(request, 'blog_app/register.html')

def logout(request):
    """Logs user out and redirect to homepage."""
    auth.logout(request)
    return redirect('blog_app:home')