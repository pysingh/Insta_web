from .database import *

def get_all_cards_info(i,bot):
    if i.target == 'username':
        print(i.target_value)
        info = bot.get_user_info(i.target_value)
        bot.logout()

        if i.status == 'active':
            # link = "pause_target_functionality('"+ i.link_id + "','/pause/','" +  i.instagram_username + "','" + i.target_value +"');"
            link = "pause_target_functionality('" + i.link_id + "','/pause/','" + i.instagram_username + "','" + i.target_value + "');"

        else:
            link = "start_target_functionality('" + i.link_id + "','/play/','" + i.instagram_username + "','" + i.target_value + "');"

        if i.pause_like == False:
            link = "pause_likes_functionality('likes_check_" + i.link_id + "','" + i.link_id + "','/like_pause/','" + i.instagram_username + "','" + i.target_value + "');"

        else:
            link = "start_likes_functionality('likes_check_" + i.link_id + "','" + i.link_id + "','/like_play/','" + i.instagram_username + "','" + i.target_value + "');"

        delete_link = "delete_target_functionality('" + i.link_id + "','/delete/','" + i.instagram_username + "','" + i.pid + "');"
        follows = info['followed_by']['count']
        following = info['follows']['count']
        print(follows, following)
        update_target_functionalities(i,follows,following)

        return {
            'username': i.username,
            'instagram_username': i.instagram_username,
            'target_value': i.target_value,
            'target': i.target,
            'pid': i.pid,
            'follow': follows,
            'following': following,
            'play_pause_link': link,
            'delete_link': delete_link,
            'link_id': i.link_id,
            'status': i.status,
            'pause_like': i.pause_like,
        }

    elif i.target == 'tag':
        print(i.target_value)
        if i.status == 'active':
            link = "pause_target_functionality('" + i.link_id + "','/pause/','" + i.instagram_username + "','" + i.target_value + "','" + i.pid + "');"
        else:
            link = "start_target_functionality('" + i.link_id + "','/play/','" + i.instagram_username + "','" + i.target_value + "');"

        delete_link = "delete_target_functionality('" + i.link_id + "','/delete/','" + i.instagram_username + "','" + i.pid + "');"

        return {
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
        }

def get_message_list(messages,hyperlinks):
    messages = messages['paramName']
    hyperlinks = hyperlinks['paramName']
    print(messages)
    print(hyperlinks)
    messages_list = []
    messages_list.append({'message': messages[0], 'hyperlink': hyperlinks[0]})
    messages_list.append({'message': messages[1], 'hyperlink': hyperlinks[1]})
    messages_list.append({'message': messages[2], 'hyperlink': hyperlinks[2]})

    if len(messages) == 3:
        return messages_list

    elif len(messages) == 4:
        messages_list.append({'message': messages[3], 'hyperlink': hyperlinks[3]})
        return messages_list

    elif len(messages) == 5:
        messages_list.append({'message': messages[3], 'hyperlink': hyperlinks[3]})
        messages_list.append({'message': messages[4], 'hyperlink': hyperlinks[4]})
        return messages_list


    elif len(messages) == 6:
        messages_list.append({'message': messages[3], 'hyperlink': hyperlinks[3]})
        messages_list.append({'message': messages[4], 'hyperlink': hyperlinks[4]})
        messages_list.append({'message': messages[5], 'hyperlink': hyperlinks[5]})
        return messages_list