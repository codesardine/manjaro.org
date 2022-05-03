from wagtail.core import blocks
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images.blocks import ImageChooserBlock


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""

    def get_api_representation(self, value, context=None):
        return richtext(value.source)

    class Meta:  
        template = "richtext_block.html"
        icon = "doc-full"
        label = "RichText"


class ProductBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text="Vendor")
    description = blocks.CharBlock(required=True, help_text="Very Short Vendor Description")
    vendor_logo = ImageChooserBlock(required=True)
    product_details = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("certified", blocks.BooleanBlock(required=False, help_text="if the hardware is Manjaro certified")),
                ("image", ImageChooserBlock(required=True)),
                ("model", blocks.CharBlock(required=True, max_length=100)),
                ("processor", blocks.CharBlock(required=True, max_length=100)),
                ("screen", blocks.CharBlock(required=True, max_length=100)),
                ("memory", blocks.CharBlock(required=True, max_length=100)),
                ("storage", blocks.CharBlock(required=True, max_length=100)),
                ("ports", blocks.CharBlock(required=True, max_length=150)),
                ("graphics", blocks.CharBlock(required=False, max_length=100)),
                ("description", blocks.TextBlock(required=False, max_length=450)),
                ("button_url", blocks.URLBlock(required=True)),
            ]
        )
    )

    class Meta:
        template = "pricing-component.html"
        icon = "form"
        label = "Product Details"


class PartnerBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text="Vendor")
    description = blocks.TextBlock(required=True, help_text="Short Vendor Description")
    vendor_logo = ImageChooserBlock(required=False)

    class Meta:
        template = "partner-component.html"
        icon = "user"
        label = "Partner"


class AffiliateBlock(blocks.StructBlock):

    promotion = blocks.StructBlock(
            [
                ("text", blocks.CharBlock(required=True)),
                ("url", blocks.URLBlock(required=True)),
                ("background", ImageChooserBlock(required=True, help_text="Vendor Background Image")),
            ]
          )

    class Meta:
        template = "affiliate-component.html"
        icon = "user"
        label = "Affiliate"



