from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from Insta_Web.forms import *
from Insta_Web.models import *
from Insta_bot.apollo import Apollo
from Insta_bot.run import main
from multiprocessing import Process
from datetime import datetime
import os,json
from .extra_functions import *
from time import sleep
import django.db
from .database import *

class HomePage(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'landing.html')
        else:
            print(request.user)
            db_obj = get_all_instagram_accounts(request)
            for i in db_obj.all():
                print(i.username + " " + i.instagram_username)
            return render(request, 'home.html', {'accounts':db_obj.all()})


class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('index')


class Home(View):
    def get(self, request):
        print('HOME')
        username = request.GET['account_username']
        password = request.GET['account_password']
        print(request.user)
        print(username,password)

        db_obj = get_insta_account(request.user,username)
        if db_obj.count() == 0:
            bot = Apollo(login=username, password=password)
            if not bot.login_status:
                print('Credentials not correct')
                return JsonResponse({'res': 'Invalid Username or Password!'})
            else:
                user = bot.get_user_info(username)
                print(user['profile_pic_url_hd'])
                bot.logout()
                save_user_details_in_database(request.user,username, password,user['profile_pic_url_hd'])
                return JsonResponse({'res':'Account Successfully Added!'})

        return JsonResponse({'res':'Account Already Present. Cannot Add again!'})


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid login'})
        return render(request, 'login.html', {'error_message': 'Invalid login'})


class SignUp(View):
    def validate_data(self, request):
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if fname or lname or username or password or email is "":
            return ""

    def get(self, request):
        form = UserForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, 'signup.html',context)

    def post(self, request):

        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
        context = {
            "form": form,
        }

        return render(request, 'signup.html',context=context)


class Dashboard(View):
    def get(self, request, username):
        items = []

        acc = get_insta_account(request.user,username)
        db_obj = get_target_functionalities(request.user,acc.instagram_username)

        bot = Apollo(login=acc.instagram_username, password=acc.instagram_password)
        user = bot.get_user_info(username)
        print("Nishaf")
        print(db_obj.count())
        if db_obj.count() > 0:
            for i in db_obj:
                item = get_all_cards_info(i,bot)
                items.append(item)

        unfollow_status = get_unfollow_status(request.user, acc.instagram_username)
        return render(request,'dashboard.html', {'items':items,'user':user, 'status':acc.instagram_account_status,
                        'unfollow': unfollow_status})


class InstagramFunctions(View):
    def get(self, request):
        print('sahsidhsd')
        print('In Instagram Functions')
        print(request.GET['button_clicked'])
        username = request.GET['username']
        input_user = request.GET['input']

        django.db.close_old_connections()
        db_obj = InstagramAccounts.objects.filter(username=request.user, instagram_username=username)[0]
        if request.GET['button_clicked'] == 'username_submit':
            print('Username Clicked!')
            bot = Apollo(login=db_obj.instagram_username, password=db_obj.instagram_password)
            user = bot.get_user_info(input_user)
            bot.logout()
            link_id =input_user+ "_" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(username)
            follows = user['followed_by']['count']
            following = user['follows']['count']

            p = Process(target=main, kwargs={'target_username': input_user, 'username': db_obj.instagram_username,
                                             'password': db_obj.instagram_password, 'pause_follow': False,'account_user':request.user,
                                             'max_follows_per_hour': 1000,'link_id':link_id})  # )})int(request.GET['max_follows_per_hour'])
            print(os.getpid())
            p.start()
            pid = p.pid
            print(pid)

            save_target_username_functionality(request.user,db_obj.instagram_username,pid,input_user,link_id,follows,following)

            print(follows,following)
            user = {
                'follow':follows,
                'following': following,
                'input_username': input_user,
                'username': username,
                'pid': pid,
                'link_id': link_id,
                'pause_link': '/pause/',
                'delete_link': '/delete/',
                'likes_play_link': '/like_play/'

            }
            return JsonResponse({'user':user})


        elif request.GET['button_clicked'] == 'tags_submit':
            print('In tags_submit.')
            print(input_user)
            link_id = input_user + "_" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            p = Process(target=main, kwargs={'target_type':'tag','link_id':link_id,'account_user':request.user,'target_tag': input_user, 'username': db_obj.instagram_username,
                                              'max_follows_per_hour': 1000,'password': db_obj.instagram_password, 'pause_follow': False}) #int(request.GET['max_follows_per_hour'])
            print(os.getpid())
            p.start()
            pid = p.pid
            print(pid)

            save_target_tag_functionality(request.user,db_obj.instagram_username,pid,input_user,link_id)
            while True:

                item = get_target_tag_functionality(request.user,db_obj.instagram_username,link_id,input_user)
                if item.following_mediaids == '0' and item.followers_usernameids == '0':
                    print("Empty Field")
                    sleep(10)
                    continue
                else:
                    print("DATA FOUND!!!")
                    print(item.followers_usernameids)
                    print(item.following_mediaids)
                    break

            print(username)
            user = {
                'following': item.following_mediaids,
                'follow': item.followers_usernameids,
                'input_tag': input_user,
                'username': username,
                'pid': pid,
                'link_id': link_id,
                'pause_link': '/pause/',
                'delete_link': '/delete/',
                'likes_play_link': '/like_play/'

            }

            return JsonResponse({'user': user})



