from rest_framework import serializers
from .models import Initiate, Perform, Termination, Report, Chekpolis

class InitiateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initiate
        exclude = ('created_at', 'updated_at')


class PerformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perform
        exclude = ('created_at', 'updated_at')


class TerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination
        exclude = ('created_at', 'updated_at')

class ChekpolisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chekpolis
        exclude = ('created_at', 'updated_at')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('result', 'result_message', 'polis_status', 'polis_begin', 'polis_end', 'polis_owner')