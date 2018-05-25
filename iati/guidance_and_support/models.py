from django.db import models

from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from home.models import AbstractContentPage, AbstractIndexPage, IATIStreamBlock


class GuidanceAndSupportPage(AbstractContentPage):
    """A base for the Guidance and Support page."""
    parent_page_types = ['home.HomePage']
    subpage_types = ['guidance_and_support.GuidanceGroupPage', 'guidance_and_support.KnowledgebaseIndexPage']

    @property
    def guidance_groups(self):
        """Get all GuidanceGroupPage objects that have been published."""
        guidance_groups = GuidanceGroupPage.objects.child_of(self).live()
        return guidance_groups


class GuidanceGroupPage(AbstractContentPage):
    """A base for Guidance Group pages."""
    subpage_types = ['guidance_and_support.GuidanceGroupPage', 'guidance_and_support.GuidancePage']

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This is the image that will be displayed for the guidance index page on the main guidance and support page. Ignore if this page is being used as a sub-index page.'
    )

    feed_content = StreamField(IATIStreamBlock(required=False), null=True, blank=True, help_text='A small amount of content to appear on the main page (e.g. bullet points). Ignore if this page is being used as a sub-index page.')

    feed_button_text = models.TextField(max_length=255, null=True, blank=True, help_text='The text to appear on the button of the main guidance and support page. Ignore if this page is being used as a sub-index page.')

    @property
    def guidance_groups(self):
        """Get all objects that are children of the instantiated GuidanceGroupPage.

        Note:
            These can be other guidance group pages or single guidance pages.

        """
        guidance_groups = Page.objects.child_of(self).specific().live()
        guidance_group_list = [{"page": page, "count": len(page.get_children())} for page in guidance_groups]
        return guidance_group_list

    translation_fields = AbstractContentPage.translation_fields + ["feed_content", "feed_button_text"]

    multilingual_field_panels = [
        ImageChooserPanel('feed_image'),
    ]


class GuidancePage(AbstractContentPage):
    subpage_types = []


class KnowledgebaseIndexPage(AbstractIndexPage):
    subpage_types = ['guidance_and_support.KnowledgebasePage']


class KnowledgebasePage(AbstractContentPage):
    subpage_types = []
