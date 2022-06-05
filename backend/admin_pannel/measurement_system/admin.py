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
class VendorAdmin(admin.ModelAdmin):
    ...


@admin.register(ApplicationArea)
class ApplicationAreaAdmin(admin.ModelAdmin):
    inlines = [TypeDescriptionInLine]


@admin.register(TypeDescription)
class TypeDescriptionAppAdmin(admin.ModelAdmin):
    inlines = [VerificationInLine]


@admin.register(RegexSettings)
class RegexSettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'rows': 4, 'cols': 60})},
    }
