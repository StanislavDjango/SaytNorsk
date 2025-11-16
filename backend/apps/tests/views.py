from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Lesson, Test, Question, Answer, StudentResult, StudentAnswer
from .serializers import (
    LessonSerializer, TestSerializer, QuestionSerializer, AnswerSerializer,
    StudentResultSerializer, StudentAnswerSerializer
)


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson model"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['level']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'level']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TestViewSet(viewsets.ModelViewSet):
    """ViewSet for Test model"""
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lesson', 'test_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def submit_answers(self, request, pk=None):
        """Submit test answers and get results"""
        test = self.get_object()
        answers_data = request.data.get('answers', [])
        student_name = request.data.get('student_name', '')
        
        total_questions = test.questions.count()
        correct_count = 0
        student_answers = []
        
        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            student_answer = answer_data.get('answer', '')
            
            try:
                question = test.questions.get(id=question_id)
                correct_answer = question.answers.filter(is_correct=True).first()
                
                is_correct = correct_answer and (
                    correct_answer.text.lower() == student_answer.lower()
                )
                
                if is_correct:
                    correct_count += 1
                
                student_answers.append({
                    'question': question_id,
                    'student_answer': student_answer,
                    'correct_answer': correct_answer.text if correct_answer else '',
                    'is_correct': is_correct,
                })
            except Question.DoesNotExist:
                continue
        
        # Calculate score
        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        # Determine letter grade
        if score_percentage >= 90:
            score_letter = 'A'
        elif score_percentage >= 80:
            score_letter = 'B'
        elif score_percentage >= 70:
            score_letter = 'C'
        elif score_percentage >= 60:
            score_letter = 'D'
        elif score_percentage >= 50:
            score_letter = 'E'
        else:
            score_letter = 'F'
        
        # Create result
        result = StudentResult.objects.create(
            student_name=student_name,
            test=test,
            total_questions=total_questions,
            correct_answers=correct_count,
            score_percentage=score_percentage,
            score_letter=score_letter,
        )
        
        # Create student answers
        for answer_data in student_answers:
            StudentAnswer.objects.create(result=result, **answer_data)
        
        return Response({
            'id': result.id,
            'score_percentage': result.score_percentage,
            'score_letter': result.score_letter,
            'correct_answers': result.correct_answers,
            'total_questions': result.total_questions,
            'answers': student_answers,
        }, status=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for Question model"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['test', 'difficulty']
    ordering_fields = ['order', 'difficulty']
    ordering = ['order']


class AnswerViewSet(viewsets.ModelViewSet):
    """ViewSet for Answer model"""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
