from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html,format_html_join
from django.urls import path
from django.utils.html import format_html
from django.forms.models import BaseInlineFormSet
import nested_admin
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from django.utils.safestring import mark_safe
from django import forms
import json
from django.template.response import TemplateResponse
from django.contrib.auth.models import User, Group
from .forms import  HomeInteriorBannerForm,SettingAdminForm, HomeExteriorBannerForm, ColourPaletteForm, ParallaxForm,WaterproofHomeForm,HomeBannerImageForm,AboutUsAdminForm,TestimonialAdminForm,\
    BrochureForm, AdditionalInfoForm, AdminContactDetailsForm, CategoryForm, ProductForm, HomeForm, GalleryBannerForm,GalleryBannerImageForm,InspirationForm,AboutUsForm, HomeWaterProofForm,\
    AboutUsTopBannerForm, ColorPalletsBannerForm, ProductBannerForm, ContactUsBannerForm, HomeWaterproofingBannerForm,HomeAdminForm,HomeExteriorForm, \
    AboutUsBottomVideoBannerForm, BaseBannerForm,HomeInteriorForm, BaseHomeInteriorForm, HomeInteriorDifferentRoomForm,HomeExteriordataForm,BaseBannerMultipleImageForm,BannerImageInline
from .models import AboutUsBottomVideoBanner, PaintProduct,PaintCalculator,ColourCode,HomeExteriorBanner,WaterProduct, Testimonial,HomeInteriorBanner,  PaintBudgetCalculator, ColourPalette,WaterproofHome,Inspiration, \
    Parallax, Brochure, AdditionalInfo, AdminContactDetails, WaterProofCalculator, Category, Product, UserInfo, Home,CategoryImage, TypeImage,HomeProxy,HomeExterior,\
    Banner, GalleryBanner,CategoryImage,AboutUsTopBanner, ColorPalletsBanner, ProductBanner, ContactUsBanner, Category, CategoryImage,AboutUs, WaterCalculator,HomeWaterProof,\
    HomeWaterproofingBanner,HomeInterior, HomeInteriorCategory,HomeInteriorSubCategory, HomeInteriorSubCategoryImage,HomeInteriorFeature, AboutUsBottomVideoBanner,ExteriorHomeCategory, ExteriorCategoryImage, Setting, HomeBanner,BannerImage, HomeInterior,HomeInteriorDifferentRoom,HomeInteriorColorCategory, CategoryImage,ColourPaletteWithImages, ColourPaletteImage,MultiColorPalette


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

# class ColourPaletteImageInline(admin.TabularInline):
#     model = ColourPaletteImage
#     extra = 1
#     readonly_fields = ['preview']  # Show preview but prevent editing it
#     fields = ['image', 'preview']  # Fields to show

#     def preview(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" width="100" height="100" style="object-fit: contain;" />', obj.image.url)
#         return "-"
#     preview.short_description = 'Image Preview'


# Admin for proxy model only (editable: title, description, and inline images)

class ColourPaletteImageInline(admin.TabularInline):  # or StackedInline if preferred
    model = ColourPaletteImage
    extra = 1  # Number of empty image forms to show
    max_num = 10  # Optional limit

