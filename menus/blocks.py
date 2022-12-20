from wagtail import blocks


class SubmenuBlock(blocks.StructBlock):

    submenu_item = blocks.StructBlock(
            [
                ("title", blocks.CharBlock(
                    required=True,
                    blank=True,
                    null=True,
                    max_length=50
                    )
                ),
                ("icon", blocks.CharBlock(
                    required=True,
                    max_length=150,
                    blank=True,
                    null=True,
                    )
                ),
                ("description", blocks.CharBlock(
                    required=True,
                    max_length=150,
                    blank=True,
                    null=True,
                    )
                ),
                ("url", blocks.CharBlock(
                    required=True,
                    max_length=500,
                    blank=True,
                    null=True,
                    )
                ),
                ("open_in_new_tab", blocks.BooleanBlock(required=False))
            ]
          )

    class Meta:
        template = "submenu-item.html"
        icon = "user"
        label = "Submenu Item"