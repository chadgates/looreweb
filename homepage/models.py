from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel

from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wagtail.wagtailsearch import index

from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtail.wagtailforms.models import AbstractFormField
from wagtail.wagtailcore.fields import RichTextField
from modelcluster.fields import ParentalKey


ALIGN_CHOICES = (
    ('left', "Left"),
    ('right', "Right"),
    ('center', "Centre"),
)

SIZE_CHOICES = (
    ('auto', "Auto"),
    ('cover', "Cover"),
    ('50%', "Small"),
    ('200%', "Large"),
)


PERCENT_CHOICES = (
    ('10%', "10%"),
    ('20%', "20%"),
    ('30%', "30%"),
    ('40%', "40%"),
    ('50%', "50%"),
    ('60%', "60%"),
    ('70%', "70%"),
    ('80%', "80%"),
    ('90%', "90%"),
    ('100%', "100%"),
)

COLOUR_CHOICES = (
    ('white', "White"),
    ('lk-row-bg-footer', "Footer"),
    ('lk-row-bg-header', "Navigaton"),
)


class OneColumnBlock(blocks.StructBlock):
    # source: https://jossingram.wordpress.com/category/wagtail-2/
    back_image = ImageChooserBlock()
    background_size = blocks.ChoiceBlock(choices=SIZE_CHOICES, default="auto")
    background_x_position = blocks.ChoiceBlock(choices=PERCENT_CHOICES, default="50%")
    background_y_position = blocks.ChoiceBlock(choices=PERCENT_CHOICES, default="50%")
    text_align = blocks.ChoiceBlock(choices=ALIGN_CHOICES, default="center")
    one_column = blocks.StreamBlock([
           ('heading', blocks.CharBlock(classname="full title")),
           ('paragraph', blocks.RichTextBlock()),
        ], icon='arrow-left', label='Parallax content')

    class Meta:
        template = 'homepage/one_column_block.html'
        icon = 'placeholder'
        label = 'Parallax Column'


class GoogleMapBlock(blocks.StructBlock):
    map_width = blocks.CharBlock(required=True, max_length=4, default="600")
    map_height = blocks.CharBlock(required=True, max_length=4, default="450")

    class Meta:
        template = 'homepage/google_map.html'
        icon = 'cogs'
        label = 'Google Map'


class TwoColumnBlock(blocks.StructBlock):

    background = blocks.ChoiceBlock(choices=COLOUR_CHOICES,default="white")
    left_column = blocks.StreamBlock([
            ('heading', blocks.CharBlock(classname="full title")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('embedded_video', EmbedBlock()),
            ('google_map', GoogleMapBlock()),
        ], icon='arrow-left', label='Left column content')

    right_column = blocks.StreamBlock([
            ('heading', blocks.CharBlock(classname="full title")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('embedded_video', EmbedBlock()),
            ('google_map', GoogleMapBlock()),
        ], icon='arrow-right', label='Right column content')

    class Meta:
        template = 'homepage/two_column_block.html'
        icon = 'placeholder'
        label = 'Two Columns'


class ImpressumPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]


class HomePage(Page):
    body = StreamField(
        [('RTF', blocks.RichTextBlock(classname='container')),
        ('OneColumn', OneColumnBlock()),
        ('TwoColumn', TwoColumnBlock()),
        ], default="")

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class MemberBlock(blocks.StructBlock):
    photo = ImageChooserBlock()
    comment = blocks.RichTextBlock()

    class Meta:
        icon = 'user'
        template = 'homepage/member.html'

class MemberPage(Page):
    body = StreamField(
        [('member', MemberBlock()),
         ], default="")

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(WagtailCaptchaEmailForm):
    intro = RichTextField(blank=True, help_text='Edit the content you want to see before the form.')
    thank_you_text = RichTextField(blank=True, help_text='Set the message users will see after submitting the form.')

    class Meta:
        verbose_name = "Form submission page"


    content_panels = WagtailCaptchaEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email")
    ]


