import random
import re
import imaplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
import os
import time
import smtplib, ssl
import datetime
import pickle

daily_message = """Subject: Coffee Chatter Inquiry for {}
Hello there!

I'm the coffee chatter bot, checking to see if you'd be interested in being matched for a one-on-one chat tomorrow. 

Please reply "MATCH" by 5am PDT if you would like me to match you with someone in your group.

If you do not reply, I will assume you are not interested. If you would like to no longer recieve these emails, please send me "STOP" or "UNSUBSCRIBE". 

Best,

~ C. Chatter
"""

matched_message = """Subject: Coffee Chat Match {}
CC: {}, {}
Hi! 

Here is today's match for you: {} and {}.

Reply all to this email to figure out a time to chat.

Best,

~ C. Chatter
"""

unmatched_message = """Subject: Coffee Chat Match {}
Hi! 

Unfortunately, due to odd numbers of signups, you were randomly selected to be the odd one out and we were unable to find you a match. Try again tomorrow!

"""

class EmailParser:
    def __init__(self, username, password, group):
        self.username = username
        self.password = password
        self.group = group
        self.regexp = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(username, password)
        status, messages = imap.select("INBOX")
        self.prev_msgs = int(messages[0])

    def sendEmail(self, recipient, content):
        print("Sending email")
        port = 465
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, recipient, content)

    def sendReply(self, original_message, content):
        print("Sending reply")
        new = MIMEMultipart("mixed")
        body = MIMEMultipart("alternative")
        body.attach( MIMEText(content, "plain") )
        new.attach(body)
        new["Message-ID"] = email.utils.make_msgid()
        new["In-Reply-To"] = original_message["Message-ID"]
        new["References"] = original_message["Message-ID"]
        new["Subject"] = "Re: " + original_message["Subject"]
        new["To"] = original_message["Reply-To"] or original_message["From"]
        new["From"] = self.username
        print(new)
        self.sendEmail([new["To"]], new.as_string())

    def getNewEmails(self):
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(self.username, self.password)
        status, messages = imap.select("INBOX")
        n_msgs = int(messages[0])
        print("Num unhandles messages: {}".format(n_msgs - self.prev_msgs))
        emails = []
        for i in range(self.prev_msgs + 1, n_msgs + 1):
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    message = email.message_from_bytes(response[1])
                    subject = decode_header(message["Subject"])[0][0]

                    if "Re: Coffee Chat Match" in subject:
                        continue

                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    sender = message.get("From")
                    print("Subject: {}".format(subject))
                    print("From: {}".format(sender))


                    for part in message.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode()
                                emails.append({"sender":sender, "subject":subject, "body":body, "message":message})
                            except:
                                pass
        self.prev_msgs = n_msgs
        return emails

    def parseBody(self, body):
        lines = body.split("\n")
        for line in lines:
            line = line.strip().upper()
            if line == "":
                continue
            elif line == "STOP" or line == "REMOVE" or line == "UNSUBSCRIBE":
                return ["Aww, sorry that you'd like to stop. Hopefully, we'll see you later! We won't email or match you anymore", -1]
            elif line == "MATCH":
                return ["Great! I'll match you for tomorrow.", 1]
            elif "ADD ME" in line:
                return ["Awesome! I'll add you to the daily matching inquiry, sent at ~1pm PDT. If you don't respond by 5am PDT the next day, we won't match you with anyone. Don't feel pressured to match every day!", 2]
            elif line == "DEBUG":
                return ["group signups: {}".format(self.group.skipDict), 0]
            else:
                return ["I'm really sorry - I didn't understand your message. Can you please use one of the following words?\n MATCH - to sign up to be matched for tomorrow\n STOP - to stop recieving these emails.", 0]

    def handleEmails(self):
        print("Current group: {}".format(self.group.skipDict))
        email_messages = self.getNewEmails()
        for email_message in email_messages:
            response = self.parseBody(email_message["body"])
            sender =  email_message["sender"]
            if response[1] == 1:
                self.group.unskipMember(sender)
            if response[1] == 2:
                self.group.addMember(sender)
            if response[1] == -1:
                self.group.removeMember(sender)
            with open("group_pickle", "wb") as picklefile:
                print("Saving pickle")
                pickle.dump(self.group, picklefile)
                
            self.sendReply(email_message["message"], response[0])

    def sendDailyMessage(self):
        for member in self.group:
            self.group.skipMember(member)
            self.sendEmail(member, daily_message.format((datetime.datetime.now() + datetime.timedelta(1)).date()))
        print(self.group.skipDict)

    def sendMatchingMessage(self):
        matches = self.group.matchMembers()
        print("Resulting matches: {}".format(matches))
        for match in matches[0]:
            self.sendEmail(match, matched_message.format(datetime.date.today(), match[0], match[1], match[0], match[1]))
        for unmatch in matches[1]:
            self.sendEmail(unmatch, unmatched_message.format(datetime.date.today()))
           
            

class Group:
    def __init__(self):
        self.group = []
        self.skipDict = {}
        self.num_messages = 0

    def __iter__(self):
        return iter(self.group)

    def addMember(self, email):
        print("Adding member")
        self.group.append(email)
        print(self.group)
        self.skipDict[email] = True

    def removeMember(self, email):
        if email in self.group:
            self.group.remove(email)
            del self.skipDict[email]

    def skipMember(self, email):
        self.skipDict[email] = True
    
    def unskipMember(self, email):
        self.skipDict[email] = False

    def matchMembers(self):
        random.shuffle(self.group)
        currMatches = []
        matchedMembers = []
        for i in range(len(self.group)):
            if self.group[i] not in matchedMembers and not self.skipDict[self.group[i]]: 
                for j in range(len(self.group)):
                    print(self.group[j] not in matchedMembers, not self.skipDict[self.group[j]], i != j)
                    if self.group[j] not in matchedMembers and not self.skipDict[self.group[j]] and i != j:
                        currMatches.append([self.group[i], self.group[j]])
                        matchedMembers.append(self.group[i])
                        matchedMembers.append(self.group[j])
                        break
        unmatchedMembers = []
        for member in self.group:
            if member not in matchedMembers and not self.skipDict[member]:
                unmatchedMembers.append(member)
        return [currMatches, unmatchedMembers]
            

g = Group()
if os.path.isfile("group_pickle"):
    with open("group_pickle", "rb") as picklefile:
        print("Reading pickle file")
        g = pickle.load(picklefile)

e = EmailParser("coffeechatterbot@gmail.com", "low@des-veab4DILK", g)

import schedule
import time

def sendDailyMessage():
    print("Sending daily message")
    e.sendDailyMessage()

def sendMatchingMessage():
    print("Sending matching message")
    e.sendMatchingMessage()

def handleEmails():
    print("Handling emails")
    e.handleEmails()

schedule.every().monday.at("19:00").do(sendDailyMessage)
schedule.every().wednesday.at("19:00").do(sendDailyMessage)
schedule.every().thursday.at("19:00").do(sendDailyMessage)
schedule.every().tuesday.at("12:00").do(sendMatchingMessage)
schedule.every().thursday.at("12:00").do(sendMatchingMessage)
schedule.every().friday.at("12:00").do(sendMatchingMessage)

while True:
    schedule.run_pending()
    handleEmails()
    time.sleep(60)

