import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
import datetime
from pathlib import Path
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import random
import time

class SimuladorSO:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Operativo - Simulador")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0078d4")
        
        # Variables del sistema
        self.current_user = None
        self.user_type = None
        self.files_data = {}
        self.programs_data = {}
        self.open_windows = []
        self.taskbar_buttons = []
        self.start_menu_open = False
        self.utilities_panel_open = False
        
        # Cache de imágenes mejorado
        self.image_cache = {}
        self.original_images = {}
        self.program_icons_small = {}  # Para iconos pequeños del gestor
        
        # Variables para aplicaciones mejoradas
        self.whatsapp_messages = [
            {"sender": "Contacto", "message": "¡Hola! ¿Cómo estás?", "time": "10:30"},
            {"sender": "Tú", "message": "¡Hola! Todo bien, gracias", "time": "10:31"},
            {"sender": "Contacto", "message": "¿Qué tal el trabajo?", "time": "10:32"},
            {"sender": "Tú", "message": "Muy bien, trabajando", "time": "10:33"}
        ]
        
        self.spotify_songs = [
            {"title": "Bohemian Rhapsody", "artist": "Queen", "duration": "5:55", "playing": False},
            {"title": "Imagine", "artist": "John Lennon", "duration": "3:07", "playing": False},
            {"title": "Hotel California", "artist": "Eagles", "duration": "6:30", "playing": False},
            {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "duration": "8:02", "playing": False},
            {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses", "duration": "5:03", "playing": False}
        ]
        self.current_song = None
        self.is_playing = False
        
        # Crear directorios necesarios
        self.setup_directories()
        
        # FORZAR recreación de datos de programas
        self.force_recreate_programs_data()
        
        # Cargar datos
        self.load_data()
        
        # Cargar imágenes desde archivos
        self.load_images()
        
        # Mostrar pantalla de login
        self.show_login()
        
    def setup_directories(self):
        """Crear directorios necesarios para el sistema"""
        directories = ['data', 'data/files', 'data/programs', 'data/users', 'images', 'user_files', 'user_files/documents', 'user_files/images', 'user_files/music', 'user_files/videos']
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def force_recreate_programs_data(self):
        """FORZAR la recreación completa de datos de programas - HASTA OUTLOOK"""
        print("🔄 FORZANDO recreación de datos de programas...")
        
        # Eliminar archivo existente si existe
        programs_file = 'data/programs/programs.json'
        if os.path.exists(programs_file):
            os.remove(programs_file)
            print("🗑️ Archivo anterior eliminado")
        
        # Crear datos completos desde cero 
        self.programs_data = {
            # Aplicaciones principales instaladas (con funcionalidad completa)
            "WhatsApp": {"version": "2.23.1", "installed": True, "size": "150 MB", "icon": "whatsapp", "uninstallable": True},
            "Spotify": {"version": "1.2.13", "installed": True, "size": "280 MB", "icon": "spotify", "uninstallable": True},
            "Chrome": {"version": "120.0", "installed": True, "size": "200 MB", "icon": "chrome", "uninstallable": True},
            
            # Utilerías del sistema (NO desinstalables, siempre funcionales)
            "Calculadora": {"version": "1.0", "installed": True, "size": "5 MB", "icon": "calculator", "uninstallable": False},
            "Calendario": {"version": "1.0", "installed": True, "size": "8 MB", "icon": "calendar", "uninstallable": False},
            "Bloc de Notas": {"version": "1.0", "installed": True, "size": "2 MB", "icon": "notepad", "uninstallable": False},
            "Explorador de Archivos": {"version": "1.0", "installed": True, "size": "25 MB", "icon": "files", "uninstallable": False},
            "Gestor de Programas": {"version": "1.0", "installed": True, "size": "12 MB", "icon": "programs", "uninstallable": False},
            "Monitor Sistema": {"version": "1.0", "installed": True, "size": "8 MB", "icon": "utilities", "uninstallable": False},
            
            # TODOS los programas adicionales (NO INSTALADOS inicialmente) 
            "Word": {"version": "16.0", "installed": False, "size": "1.2 GB", "icon": "word", "uninstallable": True},
            "Excel": {"version": "16.0", "installed": False, "size": "1.1 GB", "icon": "excel", "uninstallable": True},
            "PowerPoint": {"version": "16.0", "installed": False, "size": "1.0 GB", "icon": "powerpoint", "uninstallable": True},
            "Photoshop": {"version": "24.0", "installed": False, "size": "2.8 GB", "icon": "photoshop", "uninstallable": True},
            "Discord": {"version": "1.0.9", "installed": False, "size": "120 MB", "icon": "discord", "uninstallable": True},
            "Steam": {"version": "3.4.1", "installed": False, "size": "1.5 GB", "icon": "steam", "uninstallable": True},
            "Zoom": {"version": "5.16.2", "installed": False, "size": "180 MB", "icon": "zoom", "uninstallable": True},
            "VLC Media Player": {"version": "3.0.18", "installed": False, "size": "95 MB", "icon": "vlc", "uninstallable": True},
            "Telegram": {"version": "4.9.3", "installed": False, "size": "85 MB", "icon": "telegram", "uninstallable": True},
            "Netflix": {"version": "6.98.1", "installed": False, "size": "150 MB", "icon": "netflix", "uninstallable": True},
            "Visual Studio Code": {"version": "1.84.2", "installed": False, "size": "350 MB", "icon": "vscode", "uninstallable": True},
            "Skype": {"version": "8.98.0", "installed": False, "size": "75 MB", "icon": "skype", "uninstallable": True},
            "Adobe Illustrator": {"version": "28.0", "installed": False, "size": "2.2 GB", "icon": "adobe", "uninstallable": True},
            "Outlook": {"version": "16.0", "installed": False, "size": "800 MB", "icon": "outlook", "uninstallable": True}
        }
        
        # Guardar inmediatamente
        self.save_programs_data()
        
        print(f"✅ Datos recreados con {len(self.programs_data)} programas")
        print("📋 Programas disponibles:")
        for name, info in self.programs_data.items():
            status = "✅ Instalado" if info['installed'] else "❌ No instalado"
            print(f"   • {name}: {status}")
            
    def load_images(self):
        """Cargar todas las imágenes desde archivos con alta calidad"""
        image_files = {
            'avatar_admin': 'images/avatar_admin.png',
            'avatar_user': 'images/avatar_user.png',
            'icon_whatsapp': 'images/icon_whatsapp.png',
            'icon_spotify': 'images/icon_spotify.png',
            'icon_word': 'images/icon_word.png',
            'icon_chrome': 'images/icon_chrome.png',
            'icon_calculator': 'images/icon_calculator.png',
            'icon_calendar': 'images/icon_calendar.png',
            'icon_files': 'images/icon_files.png',
            'icon_programs': 'images/icon_programs.png',
            'icon_utilities': 'images/icon_utilities.png',
            'icon_recycle': 'images/icon_recycle.png',
            'logo_system': 'images/logo_system.png',
            'icon_start': 'images/icon_start.png',
            'icon_notepad': 'images/icon_notepad.png',
            'icon_photoshop': 'images/icon_photoshop.png',
            'icon_discord': 'images/icon_discord.png',
            'icon_steam': 'images/icon_steam.png',
            'icon_zoom': 'images/icon_zoom.png',
            'icon_vlc': 'images/icon_vlc.png',
            'icon_excel': 'images/icon_excel.png',
            'icon_powerpoint': 'images/icon_powerpoint.png',
            'icon_telegram': 'images/icon_telegram.png',
            'icon_netflix': 'images/icon_netflix.png',
            'icon_vscode': 'images/icon_vscode.png',
            'icon_skype': 'images/icon_skype.png',
            'icon_adobe': 'images/icon_adobe.png',
            'icon_outlook': 'images/icon_outlook.png'
        }
        
        for key, path in image_files.items():
            try:
                if os.path.exists(path):
                    original_image = Image.open(path)
                    if original_image.mode != 'RGBA':
                        original_image = original_image.convert('RGBA')
                    
                    self.original_images[key] = original_image
                    optimized_image = self.optimize_image(original_image, key)
                    self.image_cache[key] = ImageTk.PhotoImage(optimized_image)
                    
                    # Crear versión pequeña para el gestor de programas
                    if key.startswith('icon_'):
                        small_image = self.progressive_resize(original_image, (20, 20))
                        small_image = self.enhance_image_quality(small_image)
                        self.program_icons_small[key] = ImageTk.PhotoImage(small_image)
                else:
                    placeholder = self.create_high_quality_placeholder(key)
                    self.original_images[key] = placeholder
                    self.image_cache[key] = ImageTk.PhotoImage(placeholder)
                    
                    # Crear versión pequeña del placeholder
                    if key.startswith('icon_'):
                        small_placeholder = self.progressive_resize(placeholder, (20, 20))
                        self.program_icons_small[key] = ImageTk.PhotoImage(small_placeholder)
            except Exception as e:
                print(f"❌ Error cargando {path}: {e}")
                placeholder = self.create_high_quality_placeholder(key)
                self.original_images[key] = placeholder
                self.image_cache[key] = ImageTk.PhotoImage(placeholder)
                
                # Crear versión pequeña del placeholder
                if key.startswith('icon_'):
                    small_placeholder = self.progressive_resize(placeholder, (20, 20))
                    self.program_icons_small[key] = ImageTk.PhotoImage(small_placeholder)

    def optimize_image(self, image, key):
        """Optimizar imagen según su tipo con alta calidad"""
        if 'avatar' in key:
            target_size = (120, 120)  # Más grande para login
        elif 'icon_' in key:
            target_size = (64, 64)
        elif 'logo' in key:
            target_size = (160, 160)
        elif key == 'icon_start':
            target_size = (32, 32)
        elif '_bg' in key:
            target_size = (400, 300)
        else:
            target_size = (64, 64)
        
        optimized = self.progressive_resize(image, target_size)
        optimized = self.enhance_image_quality(optimized)
        return optimized

    def progressive_resize(self, image, target_size):
        """Redimensionamiento progresivo para mejor calidad"""
        current_size = image.size
        target_width, target_height = target_size
        
        if current_size[0] > target_width * 2 or current_size[1] > target_height * 2:
            intermediate_size = (target_width * 2, target_height * 2)
            image = image.resize(intermediate_size, Image.Resampling.LANCZOS)
        
        final_image = image.resize(target_size, Image.Resampling.LANCZOS)
        return final_image

    def enhance_image_quality(self, image):
        """Mejorar la calidad de la imagen"""
        try:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.05)
            
            image = image.filter(ImageFilter.SMOOTH_MORE)
        except Exception as e:
            print(f"⚠️ Error mejorando calidad: {e}")
        
        return image

    def load_wallpaper(self, wallpaper_name, target_width, target_height):
        """Cargar wallpaper ajustado al tamaño específico con alta calidad"""
        path = f'images/wallpaper_{wallpaper_name}.png'
        
        try:
            if os.path.exists(path):
                image = Image.open(path)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Obtener dimensiones originales
                orig_width, orig_height = image.size
                
                # Calcular escala para cubrir completamente la pantalla
                scale_x = target_width / orig_width
                scale_y = target_height / orig_height
                scale = max(scale_x, scale_y)  # Usar el mayor para cubrir toda la pantalla
                
                # Nuevas dimensiones
                new_width = int(orig_width * scale)
                new_height = int(orig_height * scale)
                
                # Redimensionar con alta calidad
                if scale != 1.0:
                    # Usar redimensionamiento progresivo para mejor calidad
                    if scale < 0.5:
                        # Si se reduce mucho, hacer en pasos
                        intermediate_scale = scale * 2
                        intermediate_width = int(orig_width * intermediate_scale)
                        intermediate_height = int(orig_height * intermediate_scale)
                        image = image.resize((intermediate_width, intermediate_height), Image.Resampling.LANCZOS)
                    
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Recortar si es necesario para ajustar exactamente
                if new_width > target_width or new_height > target_height:
                    left = (new_width - target_width) // 2
                    top = (new_height - target_height) // 2
                    right = left + target_width
                    bottom = top + target_height
                    image = image.crop((left, top, right, bottom))
                
                # Si la imagen es más pequeña, centrarla en un fondo
                elif new_width < target_width or new_height < target_height:
                    background = Image.new('RGB', (target_width, target_height), (30, 58, 138))  # Color de fondo
                    paste_x = (target_width - new_width) // 2
                    paste_y = (target_height - new_height) // 2
                    background.paste(image, (paste_x, paste_y))
                    image = background
                
                # Mejorar calidad final
                image = self.enhance_image_quality(image)
                return ImageTk.PhotoImage(image)
                
            else:
                return self.create_placeholder_wallpaper(target_width, target_height, wallpaper_name)
                
        except Exception as e:
            print(f"❌ Error cargando wallpaper {path}: {e}")
            return self.create_placeholder_wallpaper(target_width, target_height, wallpaper_name)

    def create_placeholder_wallpaper(self, width, height, wallpaper_type):
        """Crear wallpaper placeholder de alta calidad"""
        if 'admin' in wallpaper_type:
            color1 = (30, 58, 138)
            color2 = (59, 130, 246)
        elif 'user' in wallpaper_type:
            color1 = (34, 197, 94)
            color2 = (16, 185, 129)
        else:
            color1 = (88, 28, 135)
            color2 = (147, 51, 234)
        
        image = self.create_gradient(width, height, color1, color2)
        return ImageTk.PhotoImage(image)

    def create_gradient(self, width, height, color1, color2):
        """Crear un gradiente suave entre dos colores"""
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        for y in range(height):
            factor = y / height
            r = int(color1[0] * (1 - factor) + color2[0] * factor)
            g = int(color1[1] * (1 - factor) + color2[1] * factor)
            b = int(color1[2] * (1 - factor) + color2[2] * factor)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        return image

    def create_high_quality_placeholder(self, key):
        """Crear imagen placeholder de alta calidad"""
        if 'avatar' in key:
            size = (120, 120)  # Más grande para login
            if 'admin' in key:
                color1 = (220, 38, 38)
                color2 = (239, 68, 68)
            else:
                color1 = (37, 99, 235)
                color2 = (59, 130, 246)
        elif 'icon_' in key or 'logo' in key:
            size = (64, 64) if 'logo' in key else (64, 64)
            color1 = (59, 130, 246)
            color2 = (147, 197, 253)
        elif key == 'icon_start':
            size = (32, 32)
            color1 = (59, 130, 246)
            color2 = (147, 197, 253)
        elif '_bg' in key:
            size = (400, 300)
            color1 = (75, 85, 99)
            color2 = (156, 163, 175)
        else:
            size = (64, 64)
            color1 = (128, 128, 128)
            color2 = (156, 163, 175)
        
        image = self.create_circular_gradient(size, color1, color2)
        return image

    def create_circular_gradient(self, size, color1, color2):
        """Crear un gradiente circular para placeholders"""
        width, height = size
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        pixels = image.load()
        
        center_x, center_y = width // 2, height // 2
        max_distance = min(width, height) // 2
        
        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                
                if distance <= max_distance:
                    factor = distance / max_distance
                    r = int(color1[0] * (1 - factor) + color2[0] * factor)
                    g = int(color1[1] * (1 - factor) + color2[1] * factor)
                    b = int(color1[2] * (1 - factor) + color2[2] * factor)
                    pixels[x, y] = (r, g, b, 255)
        
        return image
        
    def load_data(self):
        """Cargar datos del sistema"""
        try:
            with open('data/users/users.json', 'r', encoding='utf-8') as f:
                self.users_data = json.load(f)
        except FileNotFoundError:
            self.users_data = {
                "admin": {
                    "password": "admin123",
                    "type": "Administrador",
                    "permissions": ["read", "write", "delete", "install", "update"],
                    "wallpaper": "admin"
                },
                "usuario": {
                    "password": "user123", 
                    "type": "Usuario",
                    "permissions": ["read", "write"],
                    "wallpaper": "user"
                }
            }
            self.save_users_data()
            
        try:
            with open('data/files/files.json', 'r', encoding='utf-8') as f:
                self.files_data = json.load(f)
        except FileNotFoundError:
            self.files_data = {}
            
        # Los datos de programas ya se cargaron en force_recreate_programs_data()
        print(f"✅ Datos cargados: {len(self.programs_data)} programas disponibles")
            
    def save_users_data(self):
        """Guardar datos de usuarios"""
        with open('data/users/users.json', 'w', encoding='utf-8') as f:
            json.dump(self.users_data, f, indent=2, ensure_ascii=False)
            
    def save_files_data(self):
        """Guardar datos de archivos"""
        with open('data/files/files.json', 'w', encoding='utf-8') as f:
            json.dump(self.files_data, f, indent=2, ensure_ascii=False)
            
    def save_programs_data(self):
        """Guardar datos de programas"""
        with open('data/programs/programs.json', 'w', encoding='utf-8') as f:
            json.dump(self.programs_data, f, indent=2, ensure_ascii=False)

    def show_login(self):
        """Mostrar pantalla de login con wallpaper que se ajusta al maximizar - SIN GIF"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Forzar actualización para obtener dimensiones reales
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Crear canvas que se expande con la ventana
        self.login_canvas = tk.Canvas(
            self.root, 
            width=window_width, 
            height=window_height,
            highlightthickness=0
        )
        self.login_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Cargar wallpaper inicial
        self.update_login_wallpaper()
        
        # Crear frame de login sobre el fondo
        login_frame = tk.Frame(self.login_canvas, bg="#1e3a8a", relief=tk.RAISED, borderwidth=3)
        self.login_frame_window = self.login_canvas.create_window(
            window_width//2, window_height//2, 
            window=login_frame
        )
        
        # Logo del sistema (más grande)
        if 'logo_system' in self.image_cache:
            logo_label = tk.Label(login_frame, image=self.image_cache['logo_system'], bg="#1e3a8a")
            logo_label.pack(pady=40)
        
        # Título
        title_label = tk.Label(
            login_frame, 
            text="SISTEMA OPERATIVO", 
            font=("Arial", 24, "bold"),
            bg="#1e3a8a", 
            fg="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Subtítulo
        subtitle_label = tk.Label(
            login_frame,
            text="Selecciona tu perfil",
            font=("Arial", 14),
            bg="#1e3a8a",
            fg="#e0e7ff"
        )
        subtitle_label.pack(pady=15)
        
        # Contenedor de botones 
        buttons_frame = tk.Frame(login_frame, bg="#1e3a8a")
        buttons_frame.pack(pady=40)

        # Contenedor para el botón de administrador
        admin_container = tk.Frame(buttons_frame, bg="#1e3a8a")
        admin_container.pack(side=tk.LEFT, padx=40)

        # Botón Administrador
        if 'avatar_admin' in self.image_cache:
            admin_btn = tk.Button(
                admin_container,
                image=self.image_cache['avatar_admin'],
                bg="#1e3a8a",
                relief=tk.FLAT,
                borderwidth=0,
                command=lambda: self.login_user("admin"),
                cursor="hand2"
            )
            admin_btn.pack()
            
            tk.Label(
                admin_container,
                text="ADMINISTRADOR",
                font=("Arial", 12, "bold"),
                bg="#1e3a8a",
                fg="#dc2626"
            ).pack(pady=(10, 0))

        # Contenedor para el botón de usuario
        user_container = tk.Frame(buttons_frame, bg="#1e3a8a")
        user_container.pack(side=tk.LEFT, padx=40)

        # Botón Usuario 
        if 'avatar_user' in self.image_cache:
            user_btn = tk.Button(
                user_container,
                image=self.image_cache['avatar_user'],
                bg="#1e3a8a",
                relief=tk.FLAT,
                borderwidth=0,
                command=lambda: self.login_user("usuario"),
                cursor="hand2"
            )
            user_btn.pack()
            
            tk.Label(
                user_container,
                text="USUARIO",
                font=("Arial", 12, "bold"),
                bg="#1e3a8a",
                fg="#2563eb"
            ).pack(pady=(10, 0))

        # Información de credenciales
        info_frame = tk.Frame(login_frame, bg="#1e3a8a")
        info_frame.pack(pady=30)
        
        info_text = "admin/admin123 | usuario/user123"
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 10),
            bg="#1e3a8a",
            fg="#94a3b8"
        )
        info_label.pack()
        
        # CONFIGURAR EVENTOS DE REDIMENSIONAMIENTO
        self.root.bind('<Configure>', self.on_login_window_resize)
        
        # Configurar canvas para redimensionamiento
        def configure_canvas(event):
            # Actualizar tamaño del canvas
            canvas_width = event.width
            canvas_height = event.height
            self.login_canvas.config(width=canvas_width, height=canvas_height)
            
            # Recentrar el frame de login
            self.login_canvas.coords(
                self.login_frame_window, 
                canvas_width//2, 
                canvas_height//2
            )
        
        self.login_canvas.bind('<Configure>', configure_canvas)

    def update_login_wallpaper(self):
        """Actualizar wallpaper de login con dimensiones actuales"""
    # Obtener dimensiones actuales del canvas
        self.login_canvas.update_idletasks()
        canvas_width = self.login_canvas.winfo_width()
        canvas_height = self.login_canvas.winfo_height()
        
        # Asegurar dimensiones mínimas
        if canvas_width < 100:
            canvas_width = self.root.winfo_width() or 1200
        if canvas_height < 100:
            canvas_height = self.root.winfo_height() or 800
        
        # Cargar wallpaper estático con nuevas dimensiones
        login_bg = self.load_wallpaper('login', canvas_width, canvas_height)
        
        # Eliminar wallpaper anterior
        self.login_canvas.delete("login_bg")
        
        # Crear nuevo wallpaper
        self.login_canvas.create_image(
            canvas_width//2, canvas_height//2, 
            image=login_bg,
            tags="login_bg"
        )
        self.login_canvas.tag_lower("login_bg")  # Enviar al fondo
        
        # Mantener referencia
        self.login_bg_ref = login_bg

    def on_login_window_resize(self, event):
        """Manejar redimensionamiento de ventana en login"""
        # Solo procesar eventos de la ventana principal
        if event.widget == self.root:
            # Pequeño delay para evitar múltiples llamadas
            if hasattr(self, '_resize_timer'):
                self.root.after_cancel(self._resize_timer)
            
            self._resize_timer = self.root.after(100, self.update_login_wallpaper)
    
    def login_user(self, username):
        """Proceso de login del usuario"""
        password_window = tk.Toplevel(self.root)
        password_window.title("Autenticación")
        password_window.geometry("400x300")
        password_window.configure(bg="#1e3a8a")
        password_window.transient(self.root)
        password_window.grab_set()
        
        password_window.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 200),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 150)
        ))
        
        avatar_key = f'avatar_{username}' if username == 'admin' else 'avatar_user'
        if avatar_key in self.image_cache:
            avatar_label = tk.Label(password_window, image=self.image_cache[avatar_key], bg="#1e3a8a")
            avatar_label.pack(pady=20)
        
        tk.Label(
            password_window,
            text=f"Contraseña para {username}:",
            font=("Arial", 14, "bold"),
            bg="#1e3a8a",
            fg="white"
        ).pack(pady=10)
        
        password_entry = tk.Entry(password_window, show="*", font=("Arial", 14), width=20)
        password_entry.pack(pady=15)
        password_entry.focus()
        
        def authenticate():
            password = password_entry.get()
            if username in self.users_data and self.users_data[username]["password"] == password:
                self.current_user = username
                self.user_type = self.users_data[username]["type"]
                password_window.destroy()
                self.setup_desktop()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
                password_entry.delete(0, tk.END)
        
        tk.Button(
            password_window,
            text="Iniciar Sesión",
            command=authenticate,
            bg="#16a34a",
            fg="white",
            font=("Arial", 12, "bold"),
            width=18,
            height=2
        ).pack(pady=15)
        
        password_entry.bind('<Return>', lambda e: authenticate())
    
    def setup_desktop(self):
        """Configurar el escritorio con fondo personalizado de alta calidad"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.update()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        self.desktop_canvas = tk.Canvas(
            self.root, 
            width=window_width, 
            height=window_height,
            highlightthickness=0
        )
        self.desktop_canvas.pack(fill=tk.BOTH, expand=True)
        
        user_wallpaper = self.users_data[self.current_user].get("wallpaper", "admin")
        desktop_bg = self.load_wallpaper(user_wallpaper, window_width, window_height)
        self.desktop_canvas.create_image(window_width//2, window_height//2, image=desktop_bg)
        self.desktop_bg_ref = desktop_bg
        
        # Crear taskbar mejorada
        self.setup_enhanced_taskbar()
        
        # Crear iconos del escritorio
        self.create_desktop_icons_on_canvas()
        
        # Crear menú de inicio simplificado
        self.setup_start_menu()
            
        # Manejar redimensionamiento
        self.root.bind('<Configure>', self.on_window_resize)

    def setup_enhanced_taskbar(self):
        """Crear una taskbar mejorada con efectos visuales"""
        taskbar_height = 50
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Crear fondo de taskbar con gradiente
        taskbar_y = window_height - taskbar_height
        self.desktop_canvas.create_rectangle(
            0, taskbar_y, window_width, window_height,
            fill="#1e1e1e", outline="#333333", width=1
        )
        
        # Botón de inicio mejorado
        start_button_width = 60
        self.start_button_id = self.desktop_canvas.create_rectangle(
            5, taskbar_y + 5, start_button_width, window_height - 5,
            fill="#0078d4", outline="#005a9e", width=2
        )
        
        self.desktop_canvas.create_text(
            start_button_width//2 + 2, taskbar_y + taskbar_height//2,
            text="⊞", font=("Segoe UI", 16, "bold"), fill="white"
        )
        
        # Área de botones de aplicaciones
        self.taskbar_apps_start = start_button_width + 10
        
        # Área del sistema (reloj, etc.)
        system_area_width = 120
        system_area_x = window_width - system_area_width
        
        # Mostrar reloj
        current_time = datetime.datetime.now().strftime("%H:%M\n%d/%m")
        self.desktop_canvas.create_text(
            system_area_x + 60, taskbar_y + taskbar_height//2,
            text=current_time, font=("Segoe UI", 9), fill="white", justify=tk.CENTER
        )
        
        # Bind para el botón de inicio
        self.desktop_canvas.tag_bind(self.start_button_id, "<Button-1>", self.toggle_start_menu)

    def create_desktop_icons_on_canvas(self):
        """Crear iconos del escritorio directamente en el canvas"""
        icons = [
            ("files", "Archivos", 50, 50, self.open_file_manager),
            ("programs", "Programas", 50, 150, self.open_program_manager),
            ("utilities", "Utilerías", 50, 250, self.open_utilities_menu),
            ("recycle", "Papelera", 50, 350, self.open_recycle_bin),
            ("whatsapp", "WhatsApp", 150, 50, lambda: self.execute_program_direct("WhatsApp")),
            ("spotify", "Spotify", 150, 150, lambda: self.execute_program_direct("Spotify")),
            ("calculator", "Calculadora", 150, 250, self.open_calculator),
            ("calendar", "Calendario", 150, 350, self.open_calendar)
        ]
        
        self.desktop_icons = []
        
        for icon_name, text, x, y, command in icons:
            self.create_desktop_icon_on_canvas(icon_name, text, x, y, command)

    def create_desktop_icon_on_canvas(self, icon_name, text, x, y, command):
        """Crear un icono individual del escritorio en el canvas"""
        icon_key = f'icon_{icon_name}'
        
        if icon_key in self.image_cache:
            icon_id = self.desktop_canvas.create_image(
                x + 32, y + 32, 
                image=self.image_cache[icon_key]
            )
            
            text_id = self.desktop_canvas.create_text(
                x + 32, y + 75,
                text=text,
                fill="white",
                font=("Arial", 9, "bold"),
                width=70
            )
            
            rect_id = self.desktop_canvas.create_rectangle(
                x, y, x + 64, y + 90,
                fill="",
                outline="",
                width=0
            )
            
            # Eventos
            self.desktop_canvas.tag_bind(icon_id, "<Button-1>", lambda e, cmd=command: cmd())
            self.desktop_canvas.tag_bind(text_id, "<Button-1>", lambda e, cmd=command: cmd())
            self.desktop_canvas.tag_bind(rect_id, "<Button-1>", lambda e, cmd=command: cmd())
            
            self.desktop_canvas.tag_bind(icon_id, "<Double-Button-1>", lambda e, cmd=command: cmd())
            self.desktop_canvas.tag_bind(text_id, "<Double-Button-1>", lambda e, cmd=command: cmd())
            self.desktop_canvas.tag_bind(rect_id, "<Double-Button-1>", lambda e, cmd=command: cmd())
            
            # Efectos hover
            self.desktop_canvas.tag_bind(rect_id, "<Enter>", 
                lambda e, r=rect_id: self.desktop_canvas.itemconfig(r, fill="#2563eb", outline="#2563eb"))
            self.desktop_canvas.tag_bind(rect_id, "<Leave>", 
                lambda e, r=rect_id: self.desktop_canvas.itemconfig(r, fill="", outline=""))
            
            self.desktop_icons.append((icon_id, text_id, rect_id))

    def on_window_resize(self, event):
        """Manejar redimensionamiento de ventana"""
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height
            
            if hasattr(self, 'current_user') and self.current_user:
                user_wallpaper = self.users_data[self.current_user].get("wallpaper", "admin")
                desktop_bg = self.load_wallpaper(user_wallpaper, new_width, new_height)
                
                self.desktop_canvas.delete("background")
                self.desktop_canvas.create_image(
                    new_width//2, new_height//2, 
                    image=desktop_bg, 
                    tags="background"
                )
                
                self.desktop_canvas.tag_lower("background")
                self.desktop_bg_ref = desktop_bg

    def setup_enhanced_taskbar(self):
        """Crear la barra de tareas mejorada con botón Start SOLO IMAGEN"""
        self.taskbar = tk.Frame(self.root, bg="#1f2937", height=50)
        self.taskbar.place(x=0, y=self.root.winfo_height()-50, relwidth=1.0)
        
        # Botón Start SOLO con imagen 
        if 'icon_start' in self.image_cache:
            self.start_button = tk.Button(
                self.taskbar,
                image=self.image_cache['icon_start'],
                bg="#374151", 
                fg="white",
                relief=tk.RAISED,
                command=self.toggle_start_menu,
                width=60,  # Más largo
                height=40
            )
            self.start_button.pack(side=tk.LEFT, padx=8, pady=5)
        
        # Información del usuario
        user_info = tk.Label(
            self.taskbar,
            text=f"Usuario: {self.current_user} ({self.user_type})",
            bg="#1f2937",
            fg="#d1d5db",
            font=("Arial", 10)
        )
        user_info.pack(side=tk.LEFT, padx=20)
        
        # Área de botones de ventanas abiertas
        self.window_buttons_frame = tk.Frame(self.taskbar, bg="#1f2937")
        self.window_buttons_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Reloj del sistema
        self.clock_label = tk.Label(
            self.taskbar, 
            bg="#1f2937", 
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.clock_label.pack(side=tk.RIGHT, padx=15, pady=8)
        self.update_clock()
        
        # Botón cerrar sesión
        logout_btn = tk.Button(
            self.taskbar,
            text="Salir",
            bg="#dc2626",
            fg="white",
            font=("Arial", 10),
            command=self.logout,
            width=6
        )
        logout_btn.pack(side=tk.RIGHT, padx=5, pady=8)
        
        # Actualizar posición del taskbar
        def update_taskbar_position():
            self.taskbar.place(x=0, y=self.root.winfo_height()-50, relwidth=1.0)
            self.root.after(100, update_taskbar_position)
        
        update_taskbar_position()

    def setup_start_menu(self):
        """Crear el menú Start simplificado"""
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.title("")
        self.start_menu.geometry("350x400+10+200")
        self.start_menu.configure(bg="#1f2937")
        self.start_menu.withdraw()
        self.start_menu.overrideredirect(True)
        
        # Header del menú
        header_frame = tk.Frame(self.start_menu, bg="#374151", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        avatar_key = f'avatar_{self.current_user}' if self.current_user == 'admin' else 'avatar_user'
        if avatar_key in self.image_cache:
            avatar_label = tk.Label(header_frame, image=self.image_cache[avatar_key], bg="#374151")
            avatar_label.pack(side=tk.LEFT, padx=15, pady=15)
        
        user_info_frame = tk.Frame(header_frame, bg="#374151")
        user_info_frame.pack(side=tk.LEFT, padx=10, pady=15)
        
        tk.Label(
            user_info_frame, 
            text=self.current_user, 
            bg="#374151", 
            fg="white",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")
        
        tk.Label(
            user_info_frame, 
            text=self.user_type, 
            bg="#374151", 
            fg="#9ca3af",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        # Secciones principales simplificadas
        sections_frame = tk.Frame(self.start_menu, bg="#1f2937")
        sections_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Solo 3 opciones principales
        main_options = [
            ("files", "📁 Gestor de Archivos", "Administrar y organizar archivos", self.open_file_manager),
            ("programs", "💻 Gestor de Programas", "Instalar y ejecutar aplicaciones", self.open_program_manager),
            ("utilities", "🛠️ Utilerías del Sistema", "Herramientas y utilidades", self.open_utilities_menu)
        ]
        
        for icon_name, title, description, command in main_options:
            self.create_main_menu_option(sections_frame, icon_name, title, description, command)

    def create_main_menu_option(self, parent, icon_name, title, description, command):
        """Crear una opción principal del menú"""
        option_frame = tk.Frame(parent, bg="#374151", relief=tk.RAISED, borderwidth=1)
        option_frame.pack(fill='x', pady=8)
        
        # Contenido de la opción
        content_frame = tk.Frame(option_frame, bg="#374151")
        content_frame.pack(fill='x', padx=15, pady=12)
        
        # Icono
        icon_key = f'icon_{icon_name}'
        if icon_key in self.original_images:
            try:
                medium_image = self.progressive_resize(self.original_images[icon_key], (32, 32))
                medium_image = self.enhance_image_quality(medium_image)
                medium_photo = ImageTk.PhotoImage(medium_image)
                
                icon_label = tk.Label(content_frame, image=medium_photo, bg="#374151")
                icon_label.image = medium_photo
                icon_label.pack(side=tk.LEFT, padx=(0, 15))
            except Exception as e:
                print(f"⚠️ Error creando icono mediano: {e}")
        
        # Texto
        text_frame = tk.Frame(content_frame, bg="#374151")
        text_frame.pack(side=tk.LEFT, fill='x', expand=True)
        
        title_label = tk.Label(
            text_frame,
            text=title,
            bg="#374151",
            fg="white",
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        title_label.pack(fill='x')
        
        desc_label = tk.Label(
            text_frame,
            text=description,
            bg="#374151",
            fg="#9ca3af",
            font=("Arial", 9),
            anchor="w"
        )
        desc_label.pack(fill='x')
        
        # Hacer toda la opción clickeable
        def on_click(event=None):
            command()
            self.toggle_start_menu()  # Cerrar menú después de hacer clic
        
        for widget in [option_frame, content_frame, text_frame, title_label, desc_label]:
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", lambda e, frame=option_frame: frame.configure(bg="#4b5563"))
            widget.bind("<Leave>", lambda e, frame=option_frame: frame.configure(bg="#374151"))
        
        # También aplicar hover a los labels de texto
        for label in [title_label, desc_label]:
            label.bind("<Enter>", lambda e, frame=option_frame, lbl=label: [
                frame.configure(bg="#4b5563"),
                lbl.configure(bg="#4b5563")
            ])
            label.bind("<Leave>", lambda e, frame=option_frame, lbl=label: [
                frame.configure(bg="#374151"),
                lbl.configure(bg="#374151")
            ])

    def toggle_start_menu(self):
        """Mostrar/ocultar el menú Start"""
        if self.start_menu_open:
            self.start_menu.withdraw()
            self.start_menu_open = False
        else:
            self.start_menu.deiconify()
            self.start_menu_open = True

    def update_clock(self):
        """Actualizar el reloj del sistema"""
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M\n%d/%m/%Y")
        self.clock_label.config(text=time_str)
        self.root.after(1000, self.update_clock)

    def create_window(self, title, content_func, width=600, height=400):
        """Crear una nueva ventana"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(f"{width}x{height}+{100 + len(self.open_windows) * 30}+{100 + len(self.open_windows) * 30}")
        window.configure(bg="white")
        
        self.open_windows.append(window)
        
        taskbar_btn = tk.Button(
            self.window_buttons_frame,
            text=title[:20] + "..." if len(title) > 20 else title,
            bg="#374151",
            fg="white",
            font=("Arial", 9),
            command=lambda: self.focus_window(window),
            relief=tk.RAISED
        )
        taskbar_btn.pack(side=tk.LEFT, padx=2, pady=5)
        self.taskbar_buttons.append(taskbar_btn)
        
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(window, taskbar_btn))
        content_func(window)
        return window

    def focus_window(self, window):
        """Enfoca una ventana específica"""
        window.lift()
        window.focus_set()

    def close_window(self, window, taskbar_btn):
        """Cierra una ventana y limpia referencias"""
        if window in self.open_windows:
            self.open_windows.remove(window)
        if taskbar_btn in self.taskbar_buttons:
            self.taskbar_buttons.remove(taskbar_btn)
            taskbar_btn.destroy()
        window.destroy()

    def logout(self):
        """Cerrar sesión"""
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que quieres cerrar sesión?"):
            for window in self.open_windows[:]:
                window.destroy()
            self.open_windows.clear()
            self.taskbar_buttons.clear()
            self.show_login()

    # ==================== GESTOR DE ARCHIVOS CON PERMISOS ====================

    def open_file_manager(self):
        """Abrir gestor de archivos CON CONTROL DE PERMISOS"""
        def create_file_manager_content(window):
            # Header
            header = tk.Frame(window, bg="#2563eb", height=50)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(
                header,
                text="📁 GESTOR DE ARCHIVOS",
                font=("Arial", 14, "bold"),
                bg="#2563eb",
                fg="white"
            ).pack(pady=12)
            
            # Main container
            main_container = tk.Frame(window)
            main_container.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Toolbar CON CONTROL DE PERMISOS
            toolbar = tk.Frame(main_container, bg="#f3f4f6", height=40)
            toolbar.pack(fill='x')
            toolbar.pack_propagate(False)

            tk.Button(
                toolbar,
                text="📄 Nuevo Archivo",
                command=self.create_new_file,
                bg="#16a34a",
                fg="white",
                font=("Arial", 10, "bold")
            ).pack(side=tk.LEFT, padx=5, pady=5)

            # BOTÓN RENOMBRAR - SOLO PARA ADMINISTRADORES
            if self.user_type == "Administrador":
                tk.Button(
                    toolbar,
                    text="✏️ Renombrar",
                    command=self.rename_selected_file,
                    bg="#f59e0b",
                    fg="white",
                    font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=5, pady=5)
            else:
                # Botón deshabilitado para usuarios
                disabled_rename_btn = tk.Button(
                    toolbar,
                    text="🔒 Renombrar",
                    command=lambda: messagebox.showwarning("🔒 Sin permisos", 
                        "Solo el administrador puede renombrar archivos.\n\n"
                        "Tu cuenta de usuario tiene permisos limitados por seguridad."),
                    bg="#6b7280",
                    fg="white",
                    font=("Arial", 10, "bold"),
                    state="normal"
                )
                disabled_rename_btn.pack(side=tk.LEFT, padx=5, pady=5)

            # BOTÓN ELIMINAR - SOLO PARA ADMINISTRADORES
            if self.user_type == "Administrador":
                tk.Button(
                    toolbar,
                    text="🗑️ Eliminar",
                    command=self.delete_selected_file,
                    bg="#dc2626",
                    fg="white",
                    font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=5, pady=5)
            else:
                # Botón deshabilitado para usuarios
                disabled_delete_btn = tk.Button(
                    toolbar,
                    text="🔒 Eliminar",
                    command=lambda: messagebox.showwarning("🔒 Sin permisos", 
                        "Solo el administrador puede eliminar archivos.\n\n"
                        "Tu cuenta de usuario tiene permisos limitados por seguridad."),
                    bg="#6b7280",
                    fg="white",
                    font=("Arial", 10, "bold"),
                    state="normal"
                )
                disabled_delete_btn.pack(side=tk.LEFT, padx=5, pady=5)

            tk.Button(
                toolbar,
                text="🔄 Actualizar",
                command=self.refresh_file_list,
                bg="#6b7280",
                fg="white",
                font=("Arial", 10, "bold")
            ).pack(side=tk.LEFT, padx=5, pady=5)
            
            # Mostrar permisos del usuario
            permissions_label = tk.Label(
                toolbar,
                text=f"👤 {self.user_type} - Permisos: {'Completos' if self.user_type == 'Administrador' else 'Limitados'}",
                bg="#f3f4f6",
                fg="#dc2626" if self.user_type == "Administrador" else "#2563eb",
                font=("Arial", 9, "bold")
            )
            permissions_label.pack(side=tk.RIGHT, padx=10, pady=5)
            
            # Content area
            content_frame = tk.Frame(main_container)
            content_frame.pack(fill='both', expand=True, pady=10)
            
            # Left panel - Categories
            left_panel = tk.Frame(content_frame, bg="#f8fafc", width=200)
            left_panel.pack(side='left', fill='y', padx=(0, 10))
            left_panel.pack_propagate(False)
            
            tk.Label(
                left_panel,
                text="📂 Categorías",
                font=("Arial", 12, "bold"),
                bg="#f8fafc",
                fg="#1f2937"
            ).pack(pady=10)
            
            categories = [
                ("📄 Documentos", "documents"),
                ("🖼️ Imágenes", "images"),
                ("🎵 Música", "music"),
                ("🎬 Videos", "videos"),
                ("📁 Todos los archivos", "all")
            ]
            
            self.selected_category = tk.StringVar(value="all")
            
            for cat_name, cat_value in categories:
                cat_btn = tk.Radiobutton(
                    left_panel,
                    text=cat_name,
                    variable=self.selected_category,
                    value=cat_value,
                    bg="#f8fafc",
                    font=("Arial", 10),
                    command=self.filter_files_by_category,
                    anchor='w'
                )
                cat_btn.pack(fill='x', padx=10, pady=2)
            
            # Right panel - File list
            right_panel = tk.Frame(content_frame)
            right_panel.pack(side='right', fill='both', expand=True)
            
            # File list
            columns = ("Tipo", "Tamaño", "Fecha")
            self.files_tree = ttk.Treeview(right_panel, columns=columns, show="tree headings")
            
            self.files_tree.heading("#0", text="Nombre")
            self.files_tree.heading("Tipo", text="Tipo")
            self.files_tree.heading("Tamaño", text="Tamaño")
            self.files_tree.heading("Fecha", text="Fecha")
            
            # Configurar anchos
            self.files_tree.column("#0", width=200)
            self.files_tree.column("Tipo", width=100)
            self.files_tree.column("Tamaño", width=100)
            self.files_tree.column("Fecha", width=150)
            
            scrollbar_files = ttk.Scrollbar(right_panel, orient="vertical", command=self.files_tree.yview)
            self.files_tree.configure(yscrollcommand=scrollbar_files.set)
            
            self.files_tree.pack(side="left", fill="both", expand=True)
            scrollbar_files.pack(side="right", fill="y")
            
            # Doble clic para abrir archivos
            self.files_tree.bind("<Double-1>", self.open_selected_file)
            
            # Cargar archivos iniciales
            self.load_initial_files()
            self.refresh_file_list()
        
        self.create_window("Gestor de Archivos", create_file_manager_content, 900, 600)

    def rename_selected_file(self):
        """Renombrar archivo seleccionado"""
        if self.user_type != "Administrador":
            messagebox.showerror("🔒 Sin permisos", 
                "Solo el administrador puede renombrar archivos.\n\n"
                "Tu cuenta de usuario tiene permisos limitados por seguridad del sistema.")
            return
        
        if not hasattr(self, 'files_tree') or not self.files_tree.selection():
            messagebox.showwarning("Advertencia", "Selecciona un archivo para renombrar")
            return
        
        selection = self.files_tree.selection()
        item = self.files_tree.item(selection[0])
        file_name_with_icon = item['text']
        old_file_name = file_name_with_icon.split(' ', 1)[1]  # Quitar icono
        
        # Buscar archivo en datos
        file_info = None
        file_key_to_rename = None
        for key, info in self.files_data.items():
            if info['name'] == old_file_name:
                file_info = info
                file_key_to_rename = key
                break
        
        if not file_info:
            messagebox.showerror("Error", "Archivo no encontrado")
            return
        
        # Solicitar nuevo nombre
        new_file_name = simpledialog.askstring(
            "✏️ Renombrar Archivo", 
            f"Nuevo nombre para '{old_file_name}':",
            initialvalue=old_file_name
        )
        
        if not new_file_name or new_file_name == old_file_name:
            return  # Cancelado o mismo nombre
        
        # Agregar extensión si es necesario
        if file_info['type'] == "Documento" and not new_file_name.endswith('.txt'):
            new_file_name += '.txt'
        
        # Verificar que no exista otro archivo con ese nombre
        new_file_key = f"{file_info['category']}_{new_file_name}"
        if new_file_key in self.files_data:
            messagebox.showerror("Error", f"Ya existe un archivo llamado '{new_file_name}'")
            return
        
        try:
            # Renombrar archivo físico
            old_file_path = f"user_files/{file_info['category']}/{old_file_name}"
            new_file_path = f"user_files/{file_info['category']}/{new_file_name}"
            
            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
            
            # Actualizar datos en memoria
            # Crear nueva entrada con el nuevo nombre
            self.files_data[new_file_key] = {
                "name": new_file_name,
                "type": file_info['type'],
                "size": file_info['size'],
                "category": file_info['category'],
                "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "content": file_info['content']
            }
            
            # Eliminar entrada antigua
            del self.files_data[file_key_to_rename]
            
            # Guardar cambios
            self.save_files_data()
            self.refresh_file_list()
            
            messagebox.showinfo("✅ Éxito", f"Archivo renombrado correctamente:\n\n📄 '{old_file_name}' → '{new_file_name}'")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo renombrar el archivo: {e}")

    def load_initial_files(self):
        """Cargar archivos iniciales del sistema"""
        initial_files = [
            {"name": "Bienvenida.txt", "type": "Documento", "size": "2 KB", "category": "documents", "content": "¡Bienvenido al sistema operativo simulado!\n\nEste es un archivo de ejemplo que puedes editar."},
            {"name": "Notas.txt", "type": "Documento", "size": "1 KB", "category": "documents", "content": "Mis notas importantes:\n- Recordar actualizar el sistema\n- Revisar correos"},
            {"name": "Imagen1.jpg", "type": "Imagen", "size": "1.2 MB", "category": "images", "content": ""},
            {"name": "Cancion.mp3", "type": "Audio", "size": "3.5 MB", "category": "music", "content": ""},
            {"name": "Video.mp4", "type": "Video", "size": "15 MB", "category": "videos", "content": ""}
        ]
        
        # Crear archivos físicos si no existen
        for file_info in initial_files:
            if file_info["type"] == "Documento":
                file_path = f"user_files/documents/{file_info['name']}"
                if not os.path.exists(file_path):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file_info['content'])
            elif file_info["type"] == "Carpeta":
                folder_path = f"user_files/documents/{file_info['name']}"
                Path(folder_path).mkdir(exist_ok=True)
        
        # Actualizar datos en memoria
        for file_info in initial_files:
            file_key = f"{file_info['category']}_{file_info['name']}"
            self.files_data[file_key] = {
                "name": file_info['name'],
                "type": file_info['type'],
                "size": file_info['size'],
                "category": file_info['category'],
                "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "content": file_info.get('content', '')
            }
        
        self.save_files_data()

    def refresh_file_list(self):
        """Actualizar lista de archivos"""
        if hasattr(self, 'files_tree'):
            for item in self.files_tree.get_children():
                self.files_tree.delete(item)
            
            category_filter = self.selected_category.get()
            
            for file_key, file_info in self.files_data.items():
                if category_filter == "all" or file_info['category'] == category_filter:
                    # Icono según tipo
                    if file_info['type'] == "Documento":
                        icon = "📄"
                    elif file_info['type'] == "Imagen":
                        icon = "🖼️"
                    elif file_info['type'] == "Audio":
                        icon = "🎵"
                    elif file_info['type'] == "Video":
                        icon = "🎬"
                    else:
                        icon = "📄"
                    
                    self.files_tree.insert("", "end",
                                         text=f"{icon} {file_info['name']}",
                                         values=(file_info['type'], 
                                               file_info['size'], 
                                               file_info['date']))

    def filter_files_by_category(self):
        """Filtrar archivos por categoría"""
        self.refresh_file_list()

    def create_new_file(self):
        """Crear nuevo archivo"""
        file_name = simpledialog.askstring("Nuevo Archivo", "Nombre del archivo:")
        if file_name:
            if not file_name.endswith('.txt'):
                file_name += '.txt'
            
            category = self.selected_category.get()
            if category == "all":
                category = "documents"
            
            file_key = f"{category}_{file_name}"
            
            if file_key in self.files_data:
                messagebox.showerror("Error", "El archivo ya existe")
                return
            
            # Crear archivo físico
            file_path = f"user_files/{category}/{file_name}"
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("Nuevo archivo creado\n")
                
                # Agregar a datos
                self.files_data[file_key] = {
                    "name": file_name,
                    "type": "Documento",
                    "size": "1 KB",
                    "category": category,
                    "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "content": "Nuevo archivo creado\n"
                }
                
                self.save_files_data()
                self.refresh_file_list()
                messagebox.showinfo("Éxito", f"Archivo '{file_name}' creado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el archivo: {e}")


    def delete_selected_file(self):
        """Eliminar archivo seleccionado - SOLO ADMINISTRADORES"""
        # Verificar permisos PRIMERO
        if self.user_type != "Administrador":
            messagebox.showerror("🔒 Sin permisos", 
                "Solo el administrador puede eliminar archivos.\n\n"
                "Tu cuenta de usuario tiene permisos limitados por seguridad del sistema.")
            return
        
        if not hasattr(self, 'files_tree') or not self.files_tree.selection():
            messagebox.showwarning("Advertencia", "Selecciona un archivo para eliminar")
            return
        
        selection = self.files_tree.selection()
        item = self.files_tree.item(selection[0])
        file_name_with_icon = item['text']
        file_name = file_name_with_icon.split(' ', 1)[1]  # Quitar icono
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{file_name}'?\n\n⚠️ Esta acción no se puede deshacer."):
            # Buscar y eliminar de datos
            file_key_to_delete = None
            for key, file_info in self.files_data.items():
                if file_info['name'] == file_name:
                    file_key_to_delete = key
                    break
            
            if file_key_to_delete:
                file_info = self.files_data[file_key_to_delete]
                
                # Eliminar archivo físico 
                try:
                    file_path = f"user_files/{file_info['category']}/{file_name}"
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    # Eliminar de datos
                    del self.files_data[file_key_to_delete]
                    self.save_files_data()
                    self.refresh_file_list()
                    messagebox.showinfo("Éxito", f"'{file_name}' eliminado correctamente")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def open_selected_file(self, event):
        """Abrir archivo seleccionado"""
        if not self.files_tree.selection():
            return  
        
        selection = self.files_tree.selection()
        item = self.files_tree.item(selection[0])
        file_name_with_icon = item['text']
        file_name = file_name_with_icon.split(' ', 1)[1]  # Quitar icono
        
        # Buscar archivo en datos
        file_info = None
        for key, info in self.files_data.items():
            if info['name'] == file_name:
                file_info = info
                break
        
        if file_info:
            if file_info['type'] == "Documento":
                self.open_text_editor(file_name, file_info)
            else:
                messagebox.showinfo("Archivo", f"Abriendo: {file_name}\nTipo: {file_info['type']}")

    def open_text_editor(self, file_name, file_info):
        """Abrir editor de texto para archivos"""
        def create_editor_content(window):
            # Header
            header = tk.Frame(window, bg="#16a34a")
            header.pack(fill='x')
            
            tk.Label(
                header,
                text=f"📝 Editor - {file_name}",
                font=("Arial", 12, "bold"),
                bg="#16a34a",
                fg="white"
            ).pack(pady=8)
            
            # Toolbar
            toolbar = tk.Frame(window, bg="#f3f4f6")
            toolbar.pack(fill='x')
            
            tk.Button(
                toolbar,
                text="💾 Guardar",
                command=lambda: self.save_file_content(file_name, file_info, text_area.get(1.0, tk.END)),
                bg="#2563eb",
                fg="white",
                font=("Arial", 10)
            ).pack(side='left', padx=5, pady=5)
            
            tk.Button(
                toolbar,
                text="🔄 Recargar",
                command=lambda: self.reload_file_content(file_name, file_info, text_area),
                bg="#6b7280",
                fg="white",
                font=("Arial", 10)
            ).pack(side='left', padx=5, pady=5)
            
            # Text area
            text_frame = tk.Frame(window)
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_area = tk.Text(
                text_frame,
                font=("Consolas", 11),
                wrap=tk.WORD
            )
            
            scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
            text_area.configure(yscrollcommand=scrollbar.set)
            
            text_area.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Cargar contenido
            try:
                file_path = f"user_files/{file_info['category']}/{file_name}"
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        text_area.insert(1.0, content)
                else:
                    text_area.insert(1.0, file_info.get('content', ''))
            except Exception as e:
                text_area.insert(1.0, f"Error cargando archivo: {e}")
        
        self.create_window(f"Editor - {file_name}", create_editor_content, 700, 500)

    def save_file_content(self, file_name, file_info, content):
        """Guardar contenido del archivo"""
        try:
            file_path = f"user_files/{file_info['category']}/{file_name}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Actualizar datos
            for key, info in self.files_data.items():
                if info['name'] == file_name:
                    self.files_data[key]['content'] = content
                    self.files_data[key]['date'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    break
            
            self.save_files_data()
            messagebox.showinfo("Éxito", "Archivo guardado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def reload_file_content(self, file_name, file_info, text_area):
        """Recargar contenido del archivo"""
        try:
            file_path = f"user_files/{file_info['category']}/{file_name}"
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    text_area.delete(1.0, tk.END)
                    text_area.insert(1.0, content)
            messagebox.showinfo("Éxito", "Archivo recargado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recargar: {e}")

    # ==================== WHATSAPP MEJORADO ====================

    def simulate_whatsapp(self):
        """Simular WhatsApp MEJORADO"""
        def create_whatsapp_content(window):
            window.configure(bg="#075e54")
            
            # Header
            header = tk.Frame(window, bg="#128c7e", height=60)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(
                header,
                text="📱 WhatsApp",
                font=("Arial", 18, "bold"),
                bg="#128c7e",
                fg="white"
            ).pack(side='left', padx=15, pady=15)
            
            tk.Label(
                header,
                text="🟢 En línea",
                font=("Arial", 10),
                bg="#128c7e",
                fg="#dcf8c6"
            ).pack(side='right', padx=15, pady=15)
            
            # Chat area
            chat_frame = tk.Frame(window, bg="#ece5dd")
            chat_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Scrollable chat
            chat_canvas = tk.Canvas(chat_frame, bg="#ece5dd")
            chat_scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=chat_canvas.yview)
            self.chat_content = tk.Frame(chat_canvas, bg="#ece5dd")
            
            chat_canvas.configure(yscrollcommand=chat_scrollbar.set)
            chat_canvas.pack(side="left", fill="both", expand=True)
            chat_scrollbar.pack(side="right", fill="y")
            
            chat_canvas.create_window((0, 0), window=self.chat_content, anchor="nw")
            
            # Mostrar mensajes existentes
            self.display_whatsapp_messages()
            
            # Input area
            input_frame = tk.Frame(window, bg="#075e54", height=60)
            input_frame.pack(fill='x', padx=10, pady=10)
            input_frame.pack_propagate(False)
            
            self.message_entry = tk.Entry(
                input_frame, 
                font=("Arial", 12),
                bg="white",
                relief=tk.FLAT
            )
            self.message_entry.pack(side='left', fill='x', expand=True, padx=5, pady=10)
            
            send_btn = tk.Button(
                input_frame,
                text="📤",
                bg="#128c7e",
                fg="white",
                font=("Arial", 14),
                relief=tk.FLAT,
                command=self.send_whatsapp_message,
                width=3
            )
            send_btn.pack(side='right', padx=5, pady=10)
            
            # Bind Enter key
            self.message_entry.bind('<Return>', lambda e: self.send_whatsapp_message())
            self.message_entry.focus()
            
            # Update scroll region
            def configure_scroll(event):
                chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
            
            self.chat_content.bind('<Configure>', configure_scroll)
        
        self.create_window("WhatsApp", create_whatsapp_content, 450, 600)

    def display_whatsapp_messages(self):
        """Mostrar mensajes de WhatsApp"""
        for widget in self.chat_content.winfo_children():
            widget.destroy()
        
        for msg in self.whatsapp_messages:
            msg_frame = tk.Frame(self.chat_content, bg="#ece5dd")
            msg_frame.pack(fill='x', padx=10, pady=5)
            
            if msg['sender'] == "Tú":
                # Mensaje propio (derecha)
                bubble = tk.Frame(msg_frame, bg="#dcf8c6", relief=tk.RAISED, borderwidth=1)
                bubble.pack(side='right', padx=5)
                
                tk.Label(
                    bubble,
                    text=msg['message'],
                    bg="#dcf8c6",
                    font=("Arial", 10),
                    wraplength=200,
                    justify='left'
                ).pack(padx=10, pady=5)
                
                tk.Label(
                    bubble,
                    text=msg['time'],
                    bg="#dcf8c6",
                    font=("Arial", 8),
                    fg="#666"
                ).pack(anchor='e', padx=10, pady=(0, 5))
                
            else:
                # Mensaje del contacto (izquierda)
                bubble = tk.Frame(msg_frame, bg="white", relief=tk.RAISED, borderwidth=1)
                bubble.pack(side='left', padx=5)
                
                tk.Label(
                    bubble,
                    text=msg['message'],
                    bg="white",
                    font=("Arial", 10),
                    wraplength=200,
                    justify='left'
                ).pack(padx=10, pady=5)
                
                tk.Label(
                    bubble,
                    text=msg['time'],
                    bg="white",
                    font=("Arial", 8),
                    fg="#666"
                ).pack(anchor='w', padx=10, pady=(0, 5))

    def send_whatsapp_message(self):
        """Enviar mensaje en WhatsApp"""
        message = self.message_entry.get().strip()
        if message:
            # Agregar mensaje del usuario
            current_time = datetime.datetime.now().strftime("%H:%M")
            self.whatsapp_messages.append({
                "sender": "Tú",
                "message": message,
                "time": current_time
            })
            
            # Limpiar entrada
            self.message_entry.delete(0, tk.END)
            
            # Actualizar display
            self.display_whatsapp_messages()
            
            # Simular respuesta automática después de 2 segundos
            self.root.after(2000, lambda: self.simulate_contact_response(message))

    def simulate_contact_response(self, user_message):
        """Simular respuesta del contacto"""
        responses = [
            "¡Interesante! 🤔",
            "Entiendo perfectamente 👍",
            "¿En serio? ¡Qué genial! 😄",
            "Tienes razón 💯",
            "Cuéntame más sobre eso 🤗",
            "¡Excelente punto! ✨",
            "Me parece muy bien 👌"
        ]
        
        response = random.choice(responses)
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        self.whatsapp_messages.append({
            "sender": "Contacto",
            "message": response,
            "time": current_time
        })
        
        # Actualizar display
        self.display_whatsapp_messages()

    # ==================== SPOTIFY MEJORADO ====================

    def simulate_spotify(self):
        """Simular Spotify MEJORADO"""
        def create_spotify_content(window):
            window.configure(bg="#191414")
            
            # Header
            header = tk.Frame(window, bg="#1db954", height=60)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(
                header,
                text="🎵 Spotify",
                font=("Arial", 18, "bold"),
                bg="#1db954",
                fg="white"
            ).pack(side='left', padx=15, pady=15)
            
            tk.Label(
                header,
                text="Premium ✨",
                font=("Arial", 10),
                bg="#1db954",
                fg="#b3ffb3"
            ).pack(side='right', padx=15, pady=15)
            
            # Main content
            main_frame = tk.Frame(window, bg="#191414")
            main_frame.pack(fill='both', expand=True, padx=15, pady=15)
            
            # Now playing section
            now_playing = tk.Frame(main_frame, bg="#282828", relief=tk.RAISED, borderwidth=2)
            now_playing.pack(fill='x', pady=(0, 15))
            
            tk.Label(
                now_playing,
                text="🎧 Reproduciendo ahora",
                font=("Arial", 12, "bold"),
                bg="#282828",
                fg="white"
            ).pack(pady=10)
            
            self.current_song_label = tk.Label(
                now_playing,
                text="Selecciona una canción para reproducir",
                font=("Arial", 11),
                bg="#282828",
                fg="#b3b3b3"
            )
            self.current_song_label.pack(pady=5)
            
            # Controls
            controls_frame = tk.Frame(now_playing, bg="#282828")
            controls_frame.pack(pady=10)
            
            tk.Button(
                controls_frame,
                text="⏮️",
                bg="#1db954",
                fg="white",
                font=("Arial", 12),
                command=self.previous_song,
                relief=tk.FLAT,
                width=3
            ).pack(side='left', padx=5)
            
            self.play_pause_btn = tk.Button(
                controls_frame,
                text="▶️",
                bg="#1db954",
                fg="white",
                font=("Arial", 14),
                command=self.toggle_play_pause,
                relief=tk.FLAT,
                width=3
            )
            self.play_pause_btn.pack(side='left', padx=5)
            
            tk.Button(
                controls_frame,
                text="⏭️",
                bg="#1db954",
                fg="white",
                font=("Arial", 12),
                command=self.next_song,
                relief=tk.FLAT,
                width=3
            ).pack(side='left', padx=5)
            
            # Songs list
            songs_frame = tk.Frame(main_frame, bg="#191414")
            songs_frame.pack(fill='both', expand=True)
            
            tk.Label(
                songs_frame,
                text="🎶 Tu biblioteca musical",
                font=("Arial", 14, "bold"),
                bg="#191414",
                fg="white"
            ).pack(pady=(0, 10))
            
            # Songs list with scrollbar
            list_frame = tk.Frame(songs_frame, bg="#191414")
            list_frame.pack(fill='both', expand=True)
            
            songs_canvas = tk.Canvas(list_frame, bg="#191414")
            songs_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=songs_canvas.yview)
            self.songs_content = tk.Frame(songs_canvas, bg="#191414")
            
            songs_canvas.configure(yscrollcommand=songs_scrollbar.set)
            songs_canvas.pack(side="left", fill="both", expand=True)
            songs_scrollbar.pack(side="right", fill="y")
            
            songs_canvas.create_window((0, 0), window=self.songs_content, anchor="nw")
            
            # Display songs
            self.display_spotify_songs()
            
            # Update scroll region
            def configure_songs_scroll(event):
                songs_canvas.configure(scrollregion=songs_canvas.bbox("all"))
            
            self.songs_content.bind('<Configure>', configure_songs_scroll)
        
        self.create_window("Spotify", create_spotify_content, 600, 700)

    def display_spotify_songs(self):
        """Mostrar lista de canciones"""
        for widget in self.songs_content.winfo_children():
            widget.destroy()
        
        for i, song in enumerate(self.spotify_songs):
            song_frame = tk.Frame(self.songs_content, bg="#282828" if i % 2 == 0 else "#333333", cursor="hand2")
            song_frame.pack(fill='x', padx=5, pady=2)
            
            # Song info
            info_frame = tk.Frame(song_frame, bg=song_frame['bg'])
            info_frame.pack(side='left', fill='x', expand=True, padx=15, pady=10)
            
            # Title and artist
            tk.Label(
                info_frame,
                text=song['title'],
                bg=song_frame['bg'],
                fg="white",
                font=("Arial", 11, "bold"),
                anchor='w'
            ).pack(fill='x')
            
            tk.Label(
                info_frame,
                text=song['artist'],
                bg=song_frame['bg'],
                fg="#b3b3b3",
                font=("Arial", 9),
                anchor='w'
            ).pack(fill='x')
            
            # Duration and play button
            controls_frame = tk.Frame(song_frame, bg=song_frame['bg'])
            controls_frame.pack(side='right', padx=15, pady=10)
            
            tk.Label(
                controls_frame,
                text=song['duration'],
                bg=song_frame['bg'],
                fg="#b3b3b3",
                font=("Arial", 9)
            ).pack(side='right', padx=10)
            
            play_btn = tk.Button(
                controls_frame,
                text="▶️" if not song['playing'] else "⏸️",
                bg="#1db954",
                fg="white",
                font=("Arial", 10),
                command=lambda s=song: self.play_song(s),
                relief=tk.FLAT,
                width=3
            )
            play_btn.pack(side='right')
            
            # Make entire row clickable
            def make_clickable(frame, song_data):
                frame.bind("<Button-1>", lambda e: self.play_song(song_data))
                for child in frame.winfo_children():
                    child.bind("<Button-1>", lambda e: self.play_song(song_data))
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if grandchild.winfo_class() != 'Button':
                                grandchild.bind("<Button-1>", lambda e: self.play_song(song_data))
            
            make_clickable(song_frame, song)

    def play_song(self, song):
        """Reproducir canción seleccionada"""
        # Detener todas las canciones
        for s in self.spotify_songs:
            s['playing'] = False
        
        # Reproducir la seleccionada
        song['playing'] = True
        self.current_song = song
        self.is_playing = True
        
        # Actualizar interfaz
        self.current_song_label.config(text=f"🎵 {song['title']} - {song['artist']}")
        self.play_pause_btn.config(text="⏸️")
        
        # Actualizar lista
        self.display_spotify_songs()

    def toggle_play_pause(self):
        """Alternar reproducción/pausa"""
        if self.current_song:
            self.is_playing = not self.is_playing
            self.current_song['playing'] = self.is_playing
            
            if self.is_playing:
                self.play_pause_btn.config(text="⏸️")
                self.current_song_label.config(text=f"🎵 {self.current_song['title']} - {self.current_song['artist']}")
            else:
                self.play_pause_btn.config(text="▶️")
                self.current_song_label.config(text=f"⏸️ {self.current_song['title']} - {self.current_song['artist']} (Pausado)")
            
            self.display_spotify_songs()

    def next_song(self):
        """Siguiente canción"""
        if self.current_song:
            current_index = self.spotify_songs.index(self.current_song)
            next_index = (current_index + 1) % len(self.spotify_songs)
            self.play_song(self.spotify_songs[next_index])

    def previous_song(self):
        """Canción anterior"""
        if self.current_song:
            current_index = self.spotify_songs.index(self.current_song)
            prev_index = (current_index - 1) % len(self.spotify_songs)
            self.play_song(self.spotify_songs[prev_index])

    # ==================== RESTO DE FUNCIONES ====================

    def open_program_manager(self):
        """Abrir gestor de programas con iconos reales"""
        def create_program_manager_content(window):
            # Header
            header = tk.Frame(window, bg="#7c3aed", height=50)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(
                header,
                text="💻 GESTOR DE PROGRAMAS",
                font=("Arial", 14, "bold"),
                bg="#7c3aed",
                fg="white"
            ).pack(pady=12)
            
            # Main container
            main_container = tk.Frame(window)
            main_container.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Toolbar
            toolbar = tk.Frame(main_container, bg="#f3f4f6", height=40)
            toolbar.pack(fill='x')
            toolbar.pack_propagate(False)
            
            tk.Button(
                toolbar,
                text="▶️ Ejecutar",
                command=self.execute_selected_program,
                bg="#16a34a",
                fg="white",
                font=("Arial", 10, "bold")
            ).pack(side=tk.LEFT, padx=5, pady=5)
            
            if self.user_type == "Administrador":
                tk.Button(
                    toolbar,
                    text="📥 Instalar",
                    command=self.install_selected_program,
                    bg="#2563eb",
                    fg="white",
                    font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=5, pady=5)
                
                tk.Button(
                    toolbar,
                    text="🔄 Actualizar",
                    command=self.update_selected_program,
                    bg="#f59e0b",
                    fg="white",
                    font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=5, pady=5)
                
                tk.Button(
                    toolbar,
                    text="🗑️ Desinstalar",
                    command=self.uninstall_selected_program,
                    bg="#dc2626",
                    fg="white",
                    font=("Arial", 10, "bold")
                ).pack(side=tk.LEFT, padx=5, pady=5)
            
            # Lista de programas CON ICONOS REALES
            list_frame = tk.Frame(main_container)
            list_frame.pack(fill='both', expand=True, pady=10)
            
            columns = ("Estado", "Versión", "Tamaño")
            self.programs_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings")
            
            self.programs_tree.heading("#0", text="Programa")
            self.programs_tree.heading("Estado", text="Estado")
            self.programs_tree.heading("Versión", text="Versión")
            self.programs_tree.heading("Tamaño", text="Tamaño")
            
            # Configurar anchos de columnas
            self.programs_tree.column("#0", width=250)
            self.programs_tree.column("Estado", width=150)
            self.programs_tree.column("Versión", width=120)
            self.programs_tree.column("Tamaño", width=120)
            
            scrollbar_prog = ttk.Scrollbar(list_frame, orient="vertical", command=self.programs_tree.yview)
            self.programs_tree.configure(yscrollcommand=scrollbar_prog.set)
            
            self.programs_tree.pack(side="left", fill="both", expand=True)
            scrollbar_prog.pack(side="right", fill="y")
            
            self.refresh_programs_list()
        
        self.create_window("Gestor de Programas", create_program_manager_content, 800, 600)

    def refresh_programs_list(self):
        """Actualizar lista de programas con ICONOS REALES"""
        if hasattr(self, 'programs_tree'):
            for item in self.programs_tree.get_children():
                self.programs_tree.delete(item)
            
            print(f"🔄 Actualizando lista con {len(self.programs_data)} programas")
            
            for program_name, program_info in self.programs_data.items():
                status = "✅ Instalado" if program_info['installed'] else "❌ No instalado"
                
                # Obtener el icono del programa
                icon_key = f"icon_{program_info['icon']}"
                program_icon = None
                
                if icon_key in self.program_icons_small:
                    program_icon = self.program_icons_small[icon_key]
                
                # Color según estado
                tags = ("installed",) if program_info['installed'] else ("not_installed",)
                
                # Insertar con icono 
                item_id = self.programs_tree.insert("", "end",
                                        text=program_name,  
                                        values=(status, 
                                               program_info['version'], 
                                               program_info['size']),
                                        tags=tags,
                                        image=program_icon if program_icon else "")
                
                print(f"   • {program_name}: {status} (icono: {icon_key})")
            
            # Configurar colores
            self.programs_tree.tag_configure("installed", background="#dcfce7")
            self.programs_tree.tag_configure("not_installed", background="#fef2f2")

    def execute_selected_program(self):
        """Ejecutar programa seleccionado"""
        if not hasattr(self, 'programs_tree') or not self.programs_tree.selection():
            messagebox.showwarning("⚠️ Advertencia", "Selecciona un programa para ejecutar")
            return
            
        selection = self.programs_tree.selection()
        item = self.programs_tree.item(selection[0])
        program_name = item['text']  
        
        self.execute_program_direct(program_name)

    def execute_program_direct(self, program_name):
        """Ejecutar programa directamente"""
        if program_name not in self.programs_data:
            messagebox.showerror("❌ Error", f"Programa {program_name} no encontrado")
            return
            
        if not self.programs_data[program_name]['installed']:
            messagebox.showerror("❌ Error", f"{program_name} no está instalado")
            return
        
        # Solo los programas principales tienen funcionalidad completa
        main_functional_programs = [
            "WhatsApp", "Spotify", "Word", "Chrome", 
            "Calculadora", "Calendario", "Bloc de Notas", 
            "Explorador de Archivos", "Gestor de Programas", "Monitor Sistema"
        ]
        
        if program_name in main_functional_programs:
            # Ejecutar programas con funcionalidad completa
            if program_name == "WhatsApp":
                self.simulate_whatsapp()
            elif program_name == "Spotify":
                self.simulate_spotify()
            elif program_name == "Word":
                self.simulate_word()
            elif program_name == "Chrome":
                self.simulate_chrome()
            elif program_name == "Calculadora":
                self.open_calculator()
            elif program_name == "Calendario":
                self.open_calendar()
            elif program_name == "Bloc de Notas":
                self.open_notepad()
            elif program_name == "Explorador de Archivos":
                self.open_file_manager()
            elif program_name == "Gestor de Programas":
                self.open_program_manager()
            elif program_name == "Monitor Sistema":
                self.open_system_monitor()
        else:
            # Todos los demás programas muestran mensaje simple
            messagebox.showinfo("🚀 Ejecutando", 
                f"✅ {program_name} se está ejecutando...\n\n"
                f"📱 Programa instalado correctamente\n"
                f"🎯 Funcionalidad básica disponible")

    def install_selected_program(self):
        """Instalar programa seleccionado con simulación visual REAL"""
        if self.user_type != "Administrador":
            messagebox.showerror("❌ Error", "Solo el administrador puede instalar programas")
            return
        
        if not hasattr(self, 'programs_tree') or not self.programs_tree.selection():
            messagebox.showwarning("⚠️ Advertencia", "Selecciona un programa para instalar")
            return
        
        selection = self.programs_tree.selection()
        item = self.programs_tree.item(selection[0])
        program_name = item['text'] 
        
        if self.programs_data[program_name]['installed']:
            messagebox.showinfo("ℹ️ Info", f"{program_name} ya está instalado")
            return
        
        if messagebox.askyesno("📥 Instalar", f"¿Instalar {program_name}?"):
            self.simulate_installation(program_name)

    def simulate_installation(self, program_name):
        """Simular instalación de programa con barra de progreso REAL"""
        # Crear ventana de instalación
        install_window = tk.Toplevel(self.root)
        install_window.title("Instalando Programa")
        install_window.geometry("500x300")
        install_window.configure(bg="white")
        install_window.transient(self.root)
        install_window.grab_set()
        
        # Centrar ventana
        install_window.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 250),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 150)
        ))
        
        # Contenido de la ventana
        tk.Label(
            install_window,
            text=f"📥 Instalando {program_name}",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack(pady=20)
        
        # Información del programa
        program_info = self.programs_data[program_name]
        info_text = f"📦 Tamaño: {program_info['size']}\n🔢 Versión: {program_info['version']}"
        tk.Label(
            install_window,
            text=info_text,
            font=("Arial", 12),
            bg="white",
            fg="#6b7280"
        ).pack(pady=10)
        
        # Barra de progreso
        progress_frame = tk.Frame(install_window, bg="white")
        progress_frame.pack(pady=20, padx=40, fill='x')
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100, length=400)
        progress_bar.pack(fill='x')
        
        status_label = tk.Label(
            install_window,
            text="Preparando instalación...",
            font=("Arial", 12),
            bg="white",
            fg="#6b7280"
        )
        status_label.pack(pady=10)
        
        # Simular progreso REAL
        progress_steps = [
            (10, "Verificando requisitos del sistema..."),
            (25, "Descargando archivos principales..."),
            (40, "Descargando dependencias..."),
            (55, "Verificando integridad de archivos..."),
            (70, "Extrayendo archivos..."),
            (85, "Configurando programa..."),
            (95, "Registrando en el sistema..."),
            (100, "¡Instalación completada exitosamente!")
        ]
        
        def update_progress(step_index=0):
            if step_index < len(progress_steps):
                progress, status = progress_steps[step_index]
                
                # Actualizar barra de progreso gradualmente
                current_progress = progress_var.get()
                target_progress = progress
                
                def animate_progress():
                    nonlocal current_progress
                    if current_progress < target_progress:
                        current_progress += 2
                        progress_var.set(min(current_progress, target_progress))
                        install_window.after(50, animate_progress)
                    else:
                        # Actualizar texto
                        status_label.config(text=status)
                        # Continuar con el siguiente paso
                        install_window.after(800, lambda: update_progress(step_index + 1))
                
                animate_progress()
            else:
                # Instalación completada
                install_window.after(1500, lambda: self.complete_installation(program_name, install_window))
        
        # Iniciar simulación
        update_progress()

    def complete_installation(self, program_name, install_window):
        """Completar la instalación del programa"""
        # Actualizar datos REALMENTE
        self.programs_data[program_name]['installed'] = True
        self.save_programs_data()
        
        # Actualizar lista si existe
        if hasattr(self, 'programs_tree'):
            self.refresh_programs_list()
        
        # Cerrar ventana de instalación
        install_window.destroy()
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("✅ Instalación Exitosa", 
            f"🎉 {program_name} se ha instalado correctamente\n\n"
            f"🚀 Ya puedes ejecutarlo desde el gestor\n"
            f"📱 Disponible en el escritorio y menú Start")

    def update_selected_program(self):
        """Actualizar programa seleccionado con simulación REAL"""
        if self.user_type != "Administrador":
            messagebox.showerror("❌ Error", "Solo el administrador puede actualizar programas")
            return
            
        if not hasattr(self, 'programs_tree') or not self.programs_tree.selection():
            messagebox.showwarning("⚠️ Advertencia", "Selecciona un programa para actualizar")
            return
            
        selection = self.programs_tree.selection()
        item = self.programs_tree.item(selection[0])
        program_name = item['text']  
        
        if not self.programs_data[program_name]['installed']:
            messagebox.showerror("❌ Error", f"{program_name} no está instalado")
            return
            
        if messagebox.askyesno("🔄 Actualizar", f"¿Actualizar {program_name} a la última versión?"):
            self.simulate_update(program_name)

    def simulate_update(self, program_name):
        """Simular actualización de programa"""
        # Crear ventana de actualización
        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizando Programa")
        update_window.geometry("450x250")
        update_window.configure(bg="white")
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Centrar ventana
        update_window.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 225),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 125)
        ))
        
        tk.Label(
            update_window,
            text=f"🔄 Actualizando {program_name}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#f59e0b"
        ).pack(pady=20)
        
        # Barra de progreso
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(update_window, variable=progress_var, maximum=100, length=350)
        progress_bar.pack(pady=20)
        
        status_label = tk.Label(
            update_window,
            text="Verificando actualizaciones...",
            font=("Arial", 11),
            bg="white",
            fg="#6b7280"
        )
        status_label.pack(pady=10)
        
        # Simular actualización
        update_steps = [
            (20, "Descargando actualización..."),
            (50, "Aplicando parches..."),
            (80, "Configurando nueva versión..."),
            (100, "Actualización completada")
        ]
        
        def update_progress(step_index=0):
            if step_index < len(update_steps):
                progress, status = update_steps[step_index]
                progress_var.set(progress)
                status_label.config(text=status)
                update_window.after(1000, lambda: update_progress(step_index + 1))
            else:
                # Actualización completada
                update_window.after(1000, lambda: self.complete_update(program_name, update_window))
        
        update_progress()

    def complete_update(self, program_name, update_window):
        """Completar la actualización del programa"""
        # Actualizar versión REALMENTE
        current_version = self.programs_data[program_name]['version']
        version_parts = current_version.split('.')
        
        # Incrementar versión menor
        if len(version_parts) >= 2:
            try:
                minor_version = int(version_parts[-1])
                version_parts[-1] = str(minor_version + 1)
                new_version = '.'.join(version_parts)
            except:
                new_version = current_version + ".1"
        else:
            new_version = current_version + ".1"
        
        self.programs_data[program_name]['version'] = new_version
        self.save_programs_data()
        self.refresh_programs_list()
        
        # Cerrar ventana
        update_window.destroy()
        
        messagebox.showinfo("✅ Actualización Exitosa", 
            f"🔄 {program_name} actualizado correctamente\n\n"
            f"📊 Versión anterior: {current_version}\n"
            f"🆕 Nueva versión: {new_version}\n"
            f"✨ Mejoras de rendimiento y nuevas características")

    def uninstall_selected_program(self):
        """Desinstalar programa seleccionado (proteger utilerías)"""
        if self.user_type != "Administrador":
            messagebox.showerror("❌ Error", "Solo el administrador puede desinstalar programas")
            return
            
        if not hasattr(self, 'programs_tree') or not self.programs_tree.selection():
            messagebox.showwarning("⚠️ Advertencia", "Selecciona un programa para desinstalar")
            return
            
        selection = self.programs_tree.selection()
        item = self.programs_tree.item(selection[0])
        program_name = item['text']  
        
        # Verificar si es una utilería del sistema (PROTECCIÓN MEJORADA - incluye Calculadora y Calendario)
        system_utilities = ["Calculadora", "Calendario", "Bloc de Notas", "Explorador de Archivos", "Gestor de Programas", "Monitor Sistema"]
        if program_name in system_utilities:
            messagebox.showerror("🔒 Error de Sistema", 
                f"{program_name} es una utilería crítica del sistema operativo.\n\n"
                f"🚫 No se puede desinstalar por seguridad del sistema.\n"
                f"💡 Esta protección evita daños al funcionamiento básico.")
            return
        
        if not self.programs_data[program_name]['installed']:
            messagebox.showinfo("ℹ️ Info", f"{program_name} no está instalado")
            return
            
        if messagebox.askyesno("🗑️ Desinstalar", f"¿Estás seguro de desinstalar {program_name}?\n\nEsta acción no se puede deshacer."):
            self.simulate_uninstall(program_name)

    def simulate_uninstall(self, program_name):
        """Simular desinstalación de programa"""
        # Crear ventana de desinstalación
        uninstall_window = tk.Toplevel(self.root)
        uninstall_window.title("Desinstalando Programa")
        uninstall_window.geometry("450x250")
        uninstall_window.configure(bg="white")
        uninstall_window.transient(self.root)
        uninstall_window.grab_set()
        
        # Centrar ventana
        uninstall_window.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 225),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 125)
        ))
        
        tk.Label(
            uninstall_window,
            text=f"🗑️ Desinstalando {program_name}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#dc2626"
        ).pack(pady=20)
        
        # Barra de progreso
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(uninstall_window, variable=progress_var, maximum=100, length=350)
        progress_bar.pack(pady=20)
        
        status_label = tk.Label(
            uninstall_window,
            text="Preparando desinstalación...",
            font=("Arial", 11),
            bg="white",
            fg="#6b7280"
        )
        status_label.pack(pady=10)
        
        # Simular desinstalación
        uninstall_steps = [
            (25, "Cerrando procesos del programa..."),
            (50, "Eliminando archivos..."),
            (75, "Limpiando registro del sistema..."),
            (100, "Desinstalación completada")
        ]
        
        def uninstall_progress(step_index=0):
            if step_index < len(uninstall_steps):
                progress, status = uninstall_steps[step_index]
                progress_var.set(progress)
                status_label.config(text=status)
                uninstall_window.after(1000, lambda: uninstall_progress(step_index + 1))
            else:
                # Desinstalación completada
                uninstall_window.after(1000, lambda: self.complete_uninstall(program_name, uninstall_window))
        
        uninstall_progress()

    def complete_uninstall(self, program_name, uninstall_window):
        """Completar la desinstalación del programa"""
        # Actualizar datos REALMENTE
        self.programs_data[program_name]['installed'] = False
        self.save_programs_data()
        self.refresh_programs_list()
        
        # Cerrar ventana
        uninstall_window.destroy()
        
        messagebox.showinfo("✅ Desinstalación Exitosa", 
            f"🗑️ {program_name} ha sido desinstalado correctamente\n\n"
            f"🧹 Archivos eliminados del sistema\n"
            f"📊 Espacio liberado: {self.programs_data[program_name]['size']}\n"
            f"💡 Puedes reinstalarlo cuando lo necesites")

    # ==================== UTILERÍAS COMPLETAS ====================

    def open_utilities_menu(self):
        def create_utilities_content(window):
            tk.Label(
                window,
                text="🛠️ UTILERÍAS DEL SISTEMA",
                font=("Arial", 18, "bold"),
                bg="white",
                fg="#ea580c"
            ).pack(pady=30)
    

            utilities_frame = tk.Frame(window, bg="white")
            utilities_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
            utilities = [
                ("🔢", "Calculadora", self.open_calculator),
                ("📅", "Calendario", self.open_calendar),
                ("📊", "Monitor Sistema", self.open_system_monitor)
            ]
        
            for i, (emoji, name, command) in enumerate(utilities):
            # Organizar en una fila de 3 columnas
                row = 0
                col = i
            
                utility_frame = tk.Frame(utilities_frame, bg="#f8fafc", relief=tk.RAISED, borderwidth=3, cursor="hand2")
                utility_frame.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")
            
                # Hacer todo el frame clickeable
                utility_frame.bind("<Button-1>", lambda e, cmd=command: cmd())
                utility_frame.bind("<Enter>", lambda e, frame=utility_frame: frame.configure(bg="#e2e8f0"))
                utility_frame.bind("<Leave>", lambda e, frame=utility_frame: frame.configure(bg="#f8fafc"))
            
                emoji_label = tk.Label(
                    utility_frame,
                    text=emoji,
                    font=("Arial", 48),
                    bg="#f8fafc",
                    cursor="hand2"
                )
                emoji_label.pack(pady=20)
                emoji_label.bind("<Button-1>", lambda e, cmd=command: cmd())
                emoji_label.bind("<Enter>", lambda e, frame=utility_frame, lbl=emoji_label: [
                    frame.configure(bg="#e2e8f0"),
                    lbl.configure(bg="#e2e8f0")
                ])
                emoji_label.bind("<Leave>", lambda e, frame=utility_frame, lbl=emoji_label: [
                    frame.configure(bg="#f8fafc"),
                    lbl.configure(bg="#f8fafc")
                ])
            
                name_label = tk.Label(
                    utility_frame,
                    text=name,
                    font=("Arial", 14, "bold"),
                    bg="#f8fafc",
                    fg="#1f2937",
                    cursor="hand2"
                )
                name_label.pack(pady=10)
                name_label.bind("<Button-1>", lambda e, cmd=command: cmd())
                name_label.bind("<Enter>", lambda e, frame=utility_frame, lbl=name_label: [
                    frame.configure(bg="#e2e8f0"),
                    lbl.configure(bg="#e2e8f0")
                ])
                name_label.bind("<Leave>", lambda e, frame=utility_frame, lbl=name_label: [
                    frame.configure(bg="#f8fafc"),
                    lbl.configure(bg="#f8fafc")
                ])
            
                # Agregar texto indicativo
                hint_label = tk.Label(
                    utility_frame,
                    text="Clic para abrir",
                    font=("Arial", 10),
                    bg="#f8fafc",
                    fg="#6b7280",
                    cursor="hand2"
                )
                hint_label.pack(pady=(0, 15))
                hint_label.bind("<Button-1>", lambda e, cmd=command: cmd())
                hint_label.bind("<Enter>", lambda e, frame=utility_frame, lbl=hint_label: [
                    frame.configure(bg="#e2e8f0"),
                    lbl.configure(bg="#e2e8f0")
                ])
                hint_label.bind("<Leave>", lambda e, frame=utility_frame, lbl=hint_label: [
                    frame.configure(bg="#f8fafc"),
                    lbl.configure(bg="#f8fafc")
                ])
    
        # Configurar grid para 3 columnas
            utilities_frame.grid_columnconfigure(0, weight=1)
            utilities_frame.grid_columnconfigure(1, weight=1)
            utilities_frame.grid_columnconfigure(2, weight=1)
            utilities_frame.grid_rowconfigure(0, weight=1)
    
        self.create_window("Utilerías", create_utilities_content, 700, 600)

    def simulate_word(self):
        """Simular Microsoft Word"""
        def create_word_content(window):
            window.configure(bg="#ffffff")
            
            tk.Label(
                window,
                text="📄 Microsoft Word",
                font=("Arial", 16, "bold"),
                bg="#2b579a",
                fg="white"
            ).pack(fill='x', pady=10)
            
            # Toolbar
            toolbar = tk.Frame(window, bg="#f0f0f0")
            toolbar.pack(fill='x', padx=10, pady=5)
            
            toolbar_buttons = ["📄 Nuevo", "📁 Abrir", "💾 Guardar", "🖨️ Imprimir"]
            
            for btn_text in toolbar_buttons:
                tk.Button(
                    toolbar,
                    text=btn_text,
                    font=("Arial", 10),
                    command=lambda t=btn_text: messagebox.showinfo("📄", f"{t} (simulado)")
                ).pack(side='left', padx=2, pady=2)
            
            # Text area
            text_frame = tk.Frame(window)
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_area = tk.Text(
                text_frame,
                font=("Times New Roman", 12),
                wrap=tk.WORD
            )
            
            scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
            text_area.configure(yscrollcommand=scrollbar.set)
            
            text_area.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            sample_text = """📄 Documento de Microsoft Word - Simulación

Este es un procesador de texto simulado que imita las funcionalidades básicas de Microsoft Word.

Características disponibles:
• Escribir y editar texto
• Barra de herramientas funcional
• Funciones básicas de edición
• Formato de texto
• Guardar y abrir documentos (simulado)

Instrucciones:
Puedes escribir aquí tu contenido y usar las opciones de la barra de herramientas para simular las operaciones de un procesador de texto real.

"""
            text_area.insert(1.0, sample_text)
        
        self.create_window("Microsoft Word", create_word_content, 800, 600)

    def simulate_chrome(self):
        """Simular Google Chrome"""
        def create_chrome_content(window):
            window.configure(bg="#ffffff")
            
            # Address bar
            address_frame = tk.Frame(window, bg="#f1f3f4")
            address_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Button(address_frame, text="⬅️", font=("Arial", 12)).pack(side='left', padx=2)
            tk.Button(address_frame, text="➡️", font=("Arial", 12)).pack(side='left', padx=2)
            tk.Button(address_frame, text="🔄", font=("Arial", 10)).pack(side='left', padx=2)
            
            url_entry = tk.Entry(address_frame, font=("Arial", 11))
            url_entry.pack(side='left', fill='x', expand=True, padx=10)
            url_entry.insert(0, "https://www.google.com")
            
            # Content area
            content_frame = tk.Frame(window, bg="white")
            content_frame.pack(fill='both', expand=True)
            
            tk.Label(
                content_frame,
                text="🌐 Google",
                font=("Arial", 48, "bold"),
                bg="white",
                fg="#4285f4"
            ).pack(pady=80)
            
            # Search bar
            search_frame = tk.Frame(content_frame, bg="white")
            search_frame.pack(pady=20)
            
            search_entry = tk.Entry(search_frame, font=("Arial", 14), width=50)
            search_entry.pack(side='left', padx=10)
            
            tk.Button(
                search_frame,
                text="🔍 Buscar",
                font=("Arial", 11),
                command=lambda: messagebox.showinfo("🔍", f"Buscando: {search_entry.get()}")
            ).pack(side='left', padx=5)
        
        self.create_window("Google Chrome", create_chrome_content, 900, 600)

    def open_calculator(self):
        """Abrir calculadora"""
        def create_calculator_content(window):
            tk.Label(
                window,
                text="🔢 Calculadora",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#1f2937"
            ).pack(pady=20)
            
            # Display
            display_var = tk.StringVar(value="0")
            display = tk.Entry(
                window,
                textvariable=display_var,
                font=("Arial", 18, "bold"),
                justify=tk.RIGHT,
                state="readonly"
            )
            display.pack(fill='x', padx=20, pady=10)
            
            # Buttons
            buttons_frame = tk.Frame(window)
            buttons_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            buttons = [
                ["C", "/", "*", "-"],
                ["7", "8", "9", "+"],
                ["4", "5", "6", "+"],
                ["1", "2", "3", "="],
                ["0", "0", ".", "="]
            ]
            
            for i, row in enumerate(buttons):
                for j, btn_text in enumerate(row):
                    if (i == 4 and j == 1) or (i == 3 and j == 3 and i == 4 and j == 3):
                        continue
                    
                    btn = tk.Button(
                        buttons_frame,
                        text=btn_text,
                        font=("Arial", 14, "bold"),
                        command=lambda t=btn_text: messagebox.showinfo("🔢", f"Botón: {t}")
                    )
                    
                    if btn_text == "0" and i == 4:
                        btn.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=2, pady=2)
                    elif btn_text == "=" and i == 3:
                        btn.grid(row=i, column=j, rowspan=2, sticky="nsew", padx=2, pady=2)
                    else:
                        btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
            
            # Configure grid
            for i in range(5):
                buttons_frame.grid_rowconfigure(i, weight=1)
            for j in range(4):
                buttons_frame.grid_columnconfigure(j, weight=1)
        
        self.create_window("Calculadora", create_calculator_content, 300, 400)

    def open_calendar(self):
         """Calculadora completa en una sola función"""
    # Verificar si ya existe una calculadora abierta
         for window in self.open_windows:
            try:
                if window.winfo_exists() and window.title() == "Calculadora":
                    window.lift()
                    window.focus_force()
                    return
            except:
                continue
        
            calc_window = tk.Toplevel(self.root)
            calc_window.title("Calculadora")
            calc_window.geometry("320x450")
            calc_window.configure(bg="#2d2d2d")
            calc_window.resizable(False, False)
            
            # Centrar ventana
            self.center_window(calc_window, 320, 450)
            
            # Variables locales para la calculadora
            display_var = tk.StringVar()
            display_var.set("0")
            operation_data = {
                'operand1': 0,
                'operand2': 0,
                'operator': "",
                'new_number': True
            }
            
            def button_click(button_text):
                """Manejar clics en botones"""
                try:
                    current = display_var.get()
                    
                    if button_text in '0123456789':
                        if operation_data['new_number'] or current == "0":
                            display_var.set(button_text)
                            operation_data['new_number'] = False
                        else:
                            if len(current) < 15:
                                display_var.set(current + button_text)
                    
                    elif button_text == '.':
                        if operation_data['new_number']:
                            display_var.set("0.")
                            operation_data['new_number'] = False
                        elif '.' not in current:
                            display_var.set(current + ".")
                    
                    elif button_text == 'C':
                        display_var.set("0")
                        operation_data.update({'operand1': 0, 'operand2': 0, 'operator': "", 'new_number': True})
                    
                    elif button_text == '±':
                        if current != "0":
                            if current.startswith('-'):
                                display_var.set(current[1:])
                            else:
                                display_var.set('-' + current)
                    
                    elif button_text == '%':
                        try:
                            value = float(current) / 100
                            result = str(value) if value == int(value) else f"{value:.10f}".rstrip('0').rstrip('.')
                            display_var.set(result)
                            operation_data['new_number'] = True
                        except:
                            display_var.set("Error")
                            operation_data['new_number'] = True
                    
                    elif button_text in '+-×÷':
                        try:
                            if operation_data['operator'] and not operation_data['new_number']:
                                operation_data['operand2'] = float(current)
                                if operation_data['operator'] == '+':
                                    result = operation_data['operand1'] + operation_data['operand2']
                                elif operation_data['operator'] == '-':
                                    result = operation_data['operand1'] - operation_data['operand2']
                                elif operation_data['operator'] == '×':
                                    result = operation_data['operand1'] * operation_data['operand2']
                                elif operation_data['operator'] == '÷':
                                    if operation_data['operand2'] == 0:
                                        display_var.set("Error")
                                        operation_data['new_number'] = True
                                        return
                                    result = operation_data['operand1'] / operation_data['operand2']
                                
                                formatted = str(int(result)) if result == int(result) else f"{result:.10f}".rstrip('0').rstrip('.')
                                display_var.set(formatted)
                                operation_data['operand1'] = result
                            else:
                                operation_data['operand1'] = float(current)
                            
                            operation_data['operator'] = button_text
                            operation_data['new_number'] = True
                        except:
                            display_var.set("Error")
                            operation_data['new_number'] = True
                    
                    elif button_text == '=':
                        try:
                            if operation_data['operator']:
                                operation_data['operand2'] = float(current)
                                if operation_data['operator'] == '+':
                                    result = operation_data['operand1'] + operation_data['operand2']
                                elif operation_data['operator'] == '-':
                                    result = operation_data['operand1'] - operation_data['operand2']
                                elif operation_data['operator'] == '×':
                                    result = operation_data['operand1'] * operation_data['operand2']
                                elif operation_data['operator'] == '÷':
                                    if operation_data['operand2'] == 0:
                                        display_var.set("Error")
                                        operation_data['new_number'] = True
                                        return
                                    result = operation_data['operand1'] / operation_data['operand2']
                                
                                formatted = str(int(result)) if result == int(result) else f"{result:.10f}".rstrip('0').rstrip('.')
                                display_var.set(formatted)
                                operation_data['operator'] = ""
                                operation_data['new_number'] = True
                        except:
                            display_var.set("Error")
                            operation_data['new_number'] = True
                except:
                    display_var.set("Error")
                    operation_data['new_number'] = True
            
            def key_press(event):
                """Manejar teclas del teclado"""
                key_map = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9',
                        '.':'.', '+':'+', '-':'-', '*':'×', '/':'÷', '=':'=', '\r':'=', '\n':'=', 'c':'C', 'C':'C'}
                
                if event.char in key_map:
                    button_click(key_map[event.char])
                elif event.keysym == 'Escape':
                    button_click('C')
                elif event.keysym == 'BackSpace':
                    current = display_var.get()
                    if len(current) > 1 and not operation_data['new_number']:
                        display_var.set(current[:-1])
                    else:
                        display_var.set("0")
                        operation_data['new_number'] = True
            
            # Display
            display_frame = tk.Frame(calc_window, bg="#2d2d2d", pady=20)
            display_frame.pack(fill=tk.X, padx=20)
            
            tk.Entry(display_frame, textvariable=display_var, font=("Consolas", 24, "bold"),
                    bg="#1a1a1a", fg="white", relief=tk.FLAT, bd=10, justify=tk.RIGHT, 
                    state="readonly").pack(fill=tk.X, ipady=10)
            
            # Botones
            buttons_frame = tk.Frame(calc_window, bg="#2d2d2d")
            buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            buttons = [['C', '±', '%', '÷'], ['7', '8', '9', '×'], ['4', '5', '6', '-'], 
                    ['1', '2', '3', '+'], ['0', '.', '=']]
            
            for i, row in enumerate(buttons):
                for j, text in enumerate(row):
                    if text in '0123456789.':
                        bg, fg = "#404040", "white"
                    elif text in '+-×÷=':
                        bg, fg = "#ff9500", "white"
                    else:
                        bg, fg = "#a6a6a6", "black"
                    
                    colspan = 2 if text == '0' else 1
                    
                    btn = tk.Button(buttons_frame, text=text, font=("Segoe UI", 18, "bold"),
                                bg=bg, fg=fg, relief=tk.FLAT, bd=0, command=lambda t=text: button_click(t))
                    btn.grid(row=i, column=j, columnspan=colspan, sticky="nsew", padx=2, pady=2)
                    
                    # Efectos hover
                    btn.bind("<Enter>", lambda e, b=btn, orig=bg: b.configure(bg="#ffad33" if orig=="#ff9500" else "#505050" if orig=="#404040" else "#b6b6b6"))
                    btn.bind("<Leave>", lambda e, b=btn, orig=bg: b.configure(bg=orig))
            
            # Configurar grid
            for i in range(5):
                buttons_frame.grid_rowconfigure(i, weight=1)
            for j in range(4):
                buttons_frame.grid_columnconfigure(j, weight=1)
            
            # Eventos de teclado
            calc_window.bind('<Key>', key_press)
            calc_window.focus_set()
            
            self.open_windows.append(calc_window)

    def open_system_monitor(self):
        """Abrir monitor del sistema"""
        def create_monitor_content(window):
            tk.Label(
                window,
                text="📊 Monitor del Sistema",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#059669"
            ).pack(pady=20)
            
            # System info
            info_frame = tk.Frame(window, bg="#f8fafc", relief=tk.RAISED, borderwidth=2)
            info_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            tk.Label(
                info_frame,
                text="💻 Información del Sistema",
                font=("Arial", 14, "bold"),
                bg="#f8fafc",
                fg="#1f2937"
            ).pack(pady=10)
            
            system_info = [
                "🖥️ Sistema Operativo: Windows Simulator v2.1",
                "💾 Memoria RAM: 8 GB",
                "💽 Almacenamiento: 500 GB SSD",
                "⚡ Procesador: Intel Core i7",
                f"👤 Usuario actual: {self.current_user}",
                f"🔐 Tipo de cuenta: {self.user_type}",
                f"📦 Programas instalados: {sum(1 for p in self.programs_data.values() if p['installed'])}"
            ]
            
            for info in system_info:
                tk.Label(
                    info_frame,
                    text=info,
                    font=("Arial", 11),
                    bg="#f8fafc",
                    fg="#4b5563"
                ).pack(anchor='w', padx=20, pady=2)
            
            # Performance metrics
            perf_frame = tk.Frame(window, bg="#f8fafc", relief=tk.RAISED, borderwidth=2)
            perf_frame.pack(fill='x', padx=20, pady=10)
            
            tk.Label(
                perf_frame,
                text="📈 Rendimiento del Sistema",
                font=("Arial", 14, "bold"),
                bg="#f8fafc",
                fg="#1f2937"
            ).pack(pady=10)
            
            # Simulated performance
            metrics = [
                ("🔥 CPU", random.randint(20, 80)),
                ("💾 RAM", random.randint(30, 70)),
                ("💽 Disco", random.randint(10, 50)),
                ("🌐 Red", random.randint(5, 95))
            ]
            
            for metric, value in metrics:
                tk.Label(
                    perf_frame,
                    text=f"{metric}: {value}%",
                    font=("Arial", 11),
                    bg="#f8fafc",
                    fg="#4b5563"
                ).pack(anchor='w', padx=20, pady=2)
        
        self.create_window("Monitor del Sistema", create_monitor_content, 500, 700)

    def open_notepad(self):
        """Abrir bloc de notas"""
        def create_notepad_content(window):
            tk.Label(
                window,
                text="📝 Bloc de Notas",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#16a34a"
            ).pack(pady=10)
            
            # Toolbar
            toolbar = tk.Frame(window, bg="#f3f4f6")
            toolbar.pack(fill='x', padx=10, pady=5)
            
            toolbar_buttons = ["📄 Nuevo", "📁 Abrir", "💾 Guardar", "🖨️ Imprimir"]
            
            for btn_text in toolbar_buttons:
                tk.Button(
                    toolbar,
                    text=btn_text,
                    font=("Arial", 10),
                    command=lambda t=btn_text: messagebox.showinfo("📝", f"{t} (simulado)")
                ).pack(side='left', padx=2, pady=2)
            
            # Text area
            text_frame = tk.Frame(window)
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_area = tk.Text(
                text_frame,
                font=("Consolas", 11),
                wrap=tk.WORD
            )
            
            scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
            text_area.configure(yscrollcommand=scrollbar.set)
            
            text_area.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Sample text
            sample_text = """📝 Bloc de Notas - Sistema Operativo Simulado

Este es un editor de texto simple que simula las funcionalidades básicas de un bloc de notas."""
            text_area.insert(1.0, sample_text)
        
        self.create_window("Bloc de Notas", create_notepad_content, 600, 400)

    def open_recycle_bin(self):
        """Abrir papelera de reciclaje"""
        def create_recycle_content(window):
            tk.Label(
                window,
                text="🗑️ Papelera de Reciclaje",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#6b7280"
            ).pack(pady=20)
            
            tk.Label(
                window,
                text="🗑️",
                font=("Arial", 48),
                bg="white",
                fg="#6b7280"
            ).pack(pady=50)
            
            tk.Label(
                window,
                text="La papelera está vacía",
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#6b7280"
            ).pack(pady=10)
            
            tk.Label(
                window,
                text="No hay elementos eliminados para mostrar.",
                font=("Arial", 11),
                bg="white",
                fg="#9ca3af"
            ).pack(pady=5)
            
            # Buttons
            buttons_frame = tk.Frame(window, bg="white")
            buttons_frame.pack(pady=30)
            
            tk.Button(
                buttons_frame,
                text="🔄 Actualizar",
                font=("Arial", 11, "bold"),
                bg="#6b7280",
                fg="white",
                width=15,
                command=lambda: messagebox.showinfo("🔄", "Papelera actualizada")
            ).pack(side='left', padx=10)
            
            tk.Button(
                buttons_frame,
                text="🧹 Vaciar",
                font=("Arial", 11, "bold"),
                bg="#dc2626",
                fg="white",
                width=15,
                command=lambda: messagebox.showinfo("🧹", "La papelera ya está vacía")
            ).pack(side='left', padx=10)
        
        self.create_window("Papelera", create_recycle_content, 400, 350)

    def run(self):
        """Ejecutar el simulador"""
        try:
            print("🚀 Iniciando Sistema Operativo Simulado...")
            print("📁 Directorios creados correctamente")
            print("🖼️ Imágenes cargadas (o placeholders creados)")
            print("💾 Datos del sistema inicializados")
            print("✅ Sistema listo para usar")
            print("\n" + "="*50)
            print("CREDENCIALES DE ACCESO:")
            print("👤 Administrador: admin / admin123")
            print("👤 Usuario: usuario / user123")
            print("="*50 + "\n")
            self.root.mainloop()
            
        except Exception as e:
            print(f"❌ Error crítico: {e}")
            messagebox.showerror("Error Crítico", f"Error al iniciar el sistema: {e}")
        finally:
            print("🔚 Sistema Operativo Simulado cerrado")

def main():
    """Función principal del programa"""
    try:
        # Verificar dependencias
        try:
            from PIL import Image, ImageTk, ImageFilter, ImageEnhance
            print("✅ PIL/Pillow disponible")
        except ImportError:
            print("⚠️ PIL/Pillow no encontrado. Instalando...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("✅ PIL/Pillow instalado correctamente")
        
        # Crear y ejecutar el simulador
        simulator = SimuladorSO()
        simulator.run()
        
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()