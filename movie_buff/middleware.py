# middleware.py
# the follwing function deletes the session after it got expired
from venv import logger
from django.contrib.auth.middleware import AuthenticationMiddleware
from .models import UserProfile
from django.contrib.sessions.models import Session
from django.utils import timezone

# class SessionTimeoutMiddleware(AuthenticationMiddleware):
#     def process_request(self, request):
#         user = request.user
#         if user.is_authenticated:
            
#             session_key = request.session.session_key
#          #    session_exists = Session.objects.filter(session_key=session_key_to_check, expire_date__gte=timezone.now(), sessiondata__contains=user.id).exists()
#             if  Session.objects.filter(session_key=session_key, session_data__contains=str(user.id)).exists()  and UserProfile.objects.filter(user=user, session_token=session_key).exists():
#                 # Session has expired, update the session_token
#                 user_profile = user.userprofile
#                 user_profile.session_token = None
#                 user_profile.save()

# from django.contrib.auth.middleware import AuthenticationMiddleware
# from .models import UserProfile
# from django.contrib.sessions.models import Session

class SessionTimeoutMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            session_key = request.session.session_key
            session = Session.objects.get(session_key=session_key)

           

            print("Session Key:", session_key)
            logger.info("Session Key: %s", session_key)

            print("Session Expire Date:", session.expire_date)
            logger.info("Session Expire Date: %s", session.expire_date)

            print("Current Time:", timezone.now())
            logger.info("Current Time: %s", timezone.now())


            
                # if Session.objects.filter(session_key=session_key).exists():
            if  UserProfile.objects.filter(user=user, session_token=session_key).exists() :
                    if session.expire_date < timezone.now():
                        # Session has expired, update the session_token
                        user_profile = user.userprofile
                        user_profile.session_token = None
                        user_profile.save()
                    
                    else:
                        user_profile = user.userprofile
                        user_profile.session_token = "else is Executed"
                        user_profile.save()
                         
             
            # Check if the session has expired
            # session = Session.objects.get(session_key=session_key)
            # if session.expire_date < timezone.now():
            #     # Session has expired, update the session_token
            #     user_profile = user.userprofile
            #     user_profile.session_token = None
            #     user_profile.save()
               

               