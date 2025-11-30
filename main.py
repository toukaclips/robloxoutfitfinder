import requests
import time
import sys
import os
import msvcrt
from colorama import init, Style
import ctypes
import json


DISCORD_WEBHOOK = "YOUR_WEBHOOK" #put your own webhook from discord here
TYPE_SPEED = 0.01 #typewriter speed
COOLDOWN_SECONDS = 3 #cooldown beetween saving new id to ids.txt


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
    start = (0, 255, 0)
    end = (255, 255, 255)

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
    pink = (255, 79, 216)
    blue = (77, 204, 255)

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
    start = (0, 255, 0)
    end = (255, 255, 255)

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
    """
    Holt die Thumbnail-URL für ein Outfit über die thumbnails.roblox.com API.
    Gibt None zurück, falls nicht verfügbar / fehlerhaft.
    """
    try:

        thumb_api = f"https://thumbnails.roblox.com/v1/users/outfits?userOutfitIds={outfit_id}&size={size}&format=Png&isCircular=false"
        r = requests.get(thumb_api, timeout=10)
        if r.status_code != 200:
            return None
        j = r.json()
        data = j.get("data", [])
        if not data:
            return None

        el = data[0]

        if el.get("state") != "Completed":
            return None
        image_url = el.get("imageUrl")
        if not image_url:
            return None

        return image_url
    except Exception:
        return None


def send_discord_webhook_embed(webhook_url, title, description, image_url=None, footer_text=None):
    """
    Sendet ein Embed an den Discord Webhook.
    """
    embed = {
        "title": title,
        "description": description,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
    }
    if footer_text:
        embed["footer"] = {"text": footer_text}
    if image_url:
        embed["image"] = {"url": image_url}

    payload = {"embeds": [embed]}

    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=10)
        if resp.status_code in (200, 204):
            return True
        else:

            return False
    except Exception:
        return False


def main():
    with open("ids.txt", "w", encoding="utf-8"):
        pass


    type_gradient_pinkblue(TITLE)
    print()

    user_input = typewriter_input("Enter Roblox UserID or Username: ").strip()

    if not user_input:
        status("No Input recognized. Restart...")
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(0.2)
        main()
        return

    if user_input.isdigit():
        user_id = user_input
        try:
            user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10)
            if user_info.status_code == 200:
                username = user_info.json().get("name", "UnknownUser")
            else:
                username = "UnknownUser"
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

            if lookup.status_code == 200:
                j = lookup.json()
                data_list = j.get("data", [])
                if data_list:
                    entry = data_list[0]
                    uid = entry.get("id")
                    uname = entry.get("name") or entry.get("username") or username_candidate
                    if uid:
                        user_id = str(uid)
                        username = uname
                        status(f"Found @{username} -> ID {user_id}")
                    else:
                        status("Username not found. Please check your input.")
                        print()
                        type_gradient_greenwhite("Press any key to restart the process...")
                        msvcrt.getch()
                        time.sleep(1)
                        os.system("cls" if os.name == "nt" else "clear")
                        time.sleep(0.2)
                        main()
                        return
                else:
                    status("Username not found. Please check your input.")
                    print()
                    type_gradient_greenwhite("Press any key to restart the process...")
                    msvcrt.getch()
                    time.sleep(1)
                    os.system("cls" if os.name == "nt" else "clear")
                    time.sleep(0.2)
                    main()
                    return
            else:
                status(f"API error while resolving username (HTTP {lookup.status_code}).")
                print()
                type_gradient_greenwhite("Press any key to restart the process...")
                msvcrt.getch()
                time.sleep(1)
                os.system("cls" if os.name == "nt" else "clear")
                time.sleep(0.2)
                main()
                return

        except requests.exceptions.RequestException:
            status("Network error while resolving username.")
            print()
            type_gradient_greenwhite("Press any key to restart the process...")
            msvcrt.getch()
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            time.sleep(0.2)
            main()
            return

    status(f"Requesting outfits for @{username} [{user_id}]...")

    time.sleep(COOLDOWN_SECONDS)

    url = f"https://avatar.roblox.com/v1/users/{user_id}/outfits?itemsPerPage=500"
    try:
        response = requests.get(url, timeout=10)
    except Exception:
        status("Network error – could not retrieve outfits.")
        print()
        type_gradient_greenwhite("Press any key to restart the process...")
        msvcrt.getch()
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(0.2)
        main()
        return

    if response.status_code != 200:
        status("API error – could not retrieve outfits.")
        print()
        type_gradient_greenwhite("Press any key to restart the process...")
        msvcrt.getch()
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(0.2)
        main()
        return

    data = response.json()
    outfits = data.get("data", [])

    status(f"{len(outfits)} total outfits found. Filtering editable ones...")

    editable = [o for o in outfits if o.get("isEditable")]

    status(f"{len(editable)} editable (own) outfits found.")

    lines = []

    for i, outfit in enumerate(editable, start=1):
        oid = outfit["id"]
        name = outfit.get("name", "Unknown")

        status(f"Editable OutfitID {oid} ({i}/{len(editable)}) - {name}")

        lines.append(f"{oid} -- {name}")


        title = f"OutfitName: {name}"
        description = f"```{oid}```"

        image_url = get_outfit_thumbnail_url(oid, size="420x420")
        if image_url:

            ok = send_discord_webhook_embed(DISCORD_WEBHOOK, title, description, image_url=image_url, footer_text=f"From @{username}")
        else:

            ok = send_discord_webhook_embed(DISCORD_WEBHOOK, title, description, image_url=None, footer_text=f"From @{username}")

        if not ok:
            status(f"Webhook send failed for outfit {oid} (HTTP error or rate-limited). Continuing...")


        if i < len(editable):
            time.sleep(COOLDOWN_SECONDS)

    with open("ids.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    status("Done! Saved in format: id -- name (and embeds sent for editable outfits)")

    print()
    type_gradient_greenwhite("Press any key to restart the process...")
    msvcrt.getch()

    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(0.2)
    main()


if __name__ == "__main__":
    main()
