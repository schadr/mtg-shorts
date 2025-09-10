import argparse
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from datetime import datetime, timedelta


# Scopes for YouTube Data API
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.readonly'
]



def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file('youtube_client_secret.json', SCOPES)
    credentials = None
    if os.path.exists('youtube_token.pickle'):
        with open('youtube_token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            credentials = flow.run_local_server(port=0)
        with open('youtube_token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

# categoryId '20' corresponds to 'Gaming'
def upload_video(file_path, title, description, tags=None, categoryId='20', schedule_time_str=None, youtube=None):
    if youtube is None:
        youtube = authenticate_youtube()
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags if tags else [],
            'categoryId': categoryId,
            'scheduledStartTime': schedule_time_str  # ISO 8601 format, adjust time as needed
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': schedule_time_str  # ISO 8601 format, adjust time as needed
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    return f"https://youtu.be/{response['id']}"


def list_unpublished_shorts(youtube=None, max_results=50):
    if youtube is None:
        youtube = authenticate_youtube()
    request = youtube.search().list(
        part='snippet',
        forMine=True,  # Important for retrieving your own videos
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    shorts = []
    for item in response.get('items', []):
        video_id = item['id'].get('videoId')
        if not video_id:
            continue
        video_request = youtube.videos().list(
            part='snippet,status',
            id=video_id
        )
        video_response = video_request.execute()
        for video_item in video_response.get('items', []):
            status = video_item.get('status', {})
            snippet = video_item.get('snippet', {})
            # Check if scheduled (private + publishAt set)
            if status.get('privacyStatus') == 'private' and status.get('publishAt'):
                shorts.append({
                    'videoId': video_id,
                    'title': snippet.get('title'),
                    'publishAt': status.get('publishAt')
                })
                print(status.get('publishAt'))
    return shorts

def get_latest_scheduled_short_time(youtube=None, channel_id='UCj9ARMe6eplrcHWLfHg9EBA', max_results=50):
    shorts = list_unpublished_shorts(youtube, max_results)
    if not shorts:
        return None
    latest_short = max(shorts, key=lambda x: x['publishAt'])
    return latest_short['publishAt']

def upload_videos(folder="", set_name="", booster_type="", set_tag="", extra_text="", box_number=1, full_video_file=""):
    pack_total = 0
    pack_number = 0
    
    mp4_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
    pack_total = len(mp4_files)
    if full_video_file:
        pack_total -= 1

    youtube = authenticate_youtube()
    last_video_time = get_latest_scheduled_short_time(youtube)  
    # upload full_video_file first if provided
    full_video_link = None
    if full_video_file:
        full_video_path = os.path.join(folder, full_video_file)
        title = f"{set_name} - {pack_total} packs - {box_number}"
        description = f"Opening a Magic The Gathering {set_name} {booster_type} booster box {box_number}.\
        \
        \
        {set_tag} #mtg #magicthegathering #unboxing #tcg #tradingcards"
        # Parse last_video_time, add one hour, and convert back to ISO string
        dt = datetime.strptime(last_video_time, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=1)
        schedule_time = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        full_video_link = upload_video(full_video_path, title, description, tags=None, schedule_time_str=schedule_time, youtube=youtube)
  
    # upload all other videos
    for video_file in mp4_files:
        if video_file == full_video_file:
            continue
        pack_number += 1
        video_path = os.path.join(folder, video_file)

        extra_text_full = f"\nFull video at {full_video_link}\n\n" + extra_text

        description = f"Opening a Magic The Gathering {set_name} {booster_type} booster.\
        {extra_text_full}\
        \
        \
        {set_tag} #mtg #magicthegathering #unboxing #tcg #tradingcards"
        title = f"{set_tag} {booster_type} booster {pack_number} / {pack_total} of box {box_number}"

        dt = datetime.strptime(last_video_time, "%Y-%m-%dT%H:%M:%SZ")
        if dt.strftime("%H:%M:%SZ") == "19:00:00Z":
            dt += timedelta(hours=7)
        else:
            dt += timedelta(hours=17)
        last_video_time = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        upload_video(video_path, title, description, tags=[set_tag, "mtg", "magicthegathering", "unboxing", "tcg", "tradingcards"], schedule_time_str=last_video_time, youtube=youtube)

def main():
    parser = argparse.ArgumentParser(description="Config merge CLI")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('input_folder', help='Path to the input file')
    parser.add_argument('--full-video', type=str, help='Path to the full video file among the fildes in the folder')
    parser.add_argument('--set-name', type=str, required=True, help='Name of the set being opened')
    parser.add_argument('--booster-type', type=str, choices=['play', 'collector'], required=True, help='Type of booster being opened')
    parser.add_argument('--set-tag', type=str, required=True, help='Hashtag for the set being opened')
    parser.add_argument('--extra-text', type=str, default="", help='Extra text to include in the description, e.g. link to full video')
    parser.add_argument('--box-number', type=str, required=True, help='Box number being opened')

    args = parser.parse_args()
    set_name = args.set_name
    booster_type = args.booster_type
    set_tag = args.set_tag
    extra_text = args.extra_text 
    box_number = args.box_number
    folder = args.input_folder
    full_video_file = args.full_video
    mp4_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
    upload_videos(folder, set_name, booster_type, set_tag, extra_text, box_number, full_video_file)

if __name__ == "__main__":
    main()