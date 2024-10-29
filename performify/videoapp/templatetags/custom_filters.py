from django import template

register = template.Library()

@register.filter
def youtube_embed(value):
    """
    Converts a YouTube URL in the format https://www.youtube.com/watch?v=VIDEO_ID
    to https://www.youtube.com/embed/VIDEO_ID for embedding.
    """
    if "watch?v=" in value:
        return value.replace("watch?v=", "embed/")
    return value
