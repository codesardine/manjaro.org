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
                ("image", ImageChooserBlock(required=True)),
                ("Brand", blocks.CharBlock(required=True, max_length=40)),
                ("Model", blocks.CharBlock(required=True, max_length=80)),
                ("Description", blocks.TextBlock(required=True, max_length=250)),
                ("button_url", blocks.URLBlock(required=True)),
            ]
        )
    )


    class Meta:
        template = "pricing-component.html"
        icon = "#todo"
        label = "Product Details"


class PartnerBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text="Vendor")
    description = blocks.TextBlock(required=True, help_text="Short Vendor Description")
    details = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
            ]
        )
    )


    class Meta:
        template = "partner-component.html"
        icon = "#todo"
        label = "Partner"



