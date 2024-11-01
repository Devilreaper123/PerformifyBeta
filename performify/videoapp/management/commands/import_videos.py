# # from django.core.management.base import BaseCommand
# # from django.contrib.auth.models import User
# # from videoapp.models import Video, Category, SubCategory, Tag
# # import json

# # class Command(BaseCommand):
# #     help = 'Imports videos from a JSON file into the database'

# #     def handle(self, *args, **kwargs):
# #         with open('./videoapp/beta2.json', 'r', encoding='utf-8') as f:
# #             video_data = json.load(f)

# #         for video in video_data:
# #             # Get or create the artist
# #             artist_name = video['artist']
# #             artist_user, created = User.objects.get_or_create(username=artist_name)
            
# #             # Convert tags to objects
# #             category_name = video['tags'][0]  # Assuming the first tag is the category
# #             category, _ = Category.objects.get_or_create(name=category_name)
            
# #             subcategory_name = video['tags'][1] if len(video['tags']) > 1 else None
# #             subcategory = None
# #             if subcategory_name:
# #                 subcategory, _ = SubCategory.objects.get_or_create(
# #                     name=subcategory_name, category=category
# #                 )

# #             tag_names = video['tags'][2:]  # The remaining tags are specific tags
# #             tags = []
# #             for tag_name in tag_names:
# #                 tag, _ = Tag.objects.get_or_create(name=tag_name, subcategory=subcategory)
# #                 tags.append(tag)

# #             # Format the video URL
# #             video_url = video['url']
# #             if "youtu.be" in video_url:
# #                 video_id = video_url.split('/')[-1].split('?')[0]  # Extract the video ID
# #                 video_url = f"https://www.youtube.com/watch?v={video_id}"

# #             # Create the video object
# #             video_obj = Video(
# #                 title=video['title'],
# #                 artist=artist_user,
# #                 description=video['description'],
# #                 category=category,
# #                 subcategory=subcategory,
# #                 artist_description=video['artist_description'],
# #                 url=video_url
# #             )
# #             video_obj.save()
# #             video_obj.tags.set(tags)  # Set many-to-many tags

# #         self.stdout.write(self.style.SUCCESS('Successfully imported videos from JSON'))


# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from videoapp.models import Video, Category, SubCategory, Tag
# import json

# class Command(BaseCommand):
#     help = 'Imports videos from a JSON file into the database'

#     def handle(self, *args, **kwargs):
#         with open('./videoapp/beta2.json', 'r', encoding='utf-8') as f:
#             video_data = json.load(f)

#         for video in video_data:
#             # Ensure artist user exists
#             artist, created = User.objects.get_or_create(username=video['artist'])
            
#             category, _ = Category.objects.get_or_create(name=video['category'])
#             subcategory, _ = SubCategory.objects.get_or_create(name=video['subcategory'], category=category)

#             video_obj = Video(
#                 title=video['title'],
#                 artist=artist,
#                 description=video['description'],
#                 category=category,
#                 subcategory=subcategory,
#                 url=video['url'],
#                 artist_description=video['artist_description']
#             )
#             video_obj.save()

#             for tag_name in video['tags']:
#                 tag, _ = Tag.objects.get_or_create(name=tag_name, subcategory=subcategory)
#                 video_obj.tags.add(tag)

#         self.stdout.write(self.style.SUCCESS('Successfully imported videos from JSON'))


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from videoapp.models import Video, Category, SubCategory, Tag
import json

class Command(BaseCommand):
    help = 'Imports videos from a JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('./videoapp/beta2.json', 'r', encoding='utf-8') as f:
            video_data = json.load(f)

        for video in video_data:
            # Ensure artist user exists
            artist, created = User.objects.get_or_create(username=video['artist'])
            
            # Extract category, subcategory, and tags
            category_name = video['tags'][0] if len(video['tags']) > 0 else "Default Category"
            category, _ = Category.objects.get_or_create(name=category_name)
            
            subcategory_name = video['tags'][1] if len(video['tags']) > 1 else None
            subcategory = None
            if subcategory_name:
                subcategory, _ = SubCategory.objects.get_or_create(name=subcategory_name, category=category)

            # Create or get tags from the remaining entries in the tags list
            tag_names = video['tags'][2:] if len(video['tags']) > 2 else []
            tags = []
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name, subcategory=subcategory)
                tags.append(tag)

            # Format the video URL to ensure it's embedded properly
            video_url = video['url']
            if "youtu.be" in video_url:
                video_id = video_url.split('/')[-1].split('?')[0]  # Extract the video ID
                video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Create the video object
            video_obj = Video(
                title=video['title'],
                artist=artist,
                description=video['description'],
                category=category,
                subcategory=subcategory,
                artist_description=video['artist_description'],
                url=video_url
            )
            video_obj.save()

            # Link tags to the video object
            video_obj.tags.set(tags)

        self.stdout.write(self.style.SUCCESS('Successfully imported videos from JSON'))
