from django.db import models

# Create your models here.
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index


class RecipePictureBlock(blocks.StructBlock):
    rezept_bild = ImageChooserBlock()


class IngredientsBlock(blocks.StructBlock):
    amount = blocks.CharBlock(classname="full", label="Menge")
    ingredient = blocks.CharBlock(classname="full", label="Zutat")


class IngredientsWorkBlock(blocks.StructBlock):
    amount = blocks.CharBlock(classname="full", label="Menge")
    ingredient = blocks.CharBlock(classname="full", label="Zutat")
    instruktion = blocks.RichTextBlock(classname="full", label="Arbeitsschritt")


# TODO:
class CookingEventPage(Page):
    date = models.DateField()
    chefdejour = models.TextField()
    theme = models.CharField(max_length=100)
    remarks = RichTextField(blank=True)

    content_panels = Page.content_panels = [
        FieldPanel('title'),
        FieldPanel('date'),
        FieldPanel('chefdejour'),
        FieldPanel('theme'),
        FieldPanel('remarks'),
    ]

    subpage_types = ['cooking.RecipePage']

    def recipes(self):
        # Get list of live recipe pages that are descendants of this page
        recipes = RecipePage.objects.live().descendant_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        # recipes = recipes.filter(date_from__gte=date.today())

        # Order by date
        recipes = recipes.order_by('gang')

        return recipes

    def apero(self):
        # Get list of live recipe pages that are descendants of this page
        apero = RecipePage.objects.live().descendant_of(self)
        # Filter events list to get ones that are either
        # running now or start in the future
        apero = apero.filter(gang='AP')
        # Order by date
        # recipes = recipes.order_by('gang')
        return apero

    def vorspeise(self):
        vorspeise = RecipePage.objects.live().descendant_of(self)
        vorspeise = vorspeise.filter(gang='VO')
        return vorspeise

    def hauptgang(self):
        hauptgang = RecipePage.objects.live().descendant_of(self)
        hauptgang = hauptgang.filter(gang='HG')
        return hauptgang

    def dessert(self):
        dessert = RecipePage.objects.live().descendant_of(self)
        dessert = dessert.filter(gang='DE')
        return dessert


GANG_CHOICES = (
    ('AP', "Apéro"),
    ('VO', "Vorspeise"),
    ('HG', "Hauptgang"),
    ('DE', "Dessert"),
)


class RecipeFreeFormBlock(blocks.StructBlock):
    untertitel = blocks.StreamBlock([
        ('Untertitel', blocks.RichTextBlock(required=False))
        ])
    instruktionen = blocks.StreamBlock([
        ('Instruktion', blocks.RichTextBlock(required=False))
        ])

    class Meta:
        label = 'Freiform Block'
        template = 'cooking/recipe_freeform_block.html'


class RecipeTopBottomBlock(blocks.StructBlock):
    untertitel = blocks.StreamBlock([
        ('Untertitel', blocks.RichTextBlock(required=False))
        ])
    zutaten = blocks.StreamBlock([
        ('Zutat', IngredientsBlock(required=False)),
        ])
    arbeitsschritte = blocks.StreamBlock([
        ('Arbeitsschritt', blocks.RichTextBlock(required=False))
        ])

    class Meta:
        label = 'Zutaten Block - Arbeitsschritt Block'
        template = 'cooking/recipe_top_bottom_block.html'


class RecipeLeftRightBlock(blocks.StructBlock):
    untertitel = blocks.StreamBlock([
        ('Untertitel', blocks.RichTextBlock(required=False))
        ])
    zutatenarbeitsschritte = blocks.StreamBlock([
        ('ZutatArbeitsschritt', IngredientsWorkBlock(required=False)),
        ])

    class Meta:
        label = 'Arbeitsschritt Block'
        template = 'cooking/recipe_left_right_block.html'


class RecipePage(Page):
    rezeptbild = StreamField([
        ('Bild', RecipePictureBlock()),
        ])
    mengepersonen = models.CharField(max_length=100)
    kommentar = RichTextField(blank=True)
    gang = models.CharField(max_length=2, choices=GANG_CHOICES, default="HG")
    body = StreamField([
        ('RecipeTopBottomBlock', RecipeTopBottomBlock()),
        ('RecipeLeftRightBlock', RecipeLeftRightBlock()),
        ('RecipeFreeFormBlock', RecipeFreeFormBlock()),
    ])

    content_panels = Page.content_panels = [
        FieldPanel('title'),
        StreamFieldPanel('rezeptbild'),
        FieldPanel('mengepersonen'),
        FieldPanel('kommentar'),
        FieldPanel('gang'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['cooking.CookingEventPage']

    search_fields = Page.search_fields + (
        index.SearchField('kommentar'),
        index.SearchField('body'),
        # Index the human-readable string for searching.
        index.SearchField('get_gang_display'),
        # Index the value for filtering.
        index.FilterField('gang'),
    )

# DEVELOPMENT:
# TODO: Need to create an index page for cooking events - and a recipe landing page...
