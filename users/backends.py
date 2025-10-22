from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend de autenticação que permite login com email ou username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            # Tentar autenticar com email ou username
            user = UserModel.objects.get(
                Q(username=username) | Q(email=username)
            )
            
            if user.check_password(password):
                return user
                
        except UserModel.DoesNotExist:
            return None
            
        return None 