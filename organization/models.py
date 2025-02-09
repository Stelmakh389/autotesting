from django.db import models

# core/models/organization.py
class Organization(models.Model):
    name = models.CharField("Название организации полное", max_length=255, blank=True, null=True)
    shortname = models.CharField("Название организации сокращенное", max_length=255, blank=True, null=True)
    inn = models.CharField("ИНН", max_length=12, blank=True, null=True)
    kpp = models.CharField("КПП", max_length=12, blank=True, null=True)
    ogrn = models.CharField("ОГРН", max_length=15, blank=True, null=True)
    legal_address = models.TextField("Юридический адрес", blank=True, null=True)
    actual_address = models.TextField("Фактический адрес", blank=True, null=True)
    checking_account = models.CharField("Расчетный счет", max_length=20, blank=True, null=True)
    correspondent_account = models.CharField("Корреспондентский счет", max_length=20, blank=True, null=True)
    namebank = models.TextField("Название банка", blank=True, null=True)
    bik = models.CharField("БИК", max_length=9, blank=True, null=True)
    email = models.CharField("E-mail", max_length=20, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    website = models.CharField("Сайт", max_length=20, blank=True, null=True)
    accreditation_number = models.CharField("Номер записи об аккредитации", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"