#!/usr/bin/env python3
"""
CSV Processor - Lychee
A GUI and CLI interface for CSV processing modules
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("🍃" + "="*50)
    print("🍃 CSV Processor - Lychee")
    print("🍃" + "="*50)

def get_modules():
    """Get available modules"""
    return {
        "1": ("NCM Check", "ncm_check.py", "csv"),
        "2": ("Date Fix", "date_fix.py", "csv"), 
        "3": ("Table Fix", "table_fix.py", "csv"),
        "4": ("Table Out", "table_out.py", "csv"),
        "5": ("Regex Replace", "regex_replace.py", "csv"),
        "6": ("NCM Valid Generator", "ncm_valid_generator.py", "json")
    }

def show_menu():
    """Show main menu"""
    modules = get_modules()
    print("\n📋 Available Modules:")
    print("-" * 30)
    for key, (name, script, file_type) in modules.items():
        print(f"{key}. {name} ({file_type.upper()} files)")
    print("7. 📁 Open files folder")
    print("8. ❌ Exit")
    print("-" * 30)

def get_file_input(file_type):
    """Get file input from user"""
    while True:
        file_path = input(f"\n📂 Enter path to {file_type.upper()} file: ").strip()
        
        if not file_path:
            print("❌ Please enter a file path")
            continue
            
        if not os.path.exists(file_path):
            print("❌ File does not exist")
            continue
            
        if not file_path.lower().endswith(f'.{file_type}'):
            print(f"❌ File must be a {file_type.upper()} file")
            continue
            
        return file_path

def run_module(module_name, script_name, file_path):
    """Run a module with the given file"""
    print(f"\n🚀 Running {module_name}...")
    print("-" * 40)
    
    try:
        script_path = os.path.join("modules", script_name)
        
        if not os.path.exists(script_path):
            print(f"❌ Module {script_name} not found!")
            return
        
        # Run the module
        result = subprocess.run(
            ["python", script_path, file_path],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {module_name} completed successfully!")
        else:
            print(f"❌ {module_name} failed with error code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"❌ {module_name} timed out after 5 minutes")
    except KeyboardInterrupt:
        print(f"\n⚠️  {module_name} was interrupted by user")
    except Exception as e:
        print(f"❌ Error running {module_name}: {str(e)}")

def open_files_folder():
    """Open the files output folder"""
    files_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    
    try:
        if not os.path.exists(files_path):
            os.makedirs(files_path)
            print(f"📁 Created files folder: {files_path}")
        
        if os.name == 'nt':  # Windows
            os.startfile(files_path)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.run(['xdg-open', files_path])
        
        print(f"📁 Opened files folder: {files_path}")
    except Exception as e:
        print(f"❌ Could not open files folder: {str(e)}")
        print(f"📍 Files are saved in: {files_path}")

def try_gui():
    """Try to run the GUI version"""
    try:
        # Check if we have a display
        if os.name == 'posix':  # Linux/Unix
            if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
                return False
        
        # Try to import and run GUI
        import subprocess
        result = subprocess.run(
            ["python", "app_gui.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=5
        )
        return result.returncode == 0
        
    except Exception:
        return False

def main():
    """Main application function"""
    print_banner()
    
    # Try GUI first
    print("🔍 Checking for GUI support...")
    if try_gui():
        return
    
    print("💻 Running in CLI mode")
    
    modules = get_modules()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n👉 Select option (1-8): ").strip()
            
            if choice == "8":
                print("\n👋 Goodbye!")
                break
            elif choice == "7":
                open_files_folder()
                input("\nPress Enter to continue...")
                continue
            elif choice in modules:
                module_name, script_name, file_type = modules[choice]
                
                file_path = get_file_input(file_type)
                run_module(module_name, script_name, file_path)
                
                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid option. Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
