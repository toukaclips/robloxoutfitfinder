# 🎮 Outfit Loader (Roblox)

A clean and stylish Python tool to **fetch all editable Roblox outfits** of any user — using either a **UserID or Username**.  
Features animated terminal output, color gradients, automatic file export, and Discord webhook support.

> 💡 Developed by **@toukaclips**  
> 🌐 Discord: `.gg/worldvoice`

---

## ✨ Features

✅ Input via **Username or UserID**  
✅ Automatic **UserID resolution from Username**  
✅ Fetches **all outfits** from a profile  
✅ Filters only **editable (owned) outfits**  
✅ Saves results automatically to `ids.txt`  
✅ Animated terminal UI  
✅ Color gradient effects  
✅ Auto-restart after completion  
✅ **Discord Webhook**: sends an embed for each editable outfit (title, description with outfit ID, image thumbnail)  
✅ **Animated Console Title**: `"by @toukaclips"` scrolls from right to left and back without interrupting terminal output

---

## 🖥️ Preview

```text
Enter Roblox UserID or Username: @username
[+] Found @username -> ID 1234567890
[+] Requesting outfits...
[+] xxx total outfits found
[+] xx editable outfits found
[+] Done! Saved in format: id -- name (and webhooks sent for editable outfits)
