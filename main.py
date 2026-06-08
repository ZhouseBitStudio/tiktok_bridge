From flask import Flask, request
import subprocess
import sys

app = Flask(__name__)
processes = {}

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    username = data.get('username')
    port = data.get('port')
    
    if username in processes:
        return {"status": "already running"}
    
    p = subprocess.Popen([sys.executable, 'bridge.py', username, str(port)])
    processes[username] = p
    return {"status": "started"}

@app.route('/stop', methods=['POST'])
def stop():
    data = request.json
    username = data.get('username')
    
    if username in processes:
        processes[username].kill()
        del processes[username]
    return {"status": "stopped"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
