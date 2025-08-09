"""
Audio Converter Module
Handles audio file detection and batch conversion to MP3
"""
import os
from pathlib import Path
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError


def find_audio_files(source_folder, dest_folder):
    """
    Find all audio files in the source folder
    Returns list of dictionaries with file information
    """
    if not os.path.exists(source_folder):
        return []
    
    # Supported audio formats
    supported_formats = {'.m4a', '.mp4', '.wav', '.flac', '.aac', '.ogg', '.wma'}
    
    files_data = []
    source_path = Path(source_folder)
    dest_path = Path(dest_folder)
    
    for file_path in source_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            # Generate output filename
            output_name = file_path.stem + '.mp3'
            output_path = dest_path / output_name
            
            # Check if already exists
            exists = output_path.exists()
            
            files_data.append({
                'source': str(file_path),
                'dest': str(output_path),
                'filename': file_path.name,
                'output_name': output_name,
                'size': file_path.stat().st_size,
                'exists': exists
            })
    
    return files_data


def batch_convert_audio(files_data, progress_callback=None):
    """
    Convert multiple audio files to MP3
    
    Args:
        files_data: List of file dictionaries from find_audio_files()
        progress_callback: Function to call with progress updates
                          callback(converted_count, total_count, filename, success)
    
    Returns:
        Dictionary with conversion results
    """
    if not files_data:
        return {'success': 0, 'failed': 0, 'skipped': 0, 'errors': []}
    
    results = {'success': 0, 'failed': 0, 'skipped': 0, 'errors': []}
    total_files = len(files_data)
    
    for i, file_info in enumerate(files_data):
        source_path = file_info['source']
        dest_path = file_info['dest']
        filename = file_info['filename']
        
        try:
            # Skip if output already exists
            if file_info['exists']:
                results['skipped'] += 1
                if progress_callback:
                    progress_callback(i + 1, total_files, f"Atlandı: {filename}", True)
                continue
            
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Load and convert audio file
            if progress_callback:
                progress_callback(i + 1, total_files, f"Dönüştürülüyor: {filename}", None)
            
            audio = AudioSegment.from_file(source_path)
            
            # Export as MP3 with good quality
            audio.export(
                dest_path,
                format="mp3",
                bitrate="192k",
                parameters=["-q:a", "2"]  # High quality
            )
            
            results['success'] += 1
            if progress_callback:
                progress_callback(i + 1, total_files, f"Tamamlandı: {filename}", True)
                
        except CouldntDecodeError:
            error_msg = f"Desteklenmeyen format: {filename}"
            results['errors'].append(error_msg)
            results['failed'] += 1
            if progress_callback:
                progress_callback(i + 1, total_files, f"Hata: {filename}", False)
                
        except Exception as e:
            error_msg = f"Hata ({filename}): {str(e)}"
            results['errors'].append(error_msg)
            results['failed'] += 1
            if progress_callback:
                progress_callback(i + 1, total_files, f"Hata: {filename}", False)
    
    return results


def get_supported_formats():
    """Return list of supported audio formats"""
    return ['.m4a', '.mp4', '.wav', '.flac', '.aac', '.ogg', '.wma']


def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
