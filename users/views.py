from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User 
from .serializers import UserSerializer
import jwt, datetime

class RegisterView(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Registration was successful 😀')
    

class LoginView(APIView):
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        # validations
        if user is None: raise AuthenticationFailed('User not found')
        if not user.check_password(password): raise AuthenticationFailed('Passwords do not match!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        # return token via cookies
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True, samesite='None', secure=True)
        response.data = { 'message': 'You are logged in 😁', 'jwt': token }
        
        return response
    
    
class UserView(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token: raise AuthenticationFailed('User not authenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User not authenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
    
class LogoutView(APIView):
    
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = { 'message': 'Log out was successful😁' }
        response.set_cookie(key='jwt', value='', httponly=True, samesite='None', secure=True)
        
        return response
    