import pandas as pd
import os
import re
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from isodate import parse_duration
from setup_yt_channel_transcripts import G_Dev_Key, csv_zielverzeichnis, kanal_zielverzeichnis

# Kanalnamen aufgreifen

def get_channel_name(youtube, channel_id):
    response = youtube.channels().list(id=channel_id, part='snippet').execute()
    return response['items'][0]['snippet']['title']

# Videodetails für Webcrawler & Report

def get_video_details(youtube, channel_ids):
    all_video_details = {}
    for channel_id in channel_ids:
        details = []
        next_page_token = None
        while True:
            response = youtube.playlistItems().list(
                playlistId='UU' + channel_id[2:],
                part='contentDetails,snippet',
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in response['items']:
                video_id = item['contentDetails']['videoId']
                title = re.sub(r'[\\/*?:"<>|]', '', item['snippet']['title'])
                details.append((video_id, title))

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        all_video_details[get_channel_name(youtube, channel_id)] = details
    return all_video_details

# Videolängen für das Report

def get_video_length(youtube, video_id):
    response = youtube.videos().list(id=video_id, part='contentDetails').execute()
    duration = parse_duration(response['items'][0]['contentDetails']['duration'])
    return int(duration.total_seconds())

# Speicherung der Transkripte auf Ziel 

def save_transcripts(channel_name, transcripts):
    channel_path = os.path.join(kanal_zielverzeichnis, re.sub(r'[\\/*?:"<>|]', '', channel_name))
    if not os.path.exists(channel_path):
        os.makedirs(channel_path)
    for title, transcript in transcripts.items():
        filepath = os.path.join(channel_path, f"{title}.txt")
        with open(filepath, 'w', encoding='utf-8') as file:
            for item in transcript:
                file.write(f"{item['text']}\n")

# Update der Reporttabelle

def update_csv_alternative(channel_name, stats):
    csv_file_path = os.path.join(csv_zielverzeichnis, 'transcripts_overview.csv')
    
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        df = pd.DataFrame(columns=['channel_name'] + list(stats.keys()))

    channel_index = df[df['channel_name'] == channel_name].index
    if not channel_index.empty:
        # Kanalname existiert, aktualisiere die Daten
        for key, value in stats.items():
            df.at[channel_index[0], key] = value
    else:
        # Kanalname existiert nicht, füge eine neue Zeile hinzu
        new_row = pd.DataFrame([{**{'channel_name': channel_name}, **stats}])
        df = pd.concat([df, new_row], ignore_index=True, sort=False)

    df.to_csv(csv_file_path, index=False)

# eigentlicher Webcrawler

def process_channels(youtube, channel_ids):
    for channel_id in channel_ids:
        channel_name = get_channel_name(youtube, channel_id)
        video_details = get_video_details(youtube, [channel_id])
        transcripts = {}
        total_length_seconds = 0
        for video_id, title in video_details[channel_name]:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['de'])
                transcripts[title] = transcript
                video_length = get_video_length(youtube, video_id)
                total_length_seconds += video_length
            except Exception as e:
                print(f"Error getting transcript for video {title}: {e}")
        save_transcripts(channel_name, transcripts)

## Reporting

        if len(transcripts) > 0:
            words_total = sum(len(item['text'].split()) for transcript in transcripts.values() for item in transcript)
            mean_words_per_vid = words_total / len(transcripts)
            mean_vid_length = total_length_seconds / len(transcripts)
        else:
            mean_words_per_vid = 0
            mean_vid_length = 0
        stats = {
            'channel_name': channel_name, 'missing_transcripts': len(video_details[channel_name]) - len(transcripts),
            'transcribed': len(transcripts), 'vid_total': len(video_details[channel_name]),
            'words_total': words_total, 'mean_words_per_vid': mean_words_per_vid,
            'vid_length_in_seconds': total_length_seconds, 'mean_vid_length': mean_vid_length
        }
        update_csv_alternative(channel_name, stats)

youtube = build('youtube', 'v3', developerKey=G_Dev_Key)
channel_ids = ['UC0-HCgDgEkQS8iwlaKVMIzQ', 'UCgvFsn6bRKqND1cW3HpzDrA', 'UCjSkyrjqPeMwubZU0CnScXA', 'UCq2rogaxLtQFrYG3X3KYNww', 'UChkELlk5GBaUCVx8-94IK_Q', 'UCcoQ3WG2J_Xjwwyt-sJqh-w', 'UCXJBRgiZRZvfilIGQ4wN5CQ'] 
process_channels(youtube, channel_ids)