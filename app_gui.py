import dearpygui.dearpygui as dpg
import subprocess
import os
import threading
from pathlib import Path
import sys

class CSVProcessorGUI:
    def __init__(self):
        self.selected_file = ""
        self.modules_path = "./modules"
        
        # Available modules
        self.modules = {
            "NCM Check": "ncm_check.py",
            "Date Fix": "date_fix.py", 
            "Table Fix": "table_fix.py",
            "Table Out": "table_out.py",
            "Regex Replace": "regex_replace.py",
            "NCM Valid Generator": "ncm_valid_generator.py"
        }
        
    def check_display(self):
        """Check if we have a display available"""
        if os.name == 'posix':  # Linux/Unix
            if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
                print("❌ No display available. GUI requires a graphical environment.")
                print("💡 Available modules can be run directly from command line:")
                print("   python modules/ncm_check.py <file.csv>")
                print("   python modules/date_fix.py <file.csv>")
                print("   python modules/table_fix.py <file.csv>")
                print("   python modules/table_out.py <file.csv>")
                print("   python modules/regex_replace.py <file.csv>")
                print("   python modules/ncm_valid_generator.py <file.json>")
                return False
        return True
        
    def file_dialog_callback(self, sender, app_data):
        """Callback for file dialog"""
        if app_data['file_path_name']:
            self.selected_file = app_data['file_path_name']
            dpg.set_value("file_path_text", f"Selected: {os.path.basename(self.selected_file)}")
            dpg.configure_item("file_path_text", color=[0, 255, 0])  # Green color
            
            # Enable all buttons when file is selected
            for module_name in self.modules.keys():
                dpg.configure_item(f"btn_{module_name.lower().replace(' ', '_')}", enabled=True)
    
    def run_module(self, module_name, module_file):
        """Run a module script with the selected file"""
        if not self.selected_file:
            self.log_message("❌ No file selected!", [255, 0, 0])
            return
            
        if not os.path.exists(self.selected_file):
            self.log_message("❌ Selected file does not exist!", [255, 0, 0])
            return
            
        module_path = os.path.join(self.modules_path, module_file)
        if not os.path.exists(module_path):
            self.log_message(f"❌ Module {module_file} not found!", [255, 0, 0])
            return
        
        # Special case for NCM Valid Generator (needs JSON file)
        if module_name == "NCM Valid Generator":
            if not self.selected_file.endswith('.json'):
                self.log_message("❌ NCM Valid Generator requires a JSON file!", [255, 255, 0])
                return
        else:
            # Other modules need CSV files
            if not self.selected_file.endswith('.csv'):
                self.log_message("❌ This module requires a CSV file!", [255, 255, 0])
                return
        
        self.log_message(f"🚀 Running {module_name}...", [0, 255, 255])
        
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=self._execute_module, args=(module_name, module_path))
        thread.daemon = True
        thread.start()
    
    def _execute_module(self, module_name, module_path):
        """Execute the module in a separate thread"""
        try:
            # Change to project directory
            project_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Run the module
            result = subprocess.run(
                ["python", module_path, self.selected_file],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                self.log_message(f"✅ {module_name} completed successfully!", [0, 255, 0])
                if result.stdout:
                    # Show output in chunks to avoid overwhelming the log
                    output_lines = result.stdout.strip().split('\n')
                    for line in output_lines[-10:]:  # Show last 10 lines
                        if line.strip():
                            self.log_message(f"   {line}", [200, 200, 200])
            else:
                self.log_message(f"❌ {module_name} failed with error code {result.returncode}", [255, 0, 0])
                if result.stderr:
                    error_lines = result.stderr.strip().split('\n')
                    for line in error_lines[-5:]:  # Show last 5 error lines
                        if line.strip():
                            self.log_message(f"   Error: {line}", [255, 100, 100])
                            
        except subprocess.TimeoutExpired:
            self.log_message(f"❌ {module_name} timed out after 5 minutes", [255, 0, 0])
        except Exception as e:
            self.log_message(f"❌ Error running {module_name}: {str(e)}", [255, 0, 0])
    
    def log_message(self, message, color=None):
        """Add message to log with optional color"""
        if color is None:
            color = [255, 255, 255]  # White
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        
        # Add to log
        dpg.add_text(full_message, color=color, parent="log_window")
        
        # Auto-scroll to bottom
        dpg.set_y_scroll("log_window", -1.0)
    
    def clear_log(self):
        """Clear the log window"""
        dpg.delete_item("log_window", children_only=True)
        self.log_message("Log cleared", [255, 255, 0])
    
    def open_files_folder(self):
        """Open the files output folder"""
        files_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
        try:
            if os.name == 'nt':  # Windows
                os.startfile(files_path)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(['xdg-open', files_path])
            self.log_message("📁 Opened files folder", [0, 255, 255])
        except Exception as e:
            self.log_message(f"❌ Could not open files folder: {str(e)}", [255, 0, 0])
    
    def create_gui(self):
        """Create the main GUI"""
        # Create viewport
        dpg.create_viewport(title="CSV Processor - Lychee", width=800, height=600)
        dpg.setup_dearpygui()
        
        # File dialog
        with dpg.file_dialog(
            directory_selector=False,
            show=False,
            callback=self.file_dialog_callback,
            tag="file_dialog_id",
            width=700,
            height=400
        ):
            dpg.add_file_extension(".*", color=(255, 255, 255, 255))
            dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[CSV]")
            dpg.add_file_extension(".json", color=(255, 255, 0, 255), custom_text="[JSON]")
        
        # Main window
        with dpg.window(label="CSV Processor", tag="Primary Window", width=800, height=600):
            
            # Header
            dpg.add_text("🍃 CSV Processor - Lychee", color=[100, 255, 100])
            dpg.add_separator()
            
            # File selection section
            with dpg.group(horizontal=True):
                dpg.add_button(label="📁 Select File", callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_text("No file selected", tag="file_path_text", color=[255, 100, 100])
            
            dpg.add_separator()
            
            # Modules section
            dpg.add_text("Available Modules:", color=[255, 255, 100])
            
            # Create buttons for each module
            with dpg.group():
                # Row 1
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="🔍 NCM Check", 
                        callback=lambda: self.run_module("NCM Check", self.modules["NCM Check"]),
                        tag="btn_ncm_check",
                        enabled=False,
                        width=120
                    )
                    dpg.add_button(
                        label="📅 Date Fix", 
                        callback=lambda: self.run_module("Date Fix", self.modules["Date Fix"]),
                        tag="btn_date_fix",
                        enabled=False,
                        width=120
                    )
                    dpg.add_button(
                        label="🔧 Table Fix", 
                        callback=lambda: self.run_module("Table Fix", self.modules["Table Fix"]),
                        tag="btn_table_fix",
                        enabled=False,
                        width=120
                    )
                
                # Row 2
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="📤 Table Out", 
                        callback=lambda: self.run_module("Table Out", self.modules["Table Out"]),
                        tag="btn_table_out",
                        enabled=False,
                        width=120
                    )
                    dpg.add_button(
                        label="🔄 Regex Replace", 
                        callback=lambda: self.run_module("Regex Replace", self.modules["Regex Replace"]),
                        tag="btn_regex_replace",
                        enabled=False,
                        width=120
                    )
                    dpg.add_button(
                        label="⚙️ NCM Generator", 
                        callback=lambda: self.run_module("NCM Valid Generator", self.modules["NCM Valid Generator"]),
                        tag="btn_ncm_valid_generator",
                        enabled=False,
                        width=120
                    )
            
            dpg.add_separator()
            
            # Utility buttons
            with dpg.group(horizontal=True):
                dpg.add_button(label="📁 Open Files Folder", callback=self.open_files_folder)
                dpg.add_button(label="🗑️ Clear Log", callback=self.clear_log)
            
            dpg.add_separator()
            
            # Log section
            dpg.add_text("Output Log:", color=[255, 255, 100])
            
            with dpg.child_window(height=200, tag="log_window"):
                self.log_message("Welcome to CSV Processor! Select a file to begin.", [100, 255, 100])
        
        # Set primary window
        dpg.set_primary_window("Primary Window", True)
        
        # Show viewport
        dpg.show_viewport()
    
    def run(self):
        """Run the GUI application"""
        if not self.check_display():
            return
            
        try:
            self.create_gui()
            dpg.start_dearpygui()
            dpg.destroy_context()
        except Exception as e:
            print(f"❌ Error running GUI: {e}")
            print("💡 You can run modules directly from command line:")
            for name, script in self.modules.items():
                if name == "NCM Valid Generator":
                    print(f"   python modules/{script} <file.json>")
                else:
                    print(f"   python modules/{script} <file.csv>")

if __name__ == "__main__":
    app = CSVProcessorGUI()
    app.run()
