"""
YouTube Downloader Module
Handles YouTube video downloading and conversion to MP3
"""
import os
import re
from pathlib import Path
from pytubefix import YouTube
from pydub import AudioSegment
import tempfile


def validate_youtube_url(url):
    """
    Validate if the URL is a valid YouTube URL
    
    Args:
        url: String URL to validate
        
    Returns:
        Boolean indicating if URL is valid
    """
    if not url or not isinstance(url, str):
        return False
    
    # YouTube URL patterns
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url.strip()):
            return True
    
    return False


def get_youtube_info(url):
    """
    Get YouTube video information
    
    Args:
        url: YouTube video URL
        
    Returns:
        Tuple: (success, info_dict, error_message)
    """
    try:
        yt = YouTube(url)
        
        info = {
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'views': yt.views,
            'description': yt.description[:200] + "..." if len(yt.description) > 200 else yt.description,
            'thumbnail_url': yt.thumbnail_url,
            'video_id': yt.video_id
        }
        
        return True, info, None
    except Exception as e:
        # Return error information
        return False, None, str(e)


def download_youtube_audio(url, dest_folder, progress_callback=None):
    """
    Download YouTube video and convert to MP3
    
    Args:
        url: YouTube video URL
        dest_folder: Destination folder for the MP3 file
        progress_callback: Function to call with progress updates
        
    Returns:
        Tuple: (success: bool, file_path: str, message: str)
    """
    try:
        if progress_callback:
            progress_callback("Video bilgileri alınıyor...")
        
        # Create YouTube object
        yt = YouTube(url)
        
        # Get video info
        title = sanitize_filename(yt.title)
        
        if progress_callback:
            progress_callback(f"İndiriliyor: {title[:30]}...")
        
        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not audio_stream:
            return False, "", "Ses akışı bulunamadı"
        
        # Create destination directory
        os.makedirs(dest_folder, exist_ok=True)
        
        # Download to temporary file first
        with tempfile.TemporaryDirectory() as temp_dir:
            if progress_callback:
                progress_callback("Ses dosyası indiriliyor...")
            
            # Download the audio
            temp_file = audio_stream.download(output_path=temp_dir)
            
            if progress_callback:
                progress_callback("MP3'e dönüştürülüyor...")
            
            # Convert to MP3
            output_filename = f"{title}.mp3"
            output_path = os.path.join(dest_folder, output_filename)
            
            # Handle duplicate filenames
            counter = 1
            while os.path.exists(output_path):
                output_filename = f"{title} ({counter}).mp3"
                output_path = os.path.join(dest_folder, output_filename)
                counter += 1
            
            # Convert using pydub
            audio = AudioSegment.from_file(temp_file)
            audio.export(
                output_path,
                format="mp3",
                bitrate="192k",
                parameters=["-q:a", "2"]
            )
        
        if progress_callback:
            progress_callback("Tamamlandı!")
        
        return True, output_path, f"Başarıyla indirildi: {output_filename}"
        
    except Exception as e:
        error_msg = f"İndirme hatası: {str(e)}"
        if progress_callback:
            progress_callback(error_msg)
        return False, "", error_msg


def sanitize_filename(filename):
    """
    Sanitize filename for safe file system usage
    
    Args:
        filename: Original filename string
        
    Returns:
        Sanitized filename string
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove extra spaces and dots
    filename = re.sub(r'\s+', ' ', filename.strip())
    filename = filename.strip('.')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename


def format_duration(seconds):
    """
    Format duration from seconds to human readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "3:45" or "1:23:45")
    """
    if not seconds:
        return "0:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def get_video_quality_info(url):
    """
    Get available quality options for a YouTube video
    
    Args:
        url: YouTube video URL
        
    Returns:
        List of available streams with quality info
    """
    try:
        yt = YouTube(url)
        streams = []
        
        # Get audio streams
        for stream in yt.streams.filter(only_audio=True):
            streams.append({
                'type': 'audio',
                'quality': stream.abr,
                'format': stream.mime_type,
                'filesize': stream.filesize
            })
        
        return streams
    except Exception as e:
        # Silently handle error to avoid console output
        return []
