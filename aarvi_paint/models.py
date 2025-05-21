import uuid
from django.db import models
from .choices import *
import json
from django.utils.safestring import mark_safe

from ckeditor.fields import RichTextField


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
    subcategory_names = models.JSONField(default=list)

    def __str__(self):
        return "Details"


class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    short_description = models.TextField()
    long_description = RichTextField()
    keyfeature = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, to_field='id', related_name='category'
    )
    subcategory = models.JSONField(default=list, blank=True)
    url = models.JSONField()
    colour_palate1 = models.CharField(max_length=100, blank=True)
    colour_palate2 = models.CharField(max_length=100, blank=True)
    detail = models.JSONField(default=dict, null=True, blank=True)
    


    def __str__(self):
        return self.title


class UserInfo(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    pincode = models.CharField(max_length=100)
    type = models.CharField(max_length=200,null = True)
    description = models.TextField()
    whatsapp = models.CharField(max_length=3, choices=WHATSAPP_CHOICES, default='No')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)


class ColourPalette(TimeStampedModel):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    details = models.JSONField(default=dict, null=True, blank=True)
    url = models.JSONField(default=dict, null=True, blank=True)
    side_Title = models.CharField(max_length=200, null=True, blank=True)
    side_description = models.TextField()
    type = models.CharField(max_length=200, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # If the instance is one of the proxy types, set the appropriate `type`
        if isinstance(self, MultiColorPalette):
            self.type = 'multi-color-palette'
        elif isinstance(self, ColourPaletteWithImages):
            self.type = 'color-palette-with-images'

        super().save(*args, **kwargs)

    

class ColourCode(models.Model):
    palette = models.ForeignKey(ColourPalette, related_name='colour_codes', on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    colorshade = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code} - {self.category}"

    def save(self, *args, **kwargs):
        # Save the ColourCode first
        super().save(*args, **kwargs)

        # Now update the details field of the related ColourPalette
        self.update_palette_details()

    def update_palette_details(self):
        # Get all ColourCodes related to this palette
        colour_codes_data = [
            {
                "code": code.code,
                "category": code.category,
                "colorshade": code.colorshade
            }
            for code in self.palette.colour_codes.all()
        ]

        # Update the `details` field with the new data
        self.palette.details = {"colour_codes": colour_codes_data}
        self.palette.save()




class MultiColorPalette(ColourPalette):
    class Meta:
        proxy = True
        verbose_name = "Multi-Color Palette"
        verbose_name_plural = "Multi-Color Palettes"

    def update_details_from_colour_codes(self):
        # Gather data from related ColourCode objects
        codes_data = [
            {
                "code": code.code,
                "category": code.category,
                "colorshade": code.colorshade
            }
            for code in self.colour_codes.all()
        ]
        # Update the details field in the main table
        self.details = {"colour_codes": codes_data}
        self.save()

    def get_colour_codes(self):
        return self.colour_codes.all()

    def save(self, *args, **kwargs):
        self.type = 'multi-color-palette'
        super().save(*args, **kwargs)
    def __str__(self):
        return "Color Palettes"

class ColourPaletteImage(models.Model):
    palette = models.ForeignKey(ColourPalette, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='colour_palette_images/',help_text='Upload an image (must be less than 10 MB).')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # After saving the image, update the related Home's category_images field
        if self.palette:
            images = list(self.palette.images.values_list('image', flat=True))
            self.palette.url = {f"img{i+1}": image_url for i, image_url in enumerate(images)}
            self.palette.save()

    

class ColourPaletteWithImages(ColourPalette):
    class Meta:
        proxy = True
        verbose_name = 'Colour Palette With Images'
        verbose_name_plural = 'Colour Palettes With Images'

    def save(self, *args, **kwargs):
        self.type = 'color-palette-with-images'
        super().save(*args, **kwargs)

    



class Parallax(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.JSONField(default=dict, blank=True)
    priority = models.IntegerField()

    def __str__(self):
        return "parallax"

class Brochure(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.JSONField(default=dict, blank=True)
    uploaded_pdf = models.CharField(max_length=200)

    def __str__(self):
        return "Brochure"


class AdditionalInfo(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=200 , choices=ADDITIONAL_INFO_TYPE_CHOICES)
    title = models.CharField(max_length=200,null=True)
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
    
    def __str__(self):
        return "Inspiration"

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
    
    def __str__(self):
        return "Testimonial"
        


class PaintProduct(models.Model):
    additional_info = models.ForeignKey(
        'AdditionalInfo', on_delete=models.CASCADE, related_name='paint_products'
    )
    product_name = models.CharField(max_length=255)
    area = models.FloatField()

    def __str__(self):
        return f"{self.product_name} - {self.area} sq.m"


class PaintCalculator(AdditionalInfo):
    class Meta:
        proxy = True
        verbose_name = "Paint Calculator"
        verbose_name_plural = "Paint Calculators"

    def save(self, *args, **kwargs):
        self.type = "PAINT_CALCULATOR"
        super().save(*args, **kwargs)

    def __str__(self):
        # parts = [self.title]
        # subtitle = self.details.get("subtitle")
        # if subtitle:
        #     parts.append(subtitle)
        # products = self.details.get("products", [])
        # if products:
        #     summary = ", ".join([f"{p['product_name']} ({p['area']} sqm)" for p in products])
        #     parts.append(f"Products: {summary}")
        # return " | ".join(filter(None, parts))
        return "Calculator"


class WaterProduct(models.Model):
    additional_info = models.ForeignKey(
        'AdditionalInfo', on_delete=models.CASCADE, related_name='water_products'
    )
    product_name = models.CharField(max_length=255)
    area = models.FloatField()

    def __str__(self):
        return f"{self.product_name} - {self.area} sq.ft"


class WaterCalculator(AdditionalInfo):
    class Meta:
        proxy = True
        verbose_name = "Water Calculator"
        verbose_name_plural = "Water Calculators"

    def save(self, *args, **kwargs):
        self.type = "WATER_CALCULATOR"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Calculator"





class AdminContactDetails(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    google_link = models.URLField()
    social_media_links = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = 'Admin Contact detail'
        verbose_name_plural = 'Admin Contact details'

    # def __str__(self):
    #     return "Contact Details"
    def __str__(self):
        return f"Details"
    
    
    


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
    short_description = models.TextField()
    url = models.JSONField(default=dict, blank=True)

    # def __str__(self):
    #     return self.title


class BannerImage(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='banners/images/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # After saving the image, update the related Home's category_images field
        if self.banner:
            images = list(self.banner.images.values_list('image', flat=True))
            self.banner.url = {f"img{i+1}": image_url for i, image_url in enumerate(images)}
            self.banner.save()

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" />')
        return "No image"
    image_preview.short_description = 'Preview'

    def __str__(self):
        return ""
        # return f"{self.banner.title}"


class AboutUs(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200,blank=True,null=True)
    
    description = models.TextField(blank=True,null=True)
   
    details = models.JSONField(default=dict, blank=True,null=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    # def __str__(self):
    #     return f"{self.title or 'Untitled'}"
    def __str__(self):
        return "Details"


class Home(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null = True )
    description = models.TextField()
    type = models.CharField(max_length=200 , choices=Home_Type_CHOICES)
    # type = models.CharField(max_length=200, null=True, blank=True)
    # banners = models.ForeignKey(Banner,on_delete=models.CASCADE,related_name="homes", null=True, blank=True)
    category_name = models.CharField(max_length=100, null=True, blank=True)
    subcategory_name = models.CharField(max_length=100, null=True, blank=True)
    category_images = models.JSONField(default=dict,null=True, blank=True)
    type_images = models.JSONField(default=dict,null=True, blank=True)
    type_description = models.TextField(null=True, blank=True)
    title_type = models.CharField(max_length=200,null=True, blank=True)
    # categories = models.ManyToManyField("ColorCategory", through="HomeCategory", related_name="homes", blank=True)



class HomeInteriorCategory(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='homeinterior_categories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HomeInteriorSubCategory(models.Model):
    category = models.ForeignKey(HomeInteriorCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HomeInteriorSubCategoryImage(models.Model):
    subcategory = models.ForeignKey(HomeInteriorSubCategory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='homeinterior_subcategory_images/')

class HomeInteriorFeature(models.Model):
    homeinterior = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='home_interior/feature_images/')    




class ExteriorHomeCategory(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="exterior_categories")
    name = models.CharField(max_length=100)

class ExteriorCategoryImage(models.Model):
    category = models.ForeignKey(ExteriorHomeCategory, on_delete=models.CASCADE, related_name="exterior_images")
    image = models.ImageField(upload_to='exterior_category_images/')




class TypeImage(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="type_images_relation")
    image = models.ImageField(upload_to="type_images/")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # After saving the image, update the related Home's category_images field
        if self.home:
            images = list(self.home.images.values_list('image', flat=True))
            self.home.type_images = {f"img{i+1}": image_url for i, image_url in enumerate(images)}
            self.home.save()

class CategoryImage(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='category_images_relation')
    image = models.ImageField(upload_to='category_images/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # After saving the image, update the related Home's category_images field
        if self.home:
            images = list(self.home.images.values_list('image', flat=True))
            self.home.category_images = {f"img{i+1}": image_url for i, image_url in enumerate(images)}
            self.home.save()

    


class HomeInterior(Home):
    class Meta:
        proxy = True
        verbose_name = 'Home Interior'
        verbose_name_plural = 'home interiors'

    def save(self, *args, **kwargs):
        # self.type = 'home-interior'
        self.type = 'Interior'
        super().save(*args, **kwargs)
    def __str__(self):
        return "Interior"



class HomeExterior(Home):
    class Meta:
        proxy = True
        verbose_name = "Home Exterior"
        verbose_name_plural = "Home Exterior"
    
    def save(self, *args, **kwargs):
        self.type = 'Exterior'
        super().save(*args, **kwargs)
    def __str__(self):
        return "Exterior"

    

class HomeWaterProof(Home):
    class Meta:
        proxy = True
        verbose_name = "Home Waterproof"
        verbose_name_plural = "Home Waterproof"

    def save(self, *args, **kwargs):
        self.type = 'WaterProf'
        super().save(*args, **kwargs)
    def __str__(self):
        return "WaterProof"



class Setting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.JSONField(default=dict, blank=True)
    name = models.CharField(max_length=255)
    copyright = models.CharField(max_length=255)
    app_download_links = models.JSONField(default=dict)
    hide = models.BooleanField(null=False, default=False)

    def __str__(self):
        return "setting details"
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

# class AboutUs(TimeStampedModel):

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=200)
#     sub_title = models.CharField(max_length=200)
#     description = models.TextField()
#     url = models.JSONField(default=dict, blank=True)
#     details = models.JSONField(default=dict, blank=True)


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

    @property
    def main_image(self):
        """Get the first uploaded image"""
        return self.images.first()
    def __str__(self):
        return "Gallery"


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
    
    def __str__(self):
        return "Home Banner"


class HomeInteriorBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Home Interior Banner'
        verbose_name_plural = 'Home Interior Banners'

    def save(self, *args, **kwargs):
        self.type = 'home-interior-banner'
        super().save(*args, **kwargs)

    def __str__(self):
        return "Interior Banner"


class PaintCalculatorBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Paint Calculator Banner'
        verbose_name_plural = 'Paint Calculator Banners'

    def save(self, *args, **kwargs):
        self.type = 'paint-calculator-banner'
        super().save(*args, **kwargs)

    def __str__(self):
        return "Paint Calculate Banner"


class HomeExteriorBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Home Exterior Banner'
        verbose_name_plural = 'Home Exterior Banners'

    def save(self, *args, **kwargs):
        self.type = 'home-exterior-banner'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Exterior Banner"


# more proxy models


class HomeWaterproofingBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Home Waterproofing Banner'
        verbose_name_plural = 'Home Waterproofing Banners'

    def save(self, *args, **kwargs):
        self.type = 'home-waterproofing-banner'
        super().save(*args, **kwargs)
    def __str__(self):
        return "WaterProof Banner"


class AboutUsTopBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'About Us Top Banner'
        verbose_name_plural = 'About Us Top Banners'

    def save(self, *args, **kwargs):
        self.type = 'about-us-top-banner'
        super().save(*args, **kwargs)

    def __str__(self):
        return "About Us Top Banner"


class AboutUsBottomVideoBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'About Us Bottom Video Banner'
        verbose_name_plural = 'About Us Bottom Video Banners'

    def save(self, *args, **kwargs):
        self.type = 'about-us-bottom-video-banner'
        super().save(*args, **kwargs)

    def __str__(self):
        return "About Us Video"
   


class ColorPalletsBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Color Pallets Banner'
        verbose_name_plural = 'Color Pallets Banners'

    def save(self, *args, **kwargs):
        self.type = 'color-pallets-banner'
        super().save(*args, **kwargs)
    def __str__(self):
        return "Color Pallet Banner"


class ProductBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Product Banner'
        verbose_name_plural = 'Product Banners'

    def save(self, *args, **kwargs):
        self.type = 'product-banner'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Product Banner"


class ContactUsBanner(Banner):
    class Meta:
        proxy = True
        verbose_name = 'Contact Us Banner'
        verbose_name_plural = 'Contact Us Banners'

    def save(self, *args, **kwargs):
        self.type = 'contact-us-banner'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "Contact Us Banner"

