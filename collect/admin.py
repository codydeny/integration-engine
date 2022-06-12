from django.contrib import admin

# Register your models here.

from collect.models import *


class QuestionsInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline]


class AnswersInline(admin.StackedInline):
    model = Answer
    extra = 1


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    inlines = [AnswersInline]


admin.site.register(IntegrationAction)
