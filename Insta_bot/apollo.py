import json
import time
import datetime
import requests
import random
from Insta_bot.InstagramAPI.InstagramAPI import InstagramAPI

class Apollo:

    url = 'https://www.instagram.com/'
    url_likers = 'https://i.instagram.com/api/v1/media/%s/likers/?'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    media_on_feed = []
    likers_on_media = []
        
    def __init__(self, login, password):
        self.users_found = 0
        self.login_status = False
        self.user_login = login.lower()
        self.user_password = password
        self.s = requests.Session()
        self.media_on_feed = []
        self.likers_on_media = []
        self.like_counter = 0
        self.follow_counter = 0
        self.unfollow_counter = 0
        self.new_follower_count = 0
        self.message_counter = 0
        self.api = InstagramAPI(self.user_login, self.user_password)
        self.login()
        now_time = datetime.datetime.now()
        self.bot_start = now_time
        log_string = 'Apollo v0.7 started at %s:\n' % \
                (now_time.strftime("%d.%m.%Y %H:%M"))
        self.write_log(log_string)

    def getFollowCounter(self):
        value = self.follow_counter
        return value

    def getUnfollowCounter(self):
        value = self.unfollow_counter
        return value

    def login(self):
        self.api.login()
        log_string = '\nTrying to login as %s...\n' % (self.user_login)
        self.write_log(log_string)
        self.s.cookies.update({
            'sessionid': '',
            'mid': '',
            'ig_pr': '1',
            'ig_vw': '1920',
            'csrftoken': '',
            's_network': '',
            'ds_user_id': ''
        })
        self.login_post = {
            'username': self.user_login,
            'password': self.user_password
        }
        self.s.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': self.accept_language,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(
            self.url_login, data=self.login_post, allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())
        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                self.login_status = True
                log_string = '%s login success!\n' % (self.user_login)
                self.write_log(log_string)
            else:
                self.login_status = False
                self.write_log('Login error! Check your login data!\n')
        else:
            self.write_log('Login error! Connection error!\n')

    def logout(self):
        self.api.logout()
        now_time = datetime.datetime.now()
        log_string = 'Start time: %s Logout: likes - %i, follow - %i, unfollow - %i. followbacks: %i ' % \
                     (self.bot_start, self.like_counter, self.follow_counter,
                      self.unfollow_counter, self.new_follower_count)
        self.write_log(log_string)
        work_time = datetime.datetime.now() - self.bot_start
        log_time = 'Bot work time: %s' % (work_time) + "\n"
        self.write_log(log_time)

        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            self.write_log("Logout success!")
            self.login_status = False
        except:
            self.write_log("Logout error!")

        return log_string + log_time
    def getdata(self):
        s = requests.Session()


    def get_user_info(self, username):
        s = requests.Session()
        try:
            r = s.get(self.url_user_detail % (username))
            data = json.loads(r.text)
            user = data["user"]
            return user
        except:
            pass

    def get_id_by_username(self, username):
        s = requests.Session()
        try:
            r = s.get(self.url_user_detail % (username))
            data = json.loads(r.text)
            user_id = data["user"]["id"]
            return user_id
        except:
            pass

    def get_media_id_by_tag(self, tag):
        s = requests.Session()
        tag_ids = []
        if self.login_status == 1:
            url_tag = self.url_tag % (tag)
            try:
                r = s.get(url_tag)
                all_data = json.loads(r.text)
                tag_media = list(all_data['tag']['media']['nodes'])
                for i in tag_media:
                    tag_ids.append(i["id"])
            except Exception as e:
                self.write_log("Except on get_media!: %s\n"%(e))
            return tag_ids

    def get_user_feed(self, username):
        s = requests.Session()
        user_feed_ids = []
        try:
            r = s.get(self.url_user_detail % (username))
            data = json.loads(r.text)
            user_feed = list(data['user']['media']['nodes'])
            for i in user_feed[:10]:
                user_feed_ids.append(i["id"])
        except Exception as e:
            pass
        return user_feed_ids

    def get_media_likers(self, media_ids):
        s = requests.Session()
        liker_info = []
        if self.login_status:
            print("Get Media Likers")
            for media_id in media_ids:
                try:

                    print("Get Media Likers Loop")
                    r = s.get(self.url_likers % media_id)
                    like_data = json.loads(r.text)
                    likers = list(like_data["users"])
                    for liker in likers:
                        tup = (liker["username"], liker["pk"])
                        if tup not in liker_info:
                            liker_info.append(tup)
                            print(tup)
                            self.users_found += 1
                except Exception as e:
                    pass
                time.sleep(0.2)
        return liker_info

    def like(self, media_id):
        """ Send http request to like media by ID """
        if self.login_status:
            url = self.url_likes % (media_id)
            try:
                like = self.s.post(url)
                if like.status_code == 200:
                    self.like_counter += 1
                    return True
                else:
                    return False
            except:
                self.write_log("Except on like!\n")
                return False
        else:
            self.write_log("problem liking post\n")
            return False

    def follow(self, user_id):
        """ Send http request to follow """
        if self.login_status:
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    self.follow_counter += 1
                    return True
            except:
                return False
        return False

    def unfollow(self, user_id):
        """ Send http request to unfollow """
        if self.login_status:
            url = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    return True
                else:
                    return False
            except:
                return False
        return False

    def is_user_following(self, username):
        follow_status = True
        if self.login_status:
            url = self.url_user_detail % (username)
            try:
                r = self.s.get(url)
                if r.status_code == 200:
                    all_data = json.loads(r.text)
                    follow_status = all_data["user"]["follows_viewer"]
            except:
                follow_status = True
        else:
            follow_status = True
        return follow_status

    def is_user_followed(self, username):
        follow_status = True
        if self.login_status:
            url = self.url_user_detail % (username)
            try:
                r = self.s.get(url)
                if r.status_code == 200:
                    all_data = json.loads(r.text)
                    follow_status = all_data["user"]["followed_by_viewer"]
            except:
                follow_status = True
        else:
            follow_status = True
        return follow_status

    def getNewFollowers(self, followers):
        follower_info = []
        data = []
        new_followers = []

        self.api.getSelfUserFollowers()
        data.extend(self.api.LastJson['users'])
        for i in data:
            user_info = (i["username"], i["pk"])
            follower_info.append(user_info)
        for user in follower_info:
            if user not in followers:
                self.new_follower_count+=1
                new_followers.append(user)
        return new_followers

    def getFollowers(self):
        followers = []
        follower_list = self.api.getTotalSelfFollowers()
        for user in follower_list:
            user_info = (user["username"], user["pk"])
            followers.append(user_info)
        return followers

    def getFollowed(self):
        followed = []
        followed_list = self.api.getTotalSelfFollowings()
        for user in followed_list:
            user_info = (user["username"], user["pk"])
            followed.append(user_info)
        return followed

    def messageUser(self, user, message_text, link=False):
        if link:
            try:
                if self.api.sendLink(str(user[1]), message_text, link):
                    self.message_counter+=1
                    return True
            except Exception as e:
                self.write_log("Could not send message: %s\n"%(e))
        else:
            try:
                if self.api.sendMessage(str(user[1]), message_text):
                    self.message_counter+=1
                    return True
            except Exception as e:
                self.write_log("Could not send message: %s\n"%(e))
        return False

    def update_output(self):
        self.write_log("%s session: Followed: %i Liked: %i Unfollowed: %i Followbacks: %i Messaged: %i"%(self.user_login, self.follow_counter, self.like_counter, self.unfollow_counter, self.new_follower_count, self.message_counter))

    def write_log(self, log_text):
        try:
            print("", end='')
            print('\r'+log_text, end='')
        except UnicodeEncodeError:
            print("Your text has a unicode problem!")

