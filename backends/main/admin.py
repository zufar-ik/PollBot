from django.contrib import admin

from .models import Poll, Poll_answer, User_answer, Poll_class


class AnswerAdmin(admin.StackedInline):
    model = Poll


@admin.register(Poll_class)
class PostAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]

@admin.register(User_answer)
class PostAdmin1(admin.ModelAdmin):
    pass
@admin.register(Poll_answer)
class PostAdmin2(admin.ModelAdmin):
    pass

@admin.register(Poll)
class PostAdmin3(admin.ModelAdmin):
    pass