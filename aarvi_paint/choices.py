

# OBJECT_TYPE_CHOICES = [
#     ('banners', 'Banners'),
#     ('userinfo', 'User Info'),
#     ('colourpalate', 'Color Palate'),
#     ('parallax', 'Parallax'),
#     ('brochure', 'Brochure'),
# ]

Home_Type_CHOICES = [
    ('Interior','Interior'),
    ('Exterior' , 'Exterior'),
    ('WaterProf' , 'WaterProf')
]

SOURCE_CHOICES = [
        ('quote', 'Quote'),
        ('paint_budget', 'Paint Budget Calculator'),
        ('BookAppointment' , 'BookAppointment'),
        ('WaterProof' , 'WaterProof'),
    ]



ADDITIONAL_INFO_TYPE_CHOICES = [
    ("Inspiration", "Inspiration"),
    ("Testimonial", "Testimonial"),
    ("Calculator" , "Calculator"),
    ("Waterproof"  , "Waterproof"),
]


AREA_TYPE_CHOICES = [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
    ]

SURFACE_CONDITION_CHOICES_PAINT_BUDGET = [
        ('new', 'New'),
        ('repaint', 'Repaint'),
    ]

SURFACE_CONDITION_CHOICES_WATERPROOF = [
        ('Terrace/Horizontal Surface', 'Terrace/Horizontal Surface'),
        ('Exterior Walls/Vertical Surface', 'Repaint'),
    ]


ALLOWED_SOURCES = ['quote', 'BookAppointment']