@admin.register(ColourPaletteWithImages)
class ColourPaletteWithImagesAdmin(admin.ModelAdmin):
    inlines = [ColourPaletteImageInline]
    list_display = ['title', 'description', 'image_preview']

    def get_fields(self, request, obj=None):
        # Show only title and description during creation
        if obj is None:
            return ('title', 'description')
        # Show all fields during change
        return super().get_fields(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.url = {
            str(image.pk): image.image.url for image in obj.images.all()
        }
        obj.save()

    def image_preview(self, obj):
        images_html = ''.join([
            f'<img src="{image.image.url}" width="50" height="50" style="margin: 5px;" />'
            for image in obj.images.all()
        ])
        return mark_safe(images_html)

    image_preview.short_description = 'Image Previews'


# class ColourCodeInlineForm(forms.Form):
#     category = forms.CharField(max_length=200)
#     code = forms.CharField()
#     colorshade = forms.CharField(max_length=200)

# class ColourCodeInline(admin.options.InlineModelAdmin):
#     model = None  # No actual model
#     form = ColourCodeInlineForm
#     template = 'admin/edit_inline/tabular.html'
#     extra = 1

# class ColourCodeInlineFormSet(BaseInlineFormSet):
#     def save_new(self, form, commit=True):
#         return form.cleaned_data

#     def save_existing(self, form, instance, commit=True):
#         return form.cleaned_data

# Register MultiColorPalette admin
# class ColourCodeInlineForm(forms.Form):
#     category = forms.CharField(max_length=200)
#     code = forms.CharField(max_length=200)
#     colorshade = forms.CharField(max_length=200)

# # ColourPaletteAdmin class to manage ColourPalette in the admin panel
# @admin.register(ColourPalette)
# class ColourPaletteAdmin(admin.ModelAdmin):
#     fields = ('title', 'description')
#     list_display = ('title', 'description', 'display_colour_codes')

#     def get_formsets_with_inlines(self, request, obj=None):
#         # Dynamically create the formset for the inline fields
#         formset = type('DynamicFormSet', (BaseInlineFormSet,), {
#             'form': ColourCodeInlineForm,
#             'get_queryset': lambda self: [],  # Empty queryset since no model is used
#             'save_new': self.save_new,
#             'save_existing': self.save_existing,
#         })
#         yield formset(request.POST or None), None

#     def save_new(self, form, commit=True):
#         # Save the new inline form data
#         return form.cleaned_data

#     def save_existing(self, form, instance, commit=True):
#         # Save the existing inline form data
#         return form.cleaned_data

#     def save_model(self, request, obj, form, change):
#         # Save the base fields of ColourPalette model first (title, description)
#         super().save_model(request, obj, form, change)

#         # Process the color code details (category, code, colorshade)
#         raw_form_data = request.POST
#         prefix = "form-"  # Inline form prefix for the color code fields
#         count = int(raw_form_data.get("form-TOTAL_FORMS", 0))
#         details_list = []

#         # Extract and save the color code details
#         for i in range(count):
#             code = raw_form_data.get(f"{prefix}{i}-code")
#             category = raw_form_data.get(f"{prefix}{i}-category")
#             shade = raw_form_data.get(f"{prefix}{i}-colorshade")
#             if code and category and shade:
#                 details_list.append({
#                     "code": code,
#                     "category": category,
#                     "colorshade": shade
#                 })

#         # Save the details list to the ColourPalette model's `details` field
#         obj.details = details_list
#         obj.save()

#     def display_colour_codes(self, obj):
#         return json.dumps(obj.details, ensure_ascii=False, indent=2)

#     display_colour_codes.short_description = "Color Codes"




# ======================================Color pallet proxy model=================================================

# class ColourCodeInline(admin.TabularInline):
#     model = ColourCode
#     extra = 1  # Number of empty forms to display

# @admin.register(MultiColorPalette)
# class MultiColorPaletteAdmin(admin.ModelAdmin):
#     inlines = [ColourCodeInline]

#     # Only show these fields in the "General" section
#     fields = ('title', 'description')

#     list_display = ('title', 'description', 'display_colour_codes')

#     def display_colour_codes(self, obj):
#         # Prepare a list of dictionaries containing the required fields
#         colour_codes = [
#             {
#                 "category": cc.category,
#                 "code": cc.code,
#                 "colorshade": cc.colorshade
#             }
#             for cc in obj.colour_codes.all()
#         ]
        
#         # Return the JSON-formatted string
#         return json.dumps(colour_codes, ensure_ascii=False)
    
#     display_colour_codes.short_description = "Color Codes"
# =============================================================================================================

# ======================================HomE INTERIor=============================================================

# class CategoryImageInline(admin.TabularInline):
#     model = CategoryImage
#     extra = 1

# class TypeImageInline(admin.TabularInline):
#     model = TypeImage
#     extra = 1

# @admin.register(HomeProxy)
# class HomeProxyAdmin(admin.ModelAdmin):
#     inlines = [CategoryImageInline, TypeImageInline]
#     fields = ['title', 'category_name', 'subcategory_name', 'title_type', 'type_description']

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)

#         # sync category_images
#         obj.category_images = [img.image.url for img in obj.category_images_relation.all()]
#         # sync type_images
#         obj.type_images = [img.image.url for img in obj.type_images_relation.all()]
#         obj.save()


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

    list_display = [
        'title',
        'short_description',
        'short_details',  # Display details as JSON
    ]

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
    )

    def short_description(self, obj):
        return obj.description[:50] + '...' if obj.description else '—'
    short_description.short_description = 'Description'

    def short_details(self, obj):
        if not obj.details:
            return '—'
        # Render details field as a JSON string
        return mark_safe('<pre>' + json.dumps(obj.details, indent=4) + '</pre>')

    short_details.short_description = 'Details (JSON)'

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

