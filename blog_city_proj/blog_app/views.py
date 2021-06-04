from django.shortcuts import render, redirect
from django.utils.translation import activate
from .models import User, ContactInfo, Address, Post, Comment, Topic
from django.contrib import messages
from django.http import JsonResponse
import bcrypt

def index_view(request):
    try:
        # user might navigate to index while logged in
        if request.session['logged_in'] == True or request.session['logged_in'] == False:
            return render(request, 'index.html')
            
    except:
        # if session has not been created there will be an error 
        request.session['logged_in'] = False
        return render(request, 'index.html')


def blog_view(request):

    topic = request.session['topic_selected'] = False
    context = {
        'topics' : Topic.objects.all(),
        'topic_selected' : topic,
    }

    return render(request, 'blog.html', context)


def register_view(request):

    if request.method == 'POST':
        errors = User.objects.validate_reg(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)   
            return redirect('/register')

        # no errors - salt password and pass to "create"
        password = request.POST.get('reg-password-nm',None)
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # create user 
        User.objects.create(
            first_name=request.POST.get('reg-first-nm',None),
            last_name=request.POST.get('reg-last-nm',None),
            dob=request.POST.get('reg-dob-nm',None),
            email=request.POST.get('reg-email-nm',None),
            picture='default-img.jpg',
            password=password_hash,
        )

        # create instance of last record from User 
        user_added = User.objects.all().last()

        ContactInfo.objects.create(
            mobile_phone = request.POST.get('handy-phone-nm',None),
            office_phone =  request.POST.get('office-nm',None),
            office_text =  request.POST.get('office-ext-nm',None),
            url =  request.POST.get('url-nm',None),
            user = user_added,
        )

        Address.objects.create(
            street_number = request.POST.get('street-number-nm',None),
            street_name =  request.POST.get('street-name-nm',None),
            po_box =  request.POST.get('po-box-nm',None),
            state =  request.POST.get('states-nm',None),
            city =  request.POST.get('address-city-nm',None),
            zip_code =  request.POST.get('zip-address-nm',None),
            user = user_added,
        )

        # user created but still not logged in 
        request.session['logged_in'] = False

        return render(request, 'login.html')

    return render(request, 'register.html')


def login_view(request):   
    if request.method == 'POST':

        '''if email is not in db then Django returns "IndexError at /login/
        list index out of range". Is there a way to prevent? This will be caught 
        with ValidationManager within models.py but what about before?'''
        errors = User.objects.validation_log(request.POST)
        
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)  
            # return JsonResponse(errors, status=200) 
            return redirect('/login')

        active_user = User.objects.filter(email=request.POST.get('log-email-nm', None))
        context = {
            'user' : active_user[0]
        }
        
        # user is logged in 
        request.session['logged_in'] = True
        request.session['active_user_id'] = active_user[0].id
        request.session['active_user_first'] = active_user[0].first_name
        request.session['active_user_last'] = active_user[0].last_name
        # request.session['active_user_picture'] = active_user[0].picture
        # no errors - user logged in
        return render(request, 'index.html', context)


    return render(request, 'login.html')


def profile_view(request):

    if request.method == 'POST':
        # Updating User data skip email. Do not allow user to change
        
        User.objects.update_or_create(
            id=request.session['active_user_id'],
            defaults = {
                'first_name': request.POST.get('user-first-nm',None),
                'last_name': request.POST.get('user-last-nm',None),
                'dob': request.POST.get('user-dob-nm',None),
                # 'email': request.POST.get('user-email-nm',None),
                'display_name': request.POST.get('user-display-nm',None),
                'picture': request.POST.get('user-avatar-nm',None),
                'gender': request.POST.get('user-gender-nm',None),
                'description': request.POST.get('user-desc-nm',None),   
            }
        )

        return redirect('/profile') 

    active_id = request.session['active_user_id']
    context = {
        'general' : User.objects.get(id=active_id),
        'contact' : ContactInfo.objects.get(user_id=active_id),
        'address' : Address.objects.get(user_id=active_id),
        'date' : str(User.objects.get(id=active_id).dob)
    }
    
    user = User.objects.get(id=active_id)
    print('-*-*-*-*-*-*-*-*-')
    print(user.picture)
    print(user.picture.url)
    
    return render(request, 'user_profile.html', context)


def log_out(request):
        try:
            # log user out
            request.session['logged_in'] = False
            request.session['user_id'] = None


            request.session.flush()
            return render(request, 'index.html')
        except:
            request.session.flush() 
            return redirect('/') 


def contact_update(request):
    # should always be a POST but add just in-case
    if request.method == 'POST': 

        ContactInfo.objects.filter(user_id=request.session['active_user_id']).update(
            mobile_phone= request.POST.get('handy-phone-nm',None),
            office_phone= request.POST.get('office-nm',None),
            url= request.POST.get('url-nm',None),
            office_text= request.POST.get('office-text-nm',None)
        )

        return redirect('/profile')
    # if not POST but should never happen    
    return render(request, 'user_profile.html')


def profile_update(request):
        # should always be a POST but add just in-case
    if request.method == 'POST': 

        Address.objects.filter(user_id=request.session['active_user_id']).update(
            street_number= request.POST.get('street-number-nm',None),
            street_name= request.POST.get('street-name-nm',None),
            po_box= request.POST.get('po-box-nm',None),
            state= request.POST.get('states-nm',None),
            city= request.POST.get('address-city-nm',None),
            zip_code= request.POST.get('zip-address-nm',None),
        )

        return redirect('/profile')
    # if not POST but should never happen    
    return render(request, 'user_profile.html')
    pass


def add_topic(request):
    '''Allow user to create a new topic that will be assigned to them.
    Check if there is an active user to prevent error if not active user '''
    if request.method == 'POST' and request.session['logged_in'] == True:
        errors = Topic.objects.validation_topic(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)   
            return redirect('/blog-about')

        Topic.objects.create(
                topic = request.POST.get('topic-nm', None),
                user = User.objects.get(id=request.session['active_user_id']),
        )
            
        return redirect('/blog-about')
    
    # should not happen    
    return redirect('/blog-about')

def blog_about_topic(request, topic_str):

    topic = request.session['topic_selected'] = True

    posts_by_topic = Post.objects.filter(topic__topic=topic_str).order_by('created_at')

    comments_by_post = Comment.objects.filter(topic__topic=topic_str).order_by('-created_at')

    context = {
        'selected_topic' : Topic.objects.get(topic=topic_str),
        'topic_selected' : topic,
        'posts_by_topic' : posts_by_topic,
        'comments_by_post' : comments_by_post
    }
    return render(request, 'blog.html', context)
