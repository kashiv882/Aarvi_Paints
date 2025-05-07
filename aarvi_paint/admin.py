from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.models import User, Group
from .forms import  HomeInteriorBannerForm, HomeExteriorBannerForm, ColourPaletteForm, ParallaxForm,WaterproofHomeForm,HomeBannerImageForm,AboutUsAdminForm,TestimonialAdminForm,\
    BrochureForm, AdditionalInfoForm, AdminContactDetailsForm, CategoryForm, ProductForm, HomeForm, GalleryBannerForm,InspirationForm, \
    AboutUsTopBannerForm, ColorPalletsBannerForm, ProductBannerForm, ContactUsBannerForm, HomeWaterproofingBannerForm,HomeAdminForm,waterAdminForm, \
    AboutUsBottomVideoBannerForm, CalculatorAdminForm, BaseBannerForm,HomeInteriorForm, BaseHomeInteriorForm, HomeInteriorDifferentRoomForm,HomeExteriordataForm,BaseBannerMultipleImageForm,BannerImageInline
from .models import HomeExteriorBanner, Testimonial,HomeInteriorBanner,  PaintBudgetCalculator, ColourPalette,WaterproofHome,Inspiration, \
    Parallax, Brochure, AdditionalInfo, AdminContactDetails, WaterProofCalculator, Category, Product, UserInfo, Home,CategoryImage, TypeImage,HomeProxy, \
    Banner, GalleryBanner, AboutUsTopBanner, ColorPalletsBanner, ProductBanner, ContactUsBanner, Category, CategoryImage,AboutUs, WaterCalculator,\
    HomeWaterproofingBanner, AboutUsBottomVideoBanner, HomeBanner,BannerImage,Calculator, HomeInterior,HomeInteriorDifferentRoom,HomeExteriorData,HomeInteriorColorCategory, CategoryImage,ColourPaletteWithImages, ColourPaletteImage,ColourPaletteProxy,ColourCode,MultiColorPalette

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

# class BannerImageInline(admin.StackedInline):
#     model = BannerImage
#     extra = 1
#     form = BannerImageForm  # Use the custom form for the inline
#     readonly_fields = ['image_preview']

#     # Display the preview of the uploaded image
#     def image_preview(self, obj):
#         if obj.image:
#             return format_html(
#                 '<img src="{}" style="max-height: 100px;" />',
#                 obj.image.url
#             )
#         return "No image uploaded"

#     image_preview.short_description = "Preview"


# # Admin for HomeBanner
# class HomeBannerAdmin(admin.ModelAdmin):
#     form = BannerImageForm  # Link to the custom form

#     list_display = ['type', 'get_image_preview']
#     search_fields = ['type']
#     list_filter = ['type']
#     readonly_fields = ['get_image_preview']

#     def get_image_preview(self, obj):
#         image_url = obj.url.get('image') if obj.url else None
#         if image_url:
#             return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
#         return "No image available"

#     get_image_preview.short_description = "Image Preview"




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



# class CategoryImageInline(admin.TabularInline):
#     model = CategoryImage
#     extra = 1
#     readonly_fields = ['image_preview']

#     def image_preview(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" style="height:100px;"/>', obj.image.url)
#         return ""

#     image_preview.short_description = "Preview"

# @admin.register(HomeInteriorColorCategory)
# class HomeInteriorAdmin(admin.ModelAdmin):
#     inlines = [CategoryImageInline]
#     fields = ['title', 'category_name', 'subcategory_name', 'type_description', 'title_type', 'banners']
#     readonly_fields = ['type']

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type='home-interior-color-category')

#     def save_model(self, request, obj, form, change):
#         obj.type = 'home-interior-color-category'
#         super().save_model(request, obj, form, change)

# Inline model to handle multiple image uploads


# =============================Color pallets proxy models===========================================================

class ColourPaletteImageInline(admin.TabularInline):
    model = ColourPaletteImage
    extra = 1
    readonly_fields = ['preview']  # Show preview but prevent editing it
    fields = ['image', 'preview']  # Fields to show

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: contain;" />', obj.image.url)
        return "-"
    preview.short_description = 'Image Preview'