class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    form = HomeBannerImageForm
    inlines = [BannerImageInline]
    list_display = ['banner_preview', 'image_count']
    list_display_links = ['banner_preview']

    def image_count(self, obj):
        count = obj.images.count()
        return format_html(
            '<span style="color:{}; font-weight: bold;">{}</span>',
            '#4CAF50' if count else '#F44336',
            f"{count} image{'s' if count != 1 else ''}"
        )
    image_count.short_description = 'Images'

    def banner_preview(self, obj):
        images = obj.images.all()
        if images:
            return format_html(
                ''.join(
                    f'<img src="{image.image.url}" style="height: 50px; margin-right: 5px; border-radius: 4px;" />'
                    for image in images if image.image and hasattr(image.image, 'url')
                )
            )
        return format_html('<span style="color:red;">No images uploaded</span>')
    banner_preview.short_description = 'Banner Preview'

    fieldsets = (
        ('General Information', {
            'fields': (),
            'description': format_html(
                '''
                <div style="background:#f8f8f8; padding:20px; border-radius:5px;">
                    <h3 style="margin-top:0">Home Banner Management</h3>
                    <p style="margin-bottom:0">
                        <strong>Add images using the "Banner Images" section below</strong>
                    </p>
                </div>
                '''
            ),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-banner')

    def save_model(self, request, obj, form, change):
        obj.type = 'home-banner'
        super().save_model(request, obj, form, change)

# ===================================================================Additional info inspiration========================


@admin.register(Inspiration)
class InspirationAdmin(admin.ModelAdmin):
    form = InspirationForm
    list_display = ('title', 'description', 'image_preview')
    readonly_fields = ('image_preview',)
    exclude = ('type', 'url', 'details')  # hide raw JSON

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="/media/{}" width="100" height="auto" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image Preview'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='inspiration')

    def save_model(self, request, obj, form, change):
        obj.type = 'inspiration'
        super().save_model(request, obj, form, change)


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



# class PaintProductInline(admin.TabularInline):
#     model = PaintProduct
#     extra = 1
#     fields = ['product_name', 'area']
#     verbose_name = "Paint Product"
#     verbose_name_plural = "Paint Products"

# class PaintCalculatorForm(forms.ModelForm):
#     subtitle = forms.CharField(required=False, help_text="This will be stored in the details JSON field")

#     class Meta:
#         model = PaintCalculator
#         fields = ['title', 'subtitle', 'description']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.details and 'subtitle' in self.instance.details:
#             self.fields['subtitle'].initial = self.instance.details['subtitle']

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.details = instance.details or {}
#         instance.details['subtitle'] = self.cleaned_data.get('subtitle', '')
#         if commit:
#             instance.save()
#         return instance

# @admin.register(PaintCalculator)
# class PaintCalculatorAdmin(admin.ModelAdmin):
#     form = PaintCalculatorForm
#     inlines = [PaintProductInline]
#     list_display = ('title', 'display_subtitle', 'display_products', 'description_preview')
#     fields = ['title', 'subtitle', 'description']
#     search_fields = ['title', 'details__subtitle', 'paint_products__product_name']
#     readonly_fields = ('details_preview',)

#     def display_subtitle(self, obj):
#         return obj.details.get('subtitle', '—')
#     display_subtitle.short_description = 'Subtitle'

#     def display_products(self, obj):
#         products = obj.paint_products.all()
#         if products:
#             return format_html("<br>".join([f"• {p.product_name} ({p.area} units)" for p in products]))
#         return "—"
#     display_products.short_description = 'Products'

#     def description_preview(self, obj):
#         if obj.description:
#             return format_html(
#                 '<span title="{}">{}</span>',
#                 obj.description,
#                 obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
#             )
#         return "—"
#     description_preview.short_description = 'Description'

#     def details_preview(self, obj):
#         if not obj.details:
#             return "No additional details"
#         return format_html_join(
#             '\n',
#             '<div><strong>{}:</strong> {}</div>',
#             ((k, v) for k, v in obj.details.items() if k != 'subtitle')
#         )
#     details_preview.short_description = 'Additional Details'

#     def save_model(self, request, obj, form, change):
#         obj.type = "PAINT_CALCULATOR"
#         super().save_model(request, obj, form, change)

#     def get_fields(self, request, obj=None):
#         return ['title', 'subtitle', 'description']

#     def get_readonly_fields(self, request, obj=None):
#         return ['details_preview']




# @admin.register(Calculator)
# class CalculatorAdmin(admin.ModelAdmin):
#     form = CalculatorAdminForm
#     list_display = ('title', 'product', 'area')

#     fieldsets = (
#         ('Paint Budget Calculator', {
#             'fields': (
#                 'product',
#                 'area',
#             )
#         }),
#     )

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type="PAINT_BUDGET_CALCULATOR")

#     def product(self, obj):
#         return obj.details.get('product', '')

#     def area(self, obj):
#         return obj.details.get('area', '')


# class WaterProductInline(admin.TabularInline):
#     model = WaterProduct
#     extra = 1  # Show one empty form by default
#     min_num = 1
#     verbose_name = "Product"
#     verbose_name_plural = "Products"


# ===================================================water calculator========================================================
class WaterProductInline(admin.TabularInline):
    model = WaterProduct
    extra = 1
    fields = ['product_name', 'area']
    verbose_name = "Water Product"
    verbose_name_plural = "Water Products"

class WaterCalculatorForm(forms.ModelForm):
    subtitle = forms.CharField(required=False, help_text="This will be stored in the details JSON field")

    class Meta:
        model = WaterCalculator
        fields = ['title', 'subtitle', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.details and 'subtitle' in self.instance.details:
            self.fields['subtitle'].initial = self.instance.details['subtitle']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.details = instance.details or {}
        instance.details['subtitle'] = self.cleaned_data.get('subtitle', '')
        if commit:
            instance.save()
        return instance

@admin.register(WaterCalculator)
class WaterCalculatorAdmin(admin.ModelAdmin):
    form = WaterCalculatorForm
    inlines = [WaterProductInline]
    list_display = ('title', 'display_subtitle', 'display_products', 'description_preview')
    
    fields = ['title', 'subtitle', 'description']
    search_fields = ['title', 'details__subtitle', 'water_products__product_name']
    readonly_fields = ('details_preview',)  # Add this if you want to show all details

    def display_subtitle(self, obj):
        return obj.details.get('subtitle', '—')
    display_subtitle.short_description = 'Subtitle'

    def display_products(self, obj):
        products = obj.water_products.all()
        if products:
            return format_html("<br>".join([f"• {p.product_name} ({p.area} units)" for p in products]))
        return "—"
    display_products.short_description = 'Products'

    def description_preview(self, obj):
        if obj.description:
            return format_html(
                '<span title="{}">{}</span>',
                obj.description,
                obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
            )
        return "—"
    description_preview.short_description = 'Description'

    def details_preview(self, obj):
        if not obj.details:
            return "No additional details"
        return format_html_join(
            '\n',
            '<div><strong>{}:</strong> {}</div>',
            ((k, v) for k, v in obj.details.items() if k != 'subtitle')  # Exclude subtitle as it's shown separately
        )
    details_preview.short_description = 'Additional Details'

    def save_model(self, request, obj, form, change):
        obj.type = "WATER_CALCULATOR"
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        return ['title', 'subtitle', 'description']

    def get_readonly_fields(self, request, obj=None):
        return ['details_preview']


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
#         re`turn super().get_queryset(request).filter(type='home-banner')

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




# @admin.register(HomeExteriorData)
# class HomeExteriorDataAdmin(admin.ModelAdmin):
#     form = HomeExteriordataForm
#     list_display = ['title', 'type_description']

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type='home-exterior-data')


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

# @admin.register(HomeInteriorDifferentRoom)
# class HomeInteriorDifferentRoomAdmin(admin.ModelAdmin):
#     form = HomeInteriorDifferentRoomForm
#     list_display = ['title', 'type_description', 'type', 'image_preview']

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















class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1



class GalleryBannerAdmin(admin.ModelAdmin):
    form = GalleryBannerImageForm
    inlines = [BannerImageInline]
    list_display = ['banner_preview', 'image_count']
    list_display_links = ['banner_preview']

    def image_count(self, obj):
        count = obj.images.count()
        return format_html(
            '<span style="color:{}; font-weight: bold;">{}</span>',
            '#4CAF50' if count else '#F44336',
            f"{count} image{'s' if count != 1 else ''}"
        )
    image_count.short_description = 'Images'

    def banner_preview(self, obj):
        images = obj.images.all()
        if images:
            return format_html(
                ''.join(
                    f'<img src="{image.image.url}" style="height: 50px; margin-right: 5px; border-radius: 4px;" />'
                    for image in images if image.image and hasattr(image.image, 'url')
                )
            )
        return format_html('<span style="color:red;">No images uploaded</span>')
    banner_preview.short_description = 'Banner Preview'

    fieldsets = (
        ('General Information', {
            'fields': (),
            'description': format_html(
                '''
                <div style="background:#f8f8f8; padding:20px; border-radius:5px;">
                    <h3 style="margin-top:0">Home Gallery Management</h3>
                    <p style="margin-bottom:0">
                        <strong>Add images using the "Gallery Images" section below</strong>
                    </p>
                </div>
                '''
            ),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='gallery-banner')

    def save_model(self, request, obj, form, change):
        obj.type = 'gallery-banner'
        super().save_model(request, obj, form, change)
admin.site.register(GalleryBanner,GalleryBannerAdmin)



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

    display_video_urls = display_media_urls  # Assumes you have this function defined


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


# @admin.register(ColourPalette)
# class ColourPaletteAdmin(admin.ModelAdmin):
#     form = ColourPaletteForm

#     list_display = ['title', 'colour_code', 'colour_code_category', 'get_image_preview','description']
#     search_fields = ['title', 'colour_code', 'colour_code_category']
#     list_filter = ['colour_code_category']
#     readonly_fields = ['get_image_preview']

#     def get_image_preview(self, obj):
#         # Assuming 'url' field contains a key 'image' or similar
#         image_url = obj.url.get('image') if obj.url else None
#         if image_url:
#             return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
#         return "No image available"

#     get_image_preview.short_description = "Preview"


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




#
# @admin.register(Home)
# class HomeAdmin(admin.ModelAdmin):
#     form = HomeForm
#
#     def get_image_preview(self, obj):
#         try:
#             category_img = next(iter(obj.category_images.values()), None)
#             type_img = next(iter(obj.type_images.values()), None)
#             image_url = category_img or type_img
#             if image_url:
#                 return mark_safe(f'<img src="{image_url}" style="max-height: 100px; border: 1px solid #ccc;" />')
#         except Exception:
#             pass
#         return "No image available"
#
#     list_display = [
#         'title',
#         'type',
#         'category_name',
#         'subcategory_name',
#         'title_type',
#         'get_banner_title',
#         'get_banner_type',
#         'get_banner_placement_location',
#         'get_banner_short_description',
#         'category_images',
#         'type_images',
#         'type_description',
#         'get_image_preview',
#     ]
#
#
#
#     # Define methods for displaying related data in the admin
#     def get_banner_title(self, obj):
#         return obj.banners.title
#     get_banner_title.short_description = "Banner Title"
#
#     def get_banner_type(self, obj):
#         return obj.banners.type
#     get_banner_type.short_description = "Banner Type"
#
#     def get_banner_placement_location(self, obj):
#         return obj.banners.placement_location
#     get_banner_placement_location.short_description = "Banner Placement Location"
#
#     def get_banner_short_description(self, obj):
#         return obj.banners.short_description
#     get_banner_short_description.short_description = "Banner Short Description"
#


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
        'hide',
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
    form = CategoryForm
    list_display = ['name' ,'subcategory_name']
    search_fields = ['name','subcategory_name' ]
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



class TypeImageInline(admin.TabularInline):
    model = TypeImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="margin:3px;border-radius:4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="margin:3px;border-radius:4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"




class HomeInteriorSubCategoryImageInline(NestedTabularInline):
    model = HomeInteriorSubCategoryImage
    extra = 1

class HomeInteriorSubCategoryInline(NestedStackedInline):
    model = HomeInteriorSubCategory
    inlines = [HomeInteriorSubCategoryImageInline]
    extra = 1

class HomeInteriorCategoryInline(NestedStackedInline):
    model = HomeInteriorCategory
    inlines = [HomeInteriorSubCategoryInline]
    extra = 1

class HomeInteriorFeatureInline(NestedStackedInline):
    model = HomeInteriorFeature
    extra = 1


@admin.register(HomeInterior)
class HomeInteriorAdmin(NestedModelAdmin):
    inlines = [HomeInteriorCategoryInline, HomeInteriorFeatureInline]
    list_display = ['title', 'description', 'display_data_preview']
    readonly_fields = ['display_data_preview']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type="Interior")

    def get_fields(self, request, obj=None):
        return [
            'title',
            'description',
            'display_data_preview',
        ]

    def save_model(self, request, obj, form, change):
        obj.type = "Interior"
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        home = form.instance
        home.type = "Interior"

        # Process HomeInteriorCategory and SubCategory
        categories = home.homeinterior_categories.all()
        if categories.exists():
            home.category_name = categories.first().name

            subcategories = categories.first().subcategories.all()
            if subcategories.exists():
                home.subcategory_name = subcategories.first().name

                # Gather images from all subcategories
                image_urls = []
                for sub in subcategories:
                    image_urls += [img.image.url for img in sub.images.all()]
                home.category_images = {"images": image_urls}

        # Process Features
        features = home.features.all()
        if features.exists():
            home.title_type = features.first().title
            home.type_description = features.first().description
            home.type_images = {
                "images": [feature.image.url for feature in features if feature.image]
            }

        home.save()

    def display_data_preview(self, obj):
        if not obj.pk:
            return "Save and continue editing to see preview."

        html = "<h4>Categories & Subcategories</h4>"
        for cat in obj.homeinterior_categories.all():
            html += f"<strong>Category: {cat.name}</strong><br>"
            for sub in cat.subcategories.all():
                html += f"<em>Subcategory: {sub.name}</em><br>"
                for img in sub.images.all():
                    if img.image:
                        html += f'<img src="{img.image.url}" width="150" style="margin: 5px;">'
            html += "<br><br>"

        html += "<h4>Features</h4>"
        for feat in obj.features.all():
            html += f"<strong>{feat.title}</strong>: {feat.description}<br>"
            if feat.image:
                html += f'<img src="{feat.image.url}" width="150" style="margin: 5px;"><br>'
        return format_html(html)




# ==============================================Home Interior Working Code ============================================
# class HomeInteriorSubCategoryImageInline(nested_admin.NestedTabularInline):
#     model = HomeInteriorSubCategoryImage
#     extra = 1

# class HomeInteriorSubCategoryInline(nested_admin.NestedStackedInline):
#     model = HomeInteriorSubCategory
#     inlines = [HomeInteriorSubCategoryImageInline]
#     extra = 1

# class HomeInteriorCategoryInline(nested_admin.NestedStackedInline):
#     model = HomeInteriorCategory
#     inlines = [HomeInteriorSubCategoryInline]
#     extra = 1

# class HomeInteriorFeatureInline(nested_admin.NestedStackedInline):
#     model = HomeInteriorFeature
#     extra = 1

# class HomeInteriorAdmin(nested_admin.NestedModelAdmin):

#     inlines = [HomeInteriorCategoryInline, HomeInteriorFeatureInline]
#     readonly_fields = ['display_data_preview']
#     list_display = ['title', 'description', 'display_data_preview']

#     def get_fields(self, request, obj=None):
#         if obj:
#             return ['title', 'description', 'display_data_preview']
#         return ['title', 'description', 'display_data_preview']

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)

#         image_urls = []
#         for cat in obj.homeinterior_categories.all():
#             for sub in cat.subcategories.all():
#                 for img in sub.images.all():
#                     if img.image:
#                         image_urls.append(img.image.url)
#         obj.url = image_urls  # assuming `url` is a JSONField or ArrayField
#         obj.save()

#     def display_data_preview(self, obj):
#         if not obj.pk:
#             return "Save and continue editing to see preview."

#         html = '<div style="font-family: Arial, sans-serif;">'

#         # -- CATEGORY & SUBCATEGORY SECTION --
#         html += '<h3 style="color: #2c3e50;">Categories</h3>'
#         for cat in obj.homeinterior_categories.all():
#             html += f'<div style="margin-bottom: 15px;">'
#             html += f'<h4 style="margin-bottom: 5px; color:#2980b9;">Category: {cat.name}</h4>'
#             for sub in cat.subcategories.all():
#                 html += f'<div style="margin-left: 15px;">'
#                 html += f'<strong style="color:#16a085;">Subcategory: {sub.name}</strong><br>'
#                 for img in sub.images.all():
#                     if img.image:
#                         html += f'<img src="{img.image.url}" width="120" style="margin: 5px; border: 1px solid #ccc; border-radius:4px;">'
#                 html += '</div><br>'
#             html += '</div>'

#         # -- FEATURES SECTION --
#         html += '<h3 style="color: #8e44ad;">Features</h3>'
#         for feature in obj.features.all():
#             html += '<div style="margin-bottom: 15px; padding-left: 10px; border-left: 3px solid #8e44ad;">'
#             html += f'<h4 style="margin: 0; color:#8e44ad;">{feature.title}</h4>'
#             html += f'<p style="margin: 5px 0 10px; color:#555;">{feature.description}</p>'
#             if feature.image:
#                 html += f'<img src="{feature.image.url}" width="120" style="margin: 5px 0; border-radius:4px; border: 1px solid #ccc;">'
#             html += '</div>'

#         html += '</div>'
#         return format_html(html)
# admin.site.register(HomeInterior, HomeInteriorAdmin)
# ====================================================================================================================


# @admin.register(HomeInterior)
# class HomeInteriorAdmin(admin.ModelAdmin):
#     inlines = [CategoryImageInline, TypeImageInline]  # Use the inlines here
#     form = HomeInteriorForm

#     list_display = [
#         'title',
#         'category_images_preview',
#         'type_images_preview',
#         'category_name_display',
#         'subcategory_name_display',
#     ]

#     def category_images_preview(self, obj):
#         images_html = ''.join([
#             f'<img src="{image_url}" width="50" height="50" style="margin:2px; border-radius:4px;" />'
#             for image_url in obj.category_images.values()  # Access the image URLs from the JSON field
#         ])
#         return format_html(images_html) if images_html else "-"
#     category_images_preview.short_description = "Category Images"

#     def type_images_preview(self, obj):
#         images_html = ''.join([
#             f'<img src="{image_url}" width="50" height="50" style="margin:2px; border-radius:4px;" />'
#             for image_url in obj.type_images.values()  # Access the image URLs from the JSON field
#         ])
#         return format_html(images_html) if images_html else "-"
#     type_images_preview.short_description = "Type Images"

#     def category_name_display(self, obj):
#         if isinstance(obj.category_name, list):
#             return ", ".join(obj.category_name)
#         return obj.category_name or "-"
#     category_name_display.short_description = "Categories"

#     def subcategory_name_display(self, obj):
#         if isinstance(obj.subcategory_name, list):
#             return ", ".join(obj.subcategory_name)
#         return obj.subcategory_name or "-"
#     subcategory_name_display.short_description = "Subcategories"


# ===============================Working Home Exterior Admin=============================================
# class ExteriorCategoryImageInline(NestedTabularInline):
#     model = ExteriorCategoryImage
#     extra = 1

# class ExteriorHomeCategoryInline(NestedStackedInline):
#     model = ExteriorHomeCategory
#     inlines = [ExteriorCategoryImageInline]
#     extra = 1

# @admin.register(HomeExterior)
# class HomeExteriorAdmin(NestedModelAdmin):
#     inlines = [ExteriorHomeCategoryInline]
#     list_display = ['title', 'description', 'display_data_preview']
#     readonly_fields = ['display_data_preview']

#     def get_fields(self, request, obj=None):
#         return [
#             'title',
#             'description',
#             'display_data_preview',
#         ]

#     def save_model(self, request, obj, form, change):
#         obj.type = "Home Exterior"
#         super().save_model(request, obj, form, change)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "banners":
#             kwargs["queryset"] = Banner.objects.filter(type="home_banner")
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

#     def display_data_preview(self, obj):
#         if not obj.pk:
#             return "Save and continue editing to see preview."

#         html = ""
#         categories = obj.exterior_categories.all()
#         for cat in categories:
#             html += f"<strong>Category: {cat.name}</strong><br>"
#             for img in cat.exterior_images.all():
#                 if img.image:
#                     html += f'<img src="{img.image.url}" width="150" style="margin: 5px; border: 1px solid #ccc;">'
#             html += "<br><br>"

#         return format_html(html)
# =====================================================================================================================

class ExteriorCategoryImageInline(NestedTabularInline):
    model = ExteriorCategoryImage
    extra = 1

class ExteriorHomeCategoryInline(NestedStackedInline):
    model = ExteriorHomeCategory
    inlines = [ExteriorCategoryImageInline]
    extra = 1



@admin.register(HomeExterior)
class HomeExteriorAdmin(NestedModelAdmin):
    inlines = [ExteriorHomeCategoryInline]
    list_display = ['title', 'description', 'display_data_preview']
    readonly_fields = ['display_data_preview']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type="Exterior")


    def get_fields(self, request, obj=None):
        return [
            'title',
            'description',
            'display_data_preview',
        ]

    def save_model(self, request, obj, form, change):
        obj.type = "Exterior"
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        home = form.instance
        # home.type = "Exterior"
        categories = home.exterior_categories.all()

        if categories.exists():
            # Use first category's name (adjust if you need multiple)
            home.category_name = categories.first().name

            # Collect all images from all categories
            all_images = []
            for cat in categories:
                all_images += [img.image.url for img in cat.exterior_images.all()]

            # Save images to JSONField
            home.category_images = {
                "images": all_images
            }

            home.save()

        # Optional: remove inlines if you don’t want them stored
        # for cat in categories:
        #     cat.exterior_images.all().delete()
        # categories.delete()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "banners":
            kwargs["queryset"] = Banner.objects.filter(type="home_banner")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def display_data_preview(self, obj):
        if not obj.pk:
            return "Save and continue editing to see preview."

        html = ""
        categories = obj.exterior_categories.all()
        for cat in categories:
            html += f"<strong>Category: {cat.name}</strong><br>"
            for img in cat.exterior_images.all():
                if img.image:
                    html += f'<img src="{img.image.url}" width="150" style="margin: 5px; border: 1px solid #ccc;">'
            html += "<br><br>"

        return format_html(html)





# @admin.register(HomeInterior)
# class HomeInteriorAdmin(admin.ModelAdmin):
#     form = HomeInteriorForm

#     list_display = [
#         'title',
#         'type_image_preview',
#         'category_image_preview',
#         'category_name_display',
#         'subcategory_name_display',
#     ]

#     def category_name_display(self, obj):
#         if isinstance(obj.category_name, list):
#             return ", ".join(obj.category_name)
#         return obj.category_name or "-"
#     category_name_display.short_description = "Categories"

#     def subcategory_name_display(self, obj):
#         if isinstance(obj.subcategory_name, list):
#             return ", ".join(obj.subcategory_name)
#         return obj.subcategory_name or "-"
#     subcategory_name_display.short_description = "Subcategories"

#     def type_image_preview(self, obj):
#         if obj.type_images and len(obj.type_images) > 0:
#             return format_html('<img src="{}" width="100" style="border-radius:4px;" />', obj.type_images[0])
#         return "-"
#     type_image_preview.short_description = "Type Image"

#     def category_image_preview(self, obj):
#         if obj.category_images and len(obj.category_images) > 0:
#             return format_html('<img src="{}" width="100" style="border-radius:4px;" />', obj.category_images[0])
#         return "-"
#     category_image_preview.short_description = "Category Image"

 

# class HomeExteriorImageInline(admin.TabularInline):
#     model = HomeExteriorImage
#     extra = 1

#     readonly_fields = ['image_preview']

#     def image_preview(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" width="100" style="border-radius:5px;" />', obj.image.url)
#         return "-"
#     image_preview.short_description = "Image Preview"

# @admin.register(HomeExterior)
# class HomeExteriorAdmin(admin.ModelAdmin):
#     form = HomeExteriorForm
#     list_display = ['title', 'category_name', 'category_image_preview','description']

#     def category_image_preview(self, obj):
#         if obj.category_images and len(obj.category_images) > 0:
#             return format_html('<img src="{}" width="100" style="border-radius:5px;" />', obj.category_images[0])
#         return "-"
#     category_image_preview.short_description = "Preview"

#current code
# @admin.register(HomeExterior)
# class HomeExteriorAdmin(admin.ModelAdmin):
#     form = HomeExteriorForm
#     list_display = ['title', 'category_name', 'image_preview', 'description']
#     inlines = [HomeExteriorImageInline]

#     def image_preview(self, obj):
#         # Loop through all related images and create HTML image tags
#         images_html = ''.join([
#             f'<img src="{image.image.url}" width="50" height="50" style="margin: 5px; border-radius: 4px;" />'
#             for image in obj.images.all()
#         ])
#         return mark_safe(images_html)
    
#     image_preview.short_description = 'Image Previews'







@admin.register(HomeWaterProof)
class HomeWaterProofAdmin(admin.ModelAdmin):
    form = HomeWaterProofForm
    list_display = ['title', 'category_name_display', 'sideimage_preview', 'description']

    def category_name_display(self, obj):
        return ", ".join(obj.category or [])

    category_name_display.short_description = "Categories"

    def sideimage_preview(self, obj):
        if obj.sideimage_url:
            return format_html('<img src="{}" width="100" style="border-radius:4px;" />', obj.sideimage_url)
        return "-"

    sideimage_preview.short_description = "Side Image"




# class ColourCodeInlineForm(forms.Form):
#     category = forms.CharField(max_length=200)
#     code = forms.CharField(max_length=7)  # Assuming the color code is a hex code
#     colorshade = forms.CharField(max_length=200)

# class ColourPaletteAdmin(admin.ModelAdmin):
#     fields = ('title', 'description', 'details', 'url')
#     list_display = ('title', 'description', 'display_colour_codes')
    
#     def get_formsets_with_inlines(self, request, obj=None):
#         # Dynamically create a formset for color codes
#         formset = self.create_inline_formset(request)
#         # Return a tuple (formset, None) to satisfy the unpacking requirement
#         yield formset, None

#     def create_inline_formset(self, request):
#         """ Creates a custom inline formset for handling color codes. """
#         # We are not using a model, so we don't need modelformset_factory
#         formset_class = forms.formset_factory(ColourCodeInlineForm, extra=1)

#         # Create the formset and bind it to the request data
#         formset = formset_class(request.POST or None)
#         return formset

#     def save_model(self, request, obj, form, change):
#         # Save the base fields first
#         super().save_model(request, obj, form, change)

#         # Get the inline form data
#         raw_form_data = request.POST
#         prefix = "form-"  # Inline form prefix
#         count = int(raw_form_data.get("form-TOTAL_FORMS", 0))
#         details_list = []

#         # Build the details list from the form data
#         for i in range(count):
#             code = raw_form_data.get(f"{prefix}{i}-code")
#             category = raw_form_data.get(f"{prefix}{i}-category")
#             shade = raw_form_data.get(f"{prefix}{i}-colorshade")
#             if code and category and shade:
#                 details_list.append({
#                     "code": code,
#                     "category": category,
#                     "colorshade": shade
#                 })

#         # Store the list of color codes in the details field
#         obj.details = details_list
#         obj.save()

#     def display_colour_codes(self, obj):
#         return json.dumps(obj.details, ensure_ascii=False, indent=2)

#     display_colour_codes.short_description = "Color Codes"

# # Register the admin class
# admin.site.register(ColourPalette, ColourPaletteAdmin)




# Inline model for ColourCode
class ColourCodeInline(admin.TabularInline):
    model = ColourCode
    extra = 1

class ColourPaletteAdmin(admin.ModelAdmin):
    inlines = [ColourCodeInline]

    def get_fields(self, request, obj=None):
        # Show only side_Title and side_description fields
        return ('side_Title', 'side_description')

admin.site.register(ColourPalette, ColourPaletteAdmin)


# class ColourCodeInline(admin.TabularInline):
#     model = ColourCode
#     extra = 1  # Number of empty forms to display

# @admin.register(MultiColorPalette)
# class MultiColorPaletteAdmin(admin.ModelAdmin):
#     inlines = [ColourCodeInline]

#     # Only show these fields in the "General" section
#     fields = ('title', 'description')

#     list_display = ('title', 'description', 'display_colour_codes')

#     def display_colour_codes(self, obj):
#         # Prepare a list of dictionaries containing the required fields
#         colour_codes = [
#             {
#                 "category": cc.category,
#                 "code": cc.code,
#                 "colorshade": cc.colorshade
#             }
#             for cc in obj.colour_codes.all()
#         ]
        
#         # Return the JSON-formatted string
#         return json.dumps(colour_codes, ensure_ascii=False)
    
#     display_colour_codes.short_description = "Color Codes"



# ===================================================================================================


# class PaintProductInline(admin.TabularInline):
#     model = PaintProduct
#     extra = 1

# class PaintCalculatorAdminForm(forms.ModelForm):
#     subtitle = forms.CharField(required=False)

#     class Meta:
#         model = PaintCalculator
#         fields = ['title', 'description']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.details:
#             self.fields['subtitle'].initial = self.instance.details.get('subtitle', '')

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         subtitle = self.cleaned_data.get("subtitle", "")
#         details = instance.details or {}
#         details['subtitle'] = subtitle
#         instance.details = details
#         if commit:
#             instance.save()
#         return instance

# @admin.register(PaintCalculator)
# class PaintCalculatorAdmin(admin.ModelAdmin):
#     form = PaintCalculatorAdminForm
#     inlines = [PaintProductInline]

#     def get_queryset(self, request):
#         # Filter only entries of type PAINT_CALCULATOR
#         qs = super().get_queryset(request)
#         return qs.filter(type="PAINT_CALCULATOR")

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)

