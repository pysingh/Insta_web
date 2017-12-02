import os
import sys
import atexit
import threading
import time
import random
import json
import pickle
import datetime
from Insta_bot.apollo import Apollo
from Insta_Web.database import *
global likers

def main(target_type='',target_username='',target_tag=None,username='', password='', max_follows=1000, max_follows_per_hour=30,
         max_likes_per_hour=1000, max_messages=20,message_list = None,
         pause_like=True, pause_follow=True, message_pause=True, cleanup=False,link_id='',account_user=''):
    global likers
    # Initialize variables
    usernames = []
    tags = [target_tag] if target_tag is not None else []
    feed_ids = []
    likers = []
    followed = []
    messaged = []
    bot_follows = []
    followers = []
    blacklist = []
    liked_media = []
    liker_usernames = []
    cleanup_timer = time.time()
    hour_timer = time.time()
    message_timer = time.time()

    usernames = [target_username]

    username = username
    password = password
    follow_timer = time.time() + (random.randint(-1 * 60, 1 * 60)) + (3600 / max_follows_per_hour)
    like_timer = time.time() + (random.randint(-1 * 60, 1 * 60)) + (3600 / max_likes_per_hour)
    max_likes = max_likes_per_hour
    max_follows = max_follows
    max_follows_per_hour = max_follows_per_hour
    max_messages = max_messages
    message_counter = 0
    # message_string = config["message"]

    # Load data files
    #try:
        #with open("usernames.txt", "r") as name_file:
        #    for line in name_file:
        #        usernames.append(line.strip())
    #except:
        #with open("usernames.txt", "w") as name_file:
         #   print("Created file: usernames.txt\n")
    #try:
    #    with open("blacklist.txt", "r") as blacklist_file:
    #        for line in blacklist_file:
    #            blacklist.append(line.strip())
    #except:
    #    with open("blacklist.txt", "w") as blacklist_file:
    #        print("Created file: blacklist.txt\n")
    #try:
    #    with open("tags.txt", "r") as tag_file:
    #        for line in tag_file:
    #            print(line.strip())
    #            tags.append(line.strip())
    #except:
    #    with open("tags.txt", "w") as tag_file:
    #        print("Created file: tags.txt\n")

    #try:
    #    with open("liked_media.txt", "r") as liked_file:
    #        for line in liked_file:
    #            liked_media.append(int(line.strip()))
    #except:
    #    with open("liked_media.txt", "w") as liked_file:
    #        print("Created file: liked_media.txt\n")

    #try:
    #    with open("messaged.txt", "r") as messaged_file:
    #        for line in messaged_file:
    #            messaged.append(line.strip())
    #except:
    #    with open("messaged.txt", "w") as messaged_file:
    #        print("Created file: messaged.txt")

    # Initialize and Login to Bot
    bot = Apollo(login=username, password=password)
    while not bot.login_status:
        bot.write_log("Error with config file. Please update config.json\n")
        bot = Apollo(login=username, password=password)

    bot.write_log("Loading users from usernames.txt: %s\n" % (usernames))
    atexit.register(finish, bot=bot)

    try:
        bot_follows = pickle.load(open("followed.dump", "rb"))
    except:
        pass

    try:
        day_timer = pickle.load(open("timers.dump", "rb"))
    except:
        day_timer = time.time()

    try:
        bot.write_log("Getting Followed...\n")
        followed = bot.getFollowed()
        bot.write_log("Retrieved Followed: %i\n" % (len(followed)))
    except Exception as e:
        bot.write_log("Could not get Followed: %s\n" % (e))

    try:
        bot.write_log("Getting Followers...\n")
        followers = bot.getFollowers()
        bot.write_log("Retrieved Followers: %i\n" % (len(followers)))
    except Exception as e:
        bot.write_log("Could not get Followers: %s\n" % (e))
    bot.write_log("Users followed by bot: %i\n" % (len(bot_follows)))
    non_follows = [user for user in followed if user not in followers]
    bot.write_log("Users that do not follow back: %i\n" % (len(non_follows)))

    getMenu()
    #print(bot.get_user_feed(username))
    #print(bot.get_user_info(target_username))
    """Main Loop"""
    while True:
        # reset message count after one day
        if time.time() > day_timer:
            day_timer = get_timer(24 * 60 * 60)
            try:
                pickle.dump(day_timer, open("timers.dump", "wb"))
            except:
                pass
            message_counter = 0

        # Reset counters and get any new media/likers
        if time.time() > hour_timer:
            print('In Reset COunters')
            try:
                followers = bot.getFollowers()
            except:
                pass
            try:
                followed = bot.getFollowed()
            except:
                pass
            hour_timer = get_timer(3600)
            max_follow_counter = 0
            max_like_counter = 0
            feed_ids = get_target_media(bot, tags, usernames, feed_ids)
            print(feed_ids)
            likers = get_media_likers(bot, feed_ids, likers)
            print("Likers")
            print(likers)
            if target_type == 'tag':
                save_tag_details(account_user,username,link_id,feed_ids,likers)  ## Database.py


        # Unfollows 15 users at a time that do not follow you. starts with the ones the bot has followed
        if cleanup:
            print("Cleanup Working")
            if time.time() > cleanup_timer:
                cleanBotFollows(bot, bot_follows)
                #pickle.dump(bot_follows, open("followed.dump", "wb"))
                amount = 15
                count = 0
                cleanup_timer = get_timer(900)
                if amount > max_follows_per_hour - max_follow_counter:
                    amount = max_follows_per_hour - max_follow_counter
                if len(bot_follows) > 0:
                    try:
                        followed = bot.getFollowed()
                    except:
                        pass
                    if len(bot_follows) < amount:
                        amount = len(bot_follows)
                    for i in range(0, amount):
                        if cleanup_protocol(bot, bot_follows, blacklist):
                            max_follow_counter += 1
                    #pickle.dump(bot_follows, open("followed.dump", "wb"))
                else:
                    unfollow_list = [user for user in followed if user not in followers]
                    for i in range(0, amount):
                        if cleanup_protocol(bot, unfollow_list, blacklist):
                            max_follow_counter += 1
                #pickle.dump(bot_follows, open("followed.dump", "wb"))


        # db_obj = TargetFunctionalityDB.objects.filter(username=account_user, instagram_username=username,link_id=link_id)[0]
        # pause_follow = True if 'True' in db_obj.pause_follow else False
        # Follow loop
        # print(type(pause_follow))
        # print(pause_follow)
        # message new followers
        if time.time() > message_timer:
            print("In messaging")
            new_followers = []
            message_timer = get_timer(2 * 60)
            try:
                new_followers = bot.getNewFollowers(followers)
                print(new_followers)
                followers.extend(new_followers)
            except Exception as e:
                print('Except in Messaging')
                bot.write_log("\r%s\n" % (e))
                new_followers = []
            #print(followers)
            if len(new_followers) > 0 and not message_pause:
                print("Messaging new users")
                for user in followers:
                    bot.update_output()
                    message = message_list[random.randrange(len(message_list)-1)]
                    message_text,message_link = message['message'],message['hyperlink']
                    if message_text != "" and message_counter < max_messages and user[0] not in messaged:
                        if message_link != "":
                            if sendMessage(bot, messaged, user, message_text,message_link):
                                message_counter += 1
                                update_message_details(account_user,username,link_id)   ## Database.py
                        else:
                            if sendMessage(bot, messaged, user, message_text):
                                message_counter += 1
                                update_message_details(account_user, username,link_id)   ## Database.py

        ##Follow Loop
        print(time.time()>follow_timer)
        if  time.time() > follow_timer and paused_following(pause_follow,account_user,username,link_id) == False:  ## Database.py
            follow_timer = time.time() + (random.randint(-1 * 60, 1 * 60)) + (3600 / max_follows_per_hour)
            print('infollowing')
            if max_follow_counter < max_follows_per_hour:
                if follow_protocol(bot, followed, likers, blacklist, bot_follows):
                    update_follow_details(account_user,username)
                    max_follow_counter += 1
                    #pickle.dump(bot_follows, open("followed.dump", "wb"))
                    print("Bot Follows: " + str(len(bot_follows)))
                    print("Max Follows: " + str(max_follows))

                    if len(bot_follows) > max_follows:
                        unfollow_list = []
                        while bot.follow_counter > bot.unfollow_counter + max_follows:
                            print("Bot Follow Counter: " + str(bot.follow_counter))
                            if unfollow_protocol(bot, bot_follows, blacklist):
                                max_follow_counter += 1

                        #pickle.dump(bot_follows, open("followed.dump", "wb"))


        if time.time() > like_timer and not paused_liking(account_user,username,link_id):
            print("Liking")
            like_timer = time.time() + (random.randint(-1 * 60, 1 * 60)) + (3600 / max_likes_per_hour)
            if max_like_counter < max_likes:
                print('in if')
                if like_protocol(bot, liked_media, likers):
                    update_likes_details(account_user, username)
                max_like_counter += 1

        time.sleep(0.8)


