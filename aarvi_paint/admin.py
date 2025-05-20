from pyexpat.errors import messages
from django.contrib import admin,messages
from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.html import format_html,format_html_join
from django.urls import path, reverse
from django.utils.html import format_html
from django.forms.models import BaseInlineFormSet
import nested_admin
from .admin_mixins import NoSuccessMessageAdminMixin  
from nested_admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from django.utils.safestring import mark_safe
from django import forms
import json
from django.template.response import TemplateResponse
from django.contrib.auth.models import User, Group
from .forms import  HomeInteriorBannerForm,PaintCalculatorBannerForm,SettingAdminForm, HomeExteriorBannerForm, ColourPaletteForm, ParallaxForm,HomeBannerImageForm,AboutUsAdminForm,TestimonialAdminForm,\
    BrochureForm, AdditionalInfoForm, AdminContactDetailsForm, CategoryForm, ProductForm, HomeForm, GalleryBannerForm,GalleryBannerImageForm,InspirationForm,AboutUsForm, HomeWaterProofForm,\
    AboutUsTopBannerForm, ColorPalletsBannerForm, ProductBannerForm, ContactUsBannerForm, HomeWaterproofingBannerForm,HomeExteriorForm,ColourPaletteImageInlineForm,WaterCalculatorAdminForm, PaintCalculatorAdminForm,\
    AboutUsBottomVideoBannerForm, BaseBannerForm,HomeInteriorForm, BaseHomeInteriorForm,HomeExteriordataForm,BannerImageInline,MultiColorPaletteForm
from .models import PaintCalculatorBanner,AboutUsBottomVideoBanner, PaintProduct,PaintCalculator,ColourCode,HomeExteriorBanner,WaterProduct, Testimonial,HomeInteriorBanner,  PaintBudgetCalculator, ColourPalette,Inspiration, \
    Parallax, Brochure, AdditionalInfo, AdminContactDetails, WaterProofCalculator, Category, Product, UserInfo, Home,CategoryImage, TypeImage,HomeExterior,\
    Banner, GalleryBanner,CategoryImage,AboutUsTopBanner, ColorPalletsBanner, ProductBanner, ContactUsBanner, Category, CategoryImage,AboutUs, WaterCalculator,HomeWaterProof,\
    HomeWaterproofingBanner,HomeInterior, HomeInteriorCategory,HomeInteriorSubCategory, HomeInteriorSubCategoryImage,HomeInteriorFeature, AboutUsBottomVideoBanner,ExteriorHomeCategory, ExteriorCategoryImage, Setting, HomeBanner,BannerImage, HomeInterior, CategoryImage,ColourPaletteWithImages, ColourPaletteImage,MultiColorPalette


# Unregister default auth models (optional if you only want superuser access)
admin.site.unregister(User)
admin.site.unregister(Group)
# ===================================Remove change messages ====================================
# class NoSuccessMessageAdminMixin:
#     def response_add(self, request, obj, post_url_continue=None):
#         url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist")
#         return HttpResponseRedirect(url)

#     def response_change(self, request, obj):
#         url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist")
#         return HttpResponseRedirect(url)

#     def response_delete(self, request, obj_display, obj_id):
#         url = reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist")
#         return HttpResponseRedirect(url)
# ========================================================================




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
            # f"<a href='{obj.url['video']}' target='_blank'>{obj.url['video']}</a><br>"
        )

    return mark_safe(html)


display_media_urls.short_description = "Media URLs"



# ======================================================================================================