#         instance = form.instance
#         products = instance.paint_products.all()
#         instance.details["products"] = [
#             {"product_name": p.product_name, "area": p.area} for p in products
#         ]
#         instance.save()



class PaintProductInline(admin.TabularInline):
    model = PaintProduct
    extra = 1

class PaintCalculatorAdminForm(forms.ModelForm):
    subtitle = forms.CharField(required=False, label="Subtitle")

    class Meta:
        model = PaintCalculator
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.details:
            self.fields['subtitle'].initial = self.instance.details.get('subtitle', '')

    def save(self, commit=True):
        instance = super().save(commit=False)
        subtitle = self.cleaned_data.get("subtitle", "")
        details = instance.details or {}
        details['subtitle'] = subtitle
        instance.details = details
        if commit:
            instance.save()
        return instance



@admin.register(PaintCalculator)
class PaintCalculatorAdmin(admin.ModelAdmin):
    form = PaintCalculatorAdminForm
    inlines = [PaintProductInline]

    def get_queryset(self, request):
        # Filter only entries of type PAINT_CALCULATOR
        qs = super().get_queryset(request)
        return qs.filter(type="PAINT_CALCULATOR")

    list_display = ['title', 'get_subtitle', 'short_description', 'display_products']

    def get_subtitle(self, obj):
        return obj.details.get('subtitle', '—')
    get_subtitle.short_description = 'Subtitle'

    def short_description(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description or '—'
    short_description.short_description = 'Description'

    def display_products(self, obj):
        products = obj.paint_products.all()
        if not products:
            return '—'

        product_data = [
            {"product_name": p.product_name, "area": p.area} for p in products
        ]
        return mark_safe(f'<pre>{json.dumps(product_data, indent=4)}</pre>')
    display_products.short_description = 'Products'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        products = instance.paint_products.all()
        instance.details["products"] = [
            {"product_name": p.product_name, "area": p.area} for p in products
        ]
        instance.save()
# @admin.register(PaintCalculator)
# class PaintCalculatorAdmin(admin.ModelAdmin):
#     form = PaintCalculatorAdminForm
#     inlines = [PaintProductInline]

    
#     def get_queryset(self, request):
#         # Filter only entries of type PAINT_CALCULATOR
#         qs = super().get_queryset(request)
#         return qs.filter(type="PAINT_CALCULATOR")

#     list_display = ['title', 'get_subtitle', 'short_description', 'display_products']

#     def get_subtitle(self, obj):
#         return obj.details.get('subtitle', '—')
#     get_subtitle.short_description = 'Subtitle'

#     def short_description(self, obj):
#         return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description or '—'
#     short_description.short_description = 'Description'

#     def display_products(self, obj):
#         products = obj.paint_products.all()
#         if not products:
#             return '—'
#             product_data = [
#             {"product_name": p.product_name, "area": p.area} for p in products
#             ]
#             return mark_safe(f'<pre>{json.dumps(product_data, indent=4)}</pre>')
#     display_products.short_description = 'Products'

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         instance = form.instance
#         products = instance.paint_products.all()
#         instance.details["products"] = [
#             {"product_name": p.product_name, "area": p.area} for p in products
#         ]
#         instance.save()
