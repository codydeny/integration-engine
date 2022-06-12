from rest_framework import serializers

from collect.models import *


class IntegrationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationAction
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        depth = 1
        fields = ['id', 'name', 'description', 'is_active', 'is_published',
                  'is_signin_required', 'question_set', 'integrationaction_set']


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        depth = 1
        fields = ['id', 'is_filled', 'is_submitted', 'answer_set', 'steps_data']

