from django.contrib import admin
from django.utils import timezone

from enterprises.models import ContactFormSubmission, FrequentlyAskedQuestion


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "ordering", "service_type"]
    ordering = ["ordering"]


@admin.action(description="Mark selected submissions as read")
def mark_as_read(modeladmin, request, queryset):
    queryset.update(read=True)


@admin.action(description="Mark selected submissions as unread")
def mark_as_unread(modeladmin, request, queryset):
    queryset.update(read=False)


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    ordering = ["submitted_at"]
    list_display = ["name", "read", "submitted_at", "read_at"]
    list_filter = ["read"]
    actions = [mark_as_read, mark_as_unread]

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.model.objects.get(pk=object_id)
        obj.read = True
        obj.read_at = timezone.localtime()
        obj.save()

        extra_context = extra_context or {}
        extra_context["show_delete_link"] = True
        extra_context["mailto_link"] = (
            f"mailto:{obj.reply_email}?"
            f"subject=Response%20from%20Evan%20Duke%20Enterprises&body={obj.submission}"
        )

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    def has_add_permission(self, request):
        return False

    change_form_template = "admin/contact_submission.html"
