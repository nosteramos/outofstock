import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




def send_mail(rcpt_list, subject, body_text):
    sender_email = "amosmastbaum@gmail.com"
    receiver_email = rcpt_list
    password = "@noamassaf@"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = body_text
    # html = """\
    # <html>
    #   <body>
    #     <p>Hello Brother<br>
    #        ?<br>
    #        <a href="http://www.realpython.com">Real Python</a>
    #        has many great tutorials.
    #     </p>
    #   </body>
    # </html>
    # """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    # message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )



    pass
