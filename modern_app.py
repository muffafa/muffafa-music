"""
Modern Audio Converter - Portable Tkinter Application
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import sys

# Import audioop fallback for Windows PyInstaller compatibility
try:
    import audioop_fallback
except ImportError:
    pass  # Fallback not needed if audioop works normally

# Import our modular components
from audio_converter import find_audio_files, batch_convert_audio
from youtube_downloader import (
    validate_youtube_url, 
    get_youtube_info, 
    download_youtube_audio,
    format_duration
)


class ModernAudioConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.create_ui()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("🎵 Modern Audio Converter")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"900x600+{x}+{y}")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        
    def setup_variables(self):
        """Initialize variables"""
        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.youtube_url = tk.StringVar()
        self.youtube_dest = tk.StringVar()
        self.status_text = tk.StringVar(value="Hazır")
        
        self.converting = False
        self.downloading = False
        self.files_data = []
        self.youtube_queue = []  # Queue for YouTube videos
        self.current_youtube_index = 0  # Current video being downloaded
        
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 Modern Audio Converter", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_batch_tab()
        self.create_youtube_tab()
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        ttk.Label(status_frame, text="Durum:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_frame, textvariable=self.status_text)
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
    def create_batch_tab(self):
        """Create batch conversion tab"""
        batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(batch_frame, text="📁 Toplu Dönüştürme")
        
        # Configure grid
        batch_frame.columnconfigure(1, weight=1)
        batch_frame.rowconfigure(3, weight=1)
        
        # Folder selection
        ttk.Label(batch_frame, text="Kaynak Klasör:", 
                 style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        folder_frame = ttk.Frame(batch_frame)
        folder_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(0, weight=1)
        
        self.source_entry = ttk.Entry(folder_frame, textvariable=self.source_folder)
        self.source_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(folder_frame, text="Seç", 
                  command=self.choose_source_folder).grid(row=0, column=1)
        
        # Destination folder
        ttk.Label(batch_frame, text="Hedef Klasör:", 
                 style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        dest_frame = ttk.Frame(batch_frame)
        dest_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        dest_frame.columnconfigure(0, weight=1)
        
        self.dest_entry = ttk.Entry(dest_frame, textvariable=self.dest_folder)
        self.dest_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(dest_frame, text="Seç", 
                  command=self.choose_dest_folder).grid(row=0, column=1)
        
        # Buttons
        button_frame = ttk.Frame(batch_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.scan_btn = ttk.Button(button_frame, text="🔍 Dosyaları Tara", 
                                  command=self.scan_files)
        self.scan_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.convert_btn = ttk.Button(button_frame, text="🚀 Dönüştür", 
                                     command=self.start_conversion, state='disabled')
        self.convert_btn.grid(row=0, column=1)
        
        # File list
        list_frame = ttk.Frame(batch_frame)
        list_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for file list
        columns = ('file', 'duration', 'status', 'progress')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        self.file_tree.heading('file', text='Dosya Adı')
        self.file_tree.heading('duration', text='Süre')
        self.file_tree.heading('status', text='Durum')
        self.file_tree.heading('progress', text='İlerleme')
        
        self.file_tree.column('file', width=300)
        self.file_tree.column('duration', width=80)
        self.file_tree.column('status', width=120)
        self.file_tree.column('progress', width=100)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
    def create_youtube_tab(self):
        """Create YouTube download tab with queue system"""
        yt_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(yt_frame, text="📺 YouTube İndirici")
        
        # Configure grid
        yt_frame.columnconfigure(1, weight=1)
        yt_frame.rowconfigure(4, weight=1)
        
        # URL input
        ttk.Label(yt_frame, text="YouTube URL:", 
                 style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        url_frame = ttk.Frame(yt_frame)
        url_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.youtube_url)
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        self.url_entry.bind('<Return>', self.add_to_youtube_queue)
        
        self.add_url_btn = ttk.Button(url_frame, text="➕ Kuyruğa Ekle", 
                                     command=self.add_to_youtube_queue, state='disabled')
        self.add_url_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Destination folder
        ttk.Label(yt_frame, text="İndirme Klasörü:", 
                 style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        yt_dest_frame = ttk.Frame(yt_frame)
        yt_dest_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        yt_dest_frame.columnconfigure(0, weight=1)
        
        self.yt_dest_entry = ttk.Entry(yt_dest_frame, textvariable=self.youtube_dest)
        self.yt_dest_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(yt_dest_frame, text="Seç", 
                  command=self.choose_youtube_dest).grid(row=0, column=1)
        
        # Queue list
        queue_frame = ttk.LabelFrame(yt_frame, text="İndirme Kuyruğu", padding="10")
        queue_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        queue_frame.columnconfigure(0, weight=1)
        queue_frame.rowconfigure(0, weight=1)
        
        # Treeview for YouTube queue
        yt_columns = ('title', 'duration', 'channel', 'status', 'progress')
        self.youtube_tree = ttk.Treeview(queue_frame, columns=yt_columns, show='headings', height=8)
        
        self.youtube_tree.heading('title', text='Video Başlığı')
        self.youtube_tree.heading('duration', text='Süre')
        self.youtube_tree.heading('channel', text='Kanal')
        self.youtube_tree.heading('status', text='Durum')
        self.youtube_tree.heading('progress', text='İlerleme')
        
        self.youtube_tree.column('title', width=300)
        self.youtube_tree.column('duration', width=80)
        self.youtube_tree.column('channel', width=150)
        self.youtube_tree.column('status', width=120)
        self.youtube_tree.column('progress', width=100)
        
        self.youtube_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind selection event
        self.youtube_tree.bind('<<TreeviewSelect>>', self.on_youtube_tree_select)
        
        # Scrollbar for YouTube treeview
        yt_scrollbar = ttk.Scrollbar(queue_frame, orient=tk.VERTICAL, command=self.youtube_tree.yview)
        yt_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.youtube_tree.configure(yscrollcommand=yt_scrollbar.set)
        
        # Queue control buttons
        queue_btn_frame = ttk.Frame(yt_frame)
        queue_btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.clear_queue_btn = ttk.Button(queue_btn_frame, text="🗑️ Kuyruğu Temizle", 
                                         command=self.clear_youtube_queue, state='disabled')
        self.clear_queue_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.remove_selected_btn = ttk.Button(queue_btn_frame, text="❌ Seçileni Kaldır", 
                                             command=self.remove_selected_youtube, state='disabled')
        self.remove_selected_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.download_queue_btn = ttk.Button(queue_btn_frame, text="🚀 Kuyruğu İndir", 
                                            command=self.start_youtube_queue_download, state='disabled')
        self.download_queue_btn.grid(row=0, column=2)
        
        # Progress bar for YouTube queue download
        self.yt_progress = ttk.Progressbar(yt_frame, mode='determinate')
        self.yt_progress.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # YouTube status
        self.yt_status = ttk.Label(yt_frame, text="Kuyruğa video eklemek için YouTube URL'si girin")
        self.yt_status.grid(row=7, column=0, columnspan=2)
        
    def choose_source_folder(self):
        """Choose source folder"""
        folder = filedialog.askdirectory(title="Kaynak Klasörü Seç")
        if folder:
            self.source_folder.set(folder)
            
    def choose_dest_folder(self):
        """Choose destination folder"""
        folder = filedialog.askdirectory(title="Hedef Klasörü Seç")
        if folder:
            self.dest_folder.set(folder)
            
    def choose_youtube_dest(self):
        """Choose YouTube destination folder"""
        folder = filedialog.askdirectory(title="İndirme Klasörü Seçin")
        if folder:
            self.youtube_dest.set(folder)
            # Update queue buttons if there are items
            self.update_youtube_queue_buttons()
            
    def scan_files(self):
        """Scan for audio files"""
        source = self.source_folder.get()
        dest = self.dest_folder.get()
        
        if not source or not dest:
            messagebox.showwarning("Uyarı", "Lütfen kaynak ve hedef klasörlerini seçin.")
            return
            
        self.status_text.set("Dosyalar taranıyor...")
        
        # Clear previous results
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        self.files_data = find_audio_files(source, dest)
        
        if self.files_data:
            convertible_count = 0
            for file_info in self.files_data:
                # Extract information from dictionary
                fname = file_info['filename']
                exists = file_info['exists']
                size = file_info['size']
                
                # Format file size
                size_mb = size / (1024 * 1024)
                size_str = f"{size_mb:.1f} MB"
                
                # Determine status
                status = "Zaten var" if exists else "Dönüştürülecek"
                
                # Insert into treeview
                item_id = self.file_tree.insert('', 'end', values=(fname, size_str, status, ''))
                if status == "Dönüştürülecek":
                    convertible_count += 1
                    
            self.status_text.set(f"{len(self.files_data)} dosya bulundu, {convertible_count} dönüştürülecek")
            
            if convertible_count > 0:
                self.convert_btn.config(state='normal')
            else:
                self.convert_btn.config(state='disabled')
        else:
            self.status_text.set("Desteklenen ses dosyası bulunamadı")
            messagebox.showinfo("Bilgi", "Desteklenen ses dosyası bulunamadı.\n\nDesteklenen formatlar: .m4a, .mp4, .wav, .flac, .aac")
            
    def start_conversion(self):
        """Start batch conversion"""
        if self.converting:
            return
            
        self.converting = True
        self.convert_btn.config(state='disabled')
        self.scan_btn.config(state='disabled')
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self.convert_files, daemon=True)
        thread.start()
        
    def convert_files(self):
        """Convert files in background thread"""
        def progress_callback(converted, total, filename, success):
            # Update UI in main thread
            self.root.after(0, self.update_conversion_progress, converted, total, filename, success)
            
        try:
            results = batch_convert_audio(self.files_data, progress_callback)
            
            # Update UI when done
            self.root.after(0, self.conversion_complete, results)
            
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))
            
    def update_conversion_progress(self, converted, total, filename, success):
        """Update conversion progress in UI"""
        progress = f"{converted}/{total}"
        status = "✅ Tamamlandı" if success else "❌ Hata"
        
        # Find and update the item in treeview
        for item in self.file_tree.get_children():
            values = self.file_tree.item(item, 'values')
            if values[0] == filename:
                self.file_tree.item(item, values=(values[0], values[1], status, progress))
                break
                
        self.status_text.set(f"Dönüştürülüyor: {filename} ({progress})")
        
    def conversion_complete(self, results):
        """Handle conversion completion"""
        self.converting = False
        self.convert_btn.config(state='normal')
        self.scan_btn.config(state='normal')
        
        # Results is now a dictionary from batch_convert_audio
        success_count = results['success']
        failed_count = results['failed']
        skipped_count = results['skipped']
        total_count = success_count + failed_count + skipped_count
        
        self.status_text.set(f"Tamamlandı: {success_count}/{total_count} dosya başarıyla dönüştürüldü")
        
        # Show detailed results
        if failed_count == 0:
            if skipped_count > 0:
                messagebox.showinfo("Başarılı", f"🎉 İşlem tamamlandı!\n\n✅ Dönüştürülen: {success_count}\n⏭️ Atlanan: {skipped_count}")
            else:
                messagebox.showinfo("Başarılı", f"🎉 Tüm dosyalar başarıyla dönüştürüldü!\n\n{success_count}/{total_count} dosya")
        else:
            error_details = "\n".join(results['errors'][:3])  # Show first 3 errors
            if len(results['errors']) > 3:
                error_details += f"\n... ve {len(results['errors']) - 3} hata daha"
            
            messagebox.showwarning("Kısmen Başarılı", 
                                 f"⚠️ İşlem tamamlandı:\n\n"
                                 f"✅ Başarılı: {success_count}\n"
                                 f"❌ Başarısız: {failed_count}\n"
                                 f"⏭️ Atlanan: {skipped_count}\n\n"
                                 f"Hatalar:\n{error_details}")
            
    def conversion_error(self, error_msg):
        """Handle conversion error"""
        self.converting = False
        self.convert_btn.config(state='normal')
        self.scan_btn.config(state='normal')
        self.status_text.set("Hata oluştu")
        messagebox.showerror("Hata", f"Dönüştürme sırasında hata oluştu:\n{error_msg}")
        
    def on_url_change_old(self, event=None):
        """Handle URL change (old method - deprecated)"""
        # This method is no longer used with the queue system
        pass
        

            
    def get_video_info(self):
        """Get YouTube video information"""
        url = self.youtube_url.get()
        if not validate_youtube_url(url):
            return
            
        self.info_btn.config(state='disabled')
        self.yt_status.config(text="Video bilgileri alınıyor...")
        
        # Get info in separate thread
        thread = threading.Thread(target=self.fetch_video_info, args=(url,), daemon=True)
        thread.start()
        
    def fetch_video_info(self, url):
        """Fetch video info in background"""
        try:
            success, info, error = get_youtube_info(url)
            self.root.after(0, self.display_video_info, success, info, error)
        except Exception as e:
            self.root.after(0, self.display_video_info, False, None, str(e))
            
    def display_video_info(self, success, info, error):
        """Display video information"""
        self.info_btn.config(state='normal')
        
        # Clear previous info
        for widget in self.info_frame.winfo_children():
            widget.destroy()
            
        if success and info:
            ttk.Label(self.info_frame, text="Başlık:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            ttk.Label(self.info_frame, text=info['title'][:60] + "..." if len(info['title']) > 60 else info['title']).grid(row=0, column=1, sticky=tk.W)
            
            ttk.Label(self.info_frame, text="Kanal:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
            ttk.Label(self.info_frame, text=info['author']).grid(row=1, column=1, sticky=tk.W)
            
            ttk.Label(self.info_frame, text="Süre:", font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
            ttk.Label(self.info_frame, text=format_duration(info['length'])).grid(row=2, column=1, sticky=tk.W)
            
            ttk.Label(self.info_frame, text="İzlenme:", font=('Arial', 9, 'bold')).grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
            ttk.Label(self.info_frame, text=f"{info['views']:,}").grid(row=3, column=1, sticky=tk.W)
            
            self.yt_status.config(text="✅ Video bilgileri alındı", foreground='green')
        else:
            ttk.Label(self.info_frame, text=f"❌ Hata: {error}", foreground='red').grid(row=0, column=0)
            self.yt_status.config(text="❌ Video bilgileri alınamadı", foreground='red')
            
    def start_youtube_download(self):
        """Start YouTube download"""
        url = self.youtube_url.get()
        dest = self.youtube_dest.get()
        
        if not validate_youtube_url(url) or not dest:
            messagebox.showwarning("Uyarı", "Lütfen geçerli bir URL ve indirme klasörü seçin.")
            return
            
        self.downloading = True
        self.download_btn.config(state='disabled')
        self.yt_progress.start()
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_youtube, args=(url, dest), daemon=True)
        thread.start()
        
    def download_youtube(self, url, dest):
        """Download YouTube video in background"""
        def progress_callback(message):
            self.root.after(0, self.update_download_status, message)
            
        try:
            success, file_path, message = download_youtube_audio(url, dest, progress_callback)
            self.root.after(0, self.download_complete, success, file_path, message)
        except Exception as e:
            self.root.after(0, self.download_complete, False, "", str(e))
            
    def update_download_status(self, message):
        """Update download status"""
        self.yt_status.config(text=f"📥 {message}", foreground='blue')
        
    def download_complete(self, success, file_path, message):
        """Handle download completion (old method - deprecated)"""
        # This method is no longer used with the queue system
        self.downloading = False
        self.yt_progress.stop()
        
        if success:
            self.yt_status.config(text=f"✅ {message}", foreground='green')
            messagebox.showinfo("Başarılı", f"🎉 Video başarıyla indirildi!\n\nDosya: {os.path.basename(file_path)}\nKonum: {file_path}")
        else:
            self.yt_status.config(text=f"❌ {message}", foreground='red')
    
    # YouTube Queue Management Methods
    def on_youtube_tree_select(self, event=None):
        """Handle YouTube tree selection changes"""
        self.update_youtube_queue_buttons()
    
    def on_url_change(self, event=None):
        """Handle URL entry changes"""
        url = self.youtube_url.get().strip()
        if validate_youtube_url(url):
            self.add_url_btn.config(state='normal')
        else:
            self.add_url_btn.config(state='disabled')
    
    def add_to_youtube_queue(self, event=None):
        """Add YouTube URL to download queue"""
        url = self.youtube_url.get().strip()
        dest = self.youtube_dest.get().strip()
        
        if not validate_youtube_url(url):
            messagebox.showwarning("Uyarı", "Lütfen geçerli bir YouTube URL'si girin.")
            return
            
        if not dest:
            messagebox.showwarning("Uyarı", "Lütfen indirme klasörü seçin.")
            return
        
        # Check if URL already in queue
        for item in self.youtube_queue:
            if item['url'] == url:
                messagebox.showwarning("Uyarı", "Bu video zaten kuyrukta!")
                return
        
        self.yt_status.config(text="Video bilgileri alınıyor...", foreground='blue')
        self.add_url_btn.config(state='disabled')
        
        # Get video info in background thread
        thread = threading.Thread(target=self.fetch_and_add_video, args=(url, dest), daemon=True)
        thread.start()
    
    def fetch_and_add_video(self, url, dest):
        """Fetch video info and add to queue"""
        try:
            success, info, error = get_youtube_info(url)
            self.root.after(0, self.add_video_to_queue, success, info, error, url, dest)
        except Exception as e:
            self.root.after(0, self.add_video_to_queue, False, None, str(e), url, dest)
    
    def add_video_to_queue(self, success, info, error, url, dest):
        """Add video to queue after getting info"""
        self.add_url_btn.config(state='normal')
        
        if success and info:
            # Check if file already exists in destination
            safe_title = self.sanitize_filename(info['title'])
            potential_filename = f"{safe_title}.mp3"
            full_path = os.path.join(dest, potential_filename)
            
            # Check for existing file
            if os.path.exists(full_path):
                response = messagebox.askyesno(
                    "Dosya Zaten Mevcut", 
                    f"'{potential_filename}' dosyası zaten mevcut!\n\n"
                    f"Konum: {dest}\n\n"
                    f"Yine de kuyruğa eklemek istiyor musunuz?"
                )
                if not response:
                    self.yt_status.config(text=f"❌ '{info['title'][:30]}...' zaten mevcut - eklenmedi", foreground='orange')
                    return
            
            # Add to queue
            queue_item = {
                'url': url,
                'dest': dest,
                'title': info['title'],
                'duration': format_duration(info['length']),
                'channel': info['author'],
                'status': 'Beklemede',
                'progress': '0%',
                'filename': potential_filename,
                'full_path': full_path
            }
            
            self.youtube_queue.append(queue_item)
            
            # Add to treeview
            self.youtube_tree.insert('', 'end', values=(
                queue_item['title'][:50] + '...' if len(queue_item['title']) > 50 else queue_item['title'],
                queue_item['duration'],
                queue_item['channel'][:20] + '...' if len(queue_item['channel']) > 20 else queue_item['channel'],
                queue_item['status'],
                queue_item['progress']
            ))
            
            # Clear URL entry
            self.youtube_url.set('')
            
            # Update button states
            self.update_youtube_queue_buttons()
            
            file_exists_msg = " (dosya mevcut - üzerine yazılacak)" if os.path.exists(full_path) else ""
            self.yt_status.config(text=f"✅ '{queue_item['title'][:30]}...' kuyruğa eklendi{file_exists_msg}", foreground='green')
        else:
            self.yt_status.config(text=f"❌ Video bilgileri alınamadı: {error}", foreground='red')
    
    def sanitize_filename(self, filename):
        """Sanitize filename for safe file system usage"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip(' .')
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename
    
    def update_youtube_queue_buttons(self):
        """Update YouTube queue button states"""
        has_items = len(self.youtube_queue) > 0
        has_selection = bool(self.youtube_tree.selection())
        
        self.clear_queue_btn.config(state='normal' if has_items and not self.downloading else 'disabled')
        self.remove_selected_btn.config(state='normal' if has_selection and not self.downloading else 'disabled')
        self.download_queue_btn.config(state='normal' if has_items and not self.downloading else 'disabled')
    
    def clear_youtube_queue(self):
        """Clear all items from YouTube queue"""
        if messagebox.askyesno("Onay", "Tüm kuyruğu temizlemek istediğinizden emin misiniz?"):
            self.youtube_queue.clear()
            self.youtube_tree.delete(*self.youtube_tree.get_children())
            self.update_youtube_queue_buttons()
            self.yt_status.config(text="Kuyruk temizlendi")
    
    def remove_selected_youtube(self):
        """Remove selected item from YouTube queue"""
        selection = self.youtube_tree.selection()
        if not selection:
            return
        
        # Get selected item index
        item = selection[0]
        index = self.youtube_tree.index(item)
        
        # Remove from queue and treeview
        if 0 <= index < len(self.youtube_queue):
            removed_item = self.youtube_queue.pop(index)
            self.youtube_tree.delete(item)
            self.update_youtube_queue_buttons()
            self.yt_status.config(text=f"'{removed_item['title'][:30]}...' kuyruktan kaldırıldı")
    
    def start_youtube_queue_download(self):
        """Start downloading YouTube queue with smart processing"""
        if not self.youtube_queue:
            return
        
        if not self.youtube_dest.get():
            messagebox.showwarning("Uyarı", "Lütfen indirme klasörü seçin.")
            return
        
        # Analyze queue to show summary
        total_items = len(self.youtube_queue)
        existing_files = 0
        new_downloads = 0
        failed_retries = 0
        
        for i, item in enumerate(self.youtube_queue):
            file_exists = os.path.exists(item.get('full_path', ''))
            tree_items = self.youtube_tree.get_children()
            
            if i < len(tree_items):
                current_status = self.youtube_tree.item(tree_items[i], 'values')[3]
                already_completed = '✅' in current_status
                is_failed = '❌' in current_status
                
                if file_exists and already_completed:
                    existing_files += 1
                elif is_failed:
                    failed_retries += 1
                else:
                    new_downloads += 1
            else:
                new_downloads += 1
        
        # Show summary dialog
        summary_msg = f"Kuyruk İşleme Özeti:\n\n"
        summary_msg += f"Toplam video: {total_items}\n"
        summary_msg += f"Zaten mevcut (atlanacak): {existing_files}\n"
        summary_msg += f"Yeni indirme: {new_downloads}\n"
        summary_msg += f"Hatalı (tekrar denenecek): {failed_retries}\n\n"
        
        if existing_files > 0:
            summary_msg += "Not: Zaten mevcut dosyalar atlanacak.\n"
        
        if new_downloads == 0 and failed_retries == 0:
            messagebox.showinfo("Bilgi", "Tüm dosyalar zaten mevcut. İndirilecek yeni dosya yok.")
            return
        
        summary_msg += f"\n{new_downloads + failed_retries} dosya işlenecek. Devam etmek istiyor musunuz?"
        
        if not messagebox.askyesno("Kuyruğu Başlat", summary_msg):
            return
        
        self.downloading = True
        self.current_youtube_index = 0
        self.yt_progress.config(mode='determinate', maximum=len(self.youtube_queue), value=0)
        self.update_youtube_queue_buttons()
        
        # Start processing queue
        self.download_next_youtube_video()
    
    def download_next_youtube_video(self):
        """Download next video in queue"""
        # Find next video that needs to be downloaded
        while self.current_youtube_index < len(self.youtube_queue):
            current_item = self.youtube_queue[self.current_youtube_index]
            tree_items = self.youtube_tree.get_children()
            
            if self.current_youtube_index < len(tree_items):
                item_id = tree_items[self.current_youtube_index]
                current_status = self.youtube_tree.item(item_id, 'values')[3]
                
                # Check if file already exists and was successfully downloaded
                file_exists = os.path.exists(current_item.get('full_path', ''))
                already_completed = '✅' in current_status
                
                if file_exists and already_completed:
                    # Skip this file - already downloaded successfully
                    values = list(self.youtube_tree.item(item_id, 'values'))
                    values[3] = '✅ Zaten Mevcut'
                    values[4] = '100%'
                    self.youtube_tree.item(item_id, values=values)
                    
                    self.yt_status.config(text=f"Atlanıyor: {current_item['title'][:40]}... (zaten mevcut)", foreground='orange')
                    
                    # Update progress and move to next
                    self.yt_progress.config(value=self.current_youtube_index + 1)
                    self.current_youtube_index += 1
                    
                    # Small delay before checking next item
                    self.root.after(500, self.download_next_youtube_video)
                    return
            
            # This item needs to be downloaded
            break
        
        if self.current_youtube_index >= len(self.youtube_queue):
            # All downloads complete
            self.youtube_queue_complete()
            return
        
        current_item = self.youtube_queue[self.current_youtube_index]
        
        # Update status in treeview
        tree_items = self.youtube_tree.get_children()
        if self.current_youtube_index < len(tree_items):
            item_id = tree_items[self.current_youtube_index]
            values = list(self.youtube_tree.item(item_id, 'values'))
            values[3] = 'İndiriliyor...'
            values[4] = '0%'
            self.youtube_tree.item(item_id, values=values)
        
        self.yt_status.config(text=f"İndiriliyor: {current_item['title'][:40]}...", foreground='blue')
        
        # Start download in background thread
        thread = threading.Thread(
            target=self.download_youtube_queue_item, 
            args=(current_item['url'], current_item['dest'], self.current_youtube_index), 
            daemon=True
        )
        thread.start()
    
    def download_youtube_queue_item(self, url, dest, index):
        """Download single YouTube video from queue"""
        def progress_callback(message):
            self.root.after(0, self.update_youtube_queue_progress, message, index)
        
        try:
            success, file_path, message = download_youtube_audio(url, dest, progress_callback)
            self.root.after(0, self.youtube_queue_item_complete, success, file_path, message, index)
        except Exception as e:
            self.root.after(0, self.youtube_queue_item_complete, False, "", str(e), index)
    
    def update_youtube_queue_progress(self, message, index):
        """Update progress for current YouTube download"""
        # Update treeview item progress
        tree_items = self.youtube_tree.get_children()
        if index < len(tree_items):
            item_id = tree_items[index]
            values = list(self.youtube_tree.item(item_id, 'values'))
            values[4] = '50%'  # Simple progress indication
            self.youtube_tree.item(item_id, values=values)
    
    def youtube_queue_item_complete(self, success, file_path, message, index):
        """Handle completion of single YouTube download"""
        # Update treeview item status
        tree_items = self.youtube_tree.get_children()
        if index < len(tree_items):
            item_id = tree_items[index]
            values = list(self.youtube_tree.item(item_id, 'values'))
            if success:
                values[3] = '✅ Tamamlandı'
                values[4] = '100%'
            else:
                values[3] = '❌ Hata'
                values[4] = '0%'
            self.youtube_tree.item(item_id, values=values)
        
        # Update overall progress
        self.yt_progress.config(value=self.current_youtube_index + 1)
        
        # Move to next video
        self.current_youtube_index += 1
        
        # Continue with next video after a short delay
        self.root.after(1000, self.download_next_youtube_video)
    
    def youtube_queue_complete(self):
        """Handle completion of entire YouTube queue"""
        self.downloading = False
        self.current_youtube_index = 0
        self.update_youtube_queue_buttons()
        
        # Count successful downloads
        successful = sum(1 for item in self.youtube_tree.get_children() 
                        if '✅' in self.youtube_tree.item(item, 'values')[3])
        total = len(self.youtube_queue)
        
        self.yt_status.config(text=f"✅ Kuyruk tamamlandı: {successful}/{total} video indirildi", foreground='green')
        
        if successful > 0:
            messagebox.showinfo("Tamamlandı", f"🎉 YouTube kuyruğu tamamlandı!\n\n{successful}/{total} video başarıyla indirildi.")
            
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = ModernAudioConverter()
    app.run()


if __name__ == "__main__":
    main()
