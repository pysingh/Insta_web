from Insta_Web.models import *
import django.db,os

def get_all_instagram_accounts(request):
    django.db.close_old_connections()
    return InstagramAccounts.objects.filter(username=request.user)

def get_insta_account(acc_username,insta_username):
    django.db.close_old_connections()
    return InstagramAccounts.objects.filter(username=acc_username, instagram_username=insta_username)

def save_user_details_in_database(acc_username,insta_username,insta_password,image):
    django.db.close_old_connections()
    a = InstagramAccounts(username=acc_username, instagram_username=insta_username, instagram_password=insta_password,
                          instagram_image=image, instagram_account_status='active',
                          paid_date='09-11-2017')
    a.save()
    AccountDetails(username=acc_username, instagram_username=insta_username).save()


def get_target_functionalities(acc_username,insta_username):
    django.db.close_old_connections()
    return TargetFunctionalityDB.objects.filter(username=acc_username,
                                                  instagram_username=insta_username)


def get_unfollow_status(acc_username,insta_username):
    try:
        django.db.close_old_connections()
        return (InstagramUnfollowDB.objects.filter(username=acc_username, instagram_username=insta_username)[0]).cleanup
    except:
        return False

def update_target_functionalities(i,follows,following):
    django.db.close_old_connections()
    TargetFunctionalityDB.objects.filter(username=i.username, instagram_username=i.instagram_username,
                                         pid=i.pid, link_id=i.link_id).update(followers_usernameids=follows,
                                                                              following_mediaids=following)

def save_target_username_functionality(acc_username,insta_username,pid,input_user,link_id,follows,following):
    django.db.close_old_connections()
    TargetFunctionalityDB(username=acc_username, instagram_username=insta_username,
                          pid=pid, target_value=input_user, target='username', status='active',
                          link_id=link_id,
                          followers_usernameids=follows, following_mediaids=following, pause_follow=False,
                          pause_like=True).save()


def save_target_tag_functionality(acc_username, insta_username, pid, input_user, link_id):
    django.db.close_old_connections()
    TargetFunctionalityDB(username=acc_username, instagram_username=insta_username,
                          pid=pid, target='tag', target_value=input_user, status='active', link_id=link_id,
                          pause_like=True, pause_follow=False).save()


def update_likes_functionality(acc_username,insta_username,link_id,pause_like,status):
    django.db.close_old_connections()
    TargetFunctionalityDB.objects.filter(link_id=link_id,
                                         username=acc_username,
                                         instagram_username=insta_username).update(pause_like=pause_like,
                                                                                            status=status)

def update_target_functionality(acc_username,insta_username,link_id,pause_follow,status):
    django.db.close_old_connections()
    TargetFunctionalityDB.objects.filter(username=acc_username,
                                         instagram_username=insta_username,
                                         link_id=link_id).update(status=status, pause_follow=pause_follow)


def delete_target_functionality(acc_username,insta_username,link_id,pid):
    django.db.close_old_connections()
    os.system('kill -9 ' + pid)  ####   PID OF PROCESS, FOR DELETION OF DATA
    db_obj = TargetFunctionalityDB.objects.filter(username=acc_username, instagram_username=insta_username,
                                                  link_id=link_id, pid=pid)[0]
    db_obj.delete()

def get_target_tag_functionality(acc_username,insta_username,link_id,input_user):
    django.db.close_old_connections()
    return TargetFunctionalityDB.objects.filter(username=acc_username, instagram_username=insta_username,
                                                link_id=link_id, target_value=input_user)[0]

def save_tag_details(account_user,username,link_id,feed_ids,likers):
    django.db.close_old_connections()
    item = TargetFunctionalityDB.objects.filter(username=account_user,instagram_username=username,link_id=link_id)[0]
    print("Username: " + item.username)
    item.following_mediaids = len(feed_ids)
    item.followers_usernameids = len((likers))
    item.save()


def update_message_details(username,insta_user, message_id):
    django.db.close_old_connections()
    db_obj = MessageFunctionalityDB.objects.filter(username=username,instagram_username=insta_user,message_id=message_id)[0]
    db_obj.messages_sent += 1
    db_obj.save()

    django.db.close_old_connections()
    db_obj = AccountDetails.objects.filter(username=username,instagram_username=insta_user)[0]
    db_obj.messages_sent += 1
    db_obj.save()

def update_follow_details(username,insta_user):
    django.db.close_old_connections()
    db_obj = AccountDetails.objects.filter(username=username,instagram_username=insta_user)[0]
    db_obj.following += 1
    db_obj.save()

def update_likes_details(username,insta_user):
    django.db.close_old_connections()
    db_obj = AccountDetails.objects.filter(username=username,instagram_username=insta_user)[0]
    db_obj.likes += 1
    db_obj.save()


def paused_liking(account_user,username,link_id):
    try:
        django.db.close_old_connections()
        db_obj = TargetFunctionalityDB.objects.filter(username=account_user,instagram_username=username,link_id=link_id)[0]
        pause_like = True if 'True' in db_obj.pause_like else False
        return pause_like
    except:
        return True

def paused_following(pause,account_user,username,link_id):
    try:
        django.db.close_old_connections()
        db_obj = TargetFunctionalityDB.objects.filter(username=account_user, instagram_username=username,link_id=link_id)[0]
        pause_follow = True if 'True' in db_obj.pause_follow else False
        print('Pause Follow')
        print(pause_follow)
        return pause_follow
    except:
        return True


def update_unfollowed(acc_username,insta_username):
    django.db.close_old_connections()
    db_obj = InstagramUnfollowDB.objects.filter(username=acc_username,instagram_username=insta_username)[0]
    db_obj.unfollow_count += 1
    db_obj.save()
    django.db.close_old_connections()
    db_obj = AccountDetails.objects.filter(username=acc_username, instagram_username=insta_username)[0]
    db_obj.unfollow_count += 1
    db_obj.save()
    print('unfollowed')


def check_paused_message(acc_username,insta_username,link_id):
    #try:
        django.db.close_old_connections()
        db_obj = MessageFunctionalityDB.objects.filter(username=acc_username,instagram_username=insta_username,message_id=link_id)[0]
        pause_message = True if 'True' in db_obj.message_pause else False
        return pause_message
    #except:
    #    return True