from django.db import models

# Create your models here.
from wagtail.wagtaildocs.models import Document
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from django.utils.translation import ugettext_lazy as _


class RecipePictureBlock(blocks.StructBlock):
    rezept_bild = ImageChooserBlock()


class IngredientsBlock(blocks.StructBlock):
    amount = blocks.CharBlock(classname="full", label="Menge")
    ingredient = blocks.CharBlock(classname="full", label="Zutat")


class IngredientsWorkBlock(blocks.StructBlock):
    amount = blocks.CharBlock(classname="full", label="Menge")
    ingredient = blocks.CharBlock(classname="full", label="Zutat")
    instruktion = blocks.RichTextBlock(classname="full", label="Arbeitsschritt")


class CookingEventPage(Page):
    date = models.DateField()
    chefdejour = models.TextField()
    remarks = RichTextField(blank=True)
    recipefile = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels = [
        FieldPanel('title'),
        FieldPanel('date'),
        FieldPanel('chefdejour'),
        FieldPanel('remarks'),
        DocumentChooserPanel('recipefile'),
    ]

    subpage_types = ['cooking.RecipePage']
    parent_page_types = ['cooking.CookingEventIndexPage']

    def cooking_event_index(self):
        # Find closest ancestor which is an event index
        return self.get_ancestors().type(CookingEventIndexPage).last()

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

    def cooking_event(self):
        # Find closest ancestor which is an event index
        return self.get_ancestors().type(CookingEventPage).last()

    search_fields = Page.search_fields + (
        index.SearchField('kommentar'),
        index.SearchField('body'),
        # Index the human-readable string for searching.
        index.SearchField('get_gang_display'),
        # Index the value for filtering.
        index.FilterField('gang'),
    )


# TODO: Pagination of index page

class CookingEventIndexPage(Page):

    def cookingevents(self):
        cookingevents = CookingEventPage.objects.live().descendant_of(self)
        cookingevents = cookingevents.order_by('-date')
        return cookingevents

    class Meta:
        verbose_name = _('Cooking Events index')

    content_panels = Page.content_panels = [
        FieldPanel('title'),
    ]

    subpage_types = ['cooking.CookingEventPage']


# DEVELOPMENT:
# TODO: Need to create a recipe landing page...
