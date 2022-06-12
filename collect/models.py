from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

# Create your models here.
import core.engine
from core.types import IntegrationTypes, IntegrationToClassMapper


class Form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    is_signin_required = models.BooleanField(default=False)

    def __str__(self):
        return "{name} with ID={id}".format(name=self.name, id=self.id)


class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)
    steps_data = models.JSONField(default=dict, blank=True)

    @property
    def is_filled(self):
        for question in self.form.question_set.all():
            if question.required:
                if self.answer_set.filter(question=question.id).count() <= 0:
                    return False

        return True

    def __str__(self):
        return "Response of : {name}".format(name=self.form.name)


class Question(models.Model):
    TEXT = 'TEXT'
    QUESTION_TYPES = [
        (TEXT, 'Text'),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=TEXT, )
    name = models.TextField(default="")
    description = models.TextField(default="")
    order = models.PositiveSmallIntegerField()
    required = models.BooleanField(default=False)

    def __str__(self):
        return "{name}".format(name=self.name)


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, blank=True, default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(default="")

    def __str__(self):
        return "{name}".format(name=self.answer)


class IntegrationAction(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', _('NOT_STARTED')
        STARTED = 'STARTED', _('STARTED')

    type = models.CharField(
        max_length=255,
        choices=IntegrationTypes.choices,
        default=IntegrationTypes.NONE_TYPE,
    )
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    input = models.JSONField(default=dict)
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )

    def __str__(self):
        return "{name}".format(name=self.type)


# method for updating
@receiver(post_save, sender=IntegrationAction, dispatch_uid="init_integration")
def init_integration(sender, instance, created, **kwargs):
    if created:
        integration_action_instance = instance
        integration_class_string = IntegrationToClassMapper[integration_action_instance.type]
        integration_class = import_string(integration_class_string)
        response = Response.objects.none()
        engine_instance = core.engine.Engine(integration=integration_class,
                                             integration_instance=integration_action_instance,
                                             response=response
                                             )
        execution = engine_instance.init()

        if execution.success is not True:
            instance.delete()
            raise Exception('Failed To Initialize {}'.format(execution.message))