@admin.register(AboutUs)
class AboutUsAdmin(NoSuccessMessageAdminMixin, admin.ModelAdmin):
    form = AboutUsAdminForm
    actions = []

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return AboutUs.objects.count() < 1
    
    def delete_link(self, obj):
      url = reverse('admin:aarvi_paint_aboutus_delete', args=[obj.pk])
      return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')

    delete_link.short_description = 'Action'


    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    
    # def response_add(self, request, obj, post_url_continue=None):
    #     # Redirect to changelist page (list view) without messages
    #     url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist")
    #     return HttpResponseRedirect(url)

    # def response_change(self, request, obj):
    #     # Redirect to changelist page (list view) without messages
    #     url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist")
    #     return HttpResponseRedirect(url)

    # def response_delete(self, request, obj_display, obj_id):
    #     # Redirect to changelist page after delete, no success message
    #     url = reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist")
    #     return HttpResponseRedirect(url)


    list_display = [
        'title',
        'short_description',
        'get_lower_title',
        'get_lower_sub_title',
        'get_lower_description',
        'get_happy_client',
        'get_work_job',
        'get_location',
        'get_work_member',
        'delete_link',
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
            'fields': ('happy_client', 'work_job', 'location', 'work_member'),
            'classes': ('collapse',),
        }),
    )

    # Show preview of 'description'
    def short_description(self, obj):
        return obj.description[:50] + '...' if obj.description else '—'
    short_description.short_description = 'Description'

    # -- Individual accessors for details fields --
    def get_lower_title(self, obj):
        return obj.details.get('lower_title', '') if obj.details else ''
    get_lower_title.short_description = 'Lower Title'

    def get_lower_sub_title(self, obj):
        return obj.details.get('lower_sub_title', '') if obj.details else ''
    get_lower_sub_title.short_description = 'Lower Sub Title'

    def get_lower_description(self, obj):
        return obj.details.get('lower_description', '') if obj.details else ''
    get_lower_description.short_description = 'Lower Description'

    def get_happy_client(self, obj):
        return obj.details.get('happy_client', '') if obj.details else ''
    get_happy_client.short_description = 'Happy Client'

    def get_work_job(self, obj):
        return obj.details.get('work_job', '') if obj.details else ''
    get_work_job.short_description = 'Work Job'

    def get_location(self, obj):
        return obj.details.get('location', '') if obj.details else ''
    get_location.short_description = 'Location'

    def get_work_member(self, obj):
        return obj.details.get('work_member', '') if obj.details else ''
    get_work_member.short_description = 'Work Member'




# @admin.register(AboutUs)
# class AboutUsAdmin(admin.ModelAdmin):
#     form = AboutUsAdminForm
#     actions = []  

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
    
#     def has_add_permission(self, request):
#         return AboutUs.objects.count() < 1

#     list_display = [
#         'title',
#         'short_description',
#         'short_details',  # Display details as JSON
#     ]

#     fieldsets = (
#         ('Main Information', {
#             'fields': ('title', 'description')
#         }),
#         ('Lower Section', {
#             'fields': ('lower_title', 'lower_sub_title', 'lower_description'),
#             'classes': ('collapse',)
#         }),
#         # ('Additional Information', {
#         #     'fields': ('extra_info',),
#         #     'classes': ('collapse',),
#         # }),
#         ('Additional Information', {
#             'fields': ('happy_client', 'work_job', 'location', 'work_member'),
#             'classes': ('collapse',),
#         }),
#     )

#     def short_description(self, obj):
#         return obj.description[:50] + '...' if obj.description else '—'
#     short_description.short_description = 'Description'

#     def short_details(self, obj):
#         if not obj.details:
#             return '—'
#         # Render details field as a JSON string
#         return mark_safe('<pre>' + json.dumps(obj.details, indent=4) + '</pre>')

#     short_details.short_description = 'Details (JSON)'

# ==================Home Banner======================================

class BannerImageInline(admin.StackedInline):
    model = BannerImage
    extra = 1
    form = HomeBannerImageForm
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']  # Only image upload here

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.image.url
            )
        return "No image"
    # image_preview.short_description = 'Preview'

    # def get_fields(self, request, obj=None):
    #     # If it's a new object (not saved yet), show image upload field
    #     if obj and obj.pk:
    #         return ['image_preview']
    #     return ['image', 'image_preview']
    def get_fields(self, request, obj=None):
         return ['image', 'image_preview'] 

# class BannerImageInline(admin.StackedInline):
#     model = BannerImage
#     extra = 1
#     form = HomeBannerImageForm
#     readonly_fields = ['image_preview']
#     fields = ['image', 'image_preview']  # Always include both fields

#     class Media:
#         css = {
#             'all': ('css/admin_custom.css',)
#         }

#     def image_preview(self, obj):
#         if obj.image:
#             return format_html(
#                 '<img src="{}" style="max-height: 100px;"/>',
#                 obj.image.url
#             )
#         return "No image"
#     # image_preview.short_description = 'Preview'

#     def get_fields(self, request, obj=None):
#         return ['image', 'image_preview'] 
    


