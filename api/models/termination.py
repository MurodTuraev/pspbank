from django.db import models

class Termination(models.Model):
    username = models.CharField(max_length=255, )
    password = models.CharField(max_length=255, )
    agent_id = models.PositiveIntegerField()
    polis_sery = models.CharField(max_length=15, )
    polis_number = models.IntegerField()
    term_date = models.DateField()
    term_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.agent_id)