from django.db import models
from django.utils.translation import gettext_lazy as _


class IntegrationTypes(models.TextChoices):
    GOOGLE_DOCS = 'GOOGLE_DOCS', _('GOOGLE_DOCS')
    DEMO = 'DEMO', _('DEMO')
    NONE_TYPE = 'NONE_TYPE', _('NONE_TYPE')


IntegrationToClassMapper = {
    "GOOGLE_DOCS": "integrations.google_docs.google_docs_integration.GoogleDocsIntegration",
    "DEMO": "integrations.demo.demo_integration.DemoIntegration",
    "NONE_TYPE": "NONE_TYPE"
}
