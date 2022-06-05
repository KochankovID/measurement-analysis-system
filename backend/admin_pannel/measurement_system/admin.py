from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.forms import Textarea

from .models import ApplicationArea, RegexSettings, TypeDescription, Verification


class VerificationInLine(admin.StackedInline):
    model = Verification
    extra = 0


class TypeDescriptionInLine(admin.TabularInline):
    model = ApplicationArea.type_descriptions.through
    extra = 0


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = [
        "type_description",
        "si_verification_date",
        "si_verification_valid_until_date",
    ]
    list_filter = [
        "si_verification_date",
        "si_verification_valid_until_date",
    ]


@admin.register(ApplicationArea)
class ApplicationAreaAdmin(admin.ModelAdmin):
    inlines = [TypeDescriptionInLine]
    search_fields = [
        "application_area_name",
    ]


@admin.register(TypeDescription)
class TypeDescriptionAppAdmin(admin.ModelAdmin):
    list_display = [
        "gos_number",
        "si_name",
        "si_approval_date",
        "si_producer",
        "si_producer_country",
    ]
    search_fields = [
        "gos_number",
    ]
    list_filter = [
        "si_approval_date",
        "application_areas",
        "si_producer_country",
    ]
    inlines = [VerificationInLine, TypeDescriptionInLine]

    def get_queryset(self, request):
        test_model_qs = super(TypeDescriptionAppAdmin, self).get_queryset(request)
        test_model_qs = test_model_qs.prefetch_related('application_areas').order_by("application_areas__id")
        return test_model_qs

    change_list_template = 'change_list_graph.html'


@admin.register(RegexSettings)
class RegexSettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ArrayField: {"widget": Textarea(attrs={"rows": 4, "cols": 60})},
    }
