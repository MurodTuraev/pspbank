from django.db import models

class Initiate(models.Model):
    username = models.CharField(max_length=255, )
    password = models.CharField(max_length=255, )
    agent_id = models.PositiveIntegerField()
    agent_phone = models.CharField(max_length=15, )
    transaction_id = models.IntegerField()
    period_begin = models.DateField()
    product_id = models.PositiveIntegerField()
    client_name = models.CharField(max_length=512, blank=True, null=True)
    client_address = models.CharField(max_length=512, blank=True, null=True)
    client_phone = models.CharField(max_length=15, blank=True, null=True)
    client_passport = models.CharField(max_length=15, blank=True, null=True)
    beneficiary_name = models.CharField(max_length=512, blank=True, null=True)
    object = models.TextField(blank=True, null=True)
    insurance_cost = models.DecimalField(max_digits=30, decimal_places=2)
    period_end = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.transaction_id)