class PauseLikesFunctionality(View):
    def get(self, request):
        update_likes_functionality(request.user,request.GET['username'],request.GET['link_id'],True,'paused')
        return JsonResponse({'res': 'not liking', 'url': "/like_play/"})


class PlayLikesFunctionality(View):
    def get(self, request):
        update_likes_functionality(request.user,request.GET['username'],request.GET['link_id'],False,'active')
        return JsonResponse({'res': 'liking', 'url': "/like_pause/"})

class PauseFunctionality(View):
    def get(self, request):
        update_target_functionality(request.user,request.GET['username'],request.GET['link_id'],True,'pause')
        return JsonResponse({'res':'paused','url': "/play/"})


class PlayFunctionality(View):
    def get(self, request):
        update_target_functionality(request.user, request.GET['username'], request.GET['link_id'], False, 'active')
        return JsonResponse({'res':'played','url': "/pause/"})

class DeleteFunctionality(View):
    def get(self,request):
        delete_target_functionality(request.user,request.GET['username'],
                                               request.GET['link_id'],request.GET['pid'])
        return JsonResponse({'json_response':'Deleted'})


class MessageFunctionality(View):
    def get(self,request):
        messages = request.GET['messages']
        messages = json.loads(messages)
        hyperlinks = request.GET['hyperlinks']
        hyperlinks = json.loads(hyperlinks)
        messages_list = get_message_list(messages,hyperlinks)

        for i in messages_list:
            print(i)

        insta_user = request.GET['insta_username']
        print(insta_user)

        django.db.close_old_connections()
        db_obj = InstagramAccounts.objects.filter(username=request.user, instagram_username=insta_user)[0]

        link_id = insta_user +  "_"  + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


        p = Process(target=main, kwargs={'message_list': messages_list, 'username': db_obj.instagram_username,
                                         'password': db_obj.instagram_password, 'message_pause': False,
                                         'account_user': request.user,'max_messages': 30,
                                         'link_id': link_id.lower()})
        bot = Apollo(login=db_obj.instagram_username,password=db_obj.instagram_password)
        followers = bot.getFollowers()
        new_followers = bot.getNewFollowers(followers)
        print('New Followersss')
        print(new_followers)
        bot.logout()
        p.start()

        django.db.close_old_connections()
        MessageFunctionalityDB(username=request.user,instagram_username=insta_user,
                               message_id=link_id,message_pause=False,pid=p.pid).save()

        message_card = {
            'new_followers': len(new_followers),
            'messages_sent':'0',
            'pause_message':'/pause_message/',
            'delete_message':'/delete_message/',
            'insta_username':insta_user,
            'link_id': link_id,
        }

        return JsonResponse({'msg_card':message_card})

class PauseMessageFunctionality(View):
    def get(self, request):
        print(request.GET['link_id'])
        msgid = request.GET['link_id']

        django.db.close_old_connections()
        MessageFunctionalityDB.objects.filter(username=request.user,
                                                instagram_username=request.GET['insta_username'],
                                                message_id=msgid).update(status='pause',message_pause=True)
        print('Paused')
        return JsonResponse({'res':'paused','url': "/play_message/"})