# Admin for proxy model only (editable: title, description, and inline images)

@admin.register(ColourPaletteWithImages)
class ColourPaletteWithImagesAdmin(admin.ModelAdmin):
    fields = ('title', 'description')  # Only show title and description
    inlines = [ColourPaletteImageInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update the `url` field with all related image URLs
        obj.url = {
            str(image.pk): image.image.url for image in obj.images.all()
        }
        obj.save()


# ======================================Color pallet proxy model=================================================

class ColourCodeInline(admin.TabularInline):
    model = ColourCode
    extra = 1  # Number of empty forms to display

@admin.register(MultiColorPalette)
class MultiColorPaletteAdmin(admin.ModelAdmin):
    inlines = [ColourCodeInline]
    # Exclude the single color fields if you want
    exclude = ('colour_code', 'colour_code_category')
    
    # Optional: Display color codes in list view
    list_display = ('title', 'description', 'display_colour_codes')
    
    def display_colour_codes(self, obj):
        return ", ".join([f"{cc.category}: {cc.code}" for cc in obj.colour_codes.all()])
    display_colour_codes.short_description = "Color Codes"
# =============================================================================================================

# ======================================HomE INTERIor=============================================================

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1

class TypeImageInline(admin.TabularInline):
    model = TypeImage
    extra = 1

@admin.register(HomeProxy)
class HomeProxyAdmin(admin.ModelAdmin):
    inlines = [CategoryImageInline, TypeImageInline]
    fields = ['title', 'category_name', 'subcategory_name', 'title_type', 'type_description']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # sync category_images
        obj.category_images = [img.image.url for img in obj.category_images_relation.all()]
        # sync type_images
        obj.type_images = [img.image.url for img in obj.type_images_relation.all()]
        obj.save()


# ===========================================Home Exterior=========================================================


# @admin.register(Home)
# class HomeAdmin(admin.ModelAdmin):
#     form = HomeAdminForm
#     list_display = ('title', 'type', 'title_type', 'get_category_names')

#     def get_category_names(self, obj):
#         return f"{obj.category_name or '-'} / {obj.subcategory_name or '-'}"
#     get_category_names.short_description = 'Categories'

# ===========================================================================water proofing=====


@admin.register(WaterproofHome)
class WaterproofHomeAdmin(admin.ModelAdmin):
    form = WaterproofHomeForm
    list_display = ['title_type', 'admin_image_preview', 'type_description_short']
    readonly_fields = ['current_image_display']

    def admin_image_preview(self, obj):
        if obj.type_images and obj.type_images.get('url'):
            return format_html(
                '<img src="{}" style="max-height: 50px;" />',
                obj.type_images['url']
            )
        return "No image"
    admin_image_preview.short_description = 'Image Preview'

    def type_description_short(self, obj):
        return obj.type_description[:75] + '...' if obj.type_description else ""
    type_description_short.short_description = 'Description'

    def current_image_display(self, obj):
        if obj.type_images and obj.type_images.get('url'):
            return format_html(
                '''
                <div style="margin-bottom: 20px;">
                    <h3>Current Image</h3>
                    <img src="{}" style="max-height: 200px;" />
                    <p><strong>Filename:</strong> {}</p>
                </div>
                ''',
                obj.type_images['url'],
                obj.type_images.get('name', '')
            )
        return "No image currently set"
    current_image_display.short_description = 'Image'
    current_image_display.allow_tags = True

    fieldsets = (
        (None, {
            'fields': ('title_type', 'type_description')
        }),
        ('Image Management', {
            'fields': ('current_image_display', 'new_image'),
            'classes': ('collapse', 'wide'),
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/waterproof.css',)
        }
        js = ('admin/js/image_preview.js',)

# =================================================================about Us=======================================================

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsAdminForm
    list_display = ('title', )
    
    fieldsets = (
        ('Main Information', {
            'fields': ('title', 'description')
        }),
        ('Lower Section', {
            'fields': ('lower_title', 'lower_sub_title', 'lower_description'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('extra_info',),
            'classes': ('collapse',),
        }),
        # ('Advanced Options', {
        #     'fields': ('url',),
        #     'classes': ('collapse',),
        # }),
    )



# ===================================================================================================

# ===========================================================Home Banner======================================

class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']  # Only image upload here

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'

@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    form = HomeBannerImageForm
    inlines = [BannerImageInline]
    list_display = ['banner_preview','image_count']
    list_display_links = ['banner_preview']
    
    fieldsets = (
        ('General Information', {
            'fields': (),  # No actual fields
            'description': format_html(
                '''
                <div style="background:#f8f8f8; padding:20px; border-radius:5px;">
                    <h3 style="margin-top:0">Home Banner Management</h3>
                   
                    <p style="margin-bottom:0">
                        <strong>Add images using the "Banner Images" section below</strong><br>
                         <br>
                    </p>
                </div>
                '''
            ),
            'classes': ('wide',),
        }),
    )
    # New method to show image count
    def image_count(self, obj):
        count = obj.images.count()
        color = '#4CAF50' if count > 0 else '#F44336'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            f"{count} image{'s' if count != 1 else ''}"
        )
    image_count.short_description = 'Images'
    # Enhanced preview method
    def banner_preview(self, obj):
        images = obj.images.all()
        if images:
            return format_html(
                '''
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <img src="{}" style="
                        height: 50px;
                        width: auto;
                        border-radius: 4px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    "/>
                    <span style="font-size: 0.9em; color: #666;">
                        {:.25}...
                    </span>
                </div>
                ''',
                images[0].image.url,
                images[0].image.name
            )
        return format_html(
            '<span style="color: #F44336;">No images uploaded</span>'
        )

    def banner_preview(self, obj):
        if obj.main_image and obj.main_image.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.main_image.image.url
            )
        return "Upload Images"
    banner_preview.short_description = 'Banner Preview'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-banner')

    def save_model(self, request, obj, form, change):
        obj.type = 'home-banner'
        super().save_model(request, obj, form, change)


# ===================================================================Additional info inspiration========================


@admin.register(Inspiration)
class InspirationAdmin(admin.ModelAdmin):
    form = InspirationForm
    list_display = ('title', 'type', 'description_short', 'image_preview')
    list_filter = ('type',)
    readonly_fields = ('image_preview',)
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def image_preview(self, obj):
        if obj.url and obj.url.get('image'):
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.url['image']
            )
        return "No image"
    image_preview.short_description = 'Preview'

    def get_queryset(self, request):
        # Only show interior and exterior inspirations
        return super().get_queryset(request).filter(type__in=['interior', 'exterior'])


# ======================================================================================================================================/


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    form = TestimonialAdminForm
    list_display = ('name', 'description','image_preview')

    readonly_fields = ['image_display']

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'image',
                'image_display',
                'delete_image',
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type="TESTIMONIAL")

    def image_preview(self, obj):
        url = obj.url.get('image')
        if url:
            return format_html('<img src="{}" style="max-height: 100px;" />', url)
        return "No image"
    image_preview.short_description = "Image Preview"

    def image_display(self, obj):
        url = obj.url.get('image')
        if url:
            return mark_safe(f'<img src="{url}" style="max-height: 200px;" />')
        return "No image uploaded."
    image_display.short_description = "Current Image"


