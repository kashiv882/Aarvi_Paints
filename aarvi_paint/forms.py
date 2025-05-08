from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import Select, SelectMultiple

from .models import Banner, Parallax, ColourPalette, Brochure, AdditionalInfo, AdminContactDetails, Category, Product, \
    Home, AboutUs, Setting, HomeExterior, HomeWaterProof
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
        description = forms.CharField(widget=CKEditorWidget())
        model = ColourPalette
        fields = ['title', 'description', 'colour_code', 'colour_code_category']

class ParallaxForm(forms.ModelForm):
    desktop = forms.ImageField(required=False, label="Desktop Image")
    mobile = forms.ImageField(required=False, label="Mobile Image")
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Parallax
        fields = ['title', 'sub_title', 'description', 'priority', 'desktop', 'mobile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.url:
            urls = self.instance.url
            self.fields['desktop'].initial = urls.get('desktop', '')
            self.fields['mobile'].initial = urls.get('mobile', '')

    def clean(self):
        cleaned_data = super().clean()

        desktop = cleaned_data.get('desktop')
        mobile = cleaned_data.get('mobile')

        url_data = self.instance.url or {}

        if desktop:
            desktop_path = default_storage.save(f'parallax/desktop/{desktop.name}', desktop)
            url_data['desktop'] = default_storage.url(desktop_path)

        if mobile:
            mobile_path = default_storage.save(f'parallax/mobile/{mobile.name}', mobile)
            url_data['mobile'] = default_storage.url(mobile_path)

        cleaned_data['url'] = url_data

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.url = self.cleaned_data.get('url', {})
        if commit:
            instance.save()
        return instance


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




class SettingAdminForm(forms.ModelForm):
    playstore = forms.URLField(required=False, label="Play Store Link")
    appstore = forms.URLField(required=False, label="App Store Link")
    logo = forms.ImageField(required=False, label="Logo Image")
    side_image = forms.ImageField(required=False, label="Side Image")

    class Meta:
        model = Setting
        fields = ['name', 'copyright', 'logo', 'side_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.app_download_links:
            links = self.instance.app_download_links
            self.fields['playstore'].initial = links.get('playstore', '')
            self.fields['appstore'].initial = links.get('appstore', '')

    def clean(self):
        cleaned_data = super().clean()

        # Handle logo and side image uploads
        app_download_links = {
            'playstore': cleaned_data.get('playstore', ''),
            'appstore': cleaned_data.get('appstore', ''),
        }

        # Save logo and side image and get their URLs
        logo = cleaned_data.get('logo')
        side_image = cleaned_data.get('side_image')

        url_data = {}
        if logo:
            # Save logo and get the URL
            logo_path = default_storage.save(f'logos/{logo.name}', logo)
            url_data['logo'] = default_storage.url(logo_path)

        if side_image:
            # Save side image and get the URL
            side_image_path = default_storage.save(f'side_images/{side_image.name}', side_image)
            url_data['side_image'] = default_storage.url(side_image_path)

        # Save the URLs in the `url` field
        cleaned_data['url'] = url_data
        cleaned_data['app_download_links'] = app_download_links

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.app_download_links = self.cleaned_data['app_download_links']
        instance.url = self.cleaned_data['url']
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
    subcategory = forms.MultipleChoiceField(
        required=False,
        choices=[('', 'Select category first')],
        widget=SelectMultiple
    )
    short_description = forms.CharField(widget=CKEditorWidget())
    long_description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = ['title', 'subtitle', 'short_description', 'long_description', 'keyfeature',
                  'category', 'subcategory', 'colour_palate1', 'colour_palate2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].widget = forms.Select(choices=self.fields['category'].choices)

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


class HomeInteriorForm(forms.ModelForm):
    category_name = forms.CharField(
        widget=forms.Textarea,
        help_text="Comma-separated category names"
    )
    subcategory_name = forms.CharField(
        widget=forms.Textarea,
        help_text="Comma-separated subcategory names"
    )
    category_image = forms.ImageField(required=False, label="Category Image")
    type_image = forms.ImageField(required=False, label="Type Image")

    class Meta:
        model = Home
        fields = ['title', 'title_type', 'type_description', 'description', 'category_name', 'subcategory_name']

    def clean(self):
        cleaned_data = super().clean()

        # Handle single image uploads
        category_image_file = self.files.get('category_image')
        type_image_file = self.files.get('type_image')

        if category_image_file:
            category_image_path = default_storage.save(f'category_images/{category_image_file.name}', category_image_file)
            cleaned_data['category_images'] = [default_storage.url(category_image_path)]
        else:
            cleaned_data['category_images'] = []

        if type_image_file:
            type_image_path = default_storage.save(f'type_images/{type_image_file.name}', type_image_file)
            cleaned_data['type_images'] = [default_storage.url(type_image_path)]
        else:
            cleaned_data['type_images'] = []

        # Clean comma-separated fields
        cleaned_data['category_name'] = [x.strip() for x in cleaned_data.get('category_name', '').split(',')]
        cleaned_data['subcategory_name'] = [x.strip() for x in cleaned_data.get('subcategory_name', '').split(',')]

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Forcefully set type for proxy
        instance.type = "HomeInterior"

        instance.type_images = self.cleaned_data.get('type_images', [])
        instance.category_images = self.cleaned_data.get('category_images', [])
        instance.category_name = self.cleaned_data.get('category_name', [])
        instance.subcategory_name = self.cleaned_data.get('subcategory_name', [])

        if commit:
            instance.save()
        return instance


class HomeExteriorForm(forms.ModelForm):
    category_name = forms.CharField(
        label="Categories",
        widget=forms.TextInput(attrs={'placeholder': 'Enter categories separated by commas'})
    )
    category_images = forms.ImageField()

    class Meta:
        model = HomeExterior
        fields = ['title', 'description', 'category_name', 'category_images']

    def clean_category_name(self):
        data = self.cleaned_data['category_name']
        # Optionally clean and split by commas to store as list or stringified list
        categories = [cat.strip() for cat in data.split(',') if cat.strip()]
        return ', '.join(categories)  # or return categories to store as list in JSONField

    def save(self, commit=True):
        instance = super().save(commit=False)

        images = self.files.getlist('category_images')
        image_urls = []
        for img in images:

            path = default_storage.save(f"category_images/{img.name}", img)
            image_urls.append(default_storage.url(path))

        instance.category_images = image_urls

        if commit:
            instance.save()
        return instance

class HomeWaterProofForm(forms.ModelForm):
    category = forms.CharField(
        widget=forms.Textarea,
        help_text="Comma-separated category names"
    )
    sideimage = forms.ImageField(required=False, label="Side Image")

    class Meta:
        model = HomeWaterProof
        fields = ['title', 'description', 'category', 'sideimage']

    def clean(self):
        cleaned_data = super().clean()

        # Handle single image upload for sideimage
        sideimage_file = self.files.get('sideimage')
        if sideimage_file:
            sideimage_path = default_storage.save(f'side_images/{sideimage_file.name}', sideimage_file)
            cleaned_data['sideimage_url'] = default_storage.url(sideimage_path)
        else:
            cleaned_data['sideimage_url'] = ""

        # Clean category as comma-separated values
        cleaned_data['category'] = [x.strip() for x in cleaned_data.get('category', '').split(',')]

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Save the sideimage URL and category
        instance.sideimage_url = self.cleaned_data.get('sideimage_url', "")
        instance.category = self.cleaned_data.get('category', [])

        if commit:
            instance.save()
        return instance