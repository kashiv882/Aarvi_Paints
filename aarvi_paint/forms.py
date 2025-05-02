from django import forms
from .models import Banner, Parallax, ColourPalette, Brochure, AdditionalInfo, AdminContactDetails, Category, Product, \
    Home
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe

from .utils.base_image_handler import BaseImageForm


class BaseBannerForm(forms.ModelForm):
    desktop_image = forms.ImageField(required=False)
    mobile_image = forms.ImageField(required=False)
    delete_desktop = forms.BooleanField(required=False, label='Delete Desktop Image')
    delete_mobile = forms.BooleanField(required=False, label='Delete Mobile Image')

    class Meta:
        model = Banner
        fields = ['title', 'short_description', 'placement_location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = self.instance.url or {}

        desktop_url = url.get('desktop')
        mobile_url = url.get('mobile')

        if desktop_url:
            self.fields['desktop_image'].help_text = mark_safe(
                f'<br><strong>Desktop Preview:</strong><br>'
                f'<img src="{desktop_url}" style="max-height: 100px;" /><br>'
                f'<strong>URL:</strong> <a href="{desktop_url}" target="_blank">{desktop_url}</a>'
            )

        if mobile_url:
            self.fields['mobile_image'].help_text = mark_safe(
                f'<br><strong>Mobile Preview:</strong><br>'
                f'<img src="{mobile_url}" style="max-height: 100px;" /><br>'
                f'<strong>URL:</strong> <a href="{mobile_url}" target="_blank">{mobile_url}</a>'
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        url_data = instance.url or {}

        if self.cleaned_data.get('delete_desktop'):
            url_data.pop('desktop', None)
        if self.cleaned_data.get('delete_mobile'):
            url_data.pop('mobile', None)

        if self.cleaned_data.get('desktop_image'):
            path = default_storage.save(
                f'banners/desktop/{self.cleaned_data["desktop_image"].name}',
                self.cleaned_data["desktop_image"]
            )
            url_data['desktop'] = default_storage.url(path)

        if self.cleaned_data.get('mobile_image'):
            path = default_storage.save(
                f'banners/mobile/{self.cleaned_data["mobile_image"].name}',
                self.cleaned_data["mobile_image"]
            )
            url_data['mobile'] = default_storage.url(path)

        instance.url = url_data

        if commit:
            instance.save()
        return instance

# Specialized Forms
class HomeBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'placement_location', 'desktop_image', 'mobile_image', 'delete_desktop', 'delete_mobile']

class HomeInteriorBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'desktop_image', 'delete_desktop']

class HomeExteriorBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'desktop_image', 'delete_desktop']





class ColourPaletteForm(BaseImageForm):
    delete_entry = forms.BooleanField(required=False, label="Delete this Colour Palette", initial=False)

    class Meta:
        model = ColourPalette
        fields = ['title', 'description', 'colour_code', 'colour_code_category', 'image_field','delete_entry']


class ParallaxForm(BaseImageForm):
    class ParallaxForm(BaseImageForm):
        delete_entry = forms.BooleanField(required=False, label="Delete this Parallax", initial=False)

        class Meta:
            model = Parallax
            fields = ['title', 'sub_title', 'description', 'priority', 'image_field', 'delete_image']


class BrochureForm(forms.ModelForm):
    image_field = forms.ImageField(required=False, label="Upload Image")
    delete_image = forms.BooleanField(required=False, label="Delete Preview Image")
    pdf_field = forms.FileField(required=False, label="Upload PDF")
    delete_pdf = forms.BooleanField(required=False, label="Delete PDF")

    class Meta:
        model = Brochure
        fields = ['image_field', 'pdf_field', 'delete_image', 'delete_pdf']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = self.instance.url or {}
        image_url = url.get('image')

        # Set help text for preview image if available
        if image_url:
            self.fields['image_field'].help_text = mark_safe(
                f'<br><strong>Preview Image:</strong><br>'
                f'<img src="{image_url}" style="max-height: 100px;" /><br>'
                f'<strong>URL:</strong> <a href="{image_url}" target="_blank">{image_url}</a>'
            )

        # Set help text for uploaded PDF if available
        if self.instance.uploaded_pdf:
            self.fields['pdf_field'].help_text = mark_safe(
                f'<br><strong>Uploaded PDF:</strong><br>'
                f'<a href="/media/brochures/{self.instance.uploaded_pdf}" target="_blank">'
                f'{self.instance.uploaded_pdf}</a>'
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        url_data = instance.url or {}

        # Delete the image if "delete_image" is checked
        if self.cleaned_data.get('delete_image'):
            url_data.pop('image', None)
            if instance.image:
                instance.image.delete()

        # Delete the PDF if "delete_pdf" is checked
        if self.cleaned_data.get('delete_pdf'):
            instance.uploaded_pdf = ""

        # Save the new image if an image is provided
        if self.cleaned_data.get('image_field'):
            image_path = default_storage.save(
                f'brochures/images/{self.cleaned_data["image_field"].name}',
                self.cleaned_data["image_field"]
            )
            url_data['image'] = default_storage.url(image_path)

        # Save the new PDF if a PDF is provided
        if self.cleaned_data.get('pdf_field'):
            pdf_path = default_storage.save(
                f'brochures/{self.cleaned_data["pdf_field"].name}',
                self.cleaned_data["pdf_field"]
            )
            instance.uploaded_pdf = self.cleaned_data["pdf_field"].name

        instance.url = url_data

        if commit:
            instance.save()
        return instance




class AdditionalInfoForm(BaseImageForm):
    delete_entry = forms.BooleanField(required=False, label="Delete this Additional Info", initial=False)

    class Meta:
        model = AdditionalInfo
        fields = ['type', 'title', 'description', 'details', 'image_field', 'delete_image']






class AdminContactDetailsForm(forms.ModelForm):
    delete_entry = forms.BooleanField(required=False, label="Delete this Admin Contact Details", initial=False)

    class Meta:
        model = AdminContactDetails
        fields = ['location', 'phone_number', 'email', 'google_link', 'social_media_links']


class CategoryForm(forms.ModelForm):
    delete_entry = forms.BooleanField(required=False, label="Delete this Category", initial=False)

    class Meta:
        model = Category
        fields = ['name', 'subcategory_name']



class ProductForm(BaseImageForm):
    class Meta:
        model = Product
        fields = ['title', 'keyfeature', 'description', 'category']

class HomeForm(forms.ModelForm):
    category_image_field = forms.ImageField(required=False, label="Category Image")
    type_image_field = forms.ImageField(required=False, label="Type Image")

    class Meta:
        model = Home
        fields = [
            'title',
            'type',
            'category_name',
            'subcategory_name',
            'title_type',
            'category_images',  # Include model fields here
            'type_images',      # Include model fields here
            'type_description',
            'banners',
        ]

    # Exclude unwanted fields from the form display
    exclude = ['id', 'created_on', 'updated_on']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle category_images
        category_images = instance.category_images or {}
        if self.cleaned_data.get('category_image_field'):
            path = default_storage.save(
                f'uploads/{self.cleaned_data["category_image_field"].name}',
                self.cleaned_data["category_image_field"]
            )
            category_images['image'] = default_storage.url(path)
            instance.category_images = category_images

        # Handle type_images
        type_images = instance.type_images or {}
        if self.cleaned_data.get('type_image_field'):
            path = default_storage.save(
                f'uploads/{self.cleaned_data["type_image_field"].name}',
                self.cleaned_data["type_image_field"]
            )
            type_images['image'] = default_storage.url(path)
            instance.type_images = type_images

        if commit:
            instance.save()
        return instance

