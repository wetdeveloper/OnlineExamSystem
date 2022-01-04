from app import *
import email.message
import smtplib

def mailVerCode(Email="",Code=""):
        msg = email.message.Message()
        msg['Subject'] = 'verification code to rest the password'
        msg['From'] = app.config['service_email_address'] #service's email
        msg['To'] =Email#user's email
        try:
                msg.add_header('Content-Type','text/html')
                msg.set_payload(f"The code:{Code}")

                s = smtplib.SMTP('smtp.gmail.com')
                s.starttls()
                s.login(app.config['service_email_address'],
                        app.config['service_email_appPassword'])
                s.sendmail(msg['From'], [msg['To']], msg.as_string())
                s.quit()
        except BaseException as e:
                return False
        else:
                return True

# print(mailVerCode(Email="alexhe1998gerhanov@gmail.com",Code="ehsan here"))
