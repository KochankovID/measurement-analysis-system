# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = "alembic_version"


class AssociationTable(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    application_area = models.ForeignKey("ApplicationArea", on_delete=models.CASCADE, db_column="application_area")
    type_description = models.ForeignKey("TypeDescription", on_delete=models.CASCADE, db_column="type_description")

    class Meta:
        managed = False
        db_table = 'measurement-data"."association'


class ApplicationArea(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    type_descriptions = models.ManyToManyField(
        "TypeDescription",
        through=AssociationTable,
        verbose_name=_("Type description"),
    )
    application_area_name = models.TextField(
        _("Application area"), blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'measurement-data"."application_area'
        verbose_name = _("Application area")
        verbose_name_plural = _("Application areas")

    def __str__(self):
        return self.application_area_name


class TypeDescription(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    gos_number = models.CharField(
        _("Government number"), max_length=32, blank=True, null=True
    )
    si_name = models.CharField(_("Name"), max_length=32, blank=True, null=True)
    si_unit_of_measurement = models.CharField(
        _("Measurement unit"), max_length=32, blank=True, null=True
    )
    si_measurement_error = models.FloatField(
        _("Measurement error"), blank=True, null=True
    )
    si_measurement_error_type = models.TextField(
        _("Measurement error type"), blank=True, null=True
    )
    si_approval_date = models.DateField(_("Approval date"), blank=True, null=True)
    si_producer = models.CharField(_("Producer"), max_length=32, blank=True, null=True)
    file_name = models.CharField(_("File name"), max_length=32, blank=True, null=True)
    si_purpose = models.TextField(_("SI purpose"), blank=True, null=True)
    si_producer_country = models.TextField(_("Producer country"), blank=True, null=True)
    application_areas = models.ManyToManyField(
        "ApplicationArea",
        through=AssociationTable,
        verbose_name=_("Application area"),
    )

    def __str__(self):
        return self.gos_number

    class Meta:
        managed = False
        db_table = 'measurement-data"."type_description'
        verbose_name = _("Type description")
        verbose_name_plural = _("Type descriptions")


class Verification(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    type_description = models.ForeignKey(
        "TypeDescription",
        models.CASCADE,
        verbose_name=_("Type description"),
        blank=True,
        null=True,
    )
    si_modification = models.CharField(
        _("Modification"), max_length=32, blank=True, null=True
    )
    si_type = models.CharField(_("Type"), max_length=32, blank=True, null=True)
    si_verification_date = models.DateField(
        _("Verification date"), blank=True, null=True
    )
    si_verification_valid_until_date = models.DateField(
        _("Verification valid until date"), blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'measurement-data"."verification'
        verbose_name = _("Verification")
        verbose_name_plural = _("Verifications")

    def __str__(self):
        return f"{self.type_description} - {self.si_verification_date}"


class RegexSettings(models.Model):
    def save(self, *args, **kwargs):
        self.pk = 1
        super(RegexSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    type_description = ArrayField(
        ArrayField(models.TextField()),
        verbose_name=_("Type description regexes"),
    )
    meaning = ArrayField(
        ArrayField(models.TextField()), verbose_name=_("SI meaning regexes")
    )
    measurement_unit = ArrayField(
        ArrayField(models.TextField()), verbose_name=_("Measurement units regexes")
    )
    description = ArrayField(
        ArrayField(models.TextField()), verbose_name=_("SI description regexes")
    )

    class Meta:
        db_table = 'measurement-admin"."regex_settings'
        verbose_name = _("RegexSetting")
        verbose_name_plural = _("RegexSettings")

    def __str__(self):
        return "Настройки регулярных выражений"
