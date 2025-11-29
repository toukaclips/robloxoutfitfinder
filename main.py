import requests
import time
import sys
import os
from colorama import init, Style

init()

BLUE = "\033[94m"
RESET = "\033[0m"

TYPE_SPEED = 0.01
COOLDOWN_SECONDS = 2


def type_gradient_greenwhite(text):
    start = (0, 255, 0)
    end = (255, 255, 255)

    length = max(1, len(text))

    for i, char in enumerate(text):
        t = i / (length - 1)
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
            t = i / (length - 1)
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
        t = i / (length - 1)
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


def main():

    # ids.txt löschen / leeren
    with open("ids.txt", "w", encoding="utf-8"):
        pass

    # Titel animiert ausgeben
    type_gradient_pinkblue(TITLE)
    print()

    # animierter Input: entweder eine numerische ID oder ein Username
    user_input = typewriter_input("Enter Roblox UserID or Username: ").strip()

    if not user_input:
        status("Keine Eingabe erkannt. Neustart...")
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(0.2)
        main()
        return

    # Falls numerisch -> direkt als ID verwenden
    if user_input.isdigit():
        user_id = user_input
        # Username abrufen (nur zur Anzeige)
        try:
            user_info = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10)
            if user_info.status_code == 200:
                username = user_info.json().get("name", "UnknownUser")
            else:
                username = "UnknownUser"
        except Exception:
            username = "UnknownUser"

    else:
        # Eingabe ist kein Zahl: nehme an, es ist ein Username -> ID ermitteln (moderner POST-Endpoint)
        username_candidate = user_input
        status(f"Looking up username '{username_candidate}'...")
        try:
            lookup_url = "https://users.roblox.com/v1/usernames/users"
            payload = {"usernames": [username_candidate], "excludeBannedUsers": False}
            headers = {"Content-Type": "application/json"}
            lookup = requests.post(lookup_url, json=payload, headers=headers, timeout=10)

            if lookup.status_code == 200:
                j = lookup.json()
                # Die Antwort enthält ein Feld "data" mit Einträgen
                data_list = j.get("data", [])
                if data_list:
                    entry = data_list[0]
                    # falls matchType "exact" oder "startsWith" etc. wir nehmen den ersten Eintrag
                    uid = entry.get("id")
                    uname = entry.get("name") or entry.get("username") or username_candidate
                    if uid:
                        user_id = str(uid)
                        username = uname
                        status(f"Found @{username} -> ID {user_id}")
                    else:
                        status("Username not found. Bitte überprüfe die Eingabe.")
                        print()
                        type_gradient_greenwhite("Press ENTER to restart the process...")
                        input()
                        time.sleep(1)
                        os.system("cls" if os.name == "nt" else "clear")
                        time.sleep(0.2)
                        main()
                        return
                else:
                    status("Username not found. Bitte überprüfe die Eingabe.")
                    print()
                    type_gradient_greenwhite("Press ENTER to restart the process...")
                    input()
                    time.sleep(1)
                    os.system("cls" if os.name == "nt" else "clear")
                    time.sleep(0.2)
                    main()
                    return
            else:
                status(f"API error while resolving username (HTTP {lookup.status_code}).")
                print()
                type_gradient_greenwhite("Press ENTER to restart the process...")
                input()
                time.sleep(1)
                os.system("cls" if os.name == "nt" else "clear")
                time.sleep(0.2)
                main()
                return

        except requests.exceptions.RequestException:
            status("Network error while resolving username.")
            print()
            type_gradient_greenwhite("Press ENTER to restart the process...")
            input()
            time.sleep(1)
            os.system("cls" if os.name == "nt" else "clear")
            time.sleep(0.2)
            main()
            return

    status(f"Requesting outfits for @{username} [{user_id}]...")

    time.sleep(COOLDOWN_SECONDS)

    # -------------------------------------------------------
    #   ALLE OUTFITS MIT EINEM CALL LADEN (itemsPerPage=500)
    # -------------------------------------------------------
    url = f"https://avatar.roblox.com/v1/users/{user_id}/outfits?itemsPerPage=500"
    try:
        response = requests.get(url, timeout=10)
    except Exception:
        status("Network error – could not retrieve outfits.")
        print()
        type_gradient_greenwhite("Press ENTER to restart the process...")
        input()
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        time.sleep(0.2)
        main()
        return

    if response.status_code != 200:
        status("API error – could not retrieve outfits.")
        print()
        type_gradient_greenwhite("Press ENTER to restart the process...")
        input()
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

        if i < len(editable):
            time.sleep(COOLDOWN_SECONDS)

    with open("ids.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    status("Done! Saved in format: id -- name")

    print()
    type_gradient_greenwhite("Press ENTER to restart the process...")
    input()

    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(0.2)
    main()


if __name__ == "__main__":
    main()