def get_target_media(bot, tags, usernames, ids):
    added = 0
    for name in usernames:
        for i in bot.get_user_feed(name):
            if i not in ids:
                added += 1
                ids.append(i)
    #print(tags)
    for tag in tags:
        print("Media ID")
        for i in bot.get_media_id_by_tag(tag):
            if i not in ids:
                print(i)
                added += 1
                ids.append(i)

    return ids


def get_media_likers(bot, ids, likers):
    added = 0
    print("IDSSS")
    for i in bot.get_media_likers(ids):
        if i not in likers:
            added += 1
            print(i)
            likers.append(i)
    return likers


def get_timer(seconds):
    timer = time.time() + (seconds)
    return timer


def follow_protocol(bot, followed, users, blacklist, bot_follows):
    # Follow user from liker_ids if they have not been followed already
    print('Nishaf')
    userlist = []
    for i in users:
        userlist.append(i)

    #print(userlist)
    if len(userlist) > 0:
        user = userlist.pop(random.randint(0, len(userlist) - 1))
        while user in followed or user[0] in blacklist or bot.is_user_followed(user[0]):
            if len(userlist) > 0:
                randomnum = random.randint(0, len(userlist) - 1) if len(userlist) > 1 else 0
                user = userlist.pop(randomnum)

        try:
            if user not in followed and user[0] not in blacklist:
                if bot.follow(user[1]):                 ### IF Followed the user then here we can add that user in a list for managing users.
                    bot.update_output()
                    followed.append(user)
                    bot_follows.append(user)
                    return True
                else:
                    return False
        except Exception as e:
            bot.write_log(str(e))
            return False


