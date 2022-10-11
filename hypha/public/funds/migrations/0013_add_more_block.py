# Generated by Django 2.2.19 on 2021-02-28 21:34

from django.db import migrations
import hypha.public.funds.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('public_funds', '0012_add_box_apply_link_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseapplicationpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('box', wagtail.blocks.StructBlock([('box_content', wagtail.blocks.RichTextBlock()), ('box_class', wagtail.blocks.CharBlock(required=False))])), ('more', wagtail.blocks.StructBlock([('more_content', wagtail.blocks.RichTextBlock()), ('more_content_more', wagtail.blocks.RichTextBlock()), ('more_class', wagtail.blocks.CharBlock(required=False))])), ('apply_link', wagtail.blocks.StructBlock([('application', wagtail.blocks.PageChooserBlock())])), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.CharBlock(required=False))])), ('quote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.CharBlock(form_classname='title')), ('attribution', wagtail.blocks.CharBlock(required=False)), ('job_title', wagtail.blocks.CharBlock(required=False))])), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('call_to_action', wagtail.snippets.blocks.SnippetChooserBlock('utils.CallToActionSnippet', template='blocks/call_to_action_block.html')), ('document', wagtail.blocks.StructBlock([('document', wagtail.documents.blocks.DocumentChooserBlock()), ('title', wagtail.blocks.CharBlock(required=False))])), ('project_list', hypha.public.funds.blocks.ProjectsBlock()), ('reviewer_list', hypha.public.funds.blocks.ReviewersBlock())]),
        ),
        migrations.AlterField(
            model_name='labpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title', icon='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('box', wagtail.blocks.StructBlock([('box_content', wagtail.blocks.RichTextBlock()), ('box_class', wagtail.blocks.CharBlock(required=False))])), ('more', wagtail.blocks.StructBlock([('more_content', wagtail.blocks.RichTextBlock()), ('more_content_more', wagtail.blocks.RichTextBlock()), ('more_class', wagtail.blocks.CharBlock(required=False))])), ('apply_link', wagtail.blocks.StructBlock([('application', wagtail.blocks.PageChooserBlock())])), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.CharBlock(required=False))])), ('quote', wagtail.blocks.StructBlock([('quote', wagtail.blocks.CharBlock(form_classname='title')), ('attribution', wagtail.blocks.CharBlock(required=False)), ('job_title', wagtail.blocks.CharBlock(required=False))])), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('call_to_action', wagtail.snippets.blocks.SnippetChooserBlock('utils.CallToActionSnippet', template='blocks/call_to_action_block.html')), ('document', wagtail.blocks.StructBlock([('document', wagtail.documents.blocks.DocumentChooserBlock()), ('title', wagtail.blocks.CharBlock(required=False))])), ('reviewer_list', hypha.public.funds.blocks.ReviewersBlock())]),
        ),
    ]
