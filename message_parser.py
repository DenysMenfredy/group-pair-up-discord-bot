import re

def parse_message(message):
    """
    Parses a message from the server and returns a dictionary with the
    following keys:
    - 'type': the message type
    - 'content': the message content
    - 'channel': the channel the message was sent to
    - 'sender': the sender of the message
    - 'timestamp': the timestamp of the message
    """

    print(message.content)

    group_name = message.content.split('\n')[1]

    members_ids = re.findall(r'<@(\d+)>', message.content)
    members_names = re.findall(r'<@!(\w+)>', message.content)
    print(members_ids)
    members = []
    if len(members_ids) > 0:
        members_ids = [int(id) for id in members_ids]

    return {
        'type': 'message',
        'content': message,
        'members': members_ids,
        'sender': message.author,
        'timestamp': message.created_at,
        'group_name': group_name
    }

