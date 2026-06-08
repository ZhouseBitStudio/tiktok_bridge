Import asyncio
import socket
import json
import sys
import time
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, GiftEvent, CommentEvent, FollowEvent

username = sys.argv[1] if len(sys.argv) > 1 else "@username"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080

client = TikTokLiveClient(unique_id=username)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

while not connected:
    try:
        sock.connect(("0.0.0.0", port))
        connected = True
        print(f"[bridge] connected to port {port}")
    except Exception as e:
        print(f"[bridge] waiting on port {port}: {e}")
        time.sleep(1)

def send(data: dict):
    msg = json.dumps(data) + "\n"
    sock.sendall(msg.encode("utf-8"))

@client.on(ConnectEvent)
async def on_connect(event):
    send({"type": "connect", "message": "Connected!"})

@client.on(GiftEvent)
async def on_gift(event):
    send({
        "type": "gift",
        "user": event.user.nickname,
        "gift": event.gift.name,
        "count": event.repeat_count
    })

@client.on(CommentEvent)
async def on_comment(event):
    send({
        "type": "comment",
        "user": event.user.nickname,
        "comment": event.comment
    })

@client.on(FollowEvent)
async def on_follow(event):
    send({
        "type": "follow",
        "user": event.user.nickname
    })

try:
    client.run()
except Exception as e:
    print(f"[bridge] TikTok error: {e}")
finally:
    sock.close()