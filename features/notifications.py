import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import websockets

#відправк електронних листів
def send_email(subject, body, to_email):
    from_email = "email@gmail.com"  
    password = "email_password"     

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Error: {e}")


async def notify_user(websocket, path):
    message = "Увага! Ваш матч скоро!"
    await websocket.send(message)

async def start_websocket_server():
    server = await websockets.serve(notify_user, "localhost", 8001)
    await server.wait_closed()

