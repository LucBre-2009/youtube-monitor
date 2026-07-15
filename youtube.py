import os
import json
import requests
import feedparser
from datetime import datetime
from zoneinfo import ZoneInfo


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

CHANNEL_FILE = "channels.json"
MESSAGE_FILE = "data/message.json"
VIDEOS_FILE = "data/videos.json"


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_latest_video(channel_id):

    url = (
        "https://www.youtube.com/feeds/videos.xml?"
        f"channel_id={channel_id}"
    )

    feed = feedparser.parse(url)

    if not feed.entries:
        return None

    for video in feed.entries:

        video_link = video.link

        # Shorts überspringen
        if "/shorts/" in video_link:
            continue

        return {
            "id": video.yt_videoid,
            "title": video.title,
            "link": video_link
        }

    return None


def create_embed(videos, note=None):

    description = ""

    if note:
        description += f"⚠️ **Hinweis:** {note}\n\n"

    if not videos:
        description += "Keine neuen Videos gefunden."

    else:
        for v in videos:
            description += (
                f"📺 **{v['channel']}**\n"
                f"🎬 {v['title']}\n"
                f"🔗 {v['link']}\n\n"
            )


    now = datetime.now(
        ZoneInfo("Europe/Berlin")
    )

    last_run = now.strftime(
        "%d.%m.%Y %H:%M Uhr"
    )


    return {
        "embeds": [
            {
                "title": "📺 YouTube Monitor",
                "description": description,
                "color": 16711680,
                "footer": {
                    "text": f"Letzter Check: {last_run}"
                }
            }
        ]
    }


def send_message(payload):

    r = requests.post(
        WEBHOOK + "?wait=true",
        json=payload
    )

    r.raise_for_status()

    return r.json()["id"]


def edit_message(message_id, payload):

    url = (
        WEBHOOK
        + f"/messages/{message_id}"
    )

    r = requests.patch(
        url,
        json=payload
    )

    return r.status_code == 200



def main():

    channels = load(CHANNEL_FILE)
    old_videos = load(VIDEOS_FILE)
    message = load(MESSAGE_FILE)


    new_videos = []


    for channel in channels:

        latest = get_latest_video(channel["id"])

        if not latest:
            continue


        latest["channel"] = channel["name"]


        if old_videos.get(channel["id"]) != latest["id"]:

            new_videos.append(latest)

            old_videos[channel["id"]] = latest["id"]



    payload = create_embed(
        new_videos
    )


    message_id = message.get("message_id")


    if message_id:

        success = edit_message(
            message_id,
            payload
        )

        if not success:

            payload = create_embed(
                new_videos,
                "Neue Nachricht erstellt, weil die alte Discord-Nachricht nicht mehr erreichbar war."
            )

            message_id = send_message(payload)

            message["message_id"] = message_id


    else:

        payload = create_embed(
            new_videos,
            "Erste Nachricht erstellt, weil keine Message-ID vorhanden war."
        )

        message_id = send_message(payload)

        message["message_id"] = message_id



    save(
        VIDEOS_FILE,
        old_videos
    )

    save(
        MESSAGE_FILE,
        message
    )


if __name__ == "__main__":
    main()