@admin.register(HomeBanner)
class HomeBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    

    inlines = [BannerImageInline]
    list_display = ['banner_preview', 'image_count','delete_link']
    list_display_links = ['banner_preview']
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    
    delete_link.short_description = 'Action'    


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

    def get_fieldsets(self, request, obj=None):
        return []
    
    def has_add_permission(self, request):
        return HomeBanner.objects.filter(type='home-banner').count() < 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-banner')

    def save_model(self, request, obj, form, change):
        obj.type = 'home-banner'
        super().save_model(request, obj, form, change)

# ===================================================================Additional info inspiration========================


@admin.register(Inspiration)
class InspirationAdmin(NoSuccessMessageAdminMixin, admin.ModelAdmin):
    form = InspirationForm
    list_display = ('title', 'description', 'image_preview','delete_link')
    readonly_fields = ('image_preview',)
    exclude = ('type', 'url', 'details')  # hide raw JSON
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="/media/{}" width="100" height="auto" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Image Preview'

    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='inspiration')

    def save_model(self, request, obj, form, change):
        obj.type = 'inspiration'
        super().save_model(request, obj, form, change)


# ======================================================================================================================================/


@admin.register(Testimonial)
class TestimonialAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = TestimonialAdminForm
    list_display = ('name', 'description','image_preview','delete_link')
    readonly_fields = ['image_display']
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'image',
                'image_display',
                
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


    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'


    

    def image_display(self, obj):
        url = obj.url.get('image')
        if url:
            return mark_safe(f'<img src="{url}" style="max-height: 200px;" />')
        return "No image uploaded."
    image_display.short_description = "Current Image"





# ===================================================water calculator========================================================
class WaterProductInline(admin.TabularInline):
    model = WaterProduct
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }



@admin.register(WaterCalculator)
class WaterCalculatorAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = WaterCalculatorAdminForm
    inlines = [WaterProductInline]
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    
    def has_add_permission(self, request):
        return WaterCalculator.objects.filter(type="WATER_CALCULATOR").count() < 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type="WATER_CALCULATOR")

    list_display = ['title', 'get_subtitle', 'short_description', 'display_products','delete_link']

    def get_subtitle(self, obj):
        return obj.details.get('subtitle', '—')
    get_subtitle.short_description = 'Subtitle'
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'

    

    def short_description(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description or '—'
    short_description.short_description = 'Description'

    def display_products(self, obj):
        products = obj.water_products.all()
        if not products:
            return '—'

        rows = ''.join([
            f'<tr>'
            f'<td style="border:1px solid #ccc;padding:4px;">{p.product_name}</td>'
            f'<td style="border:1px solid #ccc;padding:4px;">{p.area}</td>'
            f'</tr>'
            for p in products
        ])

        return mark_safe(f'''
            <table style="border:1px solid #ccc; border-collapse:collapse;">
                <thead>
                    <tr>
                        <th style="border:1px solid #ccc;padding:4px;">Product Name</th>
                        <th style="border:1px solid #ccc;padding:4px;">Area</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        ''')
    display_products.short_description = 'Products'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        products = instance.water_products.all()
        instance.details["products"] = [
            {"product_name": p.product_name, "area": p.area} for p in products
        ]
        instance.save()



# class BannerImageInline(admin.TabularInline):
#     model = BannerImage
#     extra = 1



# class GalleryBannerAdmin(admin.ModelAdmin):
#     form = GalleryBannerImageForm
#     inlines = [BannerImageInline]
#     list_display = ['banner_preview', 'image_count','delete_link']
#     list_display_links = ['banner_preview']
#     actions = []  

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
    

#     def image_count(self, obj):
#         count = obj.images.count()
#         return format_html(
#             '<span style="color:{}; font-weight: bold;">{}</span>',
#             '#4CAF50' if count else '#F44336',
#             f"{count} image{'s' if count != 1 else ''}"
#         )
#     image_count.short_description = 'Images'


#     class Media:
#         css = {
#             'all': ('css/admin_custom.css',)
#         }


#     def delete_link(self, obj):
#         url = reverse(
#             f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
#             args=[obj.pk]
#         )
#         return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


#     delete_link.short_description = 'Action'


#     def banner_preview(self, obj):
#         images = obj.images.all()
#         if images:
#             return format_html(
#                 ''.join(
#                     f'<img src="{image.image.url}" style="height: 50px; margin-right: 5px; border-radius: 4px;" />'
#                     for image in images if image.image and hasattr(image.image, 'url')
#                 )
#             )
#         return format_html('<span style="color:red;">No images uploaded</span>')
#     banner_preview.short_description = 'Banner Preview'

#     fieldsets = (
#         ('General Information', {
#             'fields': (),
#             'description': format_html(
#                 '''
#                 <div style="background:#f8f8f8; padding:20px; border-radius:5px;">
#                     <h3 style="margin-top:0">Home Gallery Management</h3>
#                     <p style="margin-bottom:0">
#                         <strong>Add images using the "Gallery Images" section below</strong>
#                     </p>
#                 </div>
#                 '''
#             ),
#         }),
#     )

#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(type='gallery-banner')
    
#     def has_add_permission(self, request):
#         return HomeBanner.objects.filter(type='gallery-banner').count() < 1

#     def save_model(self, request, obj, form, change):
#         obj.type = 'gallery-banner'
#         super().save_model(request, obj, form, change)
# admin.site.register(GalleryBanner,GalleryBannerAdmin)

class GalleryBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = GalleryBannerImageForm
    inlines = [BannerImageInline]
    list_display = ['banner_preview', 'image_count', 'delete_link']
    list_display_links = ['banner_preview']
    actions = []  

    def get_fieldsets(self, request, obj=None):
        return []

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def image_count(self, obj):
        count = obj.images.count()
        return format_html(
            '<span style="color:{}; font-weight: bold;">{}</span>',
            '#4CAF50' if count else '#F44336',
            f"{count} image{'s' if count != 1 else ''}"
        )
    image_count.short_description = 'Images'

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    def response_add(self, request, obj, post_url_continue=None):
        # Redirect to changelist page (list view) without messages
        url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist")
        return HttpResponseRedirect(url)

    def response_change(self, request, obj):
        # Redirect to changelist page (list view) without messages
        url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist")
        return HttpResponseRedirect(url)

    def response_delete(self, request, obj_display, obj_id):
        # Redirect to changelist page after delete, no success message
        url = reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist")
        return HttpResponseRedirect(url)

    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')
    delete_link.short_description = 'Action'

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

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='gallery-banner')
    
    def has_add_permission(self, request):
        return HomeBanner.objects.filter(type='gallery-banner').count() < 1

    def save_model(self, request, obj, form, change):
        obj.type = 'gallery-banner'
        super().save_model(request, obj, form, change)