# ===========================================================================paint budgt calculator===========================================



@admin.register(Calculator)
class CalculatorAdmin(admin.ModelAdmin):
    form = CalculatorAdminForm
    list_display = ('title', 'product', 'area')

    fieldsets = (
        ('Paint Budget Calculator', {
            'fields': (
                'product',
                'area',
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type="PAINT_BUDGET_CALCULATOR")

    def product(self, obj):
        return obj.details.get('product', '')

    def area(self, obj):
        return obj.details.get('area', '')


@admin.register(WaterCalculator)
class WaterproofcalculatorAdmin(admin.ModelAdmin):
    form = waterAdminForm
    list_display = ( 'product', 'area')

    fieldsets = (
        ('Paint Budget Calculator', {
            'fields': (
                'product',
                'area',
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type="PAINT_BUDGET_CALCULATOR")

    def product(self, obj):
        return obj.details.get('product', '')

    def area(self, obj):
        return obj.details.get('area', '')












# =======================================================================================================================================








# class BannerImageInline(admin.TabularInline):
#     model = BannerImage  # Using your existing BannerImage model
#     extra = 1
#     readonly_fields = ['image_preview']
#     fields = ['image', 'image_preview']

#     def image_preview(self, obj):
#         if obj.image:
#             return format_html(
#                 '<img src="{}" style="max-height: 100px; max-width: 200px;"/>',
#                 obj.image.url
#             )
#         return "No image"
#     image_preview.short_description = 'Preview'

# @admin.register(HomeBanner)
# class HomeBannerAdmin(admin.ModelAdmin):
#     form = HomeBannerImageForm
#     inlines = [BannerImageInline]
#     list_display = ['banner_preview']
#     list_display_links = ['banner_preview']

#     def banner_preview(self, obj):
#         if obj.main_image and obj.main_image.image:
#             return format_html(
#                 '<img src="{}" style="max-height: 50px;"/>',
#                 obj.main_image.image.url
#             )
#         return "Upload Images"
#     banner_preview.short_description = 'Banner Preview'

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type='home-banner')

#     def save_model(self, request, obj, form, change):
#         obj.type = 'home-banner'
#         super().save_model(request, obj, form, change)

#     fieldsets = (
#         ('Upload New Image', {
#             'fields': ('new_image',),
#             'classes': ('wide',),
#         }),
#     )

#     class Media:
#         css = {
#             'all': ('admin/css/homebanner.css',)
#         }








# @admin.register(HomeBanner)
# class HomeBannerAdmin(admin.ModelAdmin):
#     form = BaseBannerMultipleImageForm  # Use the form that excludes 'type'
#     inlines = [BannerImageInline]
#     list_display = ['type']  # Display 'type' in the list view

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type='home-banner')

#     def save_model(self, request, obj, form, change):
#         # Set 'type' automatically to 'home-banner' when saving
#         obj.type = 'home-banner'
#         super().save_model(request, obj, form, change)

# =====================================================================================================================


@admin.register(HomeInterior)
class HomeInteriorAdmin(admin.ModelAdmin):
    form = HomeInteriorForm
    list_display = ['title', 'type_description']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-interior')


@admin.register(HomeExteriorData)
class HomeExteriorDataAdmin(admin.ModelAdmin):
    form = HomeExteriordataForm
    list_display = ['title', 'type_description']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-exterior-data')


# @admin.register(HomeInteriorDifferentRoom)
# class HomeInteriorDifferentRoomAdmin(admin.ModelAdmin):
#     form = HomeInteriorDifferentRoomForm
#     list_display = ['title', 'type_description','type', 'image_preview']

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type='home-interior-different-room')

#     def save_model(self, request, obj, form, change):
#         obj.type = 'home-interior-different-room'
#         super().save_model(request, obj, form, change)

#     def image_preview(self, obj):
#         image_url = obj.category_images.get('image') if obj.category_images else None
#         if image_url:
#             return format_html('<img src="{}" width="100" height="auto" />', image_url)
#         return "No image"

#     image_preview.short_description = "Image"

@admin.register(HomeInteriorDifferentRoom)
class HomeInteriorDifferentRoomAdmin(admin.ModelAdmin):
    form = HomeInteriorDifferentRoomForm
    list_display = ['title', 'type_description', 'type', 'image_preview']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-interior-different-room')

    def save_model(self, request, obj, form, change):
        obj.type = 'home-interior-different-room'
        super().save_model(request, obj, form, change)

    def image_preview(self, obj):
        image_url = obj.category_images.get('image') if obj.category_images else None
        if image_url:
            return format_html('<img src="{}" width="100" height="auto" />', image_url)
        return "No image"

    image_preview.short_description = "Image"


















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
    list_display = ['name' ,'subcategory_name']
    search_fields = ['name','subcategory_name' ]

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