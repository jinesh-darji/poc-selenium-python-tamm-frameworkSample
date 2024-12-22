import email
import imaplib
import collections

from framework.utils.StringUtil import StringUtil

email_structure = collections.namedtuple('email_structure', ['sender', 'subject', 'body'])


class MailUtil:

    def get_url_from_body(self, server, login, password, url_regex):
        global body
        for message_data in self.read_email_from_gmail(server, login, password):
            body = str(message_data.body)
        url_accept = StringUtil.get_url_from_email(url_regex, body)
        self.delete_email_from_gmail(server, login, password)
        return url_accept

    def get_message_body(self, email_message):
        for part in email_message.walk():
            if part.get_content_type() in ["text/plain", "text/html"]:
                body = part.get_payload(decode=True)
                return body

    def read_email_from_gmail(self, server, login, password):
        mail = imaplib.IMAP4_SSL(server)
        mail.login(login, password)
        mail.select('inbox')
        type, data = mail.search(None, 'ALL')

        for num in data[0].split():
            typ, email_data = mail.fetch(num, '(RFC822)')
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            yield email_structure(
                subject=email_message['subject'],
                body=self.get_message_body(email_message),
                sender=email_message['from']
            )

    def delete_email_from_gmail(self, server, login, password):
        mail = imaplib.IMAP4_SSL(server)
        mail.login(login, password)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        for num in data[0].split():
            mail.store(num, '+FLAGS', '\\Deleted')

        mail.expunge()
        mail.close()
        mail.logout()
