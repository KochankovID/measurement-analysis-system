# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class ApplicationArea(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    type_description = models.ForeignKey('TypeDescription', models.DO_NOTHING, blank=True, null=True)
    application_area_name = models.CharField(_("Application area"), max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measurement-data\".\"application_area'
        verbose_name = _("Application area")
        verbose_name_plural = _("Application areas")

    def __str__(self):
        return self.application_area_name


class TypeDescription(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    gos_number = models.CharField(_("Government number"), max_length=32, blank=True, null=True)
    si_name = models.CharField(_("Name"), max_length=32, blank=True, null=True)
    si_unit_of_measurement = models.CharField(_("Measurement unit"), max_length=32, blank=True, null=True)
    si_measurement_error = models.FloatField(_("Measurement error"), blank=True, null=True)
    si_approval_date = models.DateField(_("Approval date"), blank=True, null=True)
    si_producer = models.CharField(_("Producer"), max_length=32, blank=True, null=True)
    file_name = models.CharField(_("File name"), max_length=32, blank=True, null=True)

    def __str__(self):
        return self.gos_number

    class Meta:
        managed = False
        db_table = 'measurement-data\".\"type_description'
        verbose_name = _("Type description")
        verbose_name_plural = _("Type descriptions")


class Verification(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    type_description = models.ForeignKey("TypeDescription", models.DO_NOTHING, blank=True, null=True)
    si_modification = models.CharField(_("Modification"), max_length=32, blank=True, null=True)
    si_type = models.CharField(_("Type"), max_length=32, blank=True, null=True)
    si_verification_date = models.DateField(_("Verification date"), blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measurement-data\".\"verification'
        verbose_name = _("Verification")
        verbose_name_plural = _("Verifications")

    def __str__(self):
        return f"{self.type_description} - {self.si_verification_date}"
