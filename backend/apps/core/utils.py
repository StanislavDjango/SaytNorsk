from django.contrib.auth.models import User


class UsersManager:
    @staticmethod
    def get_user_role(user):
        """Get user role (admin, teacher, student)"""
        if user.is_superuser:
            return 'admin'
        elif user.groups.filter(name='Teacher').exists():
            return 'teacher'
        else:
            return 'student'
