from .models import Video
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
def search_videos(request):
    if request.method == "POST":
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        tags = request.POST.getlist('tags')

        # Start with a Q object to allow for dynamic queries
        query = Q(tags__icontains=main_category) & Q(
            tags__icontains=sub_category)

        # Add any selected tags to the query using Q objects
        if tags:
            for tag in tags:
                query &= Q(tags__icontains=tag)

        # Query the videos that match the built query
        videos = Video.objects.filter(query)

        return render(request, 'videoapp/matches.html', {'videos': videos})

    return render(request, 'videoapp/search.html')


@login_required
def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, 'videoapp/video_detail.html', {'video': video})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signing up
            return redirect('search_videos')  # Redirect to a page after signup
    else:
        form = UserCreationForm()
    return render(request, 'videoapp/signup.html', {'form': form})
