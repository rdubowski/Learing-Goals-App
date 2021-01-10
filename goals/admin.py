from django.contrib import admin
from .models import LearningGoal, SingleTask, Profile

class SingleTaskInline(admin.StackedInline):
    model = SingleTask
    extra = 3

class LearningGoalAdmin(admin.ModelAdmin):
    inlines = [SingleTaskInline,]
admin.site.register(LearningGoal, LearningGoalAdmin)
admin.site.register(SingleTask)
admin.site.register(Profile)