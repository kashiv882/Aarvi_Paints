from django import forms
from .models import Banner, Parallax, ColourPalette, Brochure, AdditionalInfo, AdminContactDetails, Category, Product, \
    Home, AboutUs
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe

from .utils.base_image_handler import BaseImageForm


# class BaseBannerForm(forms.ModelForm):
#     desktop_image = forms.ImageField(required=False)
#     mobile_image = forms.ImageField(required=False)
#     delete_desktop = forms.BooleanField(required=False, label='Delete Desktop Image')
#     delete_mobile = forms.BooleanField(required=False, label='Delete Mobile Image')
#
#     class Meta:
#         model = Banner
#         fields = ['title', 'short_description', 'placement_location']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         url = self.instance.url or {}
#
#         desktop_url = url.get('desktop')
#         mobile_url = url.get('mobile')
#
#         if desktop_url:
#             self.fields['desktop_image'].help_text = mark_safe(
#                 f'<br><strong>Desktop Preview:</strong><br>'
#                 f'<img src="{desktop_url}" style="max-height: 100px;" /><br>'
#                 f'<strong>URL:</strong> <a href="{desktop_url}" target="_blank">{desktop_url}</a>'
#             )
#
#         if mobile_url:
#             self.fields['mobile_image'].help_text = mark_safe(
#                 f'<br><strong>Mobile Preview:</strong><br>'
#                 f'<img src="{mobile_url}" style="max-height: 100px;" /><br>'
#                 f'<strong>URL:</strong> <a href="{mobile_url}" target="_blank">{mobile_url}</a>'
#             )
#
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         url_data = instance.url or {}
#
#         if self.cleaned_data.get('delete_desktop'):
#             url_data.pop('desktop', None)
#         if self.cleaned_data.get('delete_mobile'):
#             url_data.pop('mobile', None)
#
#         if self.cleaned_data.get('desktop_image'):
#             path = default_storage.save(
#                 f'banners/desktop/{self.cleaned_data["desktop_image"].name}',
#                 self.cleaned_data["desktop_image"]
#             )
#             url_data['desktop'] = default_storage.url(path)
#
#         if self.cleaned_data.get('mobile_image'):
#             path = default_storage.save(
#                 f'banners/mobile/{self.cleaned_data["mobile_image"].name}',
#                 self.cleaned_data["mobile_image"]
#             )
#             url_data['mobile'] = default_storage.url(path)
#
#         instance.url = url_data
#
#         if commit:
#             instance.save()
#         return instance
#
# # Specialized Forms
# class HomeBannerForm(BaseBannerForm):
#     class Meta(BaseBannerForm.Meta):
#         fields = ['title', 'placement_location', 'desktop_image', 'mobile_image', 'delete_desktop', 'delete_mobile']
#
# class HomeInteriorBannerForm(BaseBannerForm):
#     class Meta(BaseBannerForm.Meta):
#         fields = ['title', 'short_description', 'desktop_image', 'delete_desktop']
#
# class HomeExteriorBannerForm(BaseBannerForm):
#     class Meta(BaseBannerForm.Meta):
#         fields = ['title', 'short_description', 'desktop_image', 'delete_desktop']





class ColourPaletteForm(BaseImageForm):

    class Meta:
        model = ColourPalette
        fields = ['title', 'description', 'colour_code', 'colour_code_category']


class ParallaxForm(BaseImageForm):
    class ParallaxForm(BaseImageForm):

        class Meta:
            model = Parallax
            fields = ['title', 'sub_title', 'description', 'priority']


class BrochureForm(forms.ModelForm):
    image_field = forms.ImageField(required=False, label="Upload Image")

    pdf_field = forms.FileField(required=False, label="Upload PDF")


    class Meta:
        model = Brochure
        fields = ['image_field', 'pdf_field']

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


    class Meta:
        model = AdditionalInfo
        fields = ['type', 'title', 'description', 'details']


class AboutUsForm(BaseImageForm):


    class Meta:
        model = AboutUs
        fields = ['title', 'sub_title', 'description', 'details']

