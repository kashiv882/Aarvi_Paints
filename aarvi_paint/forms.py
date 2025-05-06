from django import forms
from .models import Banner, Parallax, ColourPalette, Brochure, AdditionalInfo, AdminContactDetails, Category, Product, Home,BannerImage,HomeBanner
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils.html import format_html
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


# ===============================================================================Snkalp=========================


# class BaseHomeForm(forms.ModelForm):
#     home_image = forms.ImageField(required=False)
#     delete_image = forms.BooleanField(required=False, label='Delete Image')

#     # banner_video = forms.FileField(required=False)
#     # delete_video = forms.BooleanField(required=False, label='Delete Banner Video')

#     class Meta:
#         model = Home
#         fields = [
#             'title', 'banners', 'category_name', 'subcategory_name',
#             'category_images', 'type_description', 'title_type'
#         ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         image_data = self.instance.category_images or {}

#         home_image_url = image_data.get('image')

#         if home_image_url:
#             self.fields['home_image'].help_text = mark_safe(
#                 f'<br><strong>Home Image Preview:</strong><br>'
#                 f'<img src="{home_image_url}" style="max-height: 100px;" /><br>'
#                 f'<strong>URL:</strong> <a href="{home_image_url}" target="_blank">{home_image_url}</a>'
#             )
#         # if video_url:
#         #     self.fields['banner_video'].help_text = mark_safe(
#         #         f'<br><strong>Video Preview:</strong><br>'
#         #         f'<video width="320" height="240" controls>'
#         #         f'<source src="{video_url}" type="video/mp4">'
#         #         f'Your browser does not support the video tag.'
#         #         f'</video><br>'
#         #         f'<strong>URL:</strong> <a href="{video_url}" target="_blank">{video_url}</a>'
#         #     )

#     def save(self, commit=True):
#         instance = super().save(commit=False)

#         image_data = instance.category_images or {}

#         # Delete logic
#         if self.cleaned_data.get('delete_image'):
#             image_data.pop('image', None)

#         # Upload logic
#         if self.cleaned_data.get('home_image'):
#             path = default_storage.save(
#                 f'home/image/{self.cleaned_data["home_image"].name}',
#                 self.cleaned_data["home_image"]
#             )
#             image_data['image'] = default_storage.url(path)

#         instance.category_images = image_data

#         if commit:
#             instance.save()
#         return instance

class BaseHomeInteriorForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['title', 'type_description']

class HomeInteriorForm(BaseHomeInteriorForm):
    class Meta(BaseHomeInteriorForm.Meta):
        fields = ['title', 'type_description']

#home exterior data
class BaseHomeExteriordataForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['title', 'type_description']

class HomeExteriordataForm(BaseHomeExteriordataForm):
    class Meta(BaseHomeExteriordataForm.Meta):
        fields = ['title', 'type_description']



#Working
# class BaseHomeInteriorDifferentRoomForm(forms.ModelForm):
#     image = forms.ImageField(required=False)

#     class Meta:
#         model = Home
#         fields = ['title', 'type_description', 'image']

#     def save(self, commit=True):
#         instance = super().save(commit=False)

#         # If an image is uploaded, store its URL in `category_images`
#         image = self.cleaned_data.get('image')
#         if image:
#             image_url = default_storage.save(f'home/{image.name}', image)
#             full_url = default_storage.url(image_url)
#             instance.category_images = {'image': full_url}

#         if commit:
#             instance.save()
#         return instance



class BaseHomeInteriorDifferentRoomForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    delete_image = forms.BooleanField(required=False, label="Delete current image")

    class Meta:
        model = Home
        fields = ['title', 'type_description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Display image preview if exists
        if self.instance and self.instance.category_images.get('image'):
            image_url = self.instance.category_images['image']
            self.fields['image'].help_text = mark_safe(
                f'<img src="{image_url}" width="200" style="margin-top:10px;" /><br/>'
                f'Upload a new image to replace the current one.'
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle image deletion
        if self.cleaned_data.get('delete_image'):
            instance.category_images = {}

        # Save new image if provided
        image = self.cleaned_data.get('image')
        if image:
            image_url = default_storage.save(f'home/{image.name}', image)
            full_url = default_storage.url(image_url)
            instance.category_images = {'image': full_url}

        if commit:
            instance.save()
        return instance



class HomeInteriorDifferentRoomForm(BaseHomeInteriorDifferentRoomForm):
    class Meta(BaseHomeInteriorDifferentRoomForm.Meta):
        fields = ['title', 'type_description', 'image']

# ==================================multiple image============================================
class BaseBannerMultipleImageForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = []  # Exclude all fields for now, except for those that are editable
        # We don't include 'type' in the form anymore, as it's non-editable

# Form for BannerImage inline to handle multiple images
class BannerImageInlineForm(forms.ModelForm):
    class Meta:
        model = BannerImage
        fields = ['image']  # Only allow uploading images

# Inline model for BannerImage
class BannerImageInline(admin.TabularInline):
    model = BannerImage
    form = BannerImageInlineForm
    extra = 1  # Allow adding 1 extra inline image
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" style="object-fit:contain;"/>', obj.image.url)
        return "No image"

    image_preview.short_description = "Preview"




















class GalleryBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['banner_image']








# ================================================================================================================
class BannerImageForm(BaseImageForm):
    class Meta:
        model = HomeBanner
        fields = [ 'image_field']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance.pk and self.instance.image:
    #         self.fields['image'].widget = forms.ClearableFileInput()



# class HomeBannerForm(BaseBannerForm):
#     class Meta(BaseBannerForm.Meta):
#         fields = ['banner_image']


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
