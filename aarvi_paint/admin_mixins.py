from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib import admin

class NoSuccessMessageAdminMixin:

    def message_user(self, *args, **kwargs):
        pass


class ButtonActionMixin:
    def action(self, obj):
        edit_url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=[obj.pk])
        delete_url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_delete", args=[obj.pk])

        return format_html(
            '<a href="{}" style="display:block; margin-bottom: 6px;">'
            '<button type="button" style="background-color:#4CAF50; color:white; padding:4px 12px; border:none; border-radius:4px;">Edit</button>'
            '</a>'
            '<a href="{}" style="display:block;">'
            '<button type="button" style="background-color:#f44336; color:white; padding:4px 12px; border:none; border-radius:4px;">Delete</button>'
            '</a>',
            edit_url, delete_url
        )

    action.short_description = 'Action'
    action.allow_tags = True  # optional, safe for older Django versions




class CommonAdminMixin(admin.ModelAdmin):
    list_display = [
        'display_title',
        'display_type',
        'display_short_description',
        'display_image_urls',
     
    ]
    list_display_links = None  # Disable click on title

    def display_title(self, obj):
        return obj.title
    display_title.short_description = 'Title'

    def display_type(self, obj):
        return obj.type
    display_type.short_description = 'Type'

    def display_short_description(self, obj):
        return obj.short_description[:50] + '...' if obj.short_description else '—'
    display_short_description.short_description = 'Short Description'

    def display_image_urls(self, obj):
        if hasattr(obj, 'image_url'):
            return mark_safe(f'<img src="{obj.image_url}" style="max-height: 80px;" />')
        return "No Image"
    display_image_urls.short_description = 'Image'


class CommonAdminMixinOfHome(admin.ModelAdmin):
    list_display = ['display_title', 'display_description']
    list_display_links = None  # Disable clickable links

    def display_title(self, obj):
        return obj.title
    display_title.short_description = 'Title'

    def display_description(self, obj):
        return obj.description
    display_description.short_description = 'Description'


class CommonAdminMixinOfParallax(admin.ModelAdmin):
    list_display = ['display_title', 'display_sub_title', 'display_description', 'display_priority']
    list_display_links = None

    def display_title(self, obj):
        return obj.title
    display_title.short_description = 'Title'

    def display_sub_title(self, obj):
        return obj.sub_title
    display_sub_title.short_description = 'Sub Title'

    def display_description(self, obj):
        return obj.description
    display_description.short_description = 'Description'

    def display_priority(self, obj):
        return obj.priority
    display_priority.short_description = 'Priority'


class CommonAdminMixinOfProducts(admin.ModelAdmin):
    list_display = ['get_category_name', 'get_detail_type','get_detail_quantity','get_detail_finish','get_detail_sqft','get_detail_warranty', 'display_title','display_subcategory','display_subtitle','display_keyfeature','get_image_preview', 'display_short_description', 'display_long_description', 'display_colour_palate1','display_colour_palate2',]
    list_display_links = None

    def get_category_name(self, obj):
        return obj.category.name
    get_category_name.short_description = mark_safe('<span style="white-space: nowrap;">Category Name</span>')

    def display_short_description(self, obj):
        return obj.short_description
    display_short_description.short_description = mark_safe('<span style="white-space: nowrap;">Short Description</span>')

    def display_long_description(self, obj):
        return obj.long_description
    display_long_description.short_description = mark_safe('<span style="white-space: nowrap;">Long Description</span>')

    def display_colour_palate1(self, obj):
        return obj.colour_palate1
    display_colour_palate1.short_description = mark_safe('<span style="white-space: nowrap;">Color Palette1</span>')

    def display_colour_palate2(self, obj):
        return obj.colour_palate2
    display_colour_palate2.short_description = mark_safe('<span style="white-space: nowrap;">Color Palette2</span>')

    def get_image_preview(self, obj):
        image_url = obj.url.get('image') if obj.url else None
        if image_url:
            return mark_safe(f'<img src="{image_url}" style="max-height: 100px;" />')
        return "No image"
    get_image_preview.short_description = mark_safe('<span style="white-space: nowrap;">Image Preview</span>')
    
    def display_title(self, obj):
        return obj.title
    display_title.short_description = "Title"

    def display_subtitle(self, obj):    
        return obj.subtitle
    display_subtitle.short_description = "Subtitle"

    def display_keyfeature(self, obj):
        return obj.keyfeature
    display_keyfeature.short_description = mark_safe('<span style="white-space: nowrap;">Key Feature</span>')

    def display_subcategory(self, obj):
        return obj.subcategory
    display_subcategory.short_description = "Subcategory"

    def get_detail_type(self, obj):
        details = obj.detail if isinstance(obj.detail, dict) else {}
        return details.get("type", "")  # Safely get 'type', or return empty string if not present
    get_detail_type.short_description = "Type"

    def get_detail_quantity(self, obj):
        return obj.detail.get("quantity", "") if obj.detail else ""
    get_detail_quantity.short_description = "Quantity"

    def get_detail_finish(self, obj):
        return obj.detail.get("finish", "") if obj.detail else ""
    get_detail_finish.short_description = "Finish"
    

    def get_detail_sqft(self, obj):
        return obj.detail.get("Sqft_lt", "") if obj.detail else ""
    get_detail_sqft.short_description = mark_safe('<span style="white-space: nowrap;">Sqft / lt</span>')

    def get_detail_warranty(self, obj):
        return obj.detail.get("warranty", "") if obj.detail else ""
    get_detail_warranty.short_description = mark_safe('<span style="white-space: nowrap;">Warranty</span>')
