# Simple Bot to reply to Slack messages for NXN QA
# Sample code taken from 
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
#
import os
import time
from slackclient import SlackClient
import re
import nxnqainfo

# Define some constants
BOT_ID = str(os.environ.get("SLACK_BOT_ID"))
AT_BOT = "<@" + BOT_ID + ">"
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
READ_WEBSOCKET_DELAY = 1 # delay between reading msg
#BOT_NAME = 'nxnqabot'

#set nxn tools version
os.putenv("NXN_TOOLS_VER","12")

# Define command handler. 

def handle_command(command, channel, user):
    command.strip()
    if(command.find("chase_status",0,12)!=-1): # get chase status
        my_regex = re.compile('^(chase_status)\s+(\d+)$')
        mo = my_regex.search(command)
        if(mo is not None):
            reply_msg = "Here is the list of reported new failures:\n"+nxnqainfo.chase_cp_info(mo.group(2))
        else:
            reply_msg = "Sorry, I did not understand that. Use something like \"chase_status 1234\" where 1234 is the CP number."

    elif(command.find("scan_new",0,8)!=-1): # check is scan_new is created or not
        reply_msg = nxnqainfo.scan_new_status()

    else:
        reply_msg = "Sorry, I did not understand that. Currently supported requests are \"chase_status\" and \"scan_new\"."
    
    slack_client.api_call("chat.postMessage", channel = user, 
                              text = reply_msg, as_user = True)



def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:

            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(),output['channel'], output['user']
    return None, None, None

 
def main():
    if slack_client.rtm_connect():
        print("nxnqabot connected and running")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)

    else:
        print("Unable to connect")


if __name__ == '__main__':
    main()
