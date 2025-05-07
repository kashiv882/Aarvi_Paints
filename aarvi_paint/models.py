import uuid
from django.db import models
from .choices import *
import json

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class PaintBudgetCalculator(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES)
    surface_condition = models.CharField(max_length=50, choices=SURFACE_CONDITION_CHOICES_PAINT_BUDGET)
    selected_product = models.CharField(max_length=100)
    entered_area = models.FloatField(help_text="Enter area in square meters")
    userinfo= models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='paint_budgets')


class Category(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    subcategory_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.subcategory_name}"


class Product(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    keyfeature = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='id', related_name='category')
    url = models.JSONField()



class UserInfo(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    pincode = models.CharField(max_length=100)
    type = models.CharField(max_length=200,null = True)
    description = models.TextField()
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)


class ColourPalette(TimeStampedModel):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200 ,null=True)
    description = models.TextField(null=True)
    colour_code = models.IntegerField(null=True)
    colour_code_category = models.CharField(max_length=200,null=True)
    url = models.JSONField(default=dict, blank=True)


class ColourCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    palette = models.ForeignKey(ColourPalette, related_name='colour_codes', on_delete=models.CASCADE)
    code = models.IntegerField()
    category = models.CharField(max_length=200)

class MultiColorPalette(ColourPalette):
    class Meta:
        proxy = True
        verbose_name = "Multi-Color Palette"
        verbose_name_plural = "Multi-Color Palettes"

    def get_colour_codes(self):
        return self.colour_codes.all()

class ColourPaletteImage(models.Model):
    palette = models.ForeignKey(ColourPalette, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='colour_palette_images/')

class ColourPaletteWithImages(ColourPalette):
    class Meta:
        proxy = True
        verbose_name = 'Colour Palette With Images'
        verbose_name_plural = 'Colour Palettes With Images'

    def save(self, *args, **kwargs):
        # Proxy behavior can be extended here if needed
        super().save(*args, **kwargs)


class ColourPaletteProxy(ColourPalette):
    class Meta:
        proxy = True
        verbose_name = "Colour Palette (Enhanced)"
        verbose_name_plural = "Colour Palettes (Enhanced)"

    @property
    def colour_mappings(self):
        try:
            codes = json.loads(self.colour_code or "[]")
            categories = json.loads(self.colour_code_category or "[]")
            return list(zip(codes, categories))
        except Exception:
            return []

    @colour_mappings.setter
    def colour_mappings(self, value):
        """
        Accepts a list of tuples: [(code1, cat1), (code2, cat2)]
        """
        codes, cats = zip(*value) if value else ([], [])
        self.colour_code = json.dumps(list(codes))
        self.colour_code_category = json.dumps(list(cats))




