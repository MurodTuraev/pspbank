import uuid as uuid
from django.db import models

class Report(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    transaction_id = models.IntegerField(verbose_name="Транзакция")
    insurance_cost = models.DecimalField(verbose_name="Страховая сумма", max_digits=30, decimal_places=2)
    insurance_premium = models.DecimalField(verbose_name="Страховая премия", max_digits=30, decimal_places=2)
    insurance_liability = models.DecimalField(verbose_name="Страховая ответственность", max_digits=30, decimal_places=2)
    polis_sery = models.CharField(verbose_name="Серия полиса", max_length=15, blank=True, null=True)
    polis_number = models.IntegerField(verbose_name="Номер полиса", blank=True, null=True)
    polis_status = models.CharField(verbose_name="Статус полиса", max_length=100, blank=True, null=True)
    polis_owner = models.TextField(verbose_name="Владелиц", blank=True, null=True)
    polis_begin = models.DateField(verbose_name="Дата начало", blank=True, null=True)
    polis_end = models.DateField(verbose_name="Дата окончания", blank=True, null=True)
    term_date = models.DateField(verbose_name="Дата расторжения", blank=True, null=True)
    term_amount = models.DecimalField(verbose_name="Сумма расторжения" ,max_digits=30, decimal_places=2, blank=True, null=True)
    term_note = models.TextField(verbose_name="Причина расторжения", blank=True, null=True)
    agent_id = models.PositiveIntegerField(verbose_name="Агент")
    agent_phone = models.CharField(verbose_name="Номер телефона  агента", max_length=15, blank=True, null=True)
    product_id = models.PositiveIntegerField(verbose_name="Продукт")
    client_name = models.CharField(verbose_name="ФИО клиента", max_length=512, blank=True, null=True)
    client_address = models.CharField(verbose_name="Адрес клиента", max_length=512, blank=True, null=True)
    client_phone = models.CharField(verbose_name="Номер телефона клиента", max_length=15, blank=True, null=True)
    client_passport = models.CharField(verbose_name="Паспорт клиента", max_length=15, blank=True, null=True)
    beneficiary_name = models.CharField(verbose_name="Бенифициар", max_length=512, blank=True, null=True)
    qrcode = models.URLField(verbose_name="QRCODE", null=True, blank=True, max_length=500)
    pdf = models.URLField(verbose_name="pdf вариант", null=True, blank=True, max_length=500)

    result = models.IntegerField(blank=True, null=True)
    result_message = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.uuid)