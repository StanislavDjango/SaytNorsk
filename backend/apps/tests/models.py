from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Lesson(models.Model):
    """Lesson that groups related tests by topic and level."""

    LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Mastery'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='A1')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self) -> str:
        return self.title


class Test(models.Model):
    """Test/quiz that belongs to a lesson."""

    TEST_TYPE_CHOICES = [
        ('fill-in-the-blank', 'Fill in the Blank'),
        ('multiple-choice', 'Multiple Choice'),
        ('drag-drop', 'Drag & Drop'),
        ('find-error', 'Find Error'),
        ('listening', 'Listening'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES, default='fill-in-the-blank')
    show_correct_answers = models.BooleanField(default=True, help_text="Show correct answers after test completion")
    show_errors_breakdown = models.BooleanField(default=True, help_text="Show detailed error breakdown")
    duration_minutes = models.IntegerField(default=30, validators=[MinValueValidator(1), MaxValueValidator(300)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['lesson', 'created_at']
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

    def __str__(self) -> str:
        return f"{self.lesson.title} - {self.title}"


class Question(models.Model):
    """Question that belongs to a test."""

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="Question text or sentence with [...] for fill-in-the-blank")
    audio_file = models.FileField(upload_to='audio/%Y/%m/%d/', blank=True, null=True, help_text="For listening questions")
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order of questions in test")
    difficulty = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    explanation = models.TextField(blank=True, null=True, help_text="Explanation for the correct answer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['test', 'order']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self) -> str:
        return f"{self.test.title} - Q{self.order}"


class Answer(models.Model):
    """Answer option for a question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True, null=True, help_text="Why this answer is correct/incorrect")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question', 'order']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self) -> str:
        status = 'OK' if self.is_correct else 'ALT'
        return f"{status} {self.text[:50]}"


class StudentResult(models.Model):
    """Aggregated results for a completed test."""

    student_name = models.CharField(max_length=200, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    score_percentage = models.FloatField()
    score_letter = models.CharField(max_length=1, choices=[
        ('A', 'A (90-100%)'),
        ('B', 'B (80-89%)'),
        ('C', 'C (70-79%)'),
        ('D', 'D (60-69%)'),
        ('E', 'E (50-59%)'),
        ('F', 'F (Below 50%)'),
    ])
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Results'

    def __str__(self) -> str:
        return f"{self.student_name or 'Anonymous'} - {self.test.title}: {self.score_percentage:.1f}%"


class StudentAnswer(models.Model):
    """Single answer given by a student for one question."""

    result = models.ForeignKey(StudentResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student_answer = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField()

    class Meta:
        verbose_name = 'Student Answer'
        verbose_name_plural = 'Student Answers'

    def __str__(self) -> str:
        return f"Question {self.question.order} - {'Correct' if self.is_correct else 'Incorrect'}"
