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


class HomePage(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'landing.html')
        else:
            print(request.user)
            db_obj = InstagramAccounts.objects.filter(username=request.user)
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
        db_obj = InstagramAccounts.objects.filter(username=request.user,instagram_username=username)
        if db_obj.count() == 0:
            bot = Apollo(login=username, password=password)
            if not bot.login_status:
                print('Credentials not correct')
                return JsonResponse({'res': 'Invalid Username or Password!'})
            else:
                user = bot.get_user_info(username)
                print(user['profile_pic_url_hd'])
                bot.logout()
                a = InstagramAccounts(username=request.user,instagram_username=username,instagram_password=password,
                                      instagram_image=user['profile_pic_url_hd'], instagram_account_status='active', paid_date='09-11-2017')
                a.save()
                AccountDetails(username=request.user,instagram_username=username).save()
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
        acc = InstagramAccounts.objects.filter(username=request.user, instagram_username=username)[0]
        db_obj = TargetFunctionalityDB.objects.filter(username=request.user,
                                                        instagram_username=acc.instagram_username)
        bot = Apollo(login=acc.instagram_username, password=acc.instagram_password)
        user = bot.get_user_info(username)

        print("Nishaf")
        print(db_obj.count())
        if db_obj.count() > 0:
            for i in db_obj:
                if i.target == 'username':
                    print(user)
                    print(i.target_value)
                    info = bot.get_user_info(i.target_value)
                    bot.logout()

                    if i.status == 'active':
                        #link = "pause_target_functionality('"+ i.link_id + "','/pause/','" +  i.instagram_username + "','" + i.target_value +"');"
                        link = "pause_target_functionality('"+ i.link_id + "','/pause/','" +  i.instagram_username + "','" + i.target_value +"');"

                    else:
                        link = "start_target_functionality('"+ i.link_id + "','/play/','" +  i.instagram_username + "','" + i.target_value+"');"

                    if i.pause_like == False:
                        link = "pause_likes_functionality('likes_check_"+ i.link_id  + "','" + i.link_id + "','/like_pause/','" +  i.instagram_username + "','" + i.target_value+"');"

                    else:
                        link = "start_likes_functionality('likes_check_"+ i.link_id  + "','" + i.link_id + "','/like_play/','" +  i.instagram_username + "','" + i.target_value+"');"


                    delete_link = "delete_target_functionality('"+ i.link_id + "','/delete/','" + i.instagram_username + "','" + i.pid +"');"
                    follows = info['followed_by']['count']
                    following = info['follows']['count']
                    print(follows,following)
                    TargetFunctionalityDB.objects.filter(username=i.username,instagram_username=i.instagram_username,
                                                           pid=i.pid,link_id=i.link_id).update(followers_usernameids=follows,following_mediaids=following)
                    items.append({
                        'username':i.username,
                        'instagram_username':i.instagram_username,
                        'target_value':i.target_value,
                        'target': i.target,
                        'pid': i.pid,
                        'follow': follows,
                        'following': following,
                        'play_pause_link': link,
                        'delete_link': delete_link,
                        'link_id': i.link_id,
                        'status': i.status,
                        'pause_like': i.pause_like,
                    })

                elif i.target == 'tag':
                    print(i.target_value)
                    if i.status == 'active':
                        link = "pause_target_functionality('" + i.link_id + "','/pause/','" + i.instagram_username + "','" + i.target_value + "','" + i.pid + "');"
                    else:
                        link = "start_target_functionality('" + i.link_id + "','/play/','" + i.instagram_username + "','" + i.target_value + "');"

                    delete_link = "delete_target_functionality('" + i.link_id + "','/delete/','" + i.instagram_username + "','" + i.pid + "');"


                    items.append({
                        'username': i.username,
                        'instagram_username': i.instagram_username,
                        'target_value': i.target_value,
                        'following': i.following_mediaids,
                        'follow': i.followers_usernameids,
                        'target': i.target,
                        'pid': i.pid,
                        'play_pause_link': link,
                        'delete_link': delete_link,
                        'link_id': i.link_id,
                        'status': i.status
                    })

        ##Call Following Function.
        for i in items:
            print(i['username'])
            print(i['status'])

        return render(request,'dashboard.html')#, {'items':items,'user':user, 'status':acc.instagram_account_status})


