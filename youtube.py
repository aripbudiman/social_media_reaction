from googleapiclient.discovery import build
import re
import emoji
import pandas as pd
from datetime import datetime

class YoutubeScraper:
    def __init__(self, url):
        self.url = url
        self.API_KEY='AIzaSyAWvEz_0UFsgCAFQlIZ7UKGQ8pJm-JPKPk'
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)

    def process(self):
        match = re.search(r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})(?:\?|&|$)', self.url)
        if match:
            video_id = match.group(1)
            print(f"✅ Video ID: {video_id}")
        else:
            print("❌ Invalid YouTube URL format.")
            video_id = None

        if not video_id:
            exit()
        # =====================================================
        # AMBIL METADATA VIDEO
        # =====================================================
        print("\n🔄 Mengambil metadata video...")
        video_response = self.youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        # Extract informasi video
        video_data = video_response['items'][0]
        video_snippet = video_data['snippet']
        video_statistics = video_data['statistics']

        # Video metadata
        video_title = video_snippet['title']
        video_description = video_snippet['description']
        uploader_channel_id = video_snippet['channelId']
        uploader_channel_name = video_snippet['channelTitle']
        video_published_at = video_snippet['publishedAt']
        video_tags = video_snippet.get('tags', [])

        # Video statistics
        view_count = video_statistics.get('viewCount', 0)
        like_count = video_statistics.get('likeCount', 0)
        comment_count = video_statistics.get('commentCount', 0)

        # =====================================================
        # AMBIL SEMUA KOMENTAR (LENGKAP)
        # =====================================================
        print("\n🔄 Mengambil komentar...")
        comments = []
        nextPageToken = None
        max_comments = 12000  # Batas maksimal komentar yang diambil

        while len(comments) < max_comments:
            try:
                request = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=nextPageToken,
                    textFormat='plainText'
                )
                response = request.execute()
                
                for item in response['items']:
                    # Top level comment
                    top_comment = item['snippet']['topLevelComment']['snippet']
                    
                    # Skip jika komentar dari uploader
                    if top_comment.get('authorChannelId', {}).get('value') != uploader_channel_id:
                        comment_data = {
                            'comment_id': item['snippet']['topLevelComment']['id'],
                            'author': top_comment['authorDisplayName'],
                            'author_channel_id': top_comment.get('authorChannelId', {}).get('value', ''),
                            'text': top_comment['textDisplay'],
                            'text_original': top_comment['textOriginal'],
                            'published_at': top_comment['publishedAt'],
                            'updated_at': top_comment['updatedAt'],
                            'like_count': top_comment['likeCount'],
                            'reply_count': item['snippet']['totalReplyCount'],
                            'is_reply': False,
                            'parent_id': None
                        }
                        comments.append(comment_data)
                        
                        # Ambil replies jika ada
                        if 'replies' in item:
                            for reply in item['replies']['comments']:
                                reply_snippet = reply['snippet']
                                
                                # Skip jika reply dari uploader
                                if reply_snippet.get('authorChannelId', {}).get('value') != uploader_channel_id:
                                    reply_data = {
                                        'comment_id': reply['id'],
                                        'author': reply_snippet['authorDisplayName'],
                                        'author_channel_id': reply_snippet.get('authorChannelId', {}).get('value', ''),
                                        'text': reply_snippet['textDisplay'],
                                        'text_original': reply_snippet['textOriginal'],
                                        'published_at': reply_snippet['publishedAt'],
                                        'updated_at': reply_snippet['updatedAt'],
                                        'like_count': reply_snippet['likeCount'],
                                        'reply_count': 0,
                                        'is_reply': True,
                                        'parent_id': item['snippet']['topLevelComment']['id']
                                    }
                                    comments.append(reply_data)
                
                print(f"   Collected: {len(comments)} comments...", end='\r')
                
                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    break
                    
            except Exception as e:
                print(f"\n⚠️  Error: {e}")
                break

        print(f"\n✅ Total komentar terkumpul: {len(comments)}")

        # =====================================================
        # CONVERT KE DATAFRAME
        # =====================================================
        df_raw = pd.DataFrame(comments)

        # Tambahkan metadata video
        df_raw['video_id'] = video_id
        df_raw['video_title'] = video_title
        df_raw['video_url'] = self.url
        df_raw['channel_name'] = uploader_channel_name
        df_raw['scrape_datetime'] = datetime.now()

        print("\n📊 Sample data (5 komentar pertama):")
        print(df_raw[['author', 'text', 'like_count', 'reply_count', 'published_at']].head())

        # =====================================================
        # FILTER KOMENTAR (REMOVE SPAM, HYPERLINK, EMOJI-ONLY)
        # =====================================================
        print("\n🔄 Menyaring komentar...")

        hyperlink_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )

        threshold_ratio = 0.65
        filtered_comments = []

        for idx, row in df_raw.iterrows():
            comment_text = row['text'].lower().strip()
            emojis = emoji.emoji_count(comment_text)
            text_characters = len(re.sub(r'\s', '', comment_text))
            
            # Filter conditions
            has_alphanumeric = any(char.isalnum() for char in comment_text)
            has_no_hyperlink = not hyperlink_pattern.search(comment_text)
            
            # Emoji ratio check
            if text_characters == 0:
                emoji_ratio = 0
            else:
                emoji_ratio = text_characters / (text_characters + emojis)
            
            # Apply filters
            if has_alphanumeric and has_no_hyperlink:
                if emojis == 0 or emoji_ratio > threshold_ratio:
                    filtered_comments.append(row)

        df_filtered = pd.DataFrame(filtered_comments)

        print(f"✅ Komentar setelah filtering: {len(df_filtered)}")
        print(f"   Removed: {len(df_raw) - len(df_filtered)} comments ({(len(df_raw) - len(df_filtered))/len(df_raw)*100:.1f}%)")

        # =====================================================
        # TAMBAHKAN FITUR TAMBAHAN
        # =====================================================
        print("\n🔄 Menambahkan fitur tambahan...")

        # Parse datetime
        df_filtered['published_datetime'] = pd.to_datetime(df_filtered['published_at'])
        df_filtered['published_date'] = df_filtered['published_datetime'].dt.date
        df_filtered['published_hour'] = df_filtered['published_datetime'].dt.hour
        df_filtered['day_of_week'] = df_filtered['published_datetime'].dt.dayofweek

        # Text features
        df_filtered['text_length'] = df_filtered['text'].apply(len)
        df_filtered['word_count'] = df_filtered['text'].apply(lambda x: len(str(x).split()))
        df_filtered['has_question'] = df_filtered['text'].apply(lambda x: 1 if '?' in str(x) else 0)
        df_filtered['has_exclamation'] = df_filtered['text'].apply(lambda x: str(x).count('!'))
        df_filtered['is_caps'] = df_filtered['text'].apply(lambda x: 1 if str(x).isupper() else 0)

        # Engagement features
        df_filtered['engagement_score'] = df_filtered['like_count'] + df_filtered['reply_count']

        # Platform
        df_filtered['platform'] = 'youtube'

        print("✅ Fitur tambahan berhasil ditambahkan")

        # =====================================================
        # SAVE DATA
        # =====================================================
        print("\n💾 Menyimpan data...")

        # Save semua data (raw)
        df_raw.to_csv('data/raw/youtube_comments_raw.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Raw data saved: youtube_comments_raw.csv ({len(df_raw)} comments)")

        # Save filtered data
        df_filtered.to_csv('data/filtered/youtube_comments_filtered.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Filtered data saved: youtube_comments_filtered.csv ({len(df_filtered)} comments)")

        # Save metadata video
        video_metadata = {
            'video_id': [video_id],
            'video_title': [video_title],
            'video_url': [self.url],
            'channel_id': [uploader_channel_id],
            'channel_name': [uploader_channel_name],
            'published_at': [video_published_at],
            'view_count': [view_count],
            'like_count': [like_count],
            'comment_count': [comment_count],
            'tags': [', '.join(video_tags)],
            'description': [video_description],
            'scrape_datetime': [datetime.now()]
        }
        df_metadata = pd.DataFrame(video_metadata)
        df_metadata.to_json(
            'data/metadata/youtube_video_metadata.json', 
            orient='records',
            force_ascii=False,
            indent=2
            )
        print(f"✅ Video metadata saved: youtube_video_metadata.json")