def like_protocol(bot, liked_media, users):
    user_media = []

    media_likers = []
    for i in users:
        media_likers.append(i)

    # Find media that has not been liked yet
    if len(media_likers) > 0:
        while len(user_media) <= 0 or found_user == False:
            try:
                u = media_likers.pop(random.randint(0, len(media_likers) - 1))
                user_media = bot.get_user_feed(u[0])
                media = user_media[random.randint(0, 3)]
                while media in liked_media:
                    time.sleep(random.randint(2, 3))
                    u = media_likers.pop(random.randint(0, len(media_likers) - 1))
                    user_media = bot.get_user_feed(u[0])
                    media = user_media[random.randint(0, 3)]
                found_user = True
            except IndexError:
                found_user = False
        # Try to like one of the last three pictures from selected user
        try:
            if bot.like(media):
                bot.update_output()
                #with open("liked_media.txt", "a") as liked_file:
                #    liked_file.write(str(media) + '\n')
                liked_media.append(media)
                return True
        except Exception as e:
            bot.write_log("User: %s" % (u[0]) + " " + str(e) + "\n")

    return False


def sendMessage(bot, messaged, user, message, link=False):
    message_string = ""
    for text in message:
        message_string += text[random.randint(0, len(text) - 1)]

    print("Message is: " + message_string)
    if bot.messageUser(user, message_string, link):
        messaged.append(user[0])
        #with open("messaged.txt", "a") as messaged_file:
        #    messaged_file.write(user[0] + '\n')
        return True
    return False


