

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