admin.site.register(GalleryBanner,GalleryBannerAdmin)


@admin.register(HomeInteriorBanner)
class HomeInteriorBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = HomeInteriorBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    readonly_fields = ['display_image_urls']
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'


    def has_add_permission(self, request):
        return HomeInteriorBanner.objects.filter(type="home-interior-banner").count() < 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-interior-banner')

    display_image_urls = display_media_urls


@admin.register(PaintCalculatorBanner)
class PaintCalculatorBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = PaintCalculatorBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    readonly_fields = ['display_image_urls']
    actions = [] 


    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
  
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'


    def has_add_permission(self, request):
        return PaintCalculatorBanner.objects.filter(type="paint-calculator-banner").count() < 1
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='paint-calculator-banner')

    display_image_urls = display_media_urls



@admin.register(HomeExteriorBanner)
class HomeExteriorBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = HomeExteriorBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    exclude = ['url']
    readonly_fields = ['display_image_urls']
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
 
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def has_add_permission(self, request):
        return HomeExteriorBanner.objects.filter(type="home-exterior-banner").count() < 1
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'


    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-exterior-banner')

    display_image_urls = display_media_urls


@admin.register(HomeWaterproofingBanner)
class HomeWaterproofingBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = HomeWaterproofingBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    exclude = ['url']
    readonly_fields = ['display_image_urls']
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'

    
    def has_add_permission(self, request):
        return HomeWaterproofingBanner.objects.filter(type="home-waterproofing-banner").count() < 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='home-waterproofing-banner')

    display_image_urls = display_media_urls


@admin.register(AboutUsTopBanner)
class AboutUsTopBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = AboutUsTopBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    exclude = ['url']
    readonly_fields = ['display_image_urls']
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'

    
    
    def has_add_permission(self, request):
        return AboutUsTopBanner.objects.filter(type="about-us-top-banner").count() < 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='about-us-top-banner')

    display_image_urls = display_media_urls


