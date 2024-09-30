from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Follow
from .forms import ProfileForm
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get(user=user)
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    is_owner = (user == request.user)

    return render(request, 'users/profile.html', {
        'profile_user': user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'is_owner': is_owner,
    })

@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def follow_user(request, pk):
    user_to_follow = get_object_or_404(User, pk=pk)
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('profile', pk=pk)

@login_required
def unfollow_user(request, pk):
    user_to_unfollow = get_object_or_404(User, pk=pk)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', pk=pk)