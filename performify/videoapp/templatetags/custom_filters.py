from django import template

register = template.Library()


@register.filter
def youtube_embed(value):
    """
    Converts a YouTube URL in the format https://www.youtube.com/watch?v=VIDEO_ID
    to https://www.youtube.com/embed/VIDEO_ID for embedding.
    """
    if "watch?v=" in value:
        # Replace 'watch?v=' with 'embed/' and add autoplay
        return value.replace("watch?v=", "embed/") + "?autoplay=1"
    elif "embed/" not in value:
        # Assume the last part of the URL is the video ID and add embed with autoplay
        video_id = value.split('/')[-1]
        return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
    return value + "?autoplay=1"
