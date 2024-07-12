from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User
from django.core.cache import cache
from .serializers import *
import redis
import time
from .utils import Utils
from .tasks import *
from django.db import transaction

# Create your views here.

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

class UserAuthenticationViewSet(viewsets.ViewSet):
    serializer_class = RegisterUser
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    
    # Endpoint to register new users
    @action(methods=['post'], detail=False, serializer_class=RegisterUser, url_path='signup')
    def signup(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.validated_data.get('email').lower()
                
                # Check if the email has been registered in the database
                user = User.objects.filter(email=email.lower()).first()
                if user is not None:
                    return Response({'success': True, 'message': "An account has been created with this email address"}, status=status.HTTP_409_CONFLICT)
                
                # if email does not exist, create a new user and generate OTP
                with transaction.atomic():
                    user = serializer.save()
                    otp = Utils.generate_vals('otp_num')
                    cache.set(email, otp, 300)
                    transaction.on_commit(lambda: send_email_message.delay('otp_email', email, 'OTP Verification Message', otp))
                    
                    return Response({'success': True, 'message': "User created successfully"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'success': False, 'message': f"Error creating account due to invalid data. Please try again with correct information {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': f"Error creating account due to error in data provided. Please try again with correct information {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Endpoint to verify user account using OTP generated from the registration    
    @action(methods=['post'], detail=False)
    def verify_account(self,request):
        try:
            otp = request.GET.get('otp')
            email = request.GET.get('email')
            user = User.objects.get(email=email)
            cached_otp = cache.get(email)
            
            # Check if OTP provided by user is same as cached OTP and proceed to activate user account
            if otp is not None and otp == cached_otp:
                user.is_active = True
                user.account_number = Utils.generate_vals('acct_num')
                user.save()
                cache.delete(email)
                return Response({'success': True, 'message': 'Account successfully verified. Please proceed to login'}, status=status.HTTP_200_OK)
            return Response({'success': False, 'message': 'Enter a valid otp'}, status=status.HTTP_400_BAD_REQUEST)
        except TimeoutError as e:
            return Response({'success': False, 'message': 'OTP timed out'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response({'success': False, 'message': f'Account could not be verified. Request for new OTP and try again. {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        