@admin.register(ColorPalletsBanner)
class ColorPalletsBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = ColorPalletsBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    exclude = ['url']
    readonly_fields = ['display_image_urls']
    actions = [] 

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'

    
    
    def has_add_permission(self, request):
        return ColorPalletsBanner.objects.filter(type="color-pallets-banner").count() < 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='color-pallets-banner')

    display_image_urls = display_media_urls


@admin.register(ProductBanner)
class ProductBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = ProductBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    exclude = ['url']
    readonly_fields = ['display_image_urls']
    actions = []  


    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
   
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'

    
    
    def has_add_permission(self, request):
        return ProductBanner.objects.filter(type="product-banner").count() < 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='product-banner')

    display_image_urls = display_media_urls


@admin.register(ContactUsBanner)
class ContactUsBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = ContactUsBannerForm
    list_display = ['title', 'type', 'short_description', 'display_image_urls','delete_link']
    exclude = ['url']
    readonly_fields = ['display_image_urls']
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
 
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'

    
    
    def has_add_permission(self, request):
        return ContactUsBanner.objects.filter(type="contact-us-banner").count() < 1

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type='contact-us-banner')

    display_image_urls = display_media_urls



@admin.register(AboutUsBottomVideoBanner)
class AboutUsBottomVideoBannerAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = AboutUsBottomVideoBannerForm
    list_display = ['type', 'display_video_urls','delete_link']
    exclude = ['url']
    readonly_fields = ['display_video_urls']
    actions = []  
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'


    
    
    def has_add_permission(self, request):
        return AboutUsBottomVideoBanner.objects.filter(type='about-us-bottom-video-banner').count() < 1

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
        'delete_link',
    ]
    readonly_fields = [f.name for f in PaintBudgetCalculator._meta.fields]
    # actions = None
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
 
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'
    

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



@admin.register(Parallax)
class ParallaxAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = ParallaxForm
    exclude = ('url',)
    list_display = ['title', 'sub_title', 'description', 'priority', 'get_desktop_preview', 'get_mobile_preview','delete_link']
    readonly_fields = ['get_desktop_preview', 'get_mobile_preview']
    actions = []  


    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
 

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'
    

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
class BrochureAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = BrochureForm
    readonly_fields = ['preview_image', 'preview_pdf']
    list_display = ['uploaded_pdf', 'preview_image','delete_link']
    actions = []


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
 
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'
    

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



@admin.register(AdminContactDetails)
class AdminContactDetailsAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = AdminContactDetailsForm
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def has_add_permission(self, request):
        return AdminContactDetails.objects.count() < 1
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
 
    
    

    list_display = [
        'location',
        'phone_number',
        'email',
        'google_link',
        'display_social_media_links',
        'delete_link',
    ]

    # search_fields = [
    #     'location',
    #     'phone_number',
    #     'email',
    #     'google_link',
    # ]
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'
    

    def display_social_media_links(self, obj):
        links = obj.social_media_links or {}
        instagram = links.get('instagram', '')
        facebook = links.get('facebook', '')
        whatsapp = links.get('whatsapp', '')
        return f"Insta: {instagram}, FB: {facebook}, WA: {whatsapp}"

    display_social_media_links.short_description = "Social Media Links"

@admin.register(Setting)
class SettingAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = SettingAdminForm
    actions = []
    readonly_fields = ['logo_preview', 'side_image_preview']

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return Setting.objects.count() < 1

    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')

    delete_link.short_description = 'Action'

    list_display = [
        'name',
        'copyright',
        'display_app_download_links',
        'get_logo_preview',
        'get_side_image_preview',
        'hide',
        'delete_link',
    ]

   

    # ========== PREVIEW METHODS ==========

    def logo_preview(self, obj):
        return self.get_logo_preview(obj)

    logo_preview.short_description = 'Logo Preview'

    def side_image_preview(self, obj):
        return self.get_side_image_preview(obj)

    side_image_preview.short_description = 'Side Image Preview'

    def get_logo_preview(self, obj):
        url_data = obj.url if isinstance(obj.url, dict) else {}
        logo_url = url_data.get('logo')
        if logo_url:
            return mark_safe(f'<img src="{logo_url}" style="max-height: 50px; border: 1px solid #ccc;" />')
        return "No logo available"

    def get_side_image_preview(self, obj):
        url_data = obj.url if isinstance(obj.url, dict) else {}
        side_image_url = url_data.get('side_image')
        if side_image_url:
            return mark_safe(f'<img src="{side_image_url}" style="max-height: 50px; border: 1px solid #ccc;" />')
        return "No side image available"

    def display_app_download_links(self, obj):
        links = obj.app_download_links or {}
        playstore = links.get('playstore', '')
        appstore = links.get('appstore', '')
        return f"Play Store: {playstore}, App Store: {appstore}"

    display_app_download_links.short_description = "App Download Links"

