from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from .forms import HomeBannerForm, HomeInteriorBannerForm, HomeExteriorBannerForm, ColourPaletteForm, ParallaxForm, \
    BrochureForm, AdditionalInfoForm, AdminContactDetailsForm, CategoryForm, ProductForm, HomeForm
from .models import HomeExteriorBanner, HomeInteriorBanner, HomepageBanner, PaintBudgetCalculator, ColourPalette, \
    Parallax, Brochure, AdditionalInfo, AdminContactDetails, WaterProofCalculator, Category, Product, UserInfo, Home

# Unregister default auth models (optional if you only want superuser access)
admin.site.unregister(User)
admin.site.unregister(Group)

# Shared base admin class for banners
class BaseBannerAdmin(admin.ModelAdmin):
    readonly_fields = ['display_image_urls']

    def display_image_urls(self, obj):
        if not obj.url:
            return "No images uploaded."
        html = ""
        if isinstance(obj.url, dict):
            if 'desktop' in obj.url:
                html += f"<strong>Desktop:</strong> <a href='{obj.url['desktop']}' target='_blank'>{obj.url['desktop']}</a><br>"
            if 'mobile' in obj.url:
                html += f"<strong>Mobile:</strong> <a href='{obj.url['mobile']}' target='_blank'>{obj.url['mobile']}</a><br>"
            if 'images' in obj.url and isinstance(obj.url['images'], list):
                html += "<strong>Images:</strong><br>"
                for img_url in obj.url['images']:
                    html += f"<img src='{img_url}' style='height:60px; margin:5px 5px 5px 0;' />"
        return mark_safe(html)

    display_image_urls.short_description = "Image URLs"

# Admin for HomepageBanner
@admin.register(HomepageBanner)
class HomeBannerAdmin(BaseBannerAdmin):
    form = HomeBannerForm
    list_display = ['title', 'type', 'display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-banner')

    def save_model(self, request, obj, form, change):
        obj.type = 'home-banner'
        super().save_model(request, obj, form, change)

# Admin for HomeInteriorBanner
@admin.register(HomeInteriorBanner)
class HomeInteriorBannerAdmin(BaseBannerAdmin):
    form = HomeInteriorBannerForm
    list_display = ['title', 'type', 'display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-interior-banner')

    def save_model(self, request, obj, form, change):
        obj.type = 'home-interior-banner'
        super().save_model(request, obj, form, change)

# Admin for HomeExteriorBanner
@admin.register(HomeExteriorBanner)
class HomeExteriorBannerAdmin(BaseBannerAdmin):
    form = HomeExteriorBannerForm
    list_display = ['title', 'type', 'display_image_urls']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-exterior-banner')

    def save_model(self, request, obj, form, change):
        obj.type = 'home-exterior-banner'
        super().save_model(request, obj, form, change)

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
        'get_category_images',
        'get_type_images',
        'type_description',
    ]

    # Readonly fields to prevent editing in the admin panel
    readonly_fields = [f.name for f in Home._meta.fields] + [
        'get_banner_title',
        'get_banner_type',
        'get_banner_placement_location',
        'get_banner_short_description',
        'get_category_images',
        'get_type_images'
    ]

    actions = None


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


    def get_category_images(self, obj):
        return mark_safe("<br>".join([f'<img src="{img}" style="max-height: 100px;" />' for img in obj.category_images.values()]))
    get_category_images.short_description = "Category Images"

    def get_type_images(self, obj):
        return mark_safe("<br>".join([f'<img src="{img}" style="max-height: 100px;" />' for img in obj.type_images.values()]))
    get_type_images.short_description = "Type Images"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

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
        'url',
        'keyfeature',
    ]
    search_fields = ['title', 'description', 'keyfeature']
    list_filter = ['category']

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