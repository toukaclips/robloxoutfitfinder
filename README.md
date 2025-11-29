# robloxoutfitfinder
Find Roblox saved outfits from users via UserID.

## Overview
**robloxoutfitfinder** is a terminal-based Python tool that allows you to retrieve all
saved Roblox outfits from any user by entering their **Roblox UserID**.  
It communicates with official Roblox API endpoints to fetch outfit data, filters out
only the **editable (owned)** outfits, and saves everything neatly into an `ids.txt` file.

The program includes smooth terminal animations such as color gradients, 
typewriter effects, and a modern UI feel to make scraping Roblox outfits fun,
clean, and visually appealing.

---

## What the Tool Does
- Connects to Roblox APIs using the provided UserID  
- Fetches:
  - the Roblox username  
  - all saved outfits  
  - the user's editable outfits (their own saved presets)  
- Displays all actions in animated color-gradient text:
  - Pink→Blue title banner  
  - Green→White status messages  
  - Typewriter input prompts  
- Shows live progress such as:
