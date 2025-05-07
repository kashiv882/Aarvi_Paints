from django import forms
import uuid
import os
from django.conf import settings
from .models import Banner, Parallax, ColourPalette, Brochure, AdditionalInfo, AdminContactDetails,\
         Category, Product, Home,BannerImage,Testimonial,HomeBanner,AboutUs,Inspiration,Calculator
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils.html import format_html
from .utils.base_image_handler import BaseImageForm
from django.core.files.base import ContentFile
import requests
from urllib.parse import urlparse



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

# ===================================================Home enterior=========================================================


class HomeAdminForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = '__all__'

    def clean_type(self):
        type_value = self.cleaned_data['type']
        valid_types = dict(Home_Type_CHOICES).keys()
        if type_value not in valid_types:
            raise forms.ValidationError("Invalid home type selected.")
        return type_value

    def clean(self):
        cleaned_data = super().clean()
        title_type = cleaned_data.get('title_type')
        type_description = cleaned_data.get('type_description')

        if title_type and not type_description:
            raise forms.ValidationError("Type description is required when title_type is set.")


# ==============================================water proofing===========================================

class WaterproofHomeForm(forms.ModelForm):
    new_image = forms.ImageField(
        required=False,
        label="Upload New Image",
        help_text="Image will replace the current one"
    )

    class Meta:
        model = Home
        fields = ['title_type', 'type_description',]

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_image = self.cleaned_data.get('new_image')
        
        if new_image:
            # Generate unique filename
            ext = os.path.splitext(new_image.name)[1]
            filename = f"{uuid.uuid4()}{ext}"
            upload_path = os.path.join('waterproof', filename)
            
            # Save file using Django's storage system
            default_storage.save(upload_path, new_image)
            
            # Update JSON field
            instance.type_images = {
                'url': default_storage.url(upload_path),
                'name': filename,
                'path': upload_path
            }
        
        if commit:
            instance.save()
        return instance
# ============================================================================================================

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


# =============================================color pallet ==============================================
















class GalleryBannerForm(BaseBannerForm):
    class Meta(BaseBannerForm.Meta):
        fields = ['banner_image']








# ==========================================Home banner======================================================================


class HomeBannerImageForm(forms.ModelForm):
    class Meta:
        model = HomeBanner
        fields = []  

# ==================================================================================================================

# ====================================================About Uss================================================================

class AboutUsAdminForm(forms.ModelForm):
    lower_title = forms.CharField(
        max_length=200, 
        required=False, 
        label="Lower Title",
        help_text="Title for the lower section"
    )
    lower_sub_title = forms.CharField(
        max_length=200, 
        required=False, 
        label="Lower Sub Title",
        help_text="Sub title for the lower section"
    )
    lower_description = forms.CharField(
        widget=forms.Textarea, 
        required=False, 
        label="Lower Description",
        help_text="Description for the lower section"
    )
    extra_info = forms.CharField(
        widget=forms.Textarea, 
        required=False, 
        label="Extra Info",
        help_text="Additional information to display"
    )

    class Meta:
        model = AboutUs
        fields = ['title', 'sub_title', 'description', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.details:
            details = self.instance.details
            self.fields['lower_title'].initial = details.get('lower_title', '')
            self.fields['lower_sub_title'].initial = details.get('lower_sub_title', '')
            self.fields['lower_description'].initial = details.get('lower_description', '')
            self.fields['extra_info'].initial = details.get('extra_info', '')

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['details'] = {
            'lower_title': cleaned_data.get('lower_title', ''),
            'lower_sub_title': cleaned_data.get('lower_sub_title', ''),
            'lower_description': cleaned_data.get('lower_description', ''),
            'extra_info': cleaned_data.get('extra_info', ''),
        }
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.details = self.cleaned_data['details']
        if commit:
            instance.save()
        return instance






# ===============================================================================================================================

# =========================================================Additional info Inspiration==============================================

class InspirationForm(forms.ModelForm):
    SECTION_CHOICES = [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
    ]
    
    section = forms.ChoiceField(choices=SECTION_CHOICES, label="Inspiration Section")
    image = forms.URLField(required=False, label="Image URL")
    current_image = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Inspiration
        fields = ['section', 'title', 'description', 'image', 'details']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['section'].initial = self.instance.type
            self.fields['image'].initial = self.instance.url.get('image', '')
            self.fields['current_image'].initial = self.instance.url.get('image', '')

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['type'] = cleaned_data.get('section')
        
        image_url = cleaned_data.get('image', '')
        if image_url:
            cleaned_data['url'] = {'image': image_url}
        else:
            # Keep existing image if no new one provided
            cleaned_data['url'] = {'image': cleaned_data.get('current_image', '')}
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = self.cleaned_data['type']
        instance.url = self.cleaned_data['url']
        
        if commit:
            instance.save()
        return instance

    def image_preview(self):
        if self.instance and self.instance.url.get('image'):
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                self.instance.url['image']
            )
        return "No image uploaded"
    image_preview.short_description = 'Preview'




# ========================================================================================================================================

# =============================================================additional info testimonial=================================================

class TestimonialAdminForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True, label="Name")
    description = forms.CharField(widget=forms.Textarea, required=True, label="Description")
    image = forms.ImageField(required=False, label="Upload Image")
    delete_image = forms.BooleanField(required=False, label="Delete Existing Image")

    class Meta:
        model = Testimonial
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['name'].initial = self.instance.title
            self.fields['description'].initial = self.instance.description

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.title = self.cleaned_data['name']
        instance.description = self.cleaned_data['description']

        # Handle image deletion
        if self.cleaned_data.get('delete_image'):
            instance.url = {}

        # Handle image upload
        image_file = self.cleaned_data.get('image')
        if image_file:
            path = default_storage.save(f"uploads/testimonials/{image_file.name}", ContentFile(image_file.read()))
            image_url = default_storage.url(path)
            instance.url = {'image': image_url}

        if commit:
            instance.save()
        return instance







# ===========================================================================================================================================


#  ===========================================================additional info paint budgt calculator================================================================================
class CalculatorAdminForm(forms.ModelForm):
    product = forms.CharField(required=True, label="Enter Product Name")
    area = forms.FloatField(required=True, label="Enter Area (sq ft)")

    class Meta:
        model = Calculator
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['product'].initial = self.instance.details.get('product', '')
            self.fields['area'].initial = self.instance.details.get('area', '')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.details = {
            'product': self.cleaned_data.get('product'),
            'area': self.cleaned_data.get('area'),
        }
        if commit:
            instance.save()
        return instance

class waterAdminForm(forms.ModelForm):
    product = forms.CharField(required=True, label="Enter Product Name")
    area = forms.FloatField(required=True, label="Enter Area (sq ft)")

    class Meta:
        model = Calculator
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['product'].initial = self.instance.details.get('product', '')
            self.fields['area'].initial = self.instance.details.get('area', '')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.details = {
            'product': self.cleaned_data.get('product'),
            'area': self.cleaned_data.get('area'),
        }
        if commit:
            instance.save()
        return instance



# ===========================================================================================================================================


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