class PlayMessageFunctionality(View):
    def get(self, request):
        print(request.GET['link_id'])

        django.db.close_old_connections()
        MessageFunctionalityDB.objects.filter(username=request.user,
                                                instagram_username=request.GET['insta_username'],
                                                message_id=request.GET['link_id']).update(status='active',message_pause=False)
        print('Played')
        return JsonResponse({'res':'played','url': "/pause_message/"})

class DeleteMessageFunctionality(View):
    def get(self,request):
        django.db.close_old_connections()
        db_obj = MessageFunctionalityDB.objects.filter(username=request.user,
                                                instagram_username=request.GET['insta_username'],
                                                message_id=request.GET['link_id'])[0]
        os.system('kill -9 ' + db_obj.pid)  ####   PID OF PROCESS, FOR DELETION OF DATA
        db_obj.delete()
        print('Deleted')
        return JsonResponse({'json_response':'Deleted'})

class Unfollow(View):
    def get(self,request):

        insta_user = request.GET['insta_username']
        if request.GET['checked'] == 'True':
            print('Checked')

            django.db.close_old_connections()
            db_obj = InstagramAccounts.objects.filter(username=request.user, instagram_username=insta_user)[0]

            p = Process(target=main, kwargs={'username': db_obj.instagram_username,'account_user':db_obj.username,
                                             'password': db_obj.instagram_password,'cleanup':True})
            p.start()

            django.db.close_old_connections()
            InstagramUnfollowDB(username=request.user,instagram_username=insta_user,cleanup=True,pid=p.pid).save()
            return JsonResponse({'res':'unfollowing'})
        elif request.GET['checked'] == 'False':
            print('Unchecked')
            db_obj = InstagramUnfollowDB.objects.filter(username=request.user,instagram_username=insta_user)[0]
            os.system('kill -9 ' + db_obj.pid)  ####   PID OF PROCESS, FOR DELETION OF DATA
            db_obj.delete()
            return JsonResponse({'res':'unfollow stopped'})


'''
        #username = request.POST['username']
        #password = request.POST['password']
        #first_name = request.POST['fname']
        #last_name = request.POST['lname']
        #email = request.POST['email']
        print(username,password,email,first_name,last_name)
        userr = Userform()
        user = userr.save(commit=False)
        user.username = request.POST['username']
        user.password = request.POST['password']
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.save()
        #User(username=username,password=password,email=email,first_name=first_name,last_name=last_name).save()
        #sleep(2)
        print(user.username,user.password)
        user = authenticate(username=user.username, password=user.password)
        if user is not None:
            print('not none')
            if user.is_active:
                login(request, user)
                return redirect('index')
        '''

'''
       print(request.user)
       print(request.GET['username'])
       db_obj = InstagramAccounts.objects.filter(username=request.user,
                                                 instagram_username=request.GET['username'])[0]
       print(request.GET['link_id'])
       item = TargetFunctionalityDB.objects.filter(link_id=request.GET['link_id'], username=request.user,
                                                       instagram_username=request.GET['username'])[0]
       if item.target == 'tag':
           p = Process(target=main,
                       kwargs={'target_type': 'tag', 'link_id': item.link_id, 'account_user': request.user,
                               'target_tag': item.target_value, 'username': db_obj.instagram_username,
                               'password': db_obj.instagram_password, 'pause_follow': False})
       else:
           p = Process(target=main,
                       kwargs={'target_username': request.GET['input_username'],'username': db_obj.instagram_username, 'password': db_obj.instagram_password,
                               'pause_follow': False})

       item.status = 'active'
       item.save()
       p.start()
       pid = p.pid
       '''



"""

function
spinner()
{
    var
username = $("#account_username").val();
var
password = $("#account_password").val();

alert(username);
$.ajax({
    url: "{% url 'home' %}",
    type: "GET",
    data: {
        'username': username,
        'password': password
    },
    contentType: "application/json;charset=utf-8",
    dataType: "json",
    success: function(data) {
    document.getElementById("modal-body").innerHTML = 'nishaf';
f1();
}
});
}
"""