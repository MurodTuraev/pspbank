from django.db import models

class Perform(models.Model):
    username = models.CharField(max_length=255, )
    password = models.CharField(max_length=255, )
    agent_id = models.PositiveIntegerField()
    agent_phone = models.CharField(max_length=15, )
    transaction_id = models.IntegerField()
    period_begin = models.DateField()
    payment_date = models.DateField()
    payment_type = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.transaction_id)

