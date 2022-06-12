from pprint import pprint

# Create your views here.
from django.utils.module_loading import import_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets

from collect.serializers import IntegrationActionSerializer, FormSerializer, ResponseSerializer
from collect.models import Form, IntegrationAction, Response as ResponseModel
from core.types import IntegrationTypes, IntegrationToClassMapper
from core.engine import Engine


class ListIntegrations(APIView):
    """
    View to list all integrations in the system.

    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """
        Return a list of all integrations.
        """
        integrations = vars(IntegrationTypes)["_member_map_"]
        return Response({"integrations": integrations})


class IntegrationActionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = IntegrationAction.objects.all()
    serializer_class = IntegrationActionSerializer
    permission_classes = [permissions.AllowAny]


class FormViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.AllowAny]


class ResponseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.AllowAny]


class SubmitForm(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        # check if response is complete, ie.. each required question is answered.
        response_id = request.data["response"]
        response = ResponseModel.objects.get(id=response_id)
        form = response.form
        responses = []
        if response.is_filled:
            # get form from response and get all linked integrations.
            integrations = form.integrationaction_set.all()
            for integration in integrations:
                # pass all integrations to the engine to execute(order doesn't matter)
                integration_class_string = IntegrationToClassMapper[integration.type]
                integration_class = import_string(integration_class_string)
                integration_engine_instance = Engine(integration=integration_class,
                                                     integration_instance=integration,
                                                     response=response
                                                     )
                execution = integration_engine_instance.init()
                if execution.success is not True:
                    return Response(status=400, data=execution.__dict__)
                else:
                    responses.append(execution.__dict__)

            return Response({"data": responses})
        else:
            return Response({"data": "Not Filled"})
