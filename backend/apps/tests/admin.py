from django.contrib import admin
from .models import Lesson, Test, Question, Answer, StudentResult, StudentAnswer


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'created_by', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {'fields': ('title', 'description')}),
        ('Details', {'fields': ('level', 'created_by')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'test_type', 'created_at']
    list_filter = ['test_type', 'created_at', 'lesson']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {'fields': ('lesson', 'title', 'description')}),
        ('Configuration', {'fields': ('test_type', 'show_correct_answers', 'show_errors_breakdown', 'duration_minutes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ['text', 'is_correct', 'order', 'explanation']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'test', 'difficulty', 'order']
    list_filter = ['test', 'difficulty', 'created_at']
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AnswerInline]
    fieldsets = (
        ('Basic Information', {'fields': ('test', 'text', 'order')}),
        ('Media', {'fields': ('audio_file', 'image'), 'classes': ('collapse',)}),
        ('Details', {'fields': ('difficulty', 'explanation')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'question', 'order']
    list_filter = ['is_correct', 'created_at']
    search_fields = ['text', 'question__text']
    fieldsets = (
        ('Basic Information', {'fields': ('question', 'text', 'order')}),
        ('Correctness', {'fields': ('is_correct', 'explanation')}),
    )


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ['question', 'student_answer', 'correct_answer', 'is_correct']
    can_delete = False


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'test', 'score_percentage', 'score_letter', 'completed_at']
    list_filter = ['test', 'score_letter', 'completed_at']
    search_fields = ['student_name', 'test__title']
    readonly_fields = ['completed_at', 'score_percentage', 'score_letter']
    inlines = [StudentAnswerInline]
    fieldsets = (
        ('Student Information', {'fields': ('student_name', 'completed_at')}),
        ('Test', {'fields': ('test',)}),
        ('Results', {'fields': ('total_questions', 'correct_answers', 'score_percentage', 'score_letter')}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
