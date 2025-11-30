import requests
import threading
import time
import sys
import os
import msvcrt
from colorama import init
import ctypes
import json


DISCORD_WEBHOOK = "YOUR_WEBHOOK" #put your discord webhook here
TYPE_SPEED = 0.01 #typewriter speed
COOLDOWN_SECONDS = 3 #cooldown between fetching new outfits


def animate_title(text):
    while True:

        ctypes.windll.kernel32.SetConsoleTitleW(text)
        time.sleep(1)


        for i in range(len(text), 1, -1):
            ctypes.windll.kernel32.SetConsoleTitleW(text[:i-1])
            time.sleep(0.15)


        for i in range(2, len(text)+1):
            ctypes.windll.kernel32.SetConsoleTitleW(text[:i])
            time.sleep(0.1)


threading.Thread(target=animate_title, args=("by @toukaclips",), daemon=True).start()



def set_console_size(width, height):
    STD_OUTPUT_HANDLE = -11
    hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
    size = COORD(width, height)
    ctypes.windll.kernel32.SetConsoleScreenBufferSize(hOut, size)

    class SMALL_RECT(ctypes.Structure):
        _fields_ = [("Left", ctypes.c_short),
                    ("Top", ctypes.c_short),
                    ("Right", ctypes.c_short),
                    ("Bottom", ctypes.c_short)]
    rect = SMALL_RECT(0, 0, width-1, height-1)
    ctypes.windll.kernel32.SetConsoleWindowInfo(hOut, True, ctypes.byref(rect))

try:
    set_console_size(79, 30)
except Exception:
    pass

init()

BLUE = "\033[94m"
RESET = "\033[0m"


def type_gradient_greenwhite(text):
    start, end = (0, 255, 0), (255, 255, 255)
    length = max(1, len(text))
    for i, char in enumerate(text):
        t = i / (length - 1) if length > 1 else 0
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        sys.stdout.write(f"\033[38;2;{r};{g};{b}m{char}{RESET}")
        sys.stdout.flush()
        time.sleep(TYPE_SPEED)
    print()

def status(text):
    sys.stdout.write(f"{BLUE}[+]{RESET} ")
    sys.stdout.flush()
    type_gradient_greenwhite(text)

def type_gradient_pinkblue(text):
    pink, blue = (255, 79, 216), (77, 204, 255)
    lines = text.split("\n")
    for line in lines:
        length = max(1, len(line))
        for i, char in enumerate(line):
            t = i / (length - 1) if length > 1 else 0
            r = int(pink[0] + (blue[0] - pink[0]) * t)
            g = int(pink[1] + (blue[1] - pink[1]) * t)
            b = int(pink[2] + (blue[2] - pink[2]) * t)
            sys.stdout.write(f"\033[38;2;{r};{g};{b}m{char}{RESET}")
            sys.stdout.flush()
            time.sleep(TYPE_SPEED)
        print()
        time.sleep(0.03)

def typewriter_input(prompt_text):
    start, end = (0, 255, 0), (255, 255, 255)
    length = max(1, len(prompt_text))
    for i, char in enumerate(prompt_text):
        t = i / (length - 1) if length > 1 else 0
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        sys.stdout.write(f"\033[38;2;{r};{g};{b}m{char}{RESET}")
        sys.stdout.flush()
        time.sleep(TYPE_SPEED)
    return input("")

TITLE = r"""
                █▀█ █░█ ▀█▀ █▀▀ █ ▀█▀   █░░ █▀█ ▄▀█ █▀▄ █▀▀ █▀█
                █▄█ █▄█ ░█░ █▀░ █ ░█░   █▄▄ █▄█ █▀█ █▄▀ ██▄ █▀▄
                                by @toukaclips
                                .gg/worldvoice
"""

def get_outfit_thumbnail_url(outfit_id, size="420x420"):
    try:
        thumb_api = f"https://thumbnails.roblox.com/v1/users/outfits?userOutfitIds={outfit_id}&size={size}&format=Png&isCircular=false"
        r = requests.get(thumb_api, timeout=10)
        if r.status_code != 200: return None
        data = r.json().get("data", [])
        if not data: return None
        el = data[0]
        if el.get("state") != "Completed": return None
        return el.get("imageUrl")
    except Exception:
        return None

def send_discord_webhook_embed(webhook_url, title, description, image_url=None, footer_text=None):
    embed = {
        "title": title,
        "description": description,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
    }
    if footer_text: embed["footer"] = {"text": footer_text}
    if image_url: embed["image"] = {"url": image_url}
    payload = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=10)
        return resp.status_code in (200, 204)
    except Exception:
        return False


def main():
    with open("ids.txt", "w", encoding="utf-8"): pass
    type_gradient_pinkblue(TITLE)
    print()

    user_input = typewriter_input("Enter Roblox UserID or Username: ").strip()
    if not user_input:
        status("No Input recognized. Restart...")
        time.sleep(1)
        os.system("cls")
        main()
        return

    if user_input.isdigit():
        user_id = user_input
        try:
            user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10)
            username = user_info.json().get("name", "UnknownUser") if user_info.status_code==200 else "UnknownUser"
        except Exception:
            username = "UnknownUser"
    else:
        username_candidate = user_input
        status(f"Looking up username '{username_candidate}'...")
        try:
            lookup_url = "https://users.roblox.com/v1/usernames/users"
            payload = {"usernames": [username_candidate], "excludeBannedUsers": False}
            headers = {"Content-Type": "application/json"}
            lookup = requests.post(lookup_url, json=payload, headers=headers, timeout=10)
            if lookup.status_code==200 and lookup.json().get("data"):
                entry = lookup.json()["data"][0]
                uid = entry.get("id")
                uname = entry.get("name") or username_candidate
                if uid: user_id, username = str(uid), uname; status(f"Found @{username} -> ID {user_id}")
                else: raise ValueError
            else: raise ValueError
        except Exception:
            status("Username not found / network error. Restarting...")
            time.sleep(1)
            os.system("cls")
            main()
            return

    status(f"Requesting outfits for @{username} [{user_id}]...")
    time.sleep(COOLDOWN_SECONDS)
    try:
        response = requests.get(f"https://avatar.roblox.com/v1/users/{user_id}/outfits?itemsPerPage=500", timeout=10)
        outfits = response.json().get("data", []) if response.status_code==200 else []
    except Exception:
        outfits = []

    status(f"{len(outfits)} total outfits found. Filtering editable ones...")
    editable = [o for o in outfits if o.get("isEditable")]
    status(f"{len(editable)} editable (own) outfits found.")

    lines = []
    for i, outfit in enumerate(editable, start=1):
        oid, name = outfit["id"], outfit.get("name", "Unknown")
        status(f"Editable OutfitID {oid} ({i}/{len(editable)}) - {name}")
        lines.append(f"{oid} -- {name}")
        title, description = f"OutfitName: {name}", f"```{oid}```"
        image_url = get_outfit_thumbnail_url(oid)
        send_discord_webhook_embed(DISCORD_WEBHOOK, title, description, image_url=image_url, footer_text=f"From @{username}")
        if i < len(editable): time.sleep(COOLDOWN_SECONDS)

    with open("ids.txt", "w", encoding="utf-8") as f: f.write("\n".join(lines))
    status("Done! Saved in format: id -- name (and embeds sent for editable outfits)")

    type_gradient_greenwhite("Press any key to restart the process...")
    msvcrt.getch()
    os.system("cls")
    main()


if __name__ == "__main__":
    main()




