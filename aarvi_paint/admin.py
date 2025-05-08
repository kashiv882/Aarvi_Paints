from django.contrib import admin
from django.contrib.admin import AdminSite

from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from .forms import HomeBannerForm, HomeInteriorBannerForm, HomeExteriorBannerForm, ColourPaletteForm, ParallaxForm, \
    BrochureForm, AdditionalInfoForm, AdminContactDetailsForm, CategoryForm, ProductForm, HomeForm, GalleryBannerForm, \
    AboutUsTopBannerForm, ColorPalletsBannerForm, ProductBannerForm, ContactUsBannerForm, HomeWaterproofingBannerForm, \
    AboutUsBottomVideoBannerForm, AboutUsForm, SettingAdminForm
from .models import HomeExteriorBanner, HomeInteriorBanner, PaintBudgetCalculator, ColourPalette, \
    Parallax, Brochure, AdditionalInfo, AdminContactDetails, WaterProofCalculator, Category, Product, UserInfo, Home, \
    Banner, GalleryBanner, AboutUsTopBanner, ColorPalletsBanner, ProductBanner, ContactUsBanner, \
    HomeWaterproofingBanner, AboutUsBottomVideoBanner, HomeBanner, AboutUs, Setting

# Unregister default auth models (optional if you only want superuser access)
admin.site.unregister(User)
admin.site.unregister(Group)


class CustomAdminSite(AdminSite):
    site_header = None
    site_title = None
    index_title = None


admin_site = CustomAdminSite(name='customadmin')

# =========================================================================================================================================================================

try:
    admin.site.unregister(Banner)
except admin.sites.NotRegistered:
    pass


# Shared method to display image URLs
# def display_image_urls(self, obj):
#     if not obj.url:
#         return "No images uploaded."
#     html = ''
#     if 'image' in obj.url:
#         html += f"<strong>Image:</strong> <a href='{obj.url['image']}' target='_blank'>{obj.url['image']}</a><br>"
#     return mark_safe(html)

# display_image_urls.short_description = "Image URLs"


def display_media_urls(self, obj):
    if not obj.url:
        return "No media uploaded."

    html = ''
    if 'image' in obj.url:
        html += (
            f"<strong>Image:</strong><br>"
            f"<a href='{obj.url['image']}' target='_blank'>"
            f"<img src='{obj.url['image']}' style='max-height: 100px;' /></a><br>"
        )
    if 'video' in obj.url:
        html += (
            f"<strong>Video:</strong><br>"
            f"<video width='320' height='240' controls>"
            f"<source src='{obj.url['video']}' type='video/mp4'>"
            f"Your browser does not support the video tag.</video><br>"
            f"<a href='{obj.url['video']}' target='_blank'>{obj.url['video']}</a><br>"
        )

    return mark_safe(html)


display_media_urls.short_description = "Media URLs"


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    form = HomeBannerForm
    list_display = ['type', 'display_image_urls']
    exclude = ['short_description']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-banner')

    display_image_urls = display_media_urls


@admin.register(GalleryBanner)
class GalleryBannerAdmin(admin.ModelAdmin):
    form = GalleryBannerForm
    list_display = ['type', 'display_video_urls']
    exclude = ['url']
    readonly_fields = ['display_video_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='gallery-banner')

    display_video_urls = display_media_urls


@admin.register(HomeInteriorBanner)
class HomeInteriorBannerAdmin(admin.ModelAdmin):
    form = HomeInteriorBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-interior-banner')

    display_image_urls = display_media_urls


@admin.register(HomeExteriorBanner)
class HomeExteriorBannerAdmin(admin.ModelAdmin):
    form = HomeExteriorBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls']
    exclude = ['url']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-exterior-banner')

    display_image_urls = display_media_urls


@admin.register(HomeWaterproofingBanner)
class HomeWaterproofingBannerAdmin(admin.ModelAdmin):
    form = HomeWaterproofingBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls']
    exclude = ['url']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-waterproofing-banner')

    display_image_urls = display_media_urls


@admin.register(AboutUsTopBanner)
class AboutUsTopBannerAdmin(admin.ModelAdmin):
    form = AboutUsTopBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls']
    exclude = ['url']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='about-us-top-banner')

    display_image_urls = display_media_urls


@admin.register(ColorPalletsBanner)
class ColorPalletsBannerAdmin(admin.ModelAdmin):
    form = ColorPalletsBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls']
    exclude = ['url']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='color-pallets-banner')

    display_image_urls = display_media_urls


@admin.register(ProductBanner)
class ProductBannerAdmin(admin.ModelAdmin):
    form = ProductBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls']
    exclude = ['url']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='product-banner')

    display_image_urls = display_media_urls