@admin.register(Category)
class CategoryAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = CategoryForm
    list_display = ['category', 'display_subcategories', 'delete_link']  # changed here
    # search_fields = ['name']
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')
    delete_link.short_description = 'Action'
    
    def has_add_permission(self, request):
        return Category.objects.count() < 1

    def display_subcategories(self, obj):
        return ", ".join(obj.subcategory_names or [])
    display_subcategories.short_description = 'Subcategories'

    def category(self, obj):
        return obj.name
    category.short_description = 'Category'

@admin.register(Product)
class ProductAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = ProductForm

    list_display = [
        'title',
        'subtitle',
        'short_description',
        'long_description',
        'keyfeature',
        'get_category_name',
        'subcategory',
        'colour_palate1',
        'colour_palate2',
        'get_detail_type',
        'get_detail_quantity',
        'get_detail_finish',
        'get_detail_sqft',
        'get_detail_warranty',
        'get_image_preview',
        'delete_link'
    ]

    search_fields = ['title', 'keyfeature']
    list_filter = ['category']
    actions = []

    # ---------- Helpers for details fields ----------
    def get_detail_type(self, obj):
    # Check if details is not None and is a dictionary before accessing the type key
        details = obj.detail if isinstance(obj.detail, dict) else {}
        return details.get("type", "")  # Safely get 'type', or return empty string if not present
    get_detail_type.short_description = "Type"

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    def get_detail_quantity(self, obj):
        return obj.detail.get("quantity", "") if obj.detail else ""
    get_detail_quantity.short_description = "Quantity"

    def get_detail_finish(self, obj):
        return obj.detail.get("finish", "") if obj.detail else ""
    get_detail_finish.short_description = "Finish"

    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Delete'
    

    def get_detail_sqft(self, obj):
        return obj.detail.get("Sqft_lt", "") if obj.detail else ""
    get_detail_sqft.short_description = "Sqft / lt"

    def get_detail_warranty(self, obj):
        return obj.detail.get("warranty", "") if obj.detail else ""
    get_detail_warranty.short_description = "Warranty"

    # ---------- Other helpers ----------
    def get_category_name(self, obj):
        return obj.category.name
    get_category_name.short_description = "Category Name"

    def get_image_preview(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image"
    get_image_preview.short_description = "Image Preview"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # def has_add_permission(self, request):
    #     return Product.objects.count() < 1

    class Media:
        js = ('js/product_subcategory.js',)


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
        'delete_link'
    ]
    readonly_fields = [f.name for f in WaterProofCalculator._meta.fields]
    # actions = None
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'


    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    

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

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


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

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }





class HomeInteriorSubCategoryImageInline(NestedTabularInline):
    model = HomeInteriorSubCategoryImage
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


class HomeInteriorSubCategoryInline(NestedStackedInline):
    model = HomeInteriorSubCategory
    inlines = [HomeInteriorSubCategoryImageInline]
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


class HomeInteriorCategoryInline(NestedStackedInline):
    model = HomeInteriorCategory
    inlines = [HomeInteriorSubCategoryInline]
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

class HomeInteriorFeatureInline(NestedStackedInline):
    model = HomeInteriorFeature
    extra = 1
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


@admin.register(HomeInterior)
class HomeInteriorAdmin(NoSuccessMessageAdminMixin,NestedModelAdmin):
    inlines = [HomeInteriorCategoryInline, HomeInteriorFeatureInline]
    list_display = ['title', 'description', 'display_data_preview','delete_link']
    readonly_fields = ['display_data_preview']
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def has_add_permission(self, request):
        return HomeInterior.objects.filter(type="Interior").count() < 1
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }



    delete_link.short_description = 'Action'
    

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