class InstagramFunctions(View):
    def get(self, request):
        print('sahsidhsd')
        print('In Instagram Functions')
        print(request.GET['button_clicked'])
        username = request.GET['username']
        input_user = request.GET['input']
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
                                             'max_follows_per_hour': int(request.GET['max_follows_per_hour']),'link_id':link_id})  # )})
            print(os.getpid())
            p.start()
            pid = p.pid
            print(pid)

            TargetFunctionalityDB(username=request.user, instagram_username=db_obj.instagram_username,
                                    pid=pid, target_value=input_user, target='username', status='active',
                                    link_id=link_id,
                                    followers_usernameids=follows, following_mediaids=following, pause_follow=False,
                                    pause_like=True).save()

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
                                              'max_follows_per_hour': int(request.GET['max_follows_per_hour']),'password': db_obj.instagram_password, 'pause_follow': False})
            print(os.getpid())
            p.start()
            pid = p.pid
            print(pid)

            TargetFunctionalityDB(username=request.user, instagram_username=db_obj.instagram_username,
                                    pid=pid, target='tag',target_value=input_user, status='active', link_id=link_id,
                                    pause_like=True,pause_follow=False).save()

            while True:
                item = TargetFunctionalityDB.objects.filter(username=request.user, instagram_username=db_obj.instagram_username,
                                               link_id=link_id,target_value=input_user)[0]
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
        TargetFunctionalityDB.objects.filter(link_id=request.GET['link_id'],
                                                      username=request.user,
                                                      instagram_username=request.GET['username']).update(pause_like=True, status='active')

        return JsonResponse({'res': 'not liking', 'url': "/like_play/"})


class PlayLikesFunctionality(View):
    def get(self, request):
        TargetFunctionalityDB.objects.filter(link_id=request.GET['link_id'],
                                                      username=request.user,
                                                      instagram_username=request.GET['username']).update(pause_like=False, status='active')

        return JsonResponse({'res': 'liking', 'url': "/like_pause/"})

class PauseFunctionality(View):
    def get(self, request):

        TargetFunctionalityDB.objects.filter(username=request.user,
                                                instagram_username=request.GET['username'],
                                                target_value=request.GET['input_username'],
                                                link_id=request.GET['link_id']).update(status='pause',pause_follow=True,pause_like=True)



        return JsonResponse({'res':'paused','url': "/play/"})


class PlayFunctionality(View):
    def get(self, request):

        TargetFunctionalityDB.objects.filter(link_id=request.GET['link_id'], username=request.user,
                                               instagram_username=request.GET['username']).update(pause_follow=False,pause_like=True,status='active')

        return JsonResponse({'res':'played','url': "/pause/"})

class DeleteFunctionality(View):
    def get(self,request):

        os.system('kill -9 ' + request.GET['pid'])  ####   PID OF PROCESS, FOR DELETION OF DATA
        db_obj = TargetFunctionalityDB.objects.filter(username=request.user,instagram_username=request.GET['username'],
                                               link_id=request.GET['link_id'], pid=request.GET['pid'])[0]
        db_obj.delete()
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
        MessageFunctionalityDB.objects.filter(username=request.user,
                                                instagram_username=request.GET['insta_username'],
                                                message_id=msgid).update(status='pause',message_pause=True)
        print('Paused')
        return JsonResponse({'res':'paused','url': "/play_message/"})


class PlayMessageFunctionality(View):
    def get(self, request):
        print(request.GET['link_id'])
        MessageFunctionalityDB.objects.filter(username=request.user,
                                                instagram_username=request.GET['insta_username'],
                                                message_id=request.GET['link_id']).update(status='active',message_pause=False)
        print('Played')
        return JsonResponse({'res':'played','url': "/pause_message/"})

class DeleteMessageFunctionality(View):
    def get(self,request):
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
            db_obj = InstagramAccounts.objects.filter(username=request.user, instagram_username=insta_user)[0]

            p = Process(target=main, kwargs={'username': db_obj.instagram_username,
                                             'password': db_obj.instagram_password,'cleanup':False})
            p.start()
            InstagramUnfollowDB(username=request.user,instagram_username=insta_user,cleanup_pause=False,pid=p.pid).save()

        elif request.GET['checked'] == 'False':
            print('Unchecked')
            db_obj = InstagramUnfollowDB(username=request.user,instagram_username=insta_user)
            os.system('kill -9 ' + db_obj.pid)  ####   PID OF PROCESS, FOR DELETION OF DATA
            db_obj.delete()


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