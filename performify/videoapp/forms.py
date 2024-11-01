from django import forms
from .models import Video, Category, SubCategory, Tag

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'category', 'subcategory', 'tags', 'artist_description', 'url']

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()  # Only specific categories
        self.fields['subcategory'].queryset = SubCategory.objects.none()
        self.fields['tags'].queryset = Tag.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                self.fields['tags'].queryset = Tag.objects.filter(subcategory_id=subcategory_id).order_by('name')
            except (ValueError, TypeError):
                pass
