from django.shortcuts import render, redirect
from django.utils.translation import activate
from .models import User, ContactInfo, Address, Post, Comment, Topic
from django.contrib import messages
from django.http import JsonResponse

import pytz
import bcrypt
from .CurrencyAPI import current_market_prices

from datetime import datetime, time
from django.utils.timezone import is_aware, localdate, make_aware, make_naive, localtime, localdate, now


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

    # Crypto indicators 
    symbols = 'BTC,ETH,ADA,DOT,UNI,LTC,LINK,VET,MINA,SWAP,RFOX,ATOM,CRV,MATIC,GUSD'
    symbol_list = ['BTC','ETH','ADA','DOT','UNI','LTC','LINK','VET','MINA','SWAP','RFOX','ATOM','CRV','MATIC','GUSD']

    # tl = TimeLoop
    # @tl.job(interval=timedelta(hours=1))       

    topic = request.session['topic_selected'] = False
    context = {
        'topics' : Topic.objects.all(),
        'topic_selected' : topic,
        'prices': current_market_prices(symbols, symbol_list)
    }
    
    return render(request, 'blog.html', context)


def time_zone():
    '''Allow the user to select their time  zone.'''
    timezone_list = []
    # from pytz timeszones remove the following 
    remove_2 = ['GB', 'NZ']
    remove_3 = ['EET','EST','ETC','GMT','HST','WET',
                'UCT', 'UTC', 'MET','MST','PRC', 'ROC','ROK', 'CET']
    remove_4 = ['W-SU', 'W-SU']
    remove_5 = ['GMT+0', 'GMT-0']
    remove_7 = ['MST7MDT', 'NZ-CHAT', 'GB-Eire', 'PST8PDT', 'EST5EDT', 'CST6CDT']

    idx = 1
    for tz in pytz.all_timezones:
        if tz[0:4] == 'Etc/':
            pass
        elif tz[0:2] in remove_2 and len(tz) == 2:
            pass
        elif tz[0:3] in remove_3 and len(tz) == 3:
            pass
        elif tz[0:4] in remove_4 and len(tz) == 4 :
            pass
        elif tz[0:5] in remove_5 and len(tz) == 5 :
            pass
        elif tz[0:7] in remove_7 and len(tz) == 7:
            pass
        else:
            timezone_list.append((idx,tz))
            idx += 1

    return timezone_list


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
            timezone=request.POST.get('time-zone-nm', None),
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

    time_zones = time_zone()
    context = {
        'time_zones' : time_zones
    }
    return render(request, 'register.html', context)


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
        
        '''is user does not add a profile image. When update selected 
        it will cause an error and cause profile image to be empty'''
        
        profile_pic = request.POST.get('user-avatar-nm',None)
        active_id = request.session['active_user_id']

        if profile_pic == None or profile_pic == '':
            user = User.objects.get(id=active_id)
            profile_pic = user.picture

        User.objects.update_or_create(
            id=request.session['active_user_id'],
            defaults = {
                'first_name': request.POST.get('user-first-nm',None),
                'last_name': request.POST.get('user-last-nm',None),
                'dob': request.POST.get('user-dob-nm',None),
                'timezone':request.POST.get('time-zone-nm', None),
                # 'email': request.POST.get('user-email-nm',None),
                'display_name': request.POST.get('user-display-nm',None),
                'picture': profile_pic,
                'gender': request.POST.get('user-gender-nm',None),
                'description': request.POST.get('user-desc-nm',None),   
            }
        )

        return redirect('/profile') 
    
    active_id = request.session['active_user_id']
    time_zones = time_zone()

    context = {
        'general' : User.objects.get(id=active_id),
        'contact' : ContactInfo.objects.get(user_id=active_id),
        'address' : Address.objects.get(user_id=active_id),
        'date' : str(User.objects.get(id=active_id).dob),
        'time_zones' : time_zones
    }
    
    user = User.objects.get(id=active_id)
    
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
        '''PO box is optional. If user does not add make it 0 to prevent 
        and error. '''
        po_box= request.POST.get('po-box-nm',None)
        if po_box == None or po_box == '':
            po_box = 0

        Address.objects.filter(user_id=request.session['active_user_id']).update(
            street_number= request.POST.get('street-number-nm',None),
            street_name= request.POST.get('street-name-nm',None),
            po_box= po_box,
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
        if errors == None:
            '''if no Topics errors is None. will cause error when length is checked. Set to empty dictionary'''
            errors = {}

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


def blog_about_topic(request, topic_id):
    
    # Crypto indicators 
    symbols = 'BTC,ETH,ADA,DOT,UNI,LTC,LINK,VET,MINA,SWAP,RFOX,ATOM,CRV,MATIC,GUSD'
    symbol_list = ['BTC','ETH','ADA','DOT','UNI','LTC','LINK','VET','MINA','SWAP','RFOX','ATOM','CRV','MATIC','GUSD']

    topic = request.session['topic_selected'] = True

    posts_by_topic = Post.objects.filter(topic__id=topic_id).order_by('created_at')



    context = {
        'selected_topic' : Topic.objects.get(id=topic_id),
        'topic_selected' : topic,
        'topics' : Topic.objects.all(),
        'posts_by_topic' : posts_by_topic,
        'prices': current_market_prices(symbols, symbol_list)
    }

    return render(request, 'blog.html', context)


def add_post(request):
    '''Add a Post to db. Hidden input contains the active Topic id 
    that the Post will be associated with '''

    if request.method == 'POST' and request.session['logged_in'] == True:
        user_id = request.session['active_user_id']
        active_user = User.objects.get(id=user_id)

        topic_id = request.POST.get('active-topic-id-nm', None)
        active_topic = Topic.objects.get(id=topic_id)

        new_post = Post.objects.create(
            post = request.POST.get('add-post-msg-nm', None),
            user = active_user,
            topic = active_topic
        )

        new_post.save()

        url = f'/blog-about/topic/{topic_id}'
        return redirect(url)
    # if not POST or logged-in redirect blog-about    
    return redirect('/blog-about')


def add_comment(request):
    '''Add a Comment to db. '''

    if request.method == 'POST' and request.session['logged_in'] == True:
        user_id = request.session['active_user_id']
        active_user = User.objects.get(id=user_id)

        post_id = request.POST.get('active-post-id-nm', None)
        active_post = Post.objects.get(id=post_id)
        print(f'Active Post >> {active_post}')

        topic_id = request.POST.get('active-topic-nm', None)
        print(topic_id)
        active_topic = Topic.objects.get(id=topic_id)
        print(active_topic)

        new_comment = Comment.objects.create(
            comment = request.POST.get('add-comment-msg-nm', None),
            user = active_user,
            post = active_post,
            topic = active_topic
        )

        new_comment.save()

        url = f'/blog-about/topic/{topic_id}'
        return redirect(url)
    # if not POST or logged-in redirect blog-about    
    return redirect('/blog-about')


def delete_comment(request):
    
    topic_id = request.POST.get('hidden-topic-id-nm', None)
    comment_id = request.POST.get('hidden-com-id-nm', None)
    user_id = request.POST.get('hidden-user-id-nm', None)
    comm_created_at = request.POST.get('com-created-at-nm', None)
    active_user = request.session['active_user_id']

    # What is the active_user time zone
    active_user = User.objects.get(id=request.session['active_user_id'])
    active_user_tz = active_user.timezone
    print(f'Active User TZ => {active_user_tz}')
    print(f'TZ Type => {type(active_user_tz)}')

    # adjust lowercase am/pm to uppercase 
    converted_time = comm_created_at.replace('a.m.', 'AM').replace('p.m.', 'PM')
    print(f'Check converted time => {converted_time}')

    # convert from string to datetime object
    comment_datetime = datetime.strptime(converted_time, '%B %d, %Y, %I:%M %p')
    print(f'Check if is Aware: {is_aware(comment_datetime)}')

    # time zone cannot be type string
    user_timezone = pytz.timezone(active_user_tz)
    print(f'This is the user timezone => {user_timezone}')
    print(f'User TZ Type converted correctly => {type(user_timezone)}\n')


    aware_comment_dt = make_aware(comment_datetime, timezone=user_timezone, is_dst=None)
    print(f'Check if is Aware True indicates is aware => {is_aware(aware_comment_dt)}\n')

    comment_local_time_tz = localtime(value=aware_comment_dt, timezone=user_timezone)
    print('The below should be should be 5:01PM EST => Using "localtime"')
    print(comment_local_time_tz)
    print()

    comment_local_date_tz = localdate(value=aware_comment_dt, timezone=user_timezone)
    print('The below should be should be 5:01PM EST => Using "localdate"')
    print(comment_local_date_tz)

    print()
    print('Still returning the UTC time. I created this at 5PM EST')
    print(aware_comment_dt)
    print('---------------')

    print('+++WHAT DOES DJANGO NOE RETURN?+++')
    django_date_now = now()
    print(f'Using Django now() => {django_date_now}')
    print(f'Is Django Date now() aware => {is_aware(django_date_now)}')
    print('It returns UTC\n\n')

    print('+++WHAT DOES DATETIME RETURN???+++')
    python_date_now = datetime.now()
    print(f'This is PYTHON datetime now => {python_date_now}')
    print('Python datetime now() returns local time zone, EST.')

    if request.method == 'POST' and request.session['logged_in'] == True:
        ''' Allow the user to delete the comment only if they created it'''

        if user_id == str(active_user):
            '''Active user is user that created comment they can delete'''
            comment_to_delete = Comment.objects.get(id=comment_id)
            comment_to_delete.delete()

            url = f'/blog-about/topic/{topic_id}'
            return redirect(url)
        else:
            # Comment was not created by user selecting remove
            
            url = f'/blog-about/topic/{topic_id}'
            return redirect(url)

    # Not a POST
    url = f'/blog-about/topic/{topic_id}'
    return render(url)