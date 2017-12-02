from Insta_Web.models import AccountDetails,TargetFunctionalityDB,MessageFunctionalityDB


def save_tag_details(account_user,username,link_id,feed_ids,likers):
    item = TargetFunctionalityDB.objects.filter(username=account_user,instagram_username=username,link_id=link_id)[0]
    print("Username: " + item.username)
    item.following_mediaids = len(feed_ids)
    item.followers_usernameids = len((likers))
    item.save()


def update_message_details(username,insta_user, message_id):
    db_obj = MessageFunctionalityDB.objects.filter(username=username,instagram_username=insta_user,message_id=message_id)[0]
    db_obj.messages_sent += 1
    db_obj.save()

    db_obj = AccountDetails.objects.filter(username=username,instagram_username=insta_user)[0]
    db_obj.messages_sent += 1
    db_obj.save()

def update_follow_details(username,insta_user):
    db_obj = AccountDetails.objects.filter(username=username,instagram_username=insta_user)[0]
    db_obj.following += 1
    db_obj.save()

def update_likes_details(username,insta_user):
    db_obj = AccountDetails.objects.filter(username=username,instagram_username=insta_user)[0]
    db_obj.likes += 1
    db_obj.save()


def paused_liking(account_user,username,link_id):
    try:
        db_obj = TargetFunctionalityDB.objects.filter(username=account_user,instagram_username=username,link_id=link_id)[0]
        pause_like = True if 'True' in db_obj.pause_like else False
        return pause_like
    except:
        return True

def paused_following(pause,account_user,username,link_id):
    try:
        db_obj = TargetFunctionalityDB.objects.filter(username=account_user, instagram_username=username,link_id=link_id)[0]
        print("###########################################################")
        print(db_obj.pause_follow)
        pause_follow = True if 'True' in db_obj.pause_follow else False
        return pause_follow
    except:
        return True


