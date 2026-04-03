# 🆔 Flixora ID Bot

A simple, fast, and lightweight Telegram bot built with [Pyrogram](https://docs.pyrogram.org/) to quickly get Telegram IDs. 

Whether you need a User ID, a Group/Channel ID, or the exact `file_id` of a Sticker (useful for bot development), this bot has you covered!

---

## 🌟 Features

- 👤 **User IDs:** Get your own ID or reply to a user to get theirs.
- 👥 **Group IDs:** Get the ID of the current group.
- 📢 **Channel IDs:** Reply to a forwarded message from a channel to get the Channel ID (e.g., `-100123456789`).
- 🎟️ **Sticker IDs:** Reply to any sticker to get its exact `file_id` and `file_unique_id`.
- 📱 **Menu Button:** Automatically generates a built-in Telegram Menu Button for easy access to commands.
- 🐳 **Docker Ready:** Fully configured to be deployed on Render, Heroku, or any VPS using Docker.

---

## 🛠️ Commands

| Command | Description |
| :--- | :--- |
| `/start` | Starts the bot and displays the help menu. |
| `/id` | Gets the ID of the current chat, your User ID, or the replied user/channel. |
| `/stickerid` | (Reply to a sticker) Gets the `file_id` and `file_unique_id` of the sticker. |
| `/help` | Shows instructions on how to use the bot. |

---

## 🚀 Deployment (Render)

This bot is optimized for deployment on [Render.com](https://render.com/) using Docker.

### 1. Prerequisites
Before deploying, make sure you have:
1. An `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
2. A `BOT_TOKEN` from [@BotFather](https://t.me/BotFather) on Telegram.
3. A GitHub account.

### 2. Steps to Deploy
1. **Fork or Clone** this repository to your own GitHub account.
2. Go to the [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Background Worker**.
3. Connect your GitHub account and select this repository.
4. Set the **Environment** to **Docker**.
5. Scroll down to **Environment Variables** and add the following:

   | Key | Value |
   | :--- | :--- |
   | `API_ID` | Your API ID |
   | `API_HASH` | Your API Hash |
   | `BOT_TOKEN` | Your Bot Token |

6. Click **Create Background Worker**. Render will build the Docker container and start your bot automatically!

---

## 💻 Local Installation

If you want to run the bot locally on your computer or VPS instead of Render:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/YourRepoName.git
   cd YourRepoName