from django import forms
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe


class BaseImageForm(forms.ModelForm):
    image_field = forms.ImageField(required=False, label='Upload Image',help_text='Upload an image (must be less than 10 MB)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show preview if image exists
        url = self.instance.url or {}
        image_url = url.get('image')
        if image_url:
            self.fields['image_field'].help_text = mark_safe(
                f'<br><strong>Image Preview:</strong><br>'
                f'<img src="{image_url}" style="max-height: 100px;" /><br>'
                f'<strong>URL:</strong> <a href="{image_url}" target="_blank">{image_url}</a>'
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        url_data = instance.url or {}

        # Only handle new image upload; no deletion
        if self.cleaned_data.get('image_field'):
            path = default_storage.save(
                f'uploads/{self.cleaned_data["image_field"].name}',
                self.cleaned_data["image_field"]
            )
            url_data['image'] = default_storage.url(path)

        instance.url = url_data

        if commit:
            instance.save()
        return instance
