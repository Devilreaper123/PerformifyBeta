from .models import Video
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import VideoForm
from django.http import JsonResponse
from .models import SubCategory, Tag
from django.contrib.auth.models import Group


@login_required
def search_videos(request):
    if request.method == "POST":
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        tags = request.POST.getlist('tags')

        # Start with a base query and add filters
        query = Q()

        # Filter by category name if main_category is selected
        if main_category:
            query &= Q(category__name=main_category)  # Access category's name field

        # Filter by subcategory name if sub_category is selected
        if sub_category:
            query &= Q(subcategory__name=sub_category)  # Access subcategory's name field

        # Add tag filters if any tags are selected
        if tags:
            tag_queries = Q()
            for tag in tags:
                tag_queries |= Q(tags__name=tag)  # Access tag's name field
            query &= tag_queries

        # Query the videos that match the built query
        videos = Video.objects.filter(query).distinct()  # Use distinct to avoid duplicates

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


def artist_signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        video_form = VideoForm(request.POST)

        if 'add_video' in request.POST and user_form.is_valid() and video_form.is_valid():
            user = user_form.save()
            # Add user to "Artists" group
            artists_group = Group.objects.get(name="Artists")
            user.groups.add(artists_group)
            login(request, user)

            # Save video details for the artist
            video = video_form.save(commit=False)
            video.artist = user
            video.save()

            return redirect('artist_dashboard')  # Redirect to artist dashboard
        elif 'check_availability' in request.POST:
            return render(request, 'videoapp/artist_signup.html', {
                'user_form': user_form,
                'video_form': video_form,
                'availability_message': "Feature coming soon!"
            })
    else:
        user_form = UserCreationForm()
        video_form = VideoForm()

    return render(request, 'videoapp/artist_signup.html', {
        'user_form': user_form,
        'video_form': video_form
    })


# def artist_signup(request):
#     if request.method == 'POST':
#         user_form = UserCreationForm(request.POST)
#         video_form = VideoForm(request.POST)

#         if 'add_video' in request.POST:  # Handle "Add Video" button
#             if user_form.is_valid() and video_form.is_valid():
#                 user = user_form.save()
#                 login(request, user)

#                 # Save the video with the logged-in artist
#                 video = video_form.save(commit=False)
#                 video.artist = user
#                 video.save()

#                 return redirect('artist_dashboard')  # Redirect to artist dashboard after signup and video add
#         elif 'check_availability' in request.POST:  # Handle "Check Availability" button
#             # Future functionality to check availability can be added here
#             return render(request, 'videoapp/artist_signup.html', {
#                 'user_form': user_form,
#                 'video_form': video_form,
#                 'availability_message': "Feature coming soon!"  # Placeholder message
#             })
#     else:
#         user_form = UserCreationForm()
#         video_form = VideoForm()

#     return render(request, 'videoapp/artist_signup.html', {
#         'user_form': user_form,
#         'video_form': video_form
#     })


@login_required
def artist_dashboard(request):
    # Handle form submission
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.artist = request.user  # Set the artist to the logged-in user
            video.save()
            return redirect('artist_dashboard')
    else:
        form = VideoForm()

    # Get all videos uploaded by the artist
    artist_videos = Video.objects.filter(artist=request.user)

    return render(request, 'videoapp/artist_dashboard.html', {
        'form': form,
        'artist_videos': artist_videos
    })


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(
        category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})


def get_tags(request):
    subcategory_id = request.GET.get('subcategory_id')
    tags = Tag.objects.filter(
        subcategory_id=subcategory_id).values('id', 'name')
    return JsonResponse({'tags': list(tags)})


@login_required
def dashboard_redirect(request):
    if request.user.groups.filter(name='Artists').exists():
        return redirect('artist_dashboard')
    else:
        return redirect('user_dashboard')
from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard(request):
    # Basic user dashboard, can be expanded with additional content
    return render(request, 'videoapp/user_dashboard.html')