class ExteriorCategoryImageInline(NestedStackedInline):
    model = ExteriorCategoryImage
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)  # Assuming static path is set correctly
        }

class ExteriorHomeCategoryInline(NestedStackedInline):
    model = ExteriorHomeCategory
    inlines = [ExteriorCategoryImageInline]
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }





@admin.register(HomeExterior)
class HomeExteriorAdmin(NoSuccessMessageAdminMixin,NestedModelAdmin):
    inlines = [ExteriorHomeCategoryInline]
    list_display = ['title', 'description', 'display_data_preview','delete_link']
    readonly_fields = ['display_data_preview']
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    
    def has_add_permission(self, request):
        return HomeExterior.objects.filter(type="Exterior").count() < 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type="Exterior")
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'
    


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

# =========================================================================================================================
@admin.register(HomeWaterProof)
class HomeWaterProofAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = HomeWaterProofForm
    readonly_fields = ['sideimage_preview']
    list_display = ['title', 'category_name_display', 'sideimage_preview', 'description', 'delete_link']
    actions = []

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    #  return HomeWaterProof.objects.filter(type="WaterProf").count() < 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')

    delete_link.short_description = 'Action'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type="WaterProf")

    def save_model(self, request, obj, form, change):
        obj.type = 'WaterProf'
        super().save_model(request, obj, form, change)

    def category_name_display(self, obj):
        return obj.category_name or "-"

    category_name_display.short_description = "Categories"

    def sideimage_preview(self, obj):
        sideimage_url = obj.category_images.get("sideimage") if obj.category_images else None
        if sideimage_url:
            return format_html('<img src="{}" width="100" style="border-radius:4px;" />', sideimage_url)
        return "-"

    sideimage_preview.short_description = "Side Image Preview"


class PaintProductInline(admin.TabularInline):
    model = PaintProduct
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }





@admin.register(PaintCalculator)
class PaintCalculatorAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = PaintCalculatorAdminForm
    inlines = [PaintProductInline]
    actions = []  

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

    
    def has_add_permission(self, request):
        return PaintCalculator.objects.filter(type="PAINT_CALCULATOR").count() < 1

    def get_queryset(self, request):
        # Filter only entries of type PAINT_CALCULATOR
        qs = super().get_queryset(request)
        return qs.filter(type="PAINT_CALCULATOR")

    list_display = ['title', 'get_subtitle', 'short_description', 'display_products','delete_link']

    def get_subtitle(self, obj):
        return obj.details.get('subtitle', '—')
    get_subtitle.short_description = 'Subtitle'

    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'
    

    def short_description(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description or '—'
    short_description.short_description = 'Description'

    def display_products(self, obj):
        products = obj.paint_products.all()
        if not products:
            return '—'

        table_rows = ''.join([
            f'<tr><td>{p.product_name}</td><td>{p.area}</td></tr>' for p in products
        ])

        return mark_safe(f'''
            <table style="border: 1px solid #ccc; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #ccc; padding: 4px;">Product Name</th>
                        <th style="border: 1px solid #ccc; padding: 4px;">Area</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        ''')
    display_products.short_description = 'Paint Products'
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        products = instance.paint_products.all()
        instance.details["products"] = [
            {"product_name": p.product_name, "area": p.area} for p in products
        ]
        instance.save()










# class ColourPaletteImageInline(admin.TabularInline):
#     model = ColourPaletteImage
#     extra = 1
#     max_num = 10

# @admin.register(ColourPaletteWithImages)
# class ColourPaletteWithImagesAdmin(admin.ModelAdmin):
#     inlines = [ColourPaletteImageInline]
#     list_display = ['title', 'description_preview', 'image_preview']

#     def get_fields(self, request, obj=None):
#         return ('title', 'description')

#     def save_model(self, request, obj, form, change):
#         obj.type = 'color-palette-with-images'
#         super().save_model(request, obj, form, change)

#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         instance = form.instance
#         instance.url = {
#             str(image.pk): image.image.url for image in instance.images.all()
#         }
#         instance.save()

#     def description_preview(self, obj):
#         if obj.description:
#             return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description
#         return "—"
#     description_preview.short_description = 'Description'

#     def image_preview(self, obj):
#         if not obj.images.exists():
#             return "No Images"
#         images_html = ''.join([
#             f'<img src="{image.image.url}" width="50" height="50" style="margin: 3px; border:1px solid #ccc;" />'
#             for image in obj.images.all()
#         ])
#         return mark_safe(images_html)
#     image_preview.short_description = 'Image Previews'
class ColourPaletteImageInline(admin.StackedInline):
    model = ColourPaletteImage
    form = ColourPaletteImageInlineForm
    extra = 1
    max_num = 10

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
    
    


@admin.register(ColourPaletteWithImages)
class ColourPaletteWithImagesAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    inlines = [ColourPaletteImageInline]
    list_display = ['title', 'description_preview', 'image_preview','delete_link']
    actions = []  

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def has_add_permission(self, request):
        return ColourPaletteWithImages.objects.filter(type="color-palette-with-images").count() < 1
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type='color-palette-with-images')

    def get_fields(self, request, obj=None):
        return ('title', 'description')

    def save_model(self, request, obj, form, change):
        obj.type = 'color-palette-with-images'
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        instance.url = {
            str(image.pk): image.image.url for image in instance.images.all()
        }
        instance.save()

    def description_preview(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else obj.description or '—'
    description_preview.short_description = 'Description'

    def image_preview(self, obj):
        if not obj.images.exists():
            return "No Images"
        images_html = ''.join([
            f'<img src="{img.image.url}" width="50" height="50" style="margin: 3px; border:1px solid #ccc;" />'
            for img in obj.images.all()
        ])
        return mark_safe(images_html)
    image_preview.short_description = 'Image Previews'



class ColourCodeInline(admin.TabularInline):
    model = ColourCode
    extra = 1

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }



