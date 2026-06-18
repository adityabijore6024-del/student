from django.contrib import admin
from .models import Profile
from .models import Slide
from .models import Teacher
from .models import Course
from .models import PurchasedCourse
from .models import Profile_app
from .models import SupportTicket

admin.site.register(Profile)
admin.site.register(Slide)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(PurchasedCourse)
admin.site.register(Profile_app)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "category",
        "subject",
        "status",
        "created_at"
    )

    list_filter = (
        "status",
        "category"
    )

    search_fields = (
        "user__username",
        "subject"
    )

from django.contrib import admin

from .models import (
    Test,
    Question,
    Option,
    TestAttempt,
    StudentAnswer
)


class OptionInline(admin.TabularInline):

    model = Option

    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "question_text",
        "question_type",
        "marks"
    )

    list_filter = (
        "question_type",
    )

    search_fields = (
        "question_text",
    )

    inlines = [
        OptionInline
    ]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course",
        "duration_minutes",
        "total_marks"
    )

    search_fields = (
        "title",
    )

    list_filter = (
        "course",
    )


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "option_text",
        "is_correct"
    )


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "test",
        "score",
        "percentage",
        "time_taken_seconds",
        "submitted_at"
    )

    list_filter = (
        "test",
    )

    search_fields = (
        "user__username",
    )


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "attempt",
        "question",
        "is_correct"
    )