"""
Modern Audio Converter - Portable Tkinter Application
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import sys

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
        """Create YouTube download tab"""
        yt_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(yt_frame, text="📺 YouTube İndirici")
        
        # Configure grid
        yt_frame.columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(yt_frame, text="YouTube URL:", 
                 style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        url_frame = ttk.Frame(yt_frame)
        url_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.youtube_url)
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.url_entry.bind('<KeyRelease>', self.on_url_change)
        
        self.info_btn = ttk.Button(url_frame, text="ℹ️ Bilgi Al", 
                                  command=self.get_video_info, state='disabled')
        self.info_btn.grid(row=0, column=1)
        
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
        
        # Video info frame
        self.info_frame = ttk.LabelFrame(yt_frame, text="Video Bilgileri", padding="10")
        self.info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.info_frame.columnconfigure(1, weight=1)
        
        # Download button
        self.download_btn = ttk.Button(yt_frame, text="🎵 MP3 Olarak İndir", 
                                      command=self.start_youtube_download, state='disabled')
        self.download_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Progress bar for YouTube download
        self.yt_progress = ttk.Progressbar(yt_frame, mode='indeterminate')
        self.yt_progress.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # YouTube status
        self.yt_status = ttk.Label(yt_frame, text="")
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
        """Choose YouTube download destination"""
        folder = filedialog.askdirectory(title="İndirme Klasörü Seç")
        if folder:
            self.youtube_dest.set(folder)
            self.update_download_button_state()
            
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
            for src_path, dest_path, fname, duration, status in self.files_data:
                item_id = self.file_tree.insert('', 'end', values=(fname, duration, status, ''))
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
        
        success_count = sum(1 for _, success, _ in results if success)
        total_count = len(results)
        
        self.status_text.set(f"Tamamlandı: {success_count}/{total_count} dosya başarıyla dönüştürüldü")
        
        if success_count == total_count:
            messagebox.showinfo("Başarılı", f"🎉 Tüm dosyalar başarıyla dönüştürüldü!\n\n{success_count}/{total_count} dosya")
        else:
            messagebox.showwarning("Kısmen Başarılı", f"⚠️ {success_count}/{total_count} dosya başarıyla dönüştürüldü")
            
    def conversion_error(self, error_msg):
        """Handle conversion error"""
        self.converting = False
        self.convert_btn.config(state='normal')
        self.scan_btn.config(state='normal')
        self.status_text.set("Hata oluştu")
        messagebox.showerror("Hata", f"Dönüştürme sırasında hata oluştu:\n{error_msg}")
        
    def on_url_change(self, event=None):
        """Handle URL change"""
        url = self.youtube_url.get()
        if validate_youtube_url(url):
            self.info_btn.config(state='normal')
            self.url_entry.config(foreground='black')
        else:
            self.info_btn.config(state='disabled')
            if url:
                self.url_entry.config(foreground='red')
            else:
                self.url_entry.config(foreground='black')
                
        self.update_download_button_state()
        
    def update_download_button_state(self):
        """Update download button state"""
        url_valid = validate_youtube_url(self.youtube_url.get())
        dest_valid = bool(self.youtube_dest.get())
        
        if url_valid and dest_valid and not self.downloading:
            self.download_btn.config(state='normal')
        else:
            self.download_btn.config(state='disabled')
            
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
        """Handle download completion"""
        self.downloading = False
        self.yt_progress.stop()
        self.update_download_button_state()
        
        if success:
            self.yt_status.config(text=f"✅ {message}", foreground='green')
            messagebox.showinfo("Başarılı", f"🎉 Video başarıyla indirildi!\n\nDosya: {os.path.basename(file_path)}\nKonum: {file_path}")
        else:
            self.yt_status.config(text=f"❌ {message}", foreground='red')
            messagebox.showerror("Hata", f"❌ İndirme hatası:\n{message}")
            
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = ModernAudioConverter()
    app.run()


if __name__ == "__main__":
    main()