class AdminContactDetailsForm(forms.ModelForm):

    instagram = forms.URLField(required=False, label="Instagram Link")
    facebook = forms.URLField(required=False, label="Facebook Link")
    whatsapp = forms.URLField(required=False, label="WhatsApp Link")

    class Meta:
        model = AdminContactDetails
        fields = ['location', 'phone_number', 'email', 'google_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.social_media_links:
            links = self.instance.social_media_links
            self.fields['instagram'].initial = links.get('instagram', '')
            self.fields['facebook'].initial = links.get('facebook', '')
            self.fields['whatsapp'].initial = links.get('whatsapp', '')

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['social_media_links'] = {
            'instagram': cleaned_data.get('instagram', ''),
            'facebook': cleaned_data.get('facebook', ''),
            'whatsapp': cleaned_data.get('whatsapp', ''),
        }
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.social_media_links = self.cleaned_data['social_media_links']
        if commit:
            instance.save()
        return instance

class CategoryForm(forms.ModelForm):
    subcategories = forms.CharField(
        required=False,
        label="Subcategories (comma separated)",
        widget=forms.TextInput()
    )

    class Meta:
        model = Category
        fields = ['name', 'subcategories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.subcategory_names:
            self.fields['subcategories'].initial = ', '.join(self.instance.subcategory_names)

    def clean_subcategories(self):
        data = self.cleaned_data['subcategories']
        return [s.strip() for s in data.split(',') if s.strip()]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subcategory_names = self.cleaned_data.get('subcategories', [])
        if commit:
            instance.save()
        return instance

class ProductForm(BaseImageForm):
    subcategory = forms.ChoiceField(required=False, choices=[('', 'Select category first')])

    class Meta:
        model = Product
        fields = ['title', 'keyfeature', 'description', 'category', 'subcategory']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category = None
        if 'category' in self.data:
            try:
                category = Category.objects.get(id=self.data.get('category'))
            except Category.DoesNotExist:
                pass
        elif self.instance and hasattr(self.instance, 'category') and self.instance.category:
            category = self.instance.category

        if category:
            choices = [(s, s) for s in category.subcategory_names]
            self.fields['subcategory'].choices = choices
            # Pass the selected one as data-attribute for JS
            self.fields['subcategory'].widget.attrs['data-selected'] = self.data.get('subcategory', '')
        else:
            self.fields['subcategory'].choices = [('', 'Select category first')]


class HomeForm(forms.ModelForm):
    category_image_field = forms.ImageField(required=False, label="Category Image")
    type_image_field = forms.ImageField(required=False, label="Type Image")

    class Meta:
        model = Home
        fields = [
            'title',
            'type',
            'banners',
            'category_name',
            'subcategory_name',
            'title_type',
            'type_description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Handle Category Image Preview
        category_url = self.instance.category_images.get('image') if self.instance.category_images else None
        if category_url:
            self.fields['category_image_field'].help_text = mark_safe(
                f'<br><strong>Category Image Preview:</strong><br>'
                f'<img src="{category_url}" style="max-height: 100px;" /><br>'
                f'<strong>URL:</strong> <a href="{category_url}" target="_blank">{category_url}</a>'
            )

        # Handle Type Image Preview
        type_url = self.instance.type_images.get('image') if self.instance.type_images else None
        if type_url:
            self.fields['type_image_field'].help_text = mark_safe(
                f'<br><strong>Type Image Preview:</strong><br>'
                f'<img src="{type_url}" style="max-height: 100px;" /><br>'
                f'<strong>URL:</strong> <a href="{type_url}" target="_blank">{type_url}</a>'
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle Category Image Upload or Delete
        category_data = instance.category_images or {}
        if self.cleaned_data.get('delete_category_image'):
            category_data.pop('image', None)
        if self.cleaned_data.get('category_image_field'):
            path = default_storage.save(
                f'uploads/{self.cleaned_data["category_image_field"].name}',
                self.cleaned_data["category_image_field"]
            )
            category_data['image'] = default_storage.url(path)
        instance.category_images = category_data

        # Handle Type Image Upload or Delete
        type_data = instance.type_images or {}
        if self.cleaned_data.get('delete_type_image'):
            type_data.pop('image', None)
        if self.cleaned_data.get('type_image_field'):
            path = default_storage.save(
                f'uploads/{self.cleaned_data["type_image_field"].name}',
                self.cleaned_data["type_image_field"]
            )
            type_data['image'] = default_storage.url(path)
        instance.type_images = type_data

        if commit:
            instance.save()
        return instance





class BaseBannerForm(forms.ModelForm):
    banner_image = forms.ImageField(required=False)
    delete_image = forms.BooleanField(required=False, label='Delete banner Image')

    # banner_video = forms.FileField(required=False)
    # delete_video = forms.BooleanField(required=False, label='Delete Banner Video')

    class Meta:
        model = Banner
        fields = ['title', 'short_description']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

        from django.utils.safestring import mark_safe  # ensure it's imported

        url = self.instance.url or {}
        banner_image_url = url.get('image')
        # video_url = url.get('video')

        if banner_image_url:
            self.fields['banner_image'].help_text = mark_safe(
                f'<br><strong>Banner Image Preview:</strong><br>'
                f'<img src="{banner_image_url}" style="max-height: 100px;" /><br>'
                f'<strong>URL:</strong> <a href="{banner_image_url}" target="_blank">{banner_image_url}</a>'
            )
        # if video_url:
        #     self.fields['banner_video'].help_text = mark_safe(
        #         f'<br><strong>Video Preview:</strong><br>'
        #         f'<video width="320" height="240" controls>'
        #         f'<source src="{video_url}" type="video/mp4">'
        #         f'Your browser does not support the video tag.'
        #         f'</video><br>'
        #         f'<strong>URL:</strong> <a href="{video_url}" target="_blank">{video_url}</a>'
        #     )

    def save(self, commit=True):
        instance = super().save(commit=False)

        url_data = instance.url or {}

        # Delete logic
        if self.cleaned_data.get('delete_image'):
            url_data.pop('image', None)

        # if self.cleaned_data.get('delete_video'):
        #     url_data.pop('video', None)

        # Upload logic
        if self.cleaned_data.get('banner_image'):
            path = default_storage.save(
                f'banners/image/{self.cleaned_data["banner_image"].name}',
                self.cleaned_data["banner_image"]
            )
            url_data['image'] = default_storage.url(path)

        # if self.cleaned_data.get('banner_video'):
        #     path = default_storage.save(
        #         f'banners/videos/{self.cleaned_data["banner_video"].name}',
        #         self.cleaned_data["banner_video"]
        # )
        #     url_data['video'] = default_storage.url(path)

        instance.url = url_data

        if commit:
            instance.save()
        return instance


class HomeBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['banner_image']

class GalleryBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['banner_image']


class HomeInteriorBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'banner_image']


class HomeExteriorBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'banner_image']


class HomeWaterproofingBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'banner_image']


class AboutUsTopBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'banner_image']


class ColorPalletsBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'banner_image']


class ProductBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'banner_image']


class ContactUsBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'banner_image']


# class AboutUsBottomVideoBannerForm(BaseBannerForm):
#     class Meta(BaseBannerForm.Meta):
#         fields = ['banner_video']


class AboutUsBottomVideoBannerForm(BaseBannerForm):
    video_file = forms.FileField(required=False, label='Upload Video')

    class Meta(BaseBannerForm.Meta):
        fields = ['title', 'short_description', 'video_file']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

        url = self.instance.url or {}
        video_url = url.get('video')

        if video_url:
            self.fields['video_file'].help_text = mark_safe(
                f'<br><strong>Video Preview:</strong><br>'
                f'<video width="320" height="240" controls>'
                f'<source src="{video_url}" type="video/mp4">'
                f'Your browser does not support the video tag.'
                f'</video><br>'
                f'<strong>URL:</strong> <a href="{video_url}" target="_blank">{video_url}</a>'
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        url_data = instance.url or {}

        # Upload logic for video
        if self.cleaned_data.get('video_file'):
            path = default_storage.save(
                f'banners/video/{self.cleaned_data["video_file"].name}',
                self.cleaned_data["video_file"]
            )
            url_data['video'] = default_storage.url(path)

        instance.url = url_data
        if commit:
            instance.save()

        return  instance