def cleanup_protocol(bot, followed, blacklist):
    i = 1
    fails = 0
    found = False
    if len(followed) > 0:
        while not found and fails < 2:
            try:
                if not bot.is_user_following(followed[-i][0]):
                    try:
                        time.sleep(0.2)
                        if bot.unfollow(followed[-i][1]):
                            bot.update_output()
                            del followed[-i]
                            found = True
                        else:
                            fails += 1
                            i += 1
                    except Exception as e:
                        bot.write_log("unfollow error: %s\n" % (e))
                        fails += 1
                        i += 1
                else:
                    i += 1
                    time.sleep(0.2)
            except IndexError:
                fails += 3
    return found


def unfollow_protocol(bot, followed, blacklist):
    i = 0
    fails = 0
    found = False
    if len(followed) > 0:
        while not found and fails < 2:
            try:
                if not bot.is_user_following(followed[i][0]):
                    try:
                        time.sleep(0.2)
                        if bot.unfollow(followed[i][1]):
                            bot.update_output()
                            del followed[i]
                            found = True
                        else:
                            fails += 1
                            i += 1
                    except Exception as e:
                        bot.write_log("unfollow error: %s\n" % (e))
                        fails += 1
                        i += 1
                else:
                    del followed[i]
                    i += 1
                    time.sleep(0.2)
            except IndexError:
                fails += 3
    return found


def cleanBotFollows(bot, follow_list):
    for user in follow_list:
        if bot.is_user_following(user[0]):
            follow_list.remove(user)


def getMenu():
    print("\nApollo Bot Version 0.7")
    print("---------------------------")
    print("Start auto follow/like and messaging: start all")
    print("Pause auto follow/like and messaging: pause all")
    print("Start auto follow: resume follow or start follow")
    print("Pause auto follow: pause follow")
    print("Start auto like: resume like or start like")
    print("Pause auto like: pause like")
    #print("Start messaging new followers: start message")
    #print("Pause messaging new followers: pause message")
    print("Start unfollow process: cleanup")
    print("Exit the bot: exit")
    print("---------------------------\n\n")


def finish(bot):
    bot.write_log("Attempting to logout...")
    string = bot.logout()
    #try:
        #with open("log.txt", "a") as log_file:
    #        log_file.write(string)
    #except:
    #    with open()("log.txt", "w") as log_file:
    #        log_file.write(string)

    #try:
     #   pickle.dump(day_timer, open("timers.dump", "wb"))
    #except:
    #    pass





#main(username='apollo_bot_munn', password='Shoestring99',target_username='9gag',pause_follow=False)

'''
import os



while True:
    print(os.getpid())
    user_input = input()
    print(os.getpid())
    if user_input == "exit":
        sys.exit()
    if user_input == "pause all":
        pause_follow = True
        pause_like = True
        message_pause = True
    if user_input == "start message":
        message_pause = False
    if user_input == "pause message":
        message_pause = True
    if user_input == "pause follow":
        pause_follow = True
    if user_input == "pause like":
        pause_like = True
    if user_input == "resume follow" or user_input == "start follow":
        pause_follow = False
    if user_input == "resume like" or user_input == "start like":
        pause_like = False
    if user_input == "resume all" or user_input == "start all":
        pause_follow = False
        pause_like = False
        message_pause = False
    if user_input == "cleanup":
        cleanup = not cleanup




1651003839901089420
1651003838272311840
1651003836059123044
1651003834414564146
1651003833893253677
1651003833532574864
1651003833147850510
1651003831595866890
1651003829943879469
1651003827912215823
1651003824439528545
1651003822753408440
1651003822123842578
1651003821874198405
1651003821494875830
('e.ishibaashi_aqua', 6171563586)
('k__nami__', 947396805)
('breatheitaly', 3126984542)
('chef.marchese', 1977669438)
('ohmyfashh', 2114616993)
('fredlizee', 206547364)
'''