@admin.register(MultiColorPalette)
class MultiColorPaletteAdmin(NoSuccessMessageAdminMixin,admin.ModelAdmin):
    form = MultiColorPaletteForm
    inlines = [ColourCodeInline]

    list_display = [
        'side_Title',
        'short_description',
        'display_colour_codes',
        'delete_link'
    ]

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


    actions = []

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def delete_link(self, obj):
        url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete",
            args=[obj.pk]
        )
        return mark_safe(f'<a href="{url}" style="color:red;">Delete</a>')


    delete_link.short_description = 'Action'


    def has_add_permission(self, request):
        return MultiColorPalette.objects.filter(type="multi-color-palette").count() < 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(type='multi-color-palette')

    def short_description(self, obj):
        return (obj.side_description[:50] + '...') if obj.side_description and len(obj.side_description) > 50 else obj.side_description or '—'
    short_description.short_description = 'Side Description'

    # # Show first colour code values
    # def colourcode(self, obj):
    #     first = obj.colour_codes.first()
    #     return first.code if first else '—'
    # colourcode.short_description = 'Colour Code'

    # def category(self, obj):
    #     first = obj.colour_codes.first()
    #     return first.category if first else '—'
    # category.short_description = 'Category'

    # def colorshade(self, obj):
    #     first = obj.colour_codes.first()
    #     return first.colorshade if first else '—'
    # colorshade.short_description = 'Color Shade'

    def display_colour_codes(self, obj):
        codes = obj.colour_codes.all()
        if not codes:
            return '—'

        rows = ''.join([
            f'<tr>'
            f'<td style="border:1px solid #ccc;padding:4px;">{c.code}</td>'
            f'<td style="border:1px solid #ccc;padding:4px;">{c.category}</td>'
            f'<td style="border:1px solid #ccc;padding:4px;">{c.colorshade}</td>'
            f'</tr>'
            for c in codes
        ])

        return mark_safe(f'''
            <table style="border:1px solid #ccc; border-collapse:collapse;">
                <thead>
                    <tr>
                        <th style="border:1px solid #ccc;padding:4px;">Code</th>
                        <th style="border:1px solid #ccc;padding:4px;">Category</th>
                        <th style="border:1px solid #ccc;padding:4px;">Color Shade</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        ''')
    display_colour_codes.short_description = 'All Colour Codes'


    def save_model(self, request, obj, form, change):
        obj.type = 'multi-color-palette'
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        instance = form.instance
        instance.details = {
            "colour_codes": [
                {"code": c.code, "category": c.category, "colorshade": c.colorshade}
                for c in instance.colour_codes.all()
            ]
        }
        instance.save()

