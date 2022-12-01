from flask_mail import Message
from applications.extensions.init_mail import Mail

import datetime


# def send_mail(subject, recipients, content):
#     try:
#         message = Message(subject=subject, recipients=recipients, body=content)
#         mail.send(message)
#     except Exception as e:
#         print('邮箱发送出错了')
#         raise


class Email_Module:
    def __init__(self):
        """
        The function __init__() is a constructor that initializes the class variables Mail, Message, UserName,
        and PassWord
        """
        self.Time = 2
        self.Mail = Mail
        self.Message = Message

    def CheckMessage(self, subject, recipients):
        """
        The function Message() is a method of the class Mailer, and it takes two arguments, subject and recipients

        :param subject: The subject of the email
        :param recipients: A list of email addresses to send the message to
        :return: The message object is being returned.
        """
        message = self.Message(subject=subject, recipients=recipients)
        return message

    def TimeInterval(self):
        """
        It takes the current time, adds the number of days the user wants to wait, and then returns the number of
        seconds until that time. :return: The number of seconds between now and the next week.
        """
        now = datetime.datetime.now()
        next_week = now + datetime.timedelta(minutes=self.Time if self.Time else 2)
        next_week = next_week.replace(hour=0, minute=0, second=0, microsecond=0)
        return (next_week - now).seconds

    def TimeApscheduler(self):
        """
        The function Apscheduler() is a method of the APScheduler class, and it returns a APScheduler object
        """
        JOBS = [
            {
                'id': 'job1',
                'func': 'scheduler:task',
                'args': (1, 2),
                'trigger': 'interval',
                'seconds': self.TimeInterval()
            }
        ]
        SCHEDULER_API_ENABLED = True
        return JOBS, SCHEDULER_API_ENABLED

    def SendAsyncEmail(self, message):
        """
        > This function sends an email asynchronously

        :param message: The message to be sent
        """

        return_value = {
            'status_code': 200,  # 状态码
            'msg': {
                'error_msg': '',  # 错误信息
                'email_msg': '',  # 邮件信息
            }
        }
        try:
            # todo FixBug 逻辑问题 app_context 上下文调用
            with self.Mail.app_context():
                self.Mail().send(message)
            return_value['msg']['email_msg'] = '邮件发送成功'
        except Exception as e:
            return_value['status_code'] = 500
            return_value['msg']['error_msg'] = '邮件发送失败'
            return_value['msg']['email_msg'] = str(e)

    def SendEmail(self, subject, recipients, body, html):
        """
        It creates a Message object, sets the body and html attributes, and then sends the message

        :param subject: 邮件主题
        :param recipients: A list of email addresses to send the email to
        :param body: The plain text body of the email
        :param html: The HTML body of the message
        :return: The return value is a task object.
        """
        message = self.CheckMessage(subject, recipients)
        # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
        message.body = body if body else '邮件内容'
        message.html = html if html else '邮件内容'  # <b>{data_info}</b>
        return self.SendAsyncEmail(message)


if __name__ == '__main__':
    test = Email_Module().TimeApscheduler()
    print(test)
