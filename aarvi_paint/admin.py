from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.models import User, Group
from .forms import  HomeInteriorBannerForm, HomeExteriorBannerForm, ColourPaletteForm, ParallaxForm, \
    BrochureForm, AdditionalInfoForm, AdminContactDetailsForm, CategoryForm, ProductForm, HomeForm, GalleryBannerForm, \
    AboutUsTopBannerForm, ColorPalletsBannerForm, ProductBannerForm, ContactUsBannerForm, HomeWaterproofingBannerForm, \
    AboutUsBottomVideoBannerForm,  BaseBannerForm, BannerImageForm
from .models import HomeExteriorBanner, HomeInteriorBanner,  PaintBudgetCalculator, ColourPalette, \
    Parallax, Brochure, AdditionalInfo, AdminContactDetails, WaterProofCalculator, Category, Product, UserInfo, Home, \
    Banner, GalleryBanner, AboutUsTopBanner, ColorPalletsBanner, ProductBanner, ContactUsBanner, \
    HomeWaterproofingBanner, AboutUsBottomVideoBanner, HomeBanner,BannerImage

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

    
# ======================================================================================
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

class BannerImageInline(admin.StackedInline):
    model = BannerImage
    extra = 1
    form = BannerImageForm  # Use the custom form for the inline
    readonly_fields = ['image_preview']

    # Display the preview of the uploaded image
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;" />',
                obj.image.url
            )
        return "No image uploaded"

    image_preview.short_description = "Preview"


# Admin for HomeBanner
class HomeBannerAdmin(admin.ModelAdmin):
    form = BannerImageForm  # Link to the custom form

    list_display = ['type', 'get_image_preview']
    search_fields = ['type']
    list_filter = ['type']
    readonly_fields = ['get_image_preview']

    def get_image_preview(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image available"

    get_image_preview.short_description = "Image Preview"




#     inlines = [BannerImageInline]
#     fields = ['type', 'image_preview']  # Show type and image preview fields
#     readonly_fields = ['type', 'image_preview']

#     # Display type of the banner (for proxy models)
#     def get_type(self, obj):
#         return obj.type

#     # Optionally, show the first image as a preview for the banner
#     def image_preview(self, obj):
#         if obj.images.exists():
#             return format_html(
#                 '<img src="{}" style="max-height: 100px;" />',
#                 obj.images.first().image.url
#             )
#         return "No images uploaded"

#     image_preview.short_description = "Banner Image Preview"

#     # Ensure the type is set correctly for the proxy model
#     def save_model(self, request, obj, form, change):
        
#         obj.type = 'home-banner'  # Make sure the type is always set correctly
#         super().save_model(request, obj, form, change)

#     # Permissions for admin
#     def has_add_permission(self, request):
#         return True

#     def has_change_permission(self, request, obj=None):
#         return True


# # Register HomeBanner model in admin
# admin.site.register(HomeBanner, HomeBannerAdmin)

# class HomeBannerAdmin(admin.ModelAdmin):
#     inlines = [BannerImageInline]
#     list_display = ['type']
#     readonly_fields = ['type']  # Optional: so type can't be changed manually

# admin.site.register(HomeBanner, HomeBannerAdmin)
# @admin.register(HomeBanner)
# class HomeBannerAdmin(admin.ModelAdmin):
#     form = HomeBannerForm
#     list_display = ['type', 'display_image_urls']
#     exclude = ['short_description']
#     readonly_fields = ['display_image_urls']

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type='home-banner')

#     display_image_urls = display_media_urls


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

    list_display = ['title', 'colour_code', 'colour_code_category', 'get_image_preview']
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
    form = ParallaxForm  # Link to the custom form

    list_display = ['title', 'priority', 'get_image_preview']
    search_fields = ['title', 'sub_title']
    list_filter = ['priority']
    readonly_fields = ['get_image_preview']

    def get_image_preview(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image available"

    get_image_preview.short_description = "Image Preview"



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
    search_fields = ['type', 'title', 'preview_image' , 'description','details']
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
        'get_category_images',   # Display methods in list_display
        'get_type_images',       # Display methods in list_display
        'type_description',
        'get_image_preview',     # Display image preview
    ]



    readonly_fields = [f.name for f in Home._meta.fields] + [

        'get_banner_title',
        'get_banner_type',
        'get_banner_placement_location',
        'get_banner_short_description',
    ]

    actions = None

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

    # Display the category images in the admin
    def get_category_images(self, obj):
        return mark_safe("<br>".join([f'<img src="{img}" style="max-height: 100px;" />' for img in obj.category_images.values()]))
    get_category_images.short_description = "Category Images"

    # Display the type images in the admin
    def get_type_images(self, obj):
        return mark_safe("<br>".join([f'<img src="{img}" style="max-height: 100px;" />' for img in obj.type_images.values()]))
    get_type_images.short_description = "Type Images"

@admin.register(AdminContactDetails)
class AdminContactDetailsAdmin(admin.ModelAdmin):
    form = AdminContactDetailsForm
    list_display = ['location', 'phone_number', 'email' , 'google_link' , 'social_media_links']
    search_fields = ['location', 'phone_number', 'email' , 'google_link' , 'social_media_links']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ['name' , 'subcategory_name']
    search_fields = ['name' , 'subcategory_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = [
        'title',
        'get_category_name',
        'get_subcategory_name',
        'description',
        'get_image_preview',
        'keyfeature',
    ]
    search_fields = ['title', 'description', 'keyfeature']
    list_filter = ['category']

    def get_image_preview(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image available"

    get_image_preview.short_description = "Image Preview"

    # Related Category fields
    def get_category_name(self, obj):
        return obj.category.name
    get_category_name.short_description = "Category Name"

    def get_subcategory_name(self, obj):
        return obj.category.subcategory_name
    get_subcategory_name.short_description = "Subcategory"


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