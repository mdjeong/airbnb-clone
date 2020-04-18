from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ ConversationAdmin Model Definition """

    list_display = (
        "__str__",
        "created",
        "count_messages",
        "count_participants",
    )


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ MessageAdmin Model Definition """

    list_display = (
        "__str__",
        "created",
    )
