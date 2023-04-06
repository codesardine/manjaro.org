from django.db import models
from wagtail.admin.panels import TabbedInterface, ObjectList
from wagtail.models import Page

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField
)
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class ContactPage(WagtailCaptchaEmailForm):

    template = "contact_page.html"
    landing_page_template = "contact-landing.html"

    thank_you_text = RichTextField(blank=True)


    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Email"),
    ]


    no_html = models.BooleanField(default=False, help_text="Do not allow html")
    allowed_languages = models.BooleanField(help_text="Only allow German and English", default=False)
    min_message_characters = models.IntegerField(help_text="allowed characters", default=200)
    no_links = models.BooleanField(default=False, help_text="Do not allow links")
    only_bussiness_addresses = models.BooleanField(default=False, help_text="Only allow Bussiness Addresses in company contact")
    min_name_characters = models.IntegerField(help_text="allowed characters", default=7)


    security_panels = [
        FieldPanel('no_links'),
        FieldPanel('no_html'),
        FieldPanel('allowed_languages'),
        FieldPanel('only_bussiness_addresses'),
        FieldPanel('min_message_characters'),
        FieldPanel('min_name_characters'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=('Content')),
        ObjectList(security_panels, heading=('Security')),
        ObjectList(Page.promote_panels, heading=('Promote')),
        ObjectList(Page.settings_panels, heading=('Settings')),
    ])