class Parallax(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.JSONField(default=dict, blank=True)
    priority = models.IntegerField()


class Brochure(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.JSONField(default=dict, blank=True)
    uploaded_pdf = models.CharField(max_length=200)


class AdditionalInfo(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=200 , choices=ADDITIONAL_INFO_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.JSONField(default=dict, blank=True)
    details = models.JSONField(default=dict, blank=True)

#proxy for AdditionalInfo
class Inspiration(AdditionalInfo):
    class Meta:
        proxy = True
        verbose_name = "Inspiration"
        verbose_name_plural = "Inspirations"

    @property
    def image_url(self):
        return self.url.get('image', '')

    @image_url.setter
    def image_url(self, value):
        self.url['image'] = value

    @property
    def is_interior(self):
        return self.type == 'interior'

    @property
    def is_exterior(self):
        return self.type == 'exterior'

class Testimonial(AdditionalInfo):
    class Meta:
        proxy = True
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def save(self, *args, **kwargs):
        self.type = "TESTIMONIAL"
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self.title

    @property
    def image_url(self):
        return self.url.get('image', '')
class Calculator(AdditionalInfo):
    class Meta:
        proxy = True
        verbose_name = "Paint Calculator"
        verbose_name_plural = "Paint Calculators"

    def save(self, *args, **kwargs):
        self.type = "PAINT_BUDGET_CALCULATOR"  # Automatically set type
        super().save(*args, **kwargs)

    @property
    def product(self):
        return self.details.get('product', '')

    @property
    def area(self):
        return self.details.get('area', '')

class WaterCalculator(AdditionalInfo):
    class Meta:
        proxy = True
        verbose_name = "WaterCalculator"
        verbose_name_plural = "WaterCalculators"

    def save(self, *args, **kwargs):
        self.type = "WATER_CALCULATOR"  # Ensure correct type is set
        super().save(*args, **kwargs)

    @property
    def product(self):
        return self.details.get('product', '')

    @property
    def area(self):
        return self.details.get('area', '')


class AdminContactDetails(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    google_link = models.URLField()
    social_media_links = models.JSONField(default=list, blank=True)


class WaterProofCalculator(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    surface_condition = models.CharField(max_length=50, choices=SURFACE_CONDITION_CHOICES_WATERPROOF)
    selected_product = models.CharField(max_length=100)
    entered_area = models.FloatField(help_text="Enter area in square meters")
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='waterproof_calculations')
    description = models.TextField()


class Banner(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, editable=False, null=True, blank=True)
    placement_location = models.CharField(max_length=200, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    url = models.JSONField(default=dict, blank=True)


class BannerImage(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='banners/images/')

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" />')
        return "No image"
    image_preview.short_description = 'Preview'


class AboutUs(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200,blank=True,null=True)
    sub_title = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    url = models.JSONField(default=dict, blank=True,null=True)
    details = models.JSONField(default=dict, blank=True,null=True)














class Home(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200 , choices=Home_Type_CHOICES)
    banners = models.ForeignKey(Banner,on_delete=models.CASCADE,related_name="homes", null=True, blank=True)
    category_name = models.CharField(max_length=100, null=True, blank=True)
    subcategory_name = models.CharField(max_length=100, null=True, blank=True)
    category_images = models.JSONField(default=dict,null=True, blank=True)
    type_images = models.JSONField(default=dict,null=True, blank=True)
    type_description = models.TextField(null=True, blank=True)
    title_type = models.CharField(max_length=200,null=True, blank=True)


class TypeImage(models.Model):
    home = models.ForeignKey("Home", on_delete=models.CASCADE, related_name="type_images_relation")
    image = models.ImageField(upload_to="type_images/")

class CategoryImage(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='category_images_relation')
    image = models.ImageField(upload_to='category_images/')

class HomeProxy(Home):
    class Meta:
        proxy = True
        verbose_name = "Home Custom View"
        verbose_name_plural = "Homes Custom View"

class WaterproofHome(Home):
    class Meta:
        proxy = True
        verbose_name = "Waterproof Home"
        verbose_name_plural = "Waterproof Homes"

    def __str__(self):
        return f"Waterproof: {self.title}"

    def save(self, *args, **kwargs):
        # Ensure we're working with waterproof type
        self.type = "Waterproof"  # Assuming 'Waterproof' is in your Home_Type_CHOICES
        super().save(*args, **kwargs)


# class HomeProxy(Home):
#     class Meta:
#         proxy = True  # <- Tells Django this is a proxy, not a new table
#         verbose_name = "Custom Home Entry"
#         verbose_name_plural = "Custom Home Entries"


class HomeInteriorColorCategory(Home):
    class Meta:
        proxy = True
        verbose_name = 'Home Interior Color Category'
        verbose_name_plural = 'home interior color categories'

    def save(self, *args, **kwargs):
        self.type = 'home-interior-color-category'
        super().save(*args, **kwargs)


class HomeInterior(Home):
    class Meta:
        proxy = True
        verbose_name = 'Home Interior'
        verbose_name_plural = 'home interiors'

    def save(self, *args, **kwargs):
        self.type = 'home-interior'
        super().save(*args, **kwargs)


class HomeInteriorDifferentRoom(Home):
    class Meta:
        proxy = True
        verbose_name = 'Home Interior Different Room'
        verbose_name_plural = 'home interiors Different Rooms'

    def save(self, *args, **kwargs):
        self.type = 'home-interior-different-room'
        super().save(*args, **kwargs)

class HomeExteriorData(Home):
    class Meta:
        proxy = True
        verbose_name = 'Home Exterior Data'
        verbose_name_plural = 'home exterior datas'

    def save(self, *args, **kwargs):
        self.type = 'home-exterior-data'
        super().save(*args, **kwargs)




# class CustomInfo(models.Model):
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     additional_info = models.JSONField(blank=True, null=True)
#
#
# class ObjectType(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     variable_name = models.CharField(max_length=100, unique=True)
#     fields = models.JSONField(default=dict)


# class Navbar(TimeStampedModel):
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     object_type = models.CharField(max_length=200 , choices= OBJECT_TYPE_CHOICES )
#     details= models.JSONField()
#     url =  models.JSONField(null=True)




# Proxy models

class GalleryBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Gallery Banner'
        verbose_name_plural = 'Gallery Banners'

    def save(self, *args, **kwargs):
        self.type = 'gallery-banner'
        super().save(*args, **kwargs)

# ==========================================Home Bannner============================================================================
class HomeBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Home Banner'
        verbose_name_plural = 'Home Banners'

    def save(self, *args, **kwargs):
        self.type = 'home-banner'
        super().save(*args, **kwargs)

    @property
    def main_image(self):
        """Get the first uploaded image"""
        return self.images.first()









# ====================================================================================================================================
# class HomeBanner(Banner):
#     class Meta:
#         proxy = True
#         verbose_name = 'Home Banner'
#         verbose_name_plural = 'Home Banners'

#     def save(self, *args, **kwargs):
#         self.type = 'home-banner'
#         super().save(*args, **kwargs)


class HomeInteriorBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Home Interior Banner'
        verbose_name_plural = 'Home Interior Banners'

    def save(self, *args, **kwargs):
        self.type = 'home-interior-banner'
        super().save(*args, **kwargs)


class HomeExteriorBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Home Exterior Banner'
        verbose_name_plural = 'Home Exterior Banners'

    def save(self, *args, **kwargs):
        self.type = 'home-exterior-banner'
        super().save(*args, **kwargs)


# more proxy models


class HomeWaterproofingBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Home Waterproofing Banner'
        verbose_name_plural = 'Home Waterproofing Banners'

    def save(self, *args, **kwargs):
        self.type = 'home-waterproofing-banner'
        super().save(*args, **kwargs)


class AboutUsTopBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'About Us Top Banner'
        verbose_name_plural = 'About Us Top Banners'

    def save(self, *args, **kwargs):
        self.type = 'about-us-top-banner'
        super().save(*args, **kwargs)


class AboutUsBottomVideoBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'About Us Bottom Video Banner'
        verbose_name_plural = 'About Us Bottom Video Banners'

    def save(self, *args, **kwargs):
        self.type = 'about-us-bottom-video-banner'
        super().save(*args, **kwargs)


class ColorPalletsBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Color Pallets Banner'
        verbose_name_plural = 'Color Pallets Banners'

    def save(self, *args, **kwargs):
        self.type = 'color-pallets-banner'
        super().save(*args, **kwargs)


class ProductBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Product Banner'
        verbose_name_plural = 'Product Banners'

    def save(self, *args, **kwargs):
        self.type = 'product-banner'
        super().save(*args, **kwargs)


class ContactUsBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Contact Us Banner'
        verbose_name_plural = 'Contact Us Banners'

    def save(self, *args, **kwargs):
        self.type = 'contact-us-banner'
        super().save(*args, **kwargs)

