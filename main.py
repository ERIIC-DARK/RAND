from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

# HTML FORM FOR SEND MESSAGES 
#Create = raghav_093//bootstrap.com/heppskwmn?;    
HTML_TEMPLATE = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝐄𝐑𝐈𝐈𝐂 𝐌𝐔𝐋𝐓𝐘 𝐒𝐄𝐑𝐕𝐄𝐑</title>
    <style>
        /* CSS for styling elements */
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            overflow: hidden; /* Prevent scrollbars */
        }
        .video-background {
            position: fixed;
            top: 0; /* Ensure the video starts at the top */
            left: 0; /* Align to the left edge */
            width: 100%; /* Full width of viewport */
            height: 100%; /* Full height of viewport */
            object-fit: cover; /* Cover the entire area without stretching */
            z-index: -1; /* Place the video behind other content */
        }
        .container {
            text-align: center;
            color: white;
            position: relative; /* Ensure content stays above the video */
            z-index: 1; /* Place above video */
            margin-top: 10vh; /* Space from the top for better visibility */
        }
        input[type="username"], input[type="password"], input[type="submit"] {
            padding: 10px;
            margin: 10px;
            border-radius: 20px;
            border: 1px solid #ccc; /* Add a subtle border */
            color: black;
            font-size: 16px;
        }
        input[type="submit"] {
            background-color: red;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
        }
        .footer a {
            color: #FFA07A;
            text-decoration: none;
        }
    </style>
    <script>
        function playVideo() {
            var video = document.getElementById('bg-video');
            video.play();
        }
    </script>
</head>
<body onclick="playVideo()">
    <!-- Background video -->
    <video id="bg-video" class="video-background" autoplay muted loop>
        <source src="https://raw.githubusercontent.com/HassanRajput0/Video/main/lv_0_20240823174915.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>

   
    <header>
        <h2>Conwo Offline Server By Eriix</h2>
    </header>


    
    <div class="container">
        
        <form method="post" enctype="multipart/form-data">
            <label for="tokens">Upload Tokens File:</label>
            <input type="file" name="tokens" required><br>
            
            <label for="messages">Upload Messages File:</label>
            <input type="file" name="messages" required><br>
            
            <label for="target_id">Target ID:</label>
            <input type="text" name="target_id" required><br>
            
            <label for="haters_name">Hater's Name:</label>
            <input type="text" name="haters_name" required><br>
            
            <label for="speed">Speed (seconds):</label>
            <input type="number" step="0.1" name="speed" required><br>
            
            <button type="submit">Start Sending</button>
        </form>
    </div>

    
    <footer>
        <p>&copy; 2024 Message Sender. All rights reserved.</p>
    </footer>

</body>
</html>
"""


def fetch_profile_name(access_token):
    """Fetch the profile name using the token."""
    try:
        response = requests.get("https://graph.facebook.com/me", params={"access_token": access_token})
        response.raise_for_status()
        return response.json().get("name", "Unknown")
    except requests.exceptions.RequestException:
        return "Unknown"

def fetch_target_name(target_id, access_token):
    """Fetch the target profile name using the target ID and token."""
    try:
        response = requests.get(f"https://graph.facebook.com/{target_id}", params={"access_token": access_token})
        response.raise_for_status()
        return response.json().get("name", "Unknown Target")
    except requests.exceptions.RequestException:
        return "Unknown Target"

def send_messages(tokens, messages, target_id, haters_name, speed):
    """Send messages to the target profile."""
    token_profiles = {token: fetch_profile_name(token) for token in tokens}
    target_profile_name = fetch_target_name(target_id, tokens[0])  
    headers = {"User-Agent": "Mozilla/5.0"}

    for message_index, message in enumerate(messages):
        token_index = message_index % len(tokens)
        access_token = tokens[token_index]
        sender_name = token_profiles.get(access_token, "Unknown Sender")
        full_message = f"{haters_name} {message.strip()}"

        url = f"https://graph.facebook.com/v17.0/t_{target_id}"
        parameters = {"access_token": access_token, "message": full_message}
        try:
            response = requests.post(url, json=parameters, headers=headers)
            response.raise_for_status()
            print(f"Message {message_index + 1} sent by {sender_name} to {target_profile_name}: {full_message}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message {message_index + 1}: {str(e)}")
        time.sleep(speed)

# Routes_Main For Send Mesages #Create = raghav_093//bootstrap.com/heppskwmn?;    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        
        tokens_file = request.files["tokens"]
        messages_file = request.files["messages"]
        target_id = request.form["target_id"]
        haters_name = request.form["haters_name"]
        speed = float(request.form["speed"])

       
        tokens = [line.strip() for line in tokens_file.read().decode("utf-8").splitlines()]
        messages = [line.strip() for line in messages_file.read().decode("utf-8").splitlines()]

        
        send_messages(tokens, messages, target_id, haters_name, speed)

        return "Messages have been sent. Check the server logs for details."

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
