"""
Build standalone .exe for V2 using PyInstaller
No Python installation required on target machine!
"""

import PyInstaller.__main__
import os
import sys

def build_exe_v2():
    """Build V2 executable using PyInstaller"""
    
    print("="*60)
    print("Building Customs Extractor V2 - Standalone .exe")
    print("="*60)
    print()
    
    # PyInstaller arguments
    args = [
        'customs_extractor_gui_v2.py',  # Main script
        '--name=CustomsExtractorV2',     # Executable name
        '--onefile',                     # Single file
        '--windowed',                    # No console
        '--clean',                       # Clean cache
        
        # Add data files
        '--add-data=extractor_core_v2.py;.',
        '--add-data=config.py;.',
        
        # Hidden imports
        '--hidden-import=customtkinter',
        '--hidden-import=xlrd',
        '--hidden-import=openpyxl',
        '--hidden-import=PIL',
        '--hidden-import=re',
        '--hidden-import=threading',
        
        # Icon (if you have one)
        # '--icon=app_icon.ico',
    ]
    
    try:
        print("Starting build process...")
        print("This may take 2-3 minutes...\n")
        
        PyInstaller.__main__.run(args)
        
        print("\n" + "="*60)
        print("✅ BUILD COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📦 Executable location: dist/CustomsExtractorV2.exe")
        print(f"📊 File size: ~{os.path.getsize('dist/CustomsExtractorV2.exe') / 1024 / 1024:.1f} MB")
        print("\n✨ DISTRIBUTION:")
        print("  - Copy 'CustomsExtractorV2.exe' to any Windows PC")
        print("  - Double-click to run")
        print("  - NO Python installation needed!")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ BUILD FAILED: {e}")
        print("\nTroubleshooting:")
        print("  1. Install PyInstaller: pip install pyinstaller")
        print("  2. Make sure all dependencies are installed")
        print("  3. Close any running instances of the app")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists('customs_extractor_gui_v2.py'):
        print("Error: customs_extractor_gui_v2.py not found!")
        print("Please run this script from the project directory")
        sys.exit(1)
    
    build_exe_v2()
