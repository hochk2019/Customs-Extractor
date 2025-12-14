"""
Customs Extractor V2 - GUI Application
Supports both Export (TKX) and Import (TKN) declarations with tabbed interface
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
from pathlib import Path
from typing import Optional
from config import Config
from extractor_core_v2 import ExportExtractor, ImportExtractor, ExtractionProgress, DeclarationType

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CustomsExtractorV2(ctk.CTk):
    """Main application window V2 with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration
        self.config = Config()
        
        # Window setup
        self.title("🎯 Trích xuất dữ liệu Tờ khai Hải quan - V2")
        self.geometry(self.config.get("window_geometry", "1000x750"))
        
        # Apply saved theme
        ctk.set_appearance_mode(self.config.get("theme", "dark"))
        
        # State for each tab
        self.export_state = {
            'file_var': ctk.StringVar(),
            'output_folder_var': ctk.StringVar(),
            'output_name_var': ctk.StringVar(value="DS hàng xuất"),
            'is_extracting': False,
            'extractor': None
        }
        
        self.import_state = {
            'file_var': ctk.StringVar(),
            'output_folder_var': ctk.StringVar(),
            'output_name_var': ctk.StringVar(value="DS hàng nhập"),
            'is_extracting': False,
            'extractor': None
        }
        
        # Shared options
        self.auto_open_var = ctk.BooleanVar(value=self.config.get("auto_open", True))
        self.show_preview_var = ctk.BooleanVar(value=self.config.get("show_preview", True))
        self.auto_update_output_var = ctk.BooleanVar(value=self.config.get("auto_update_output", True))
        
        # Build UI
        self.create_widgets()
        
        # Protocol for window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkLabel(
            main_frame,
            text="🎯 Trích xuất dữ liệu Tờ khai Hải quan V2",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header.pack(pady=10)
        
        # Tabview for Export and Import
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True, pady=10)
        
        # Add tabs
        self.tab_export = self.tabview.add("TK Xuất khẩu")
        self.tab_import = self.tabview.add("TK Nhập khẩu")
        
        # Build each tab
        self.build_export_tab()
        self.build_import_tab()
        
        # Shared settings section (below tabs)
        self.build_shared_settings(main_frame)
    
    def build_export_tab(self):
        """Build Export declaration tab"""
        tab = self.tab_export
        
        # Input file
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            input_frame,
            text="📁 File Excel xuất khẩu:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        input_controls = ctk.CTkFrame(input_frame)
        input_controls.pack(fill="x", padx=10, pady=5)
        
        entry = ctk.CTkEntry(
            input_controls,
            textvariable=self.export_state['file_var'],
            placeholder_text="Chọn file TKX..."
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(
            input_controls,
            text="Browse",
            command=lambda: self.browse_input_file(DeclarationType.EXPORT),
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            input_controls,
            text="Recent ▼",
            command=lambda: self.show_recent_files(DeclarationType.EXPORT),
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left")
        
        # Output folder
        output_folder_frame = ctk.CTkFrame(tab)
        output_folder_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            output_folder_frame,
            text="📂 Thư mục đầu ra:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        output_controls = ctk.CTkFrame(output_folder_frame)
        output_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkEntry(
            output_controls,
            textvariable=self.export_state['output_folder_var'],
            placeholder_text="Mặc định: cùng thư mục với file đầu vào"
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(
            output_controls,
            text="Browse",
            command=lambda: self.browse_output_folder(DeclarationType.EXPORT),
            width=100
        ).pack(side="left")
        
        # Output filename
        filename_frame = ctk.CTkFrame(tab)
        filename_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            filename_frame,
            text="📝 Tên file đầu ra:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        filename_controls = ctk.CTkFrame(filename_frame)
        filename_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkEntry(
            filename_controls,
            textvariable=self.export_state['output_name_var']
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(filename_controls, text=".xlsx").pack(side="left")
        
        # Extract button
        self.export_state['extract_btn'] = ctk.CTkButton(
            tab,
            text="⚡ Extract Data (Xuất khẩu)",
            command=lambda: self.start_extraction(DeclarationType.EXPORT),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.export_state['extract_btn'].pack(fill="x", padx=10, pady=10)
        
        # Progress
        progress_frame = ctk.CTkFrame(tab, fg_color="transparent", border_width=2)
        progress_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            progress_frame,
            text="📊 Tiến trình",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.export_state['progress_bar'] = ctk.CTkProgressBar(progress_frame)
        self.export_state['progress_bar'].pack(fill="x", padx=10, pady=5)
        self.export_state['progress_bar'].set(0)
        
        self.export_state['log_text'] = ctk.CTkTextbox(progress_frame, height=100)
        self.export_state['log_text'].pack(fill="both", expand=True, padx=10, pady=5)
        self.export_state['log_text'].configure(state="disabled")
        
        self.export_state['stats_label'] = ctk.CTkLabel(
            tab,
            text="📈 Sẵn sàng",
            font=ctk.CTkFont(size=12)
        )
        self.export_state['stats_label'].pack(pady=5)
    
    def build_import_tab(self):
        """Build Import declaration tab"""
        tab = self.tab_import
        
        # Input file
        input_frame = ctk.CTkFrame(tab)
        input_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            input_frame,
            text="📁 File Excel nhập khẩu:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        input_controls = ctk.CTkFrame(input_frame)
        input_controls.pack(fill="x", padx=10, pady=5)
        
        entry = ctk.CTkEntry(
            input_controls,
            textvariable=self.import_state['file_var'],
            placeholder_text="Chọn file TKN..."
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(
            input_controls,
            text="Browse",
            command=lambda: self.browse_input_file(DeclarationType.IMPORT),
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            input_controls,
            text="Recent ▼",
            command=lambda: self.show_recent_files(DeclarationType.IMPORT),
            width=100,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left")
        
        # Output folder
        output_folder_frame = ctk.CTkFrame(tab)
        output_folder_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            output_folder_frame,
            text="📂 Thư mục đầu ra:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        output_controls = ctk.CTkFrame(output_folder_frame)
        output_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkEntry(
            output_controls,
            textvariable=self.import_state['output_folder_var'],
            placeholder_text="Mặc định: cùng thư mục với file đầu vào"
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(
            output_controls,
            text="Browse",
            command=lambda: self.browse_output_folder(DeclarationType.IMPORT),
            width=100
        ).pack(side="left")
        
        # Output filename
        filename_frame = ctk.CTkFrame(tab)
        filename_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            filename_frame,
            text="📝 Tên file đầu ra:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        filename_controls = ctk.CTkFrame(filename_frame)
        filename_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkEntry(
            filename_controls,
            textvariable=self.import_state['output_name_var']
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(filename_controls, text=".xlsx").pack(side="left")
        
        # Extract button
        self.import_state['extract_btn'] = ctk.CTkButton(
            tab,
            text="⚡ Extract Data (Nhập khẩu)",
            command=lambda: self.start_extraction(DeclarationType.IMPORT),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.import_state['extract_btn'].pack(fill="x", padx=10, pady=10)
        
        # Progress
        progress_frame = ctk.CTkFrame(tab, fg_color="transparent", border_width=2)
        progress_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        ctk.CTkLabel(
            progress_frame,
            text="📊 Tiến trình",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.import_state['progress_bar'] = ctk.CTkProgressBar(progress_frame)
        self.import_state['progress_bar'].pack(fill="x", padx=10, pady=5)
        self.import_state['progress_bar'].set(0)
        
        self.import_state['log_text'] = ctk.CTkTextbox(progress_frame, height=100)
        self.import_state['log_text'].pack(fill="both", expand=True, padx=10, pady=5)
        self.import_state['log_text'].configure(state="disabled")
        
        self.import_state['stats_label'] = ctk.CTkLabel(
            tab,
            text="📈 Sẵn sàng",
            font=ctk.CTkFont(size=12)
        )
        self.import_state['stats_label'].pack(pady=5)
    
    def build_shared_settings(self, parent):
        """Build shared settings section"""
        settings_frame = ctk.CTkFrame(parent, fg_color="transparent", border_width=2)
        settings_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            settings_frame,
            text="⚙️ Tùy chọn chung",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        options_grid = ctk.CTkFrame(settings_frame, fg_color="transparent")
        options_grid.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkCheckBox(
            options_grid,
            text="☑ Tự động mở file sau khi extract",
            variable=self.auto_open_var
        ).pack(side="left", padx=10)
        
        ctk.CTkCheckBox(
            options_grid,
            text="☑ Hiển thị preview trước khi extract",
            variable=self.show_preview_var
        ).pack(side="left", padx=10)
        
        ctk.CTkCheckBox(
            options_grid,
            text="☑ Tự động cập nhật thư mục đầu ra",
            variable=self.auto_update_output_var
        ).pack(side="left", padx=10)
    
    def get_current_state(self, decl_type: DeclarationType):
        """Get state dict for current declaration type"""
        return self.export_state if decl_type == DeclarationType.EXPORT else self.import_state
    
    def log_message(self, message: str, decl_type: DeclarationType):
        """Add message to log viewer"""
        state = self.get_current_state(decl_type)
        log_text = state['log_text']
        log_text.configure(state="normal")
        log_text.insert("end", message + "\n")
        log_text.see("end")
        log_text.configure(state="disabled")
    
    def browse_input_file(self, decl_type: DeclarationType):
        """Browse for input Excel file"""
        state = self.get_current_state(decl_type)
        
        config_key = f"last_{decl_type.value}_folder"
        initial_dir = self.config.get(config_key, "")
        if not initial_dir or not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")
        
        filename = filedialog.askopenfilename(
            title=f"Chọn file {decl_type.value}",
            initialdir=initial_dir,
            filetypes=[("Excel files", "*.xls *.xlsx"), ("All files", "*.*")]
        )
        
        if filename:
            state['file_var'].set(filename)
            
            folder = os.path.dirname(filename)
            self.config.set(config_key, folder)
            
            if self.auto_update_output_var.get():
                state['output_folder_var'].set(folder)
    
    def browse_output_folder(self, decl_type: DeclarationType):
        """Browse for output folder"""
        state = self.get_current_state(decl_type)
        
        initial_dir = state['output_folder_var'].get() or os.path.expanduser("~")
        
        folder = filedialog.askdirectory(
            title="Chọn thư mục đầu ra",
            initialdir=initial_dir
        )
        
        if folder:
            state['output_folder_var'].set(folder)
    
    def show_recent_files(self, decl_type: DeclarationType):
        """Show recent files for this declaration type"""
        messagebox.showinfo("Recent Files", f"Recent files for {decl_type.value} - Coming soon!")
    
    def validate_inputs(self, decl_type: DeclarationType) -> bool:
        """Validate user inputs"""
        state = self.get_current_state(decl_type)
        
        if not state['file_var'].get():
            messagebox.showerror("Lỗi", "Vui lòng chọn file Excel đầu vào!")
            return False
        
        if not os.path.exists(state['file_var'].get()):
            messagebox.showerror("Lỗi", "File đầu vào không tồn tại!")
            return False
        
        if not state['output_name_var'].get():
            messagebox.showerror("Lỗi", "Vui lòng nhập tên file đầu ra!")
            return False
        
        return True
    
    def start_extraction(self, decl_type: DeclarationType):
        """Start the extraction process"""
        state = self.get_current_state(decl_type)
        
        if state['is_extracting']:
            return
        
        if not self.validate_inputs(decl_type):
            return
        
        # Clear log
        state['log_text'].configure(state="normal")
        state['log_text'].delete("1.0", "end")
        state['log_text'].configure(state="disabled")
        
        # Reset progress
        state['progress_bar'].set(0)
        
        # Determine output path
        output_folder = state['output_folder_var'].get()
        if not output_folder:
            output_folder = os.path.dirname(state['file_var'].get())
        
        output_name = state['output_name_var'].get()
        if not output_name.endswith('.xlsx'):
            output_name += '.xlsx'
        
        output_path = os.path.join(output_folder, output_name)
        
        # Create extractor
        if decl_type == DeclarationType.EXPORT:
            state['extractor'] = ExportExtractor(
                state['file_var'].get(),
                progress_callback=lambda p: self.on_progress_update(p, decl_type)
            )
        else:
            state['extractor'] = ImportExtractor(
                state['file_var'].get(),
                progress_callback=lambda p: self.on_progress_update(p, decl_type)
            )
        
        # Start extraction in thread
        state['is_extracting'] = True
        state['extract_btn'].configure(state="disabled", text="Đang xử lý...")
        
        thread = threading.Thread(
            target=self.run_extraction,
            args=(output_path, decl_type),
            daemon=True
        )
        thread.start()
    
    def run_extraction(self, output_path: str, decl_type: DeclarationType):
        """Run extraction in background thread"""
        state = self.get_current_state(decl_type)
        
        try:
            success = state['extractor'].run(output_path)
            self.after(0, lambda: self.on_extraction_complete(success, output_path, decl_type))
        except Exception as e:
            self.after(0, lambda: self.on_extraction_error(str(e), decl_type))
    
    def on_progress_update(self, progress: ExtractionProgress, decl_type: DeclarationType):
        """Handle progress updates from extractor"""
        self.after(0, lambda: self._update_progress_ui(progress, decl_type))
    
    def _update_progress_ui(self, progress: ExtractionProgress, decl_type: DeclarationType):
        """Update progress UI elements"""
        state = self.get_current_state(decl_type)
        
        state['progress_bar'].set(progress.progress_percent / 100)
        
        if progress.status_message:
            self.log_message(progress.status_message, decl_type)
        
        if progress.is_complete:
            num_blocks = len(state['extractor'].data_blocks) if state['extractor'] else 0
            state['stats_label'].configure(
                text=f"📊 Hoàn thành: {num_blocks} khối | 100% ✓"
            )
    
    def on_extraction_complete(self, success: bool, output_path: str, decl_type: DeclarationType):
        """Handle extraction completion"""
        state = self.get_current_state(decl_type)
        
        state['is_extracting'] = False
        state['extract_btn'].configure(
            state="normal", 
            text=f"⚡ Extract Data ({'Xuất khẩu' if decl_type == DeclarationType.EXPORT else 'Nhập khẩu'})"
        )
        
        if success:
            self.log_message(f"\n✅ THÀNH CÔNG! File đã được lưu tại:\n{output_path}", decl_type)
            
            messagebox.showinfo("Thành công", f"✅ Trích xuất thành công!\n\nFile: {os.path.basename(output_path)}")
            
            if self.auto_open_var.get():
                try:
                    os.startfile(output_path)
                except:
                    subprocess.run(['start', output_path], shell=True)
        else:
            error_msg = state['extractor'].progress.error_message if state['extractor'] else "Unknown error"
            self.log_message(f"\n❌ LỖI: {error_msg}", decl_type)
            messagebox.showerror("Lỗi", f"Trích xuất thất bại:\n{error_msg}")
    
    def on_extraction_error(self, error: str, decl_type: DeclarationType):
        """Handle extraction error"""
        state = self.get_current_state(decl_type)
        
        state['is_extracting'] = False
        state['extract_btn'].configure(
            state="normal",
            text=f"⚡ Extract Data ({'Xuất khẩu' if decl_type == DeclarationType.EXPORT else 'Nhập khẩu'})"
        )
        self.log_message(f"\n❌ LỖI: {error}", decl_type)
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi:\n{error}")
    
    def on_closing(self):
        """Handle window closing"""
        self.config.set("window_geometry", self.geometry())
        self.config.set("auto_open", self.auto_open_var.get())
        self.config.set("show_preview", self.show_preview_var.get())
        self.config.set("auto_update_output", self.auto_update_output_var.get())
        self.destroy()


def main():
    """Main entry point"""
    app = CustomsExtractorV2()
    app.mainloop()


if __name__ == "__main__":
    main()
