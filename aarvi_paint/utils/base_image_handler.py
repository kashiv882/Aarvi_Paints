from django import forms
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe


class BaseImageForm(forms.ModelForm):
    image_field = forms.ImageField(required=False)
    delete_image = forms.BooleanField(required=False, label='Delete Image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the instance has a URL field and set the help text for image preview
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

        if self.cleaned_data.get('delete_image'):
            url_data.pop('image', None)
            if instance.image:
                instance.image.delete()

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

