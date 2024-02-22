
from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse
from random import randint
from .models import WatchLater, movie_detail , UserProfile
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from movie_buff.encryption_util import *

import platform   #added on 21/10/23

import user_agents 

#below imports were added on 20/10/23 yesterday

from .forms import *
from django.contrib.auth.forms import PasswordChangeForm ,PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models




# Create your views here.

def index(request):
    movie_list = movie_detail.objects.all()

     
    context = {'movie_list':  movie_list}
    return render(request, 'index.html', context)
    


@login_required(login_url='loginError')
def movie_view(request, movie_id):
    if User.is_authenticated:
        
        

        movie = get_object_or_404(movie_detail, pk=movie_id)
        
        #changes made on 22/10/23 yesterday
        genre = movie.genre  # Get the genre of the clicked movie
        related_movies = movie_detail.objects.filter(genre=genre).exclude(id=movie_id)
        
        context = {
            'movie': movie,
            'related_movies': related_movies,  # Pass the related movies to the template
            
            }
        return render(request, 'movie_view.html', context)
    else:
        return redirect('loginError')





def search(request):
    query= request.GET['query']
    query= query.strip() 
    movie_list = movie_detail.objects.filter(movie_name__icontains=query)   
    search_result = {'movie_list': movie_list}
    return render(request,'search.html',search_result)



def handleSignup(request):
    if request.method == 'POST':
        #Get the Post Parameters
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        #Validating Sign up form

        if password1 != password2 :
            messages.error(request, " Kindly type same password in Confrim password ")
            return redirect('index')
        
        #below validation code added on 20/10/23

        if User.objects.filter(username=username).exists():
            messages.error(request, " Username you have Entered is already exists  ")
            return redirect('index')
        
        if User.objects.filter(email=email).exists():   
            messages.error(request, " Email you have Entered is already exists  ")
            return redirect('index')

        #Creating user
        myuser = User.objects.create_user(username,email,password1)
        myuser.username= username
        myuser.first_name= firstname
        myuser.last_name = lastname
        
        myuser.save()
        messages.success(request,"Your Movie Buff Account is Created")
        return redirect('index')
    else : 
        return HttpResponse(" 404 - Not found")


def handleLogin(request):
    if request.method == 'POST':
        login_username = request.POST['login_username']
        login_password = request.POST['login_password']

        user = authenticate(username = login_username, password=login_password)
        
        
        if user is not None:
            user_profile = user.userprofile   #code added on 21/10/23
            previous_browser_name = user_profile.browser_name
            previous_os_name = user_profile.os_name
            previous_device_name = user_profile.device_name
            
            user_agent_string = request.META.get('HTTP_USER_AGENT')
            current_user_agent = user_agents.parse(user_agent_string)

            browser = current_user_agent.browser.family
            os = current_user_agent.os.family
            device = current_user_agent.device.family
            
            user_profile.browser_name = browser
            user_profile.os_name = os
            user_profile.device_name = device
            user_profile.save() 

            if user_profile.session_token and user_profile.session_token != request.session.session_key:

                 


                 device_name = platform.node()
                 os_name     = platform.system()

                 #messages.error(request, f'You are already logged in on another device named : {device_name}, {os_name } OS')
                 messages.error(request, f'You are already logged in on another device | Browser:  {previous_browser_name} , Operating System: { previous_os_name}, Device: {previous_device_name}')
                 return redirect('index')    #code added on 21/10/23

            login(request,user)

            request.session['user']= login_username         #code added on 20/10/23

            # user_profile.browser_name = browser
            # user_profile.os_name = os
            # user_profile.device_name = device

            user_profile.session_token = request.session.session_key        #code added on 20/10/23
            user_profile.save()                          #code added on 20/10/23
            


            messages.success(request,"Successfully Logged in")
            return redirect('index')

        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('index')
    else : 
        return redirect('loginError')

#handle login code written on 22/10/2023 on 
def handleLogout(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        user_profile.session_token = None

        user_profile.browser_name = None
        user_profile.os_name = None
        user_profile.device_name = None

        user_profile.save()
        logout(request)
        messages.success(request, 'Successfully Logged Out')
        return redirect('index')
    
    else:
        return redirect('loginError')


def loginError(request):
    return render(request,"loginError.html")

@login_required(login_url='loginError')
def watch_later_list(request):
    
    user_watch_later_list = WatchLater.objects.filter(user=request.user).values_list('video', flat=True)
    movies_in_watch_later = movie_detail.objects.filter(id__in=user_watch_later_list)
    return render(request, "watch_later_list.html", {'movie_list': movies_in_watch_later})


@login_required(login_url='loginError')
def add_to_watch_later(request, movie_id):
    
    
    if request.method == 'POST':
        movie = get_object_or_404(movie_detail, id=movie_id)
        watch_later_entry, created = WatchLater.objects.get_or_create(user=request.user, video=movie)
        if created:
            messages.success(request, "Your movie is added to the watch later list")
        else:
            messages.info(request, "This movie is already in your watch later list")
        return redirect('movie_view', movie_id=movie_id)
    else:
        messages.error(request, "Not able to add movie")


def remove_from_watch_later(request, movie_id):
    movie = get_object_or_404(movie_detail, id=movie_id)
    WatchLater.objects.filter(user=request.user, video=movie).delete()
    return redirect('watch_later_list')


#below  code is writtenn on 20/10/2020 yesterday 

# EDIT PROFILE CODE below

@login_required(login_url='loginError')
def view_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your Profile has been updated")
            return redirect('view_profile')

    else:
         u_form = UserUpdateForm(instance=request.user)
         p_form = ProfileUpdateForm(instance=request.user.userprofile)
         

    context = {
        'u_form': u_form,
        'p_form' : p_form,
        

    }
    return render(request, 'view_profile.html',context)



#password change Code below

@login_required(login_url='loginError')
def change_password(request):
    if request.method == 'POST':
        # Ensure that the user is changing their own password
          
        user = request.user  # Get the currently authenticated user
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid() :
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        
        'form': form,
        }    
    return render(request, 'change_password.html', context)





@login_required
def toggle_like(request, movie_id):
    if request.method == "POST":
        movie = movie_detail.objects.get(id=movie_id)

        # Check if the user has already liked the movie in the session
        session_variable = 'liked_movie_%d' % movie.id
        if session_variable in request.session:
            liked = request.session[session_variable]
        else:
            # Default to not liked
            liked = False

        if liked:
            # User has liked the movie, so "unlike" it
            movie.likes.remove(request.user)
            request.session[session_variable] = False
        else:
            # User has not liked the movie, so "like" it
            movie.likes.add(request.user)
            request.session[session_variable] = True

        # Update the like count
        likes_count = movie.likes.count()

        return JsonResponse({'success': True, 'likes': likes_count, 'is_liked': not liked})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def most_popular(request):
    # Query the database to get the 6 most liked videos
    most_liked_videos = movie_detail.objects.filter(likes__isnull=False).annotate(like_count=models.Count('likes')).order_by('-like_count')[:6]

    
    context = {
        'most_liked_videos': most_liked_videos
    }

    return render(request, 'most_popular.html', context)        


def genre_view(request , genre):
   # Filter movies based on the selected genre
    genre_based_movies = movie_detail.objects.filter( genre = genre)
    
    context = {
        'genre': genre,
        'genre_based_movies': genre_based_movies,
    }
    
    return render(request, 'genre_view.html', context)


