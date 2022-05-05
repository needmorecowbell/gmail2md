import imaplib
import os
from email.utils import parsedate_to_datetime
from email import message as msg
from typing import List, Union
import email


# Obsidian Helper Tool: Export Gmail Receipts to Markdown
# Author: github.com/needmorecowbell

FROM_EMAIL = os.getenv("GMAIL_EMAIL","user@gmail.com")
FROM_PWD = os.getenv("GMAIL_APP_PASSWORD","APPLICATION_PASSWORD_HERE")  # Visit [ https://support.google.com/accounts/answer/185833?hl=en ] for more info 
MAILBOX="receipts" # Label to read (e.g. "INBOX")


SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

ATTACHMENT_PATH="/home/user/Notes/Obsidian Attachments/" # full path to obisidian attachments directory
REL_ATTACH_PATH="Obsidian Attachments/" # Relative path from obsidian vault to include in markdown notes for linking
NOTES_PATH="/home/user/Notes/Receipts/" # full path to obsidian Receipts directory

FNAME_TIME_FMT="%m-%d-%Y_T%H_%M" # datetime format for file name
NOTE_TIME_FMT="%b %d %Y %I:%M %p" # datetime format for inside markdown note

def get_emails_from_mailbox(mbox: str) -> List[msg.Message]:
    """
    Reads email from a mailbox and converts it to markdown
    :param mbox: mailbox to read from
    :return: list of email.Message objects
    """

    messages =[]
    try:
        mail.select(mailbox=mbox, readonly=True)
        _, mails = mail.search(None, "ALL")

        for mail_id in mails[0].decode().split()[-2:]:
            _, mail_data = mail.fetch(mail_id, '(RFC822)') ##Fetch mail data.
            messages.append(email.message_from_bytes(mail_data[0][1])) # Construct Message from mail data and add to list
        
        return messages
    except Exception as e:
        print(str(e))
    finally:
        mail.close()



def convert_to_markdown(message : msg.Message) -> Union[str,None]:
    """
    Converts an email to markdown, saving the related files to the attachments directory and adding a link to the files in the notes
    
    :param message: email.Message object
    :return: markdown string, saving files to attachment directory in the process. None if file already exists
    :rtype: str
    """

    date = parsedate_to_datetime(message.get("Date"))
    fname = date.strftime(FNAME_TIME_FMT)+"_"+message.get("Subject")
    body=""

    # if the file exists in Notes path
    if(os.path.exists(NOTES_PATH+fname+".md")):
        print(f"Email [{fname}] already exists")
        return None
    else:

        with open(ATTACHMENT_PATH+fname+".eml",'wb') as f:
            f.write(message.as_bytes())

        body+=f"\n**EML**:: [[{REL_ATTACH_PATH +fname}.eml]]\n"
        
        # I choose to just include a link to the eml file in the body. Attachments are linked separately
        for part in message.walk():            
            if part.get_content_type() == "application/pdf":
                pdf = part.get_payload(decode=True)
                with open(ATTACHMENT_PATH+fname+'_'+part.get_filename()+".pdf","wb") as f:
                    f.write(pdf)
                body+=f"\n**PDF Attachment**:: [[{REL_ATTACH_PATH +fname+'_'+part.get_filename()}.pdf]]\n"

    # Content Template
    content=f"""
---
tags: ['receipt','email']
aliases: []
---
    
# {message.get("Subject")} - {message.get("From")}

-----------
**From**:: {message.get("From")}
**To**::  {message.get("To")}
**Bcc**:: {message.get("Bcc")} 
**Date**:: {date.strftime(NOTE_TIME_FMT)}
**Subject**:: {message.get("Subject")}

-----------

## Associations

## Contents

{body}

## Notes


"""
    with open(NOTES_PATH+fname+".md","w") as f:
        f.write(content)

    return content


if __name__ == "__main__":

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    messages= get_emails_from_mailbox(MAILBOX)

    for message in messages:
        convert_to_markdown(message)

    