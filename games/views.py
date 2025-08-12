from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
def logout_view(request):
    logout(request)
    return redirect('login')
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            return render(request, 'register.html', {'error': 'die Passwörter stimmen nicht über ein.'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST ['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username oder passwort sind ungülltig'})
    return render(request, 'login.html')
@login_required(login_url ='login')
def play(request, game_id):
    if request.method == 'POST':
        game_to_refresh = get_object_or_404(Game, id = game_id, user= request.user)
        game_to_refresh.last_played = timezone.now()
        game_to_refresh.save()
        return redirect('home')    
    return redirect('home')    

@login_required(login_url ='login')
def home(request):
    games = Game.objects.filter(user = request.user)
    return render(request, 'index.html', {'games': games})
@login_required(login_url ='login')
def add(request):
    if request.method == 'POST':
        title = request.POST['game']
        price = request.POST['price']
        Game.objects.create(title = title, price = price, user = request.user)
        return redirect('home')
    return render(request, 'add.html')
@login_required(login_url ='login')
def delete(request, game_id):
    if request.method == 'POST':
        game_to_remove = get_object_or_404(Game, id = game_id, user = request.user)
        game_to_remove.delete()
        return redirect('home')
    return redirect('home')