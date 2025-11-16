from rest_framework import serializers
from .models import Lesson, Test, Question, Answer, StudentResult, StudentAnswer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'explanation', 'order']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'audio_file', 'image', 'order', 'difficulty', 'explanation', 'answers']
        read_only_fields = ['id']


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Test
        fields = [
            'id', 'lesson', 'title', 'description', 'test_type',
            'show_correct_answers', 'show_errors_breakdown', 'duration_minutes', 'questions'
        ]
        read_only_fields = ['id']


class LessonSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'level', 'created_by', 'created_at', 'updated_at', 'tests']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['question', 'student_answer', 'correct_answer', 'is_correct']


class StudentResultSerializer(serializers.ModelSerializer):
    answers = StudentAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = StudentResult
        fields = [
            'id', 'student_name', 'test', 'total_questions', 'correct_answers',
            'score_percentage', 'score_letter', 'completed_at', 'answers'
        ]
        read_only_fields = ['id', 'completed_at']
