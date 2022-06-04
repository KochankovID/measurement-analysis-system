from django.contrib import admin

from .models import ApplicationArea, TypeDescription, Verification


class VerificationInLine(admin.StackedInline):
    model = Verification
    extra = 0


@admin.register(Verification)
class VendorAdmin(admin.ModelAdmin):
    ...


@admin.register(ApplicationArea)
class ApplicationAreaAdmin(admin.ModelAdmin):
    ...


@admin.register(TypeDescription)
class TypeDescriptionAppAdmin(admin.ModelAdmin):
    inlines = [VerificationInLine]