@admin.register(ContactUsBanner)
class ContactUsBannerAdmin(admin.ModelAdmin):
    form = ContactUsBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls']
    exclude = ['url']
    readonly_fields = ['display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='contact-us-banner')

    display_image_urls = display_media_urls


@admin.register(AboutUsBottomVideoBanner)
class AboutUsBottomVideoBannerAdmin(admin.ModelAdmin):
    form = AboutUsBottomVideoBannerForm
    list_display = ['type', 'display_video_urls']
    exclude = ['url']
    readonly_fields = ['display_video_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='about-us-bottom-video-banner')

    display_video_urls = display_media_urls

@admin.register(PaintBudgetCalculator)
class PaintBudgetCalculatorAdmin(admin.ModelAdmin):
    list_display = [
        'area_type',
        'surface_condition',
        'selected_product',
        'entered_area',
        'get_user_name',
        'get_user_email',
        'get_user_phone',
        'get_user_pincode',
        'get_user_type',
        'get_user_description',
        'get_user_source',
    ]
    readonly_fields = [f.name for f in PaintBudgetCalculator._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Custom display methods for related UserInfo fields
    def get_user_name(self, obj):
        return obj.userinfo.name
    get_user_name.short_description = "User Name"

    def get_user_email(self, obj):
        return obj.userinfo.email
    get_user_email.short_description = "Email"

    def get_user_phone(self, obj):
        return obj.userinfo.phone_number
    get_user_phone.short_description = "Phone"

    def get_user_pincode(self, obj):
        return obj.userinfo.pincode
    get_user_pincode.short_description = "Pincode"

    def get_user_type(self, obj):
        return obj.userinfo.type
    get_user_type.short_description = "Type"

    def get_user_description(self, obj):
        return obj.userinfo.description
    get_user_description.short_description = "Description"

    def get_user_source(self, obj):
        return obj.userinfo.source
    get_user_source.short_description = "Source"


@admin.register(ColourPalette)
class ColourPaletteAdmin(admin.ModelAdmin):
    form = ColourPaletteForm

    list_display = ['title', 'colour_code', 'colour_code_category', 'get_image_preview','description']
    search_fields = ['title', 'colour_code', 'colour_code_category']
    list_filter = ['colour_code_category']
    readonly_fields = ['get_image_preview']

    def get_image_preview(self, obj):
        # Assuming 'url' field contains a key 'image' or similar
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image available"

    get_image_preview.short_description = "Preview"


@admin.register(Parallax)
class ParallaxAdmin(admin.ModelAdmin):
    form = ParallaxForm
    exclude = ('url',)

    list_display = ['title', 'sub_title', 'description', 'priority', 'get_desktop_preview', 'get_mobile_preview']
    search_fields = ['title', 'sub_title']
    list_filter = ['priority']
    readonly_fields = ['get_desktop_preview', 'get_mobile_preview']

    def get_desktop_preview(self, obj):
        if obj.url and 'desktop' in obj.url:
            desktop_url = obj.url['desktop']
            return mark_safe(f'<img src="{desktop_url}" style="max-height: 100px; border: 1px solid #ccc;" />')
        return "No desktop image available"

    get_desktop_preview.short_description = "Desktop Image Preview"

    def get_mobile_preview(self, obj):
        if obj.url and 'mobile' in obj.url:
            mobile_url = obj.url['mobile']
            return mark_safe(f'<img src="{mobile_url}" style="max-height: 100px; border: 1px solid #ccc;" />')
        return "No mobile image available"

    get_mobile_preview.short_description = "Mobile Image Preview"


@admin.register(Brochure)
class BrochureAdmin(admin.ModelAdmin):
    form = BrochureForm
    readonly_fields = ['preview_image', 'preview_pdf']
    list_display = ['uploaded_pdf', 'preview_image']

    def preview_image(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No preview image"

    def preview_pdf(self, obj):
        if obj.uploaded_pdf:
            return mark_safe(f'<a href="/media/brochures/{obj.uploaded_pdf}" target="_blank">View PDF</a>')
        return "No PDF uploaded"

    preview_image.short_description = "Preview Image"
    preview_pdf.short_description = "Uploaded PDF"


@admin.register(AdditionalInfo)
class AdditionalInfoAdmin(admin.ModelAdmin):
    form = AdditionalInfoForm
    list_display = ['type', 'title', 'preview_image' , 'description', 'details']
    search_fields = ['type', 'title', 'description','details']
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image"

    preview_image.short_description = "Image Preview"


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsForm
    list_display = ['title','sub_title','description','details','preview_image']
    search_fields = ['title','sub_title','description']
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image"

    preview_image.short_description = "Image Preview"



@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    form = HomeForm

    def get_image_preview(self, obj):
        try:
            category_img = next(iter(obj.category_images.values()), None)
            type_img = next(iter(obj.type_images.values()), None)
            image_url = category_img or type_img
            if image_url:
                return mark_safe(f'<img src="{image_url}" style="max-height: 100px; border: 1px solid #ccc;" />')
        except Exception:
            pass
        return "No image available"

    list_display = [
        'title',
        'type',
        'category_name',
        'subcategory_name',
        'title_type',
        'get_banner_title',
        'get_banner_type',
        'get_banner_placement_location',
        'get_banner_short_description',
        'category_images',
        'type_images',
        'type_description',
        'get_image_preview',
    ]



    # Define methods for displaying related data in the admin
    def get_banner_title(self, obj):
        return obj.banners.title
    get_banner_title.short_description = "Banner Title"

    def get_banner_type(self, obj):
        return obj.banners.type
    get_banner_type.short_description = "Banner Type"

    def get_banner_placement_location(self, obj):
        return obj.banners.placement_location
    get_banner_placement_location.short_description = "Banner Placement Location"

    def get_banner_short_description(self, obj):
        return obj.banners.short_description
    get_banner_short_description.short_description = "Banner Short Description"



@admin.register(AdminContactDetails)
class AdminContactDetailsAdmin(admin.ModelAdmin):
    form = AdminContactDetailsForm

    list_display = [
        'location',
        'phone_number',
        'email',
        'google_link',
        'display_social_media_links'
    ]

    search_fields = [
        'location',
        'phone_number',
        'email',
        'google_link',
    ]

    def display_social_media_links(self, obj):
        links = obj.social_media_links or {}
        instagram = links.get('instagram', '')
        facebook = links.get('facebook', '')
        whatsapp = links.get('whatsapp', '')
        return f"Insta: {instagram}, FB: {facebook}, WA: {whatsapp}"

    display_social_media_links.short_description = "Social Media Links"

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    form = SettingAdminForm

    list_display = [
        'name',
        'copyright',
        'display_app_download_links',
        'get_logo_preview',  # Preview for logo
        'get_side_image_preview',  # Preview for side image
    ]

    search_fields = [
        'name',
    ]

    def display_app_download_links(self, obj):
        links = obj.app_download_links or {}
        playstore = links.get('playstore', '')
        appstore = links.get('appstore', '')
        return f"Play Store: {playstore}, App Store: {appstore}"

    display_app_download_links.short_description = "App Download Links"

    def get_logo_preview(self, obj):
        if obj.url and 'logo' in obj.url:
            logo_url = obj.url['logo']
            return mark_safe(f'<img src="{logo_url}" style="max-height: 50px; border: 1px solid #ccc;" />')
        return "No logo available"

    get_logo_preview.short_description = "Logo Preview"

    def get_side_image_preview(self, obj):
        if obj.url and 'side_image' in obj.url:
            side_image_url = obj.url['side_image']
            return mark_safe(f'<img src="{side_image_url}" style="max-height: 50px; border: 1px solid #ccc;" />')
        return "No side image available"

    get_side_image_preview.short_description = "Side Image Preview"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm  # your custom form that handles comma-separated subcategories

    list_display = ['name', 'display_subcategories']
    search_fields = ['name']

    def display_subcategories(self, obj):
        return ", ".join(obj.subcategory_names or [])
    display_subcategories.short_description = 'Subcategories'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['title', 'subtitle', 'short_description', 'long_description', 'keyfeature',
                  'get_category_name', 'subcategory', 'colour_palate1', 'colour_palate2','get_image_preview']

    search_fields = ['title', 'keyfeature']
    list_filter = ['category']

    def get_category_name(self, obj):
        return obj.category.name
    get_category_name.short_description = "Category Name"

    def get_image_preview(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image"
    get_image_preview.short_description = "Image Preview"

    class Media:
        js = ('js/product_subcategory.js',)

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'phone_number',
        'pincode',
        'type',
        'description',
        'source',
    ]
    readonly_fields = [f.name for f in UserInfo._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WaterProofCalculator)
class WaterProofCalculatorAdmin(admin.ModelAdmin):
    list_display = [
        'surface_condition',
        'selected_product',
        'entered_area',
        'description',
        'get_user_name',
        'get_user_email',
        'get_user_phone',
        'get_user_pincode',
        'get_user_type',
        'get_user_description',
        'get_user_source',
    ]
    readonly_fields = [f.name for f in WaterProofCalculator._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # UserInfo field accessors
    def get_user_name(self, obj):
        return obj.userinfo.name
    get_user_name.short_description = "User Name"

    def get_user_email(self, obj):
        return obj.userinfo.email
    get_user_email.short_description = "Email"

    def get_user_phone(self, obj):
        return obj.userinfo.phone_number
    get_user_phone.short_description = "Phone"

    def get_user_pincode(self, obj):
        return obj.userinfo.pincode
    get_user_pincode.short_description = "Pincode"

    def get_user_type(self, obj):
        return obj.userinfo.type
    get_user_type.short_description = "Type"

    def get_user_description(self, obj):
        return obj.userinfo.description
    get_user_description.short_description = "Description"

    def get_user_source(self, obj):
        return obj.userinfo.source
    get_user_source.short_description = "Source"