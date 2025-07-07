#!/usr/bin/env python3
"""
SBI PDF Organizer - Helps organize PDF files into statements folder
"""

import os
import shutil
import glob
from pathlib import Path

def organize_pdfs():
    """Move PDF files to statements folder"""
    current_dir = Path(".")
    statements_dir = current_dir / "statements"
    
    # Find PDF files in current directory
    pdf_files = list(current_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("📄 No PDF files found in current directory")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF files to organize")
    
    # Create statements directory if it doesn't exist
    statements_dir.mkdir(exist_ok=True)
    print(f"📂 Created/verified statements directory: {statements_dir.absolute()}")
    
    # Move PDF files
    moved_count = 0
    skipped_count = 0
    
    for pdf_file in pdf_files:
        destination = statements_dir / pdf_file.name
        
        if destination.exists():
            print(f"⚠️  Skipped {pdf_file.name} (already exists in statements folder)")
            skipped_count += 1
        else:
            try:
                shutil.move(str(pdf_file), str(destination))
                print(f"✅ Moved {pdf_file.name} → statements/")
                moved_count += 1
            except Exception as e:
                print(f"❌ Error moving {pdf_file.name}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"✅ Moved: {moved_count} files")
    print(f"⚠️  Skipped: {skipped_count} files")
    print(f"📁 Total in statements folder: {len(list(statements_dir.glob('*.pdf')))} files")
    
    if moved_count > 0:
        print(f"\n🎉 Organization complete! Your PDFs are now in the statements folder.")
        print(f"💡 You can now run: python sbi_extractor.py")

def main():
    print("📁 SBI PDF ORGANIZER")
    print("=" * 30)
    print("This tool will move your PDF files to a 'statements' folder")
    print("for better organization with the SBI extractor.")
    print()
    
    # Check if statements folder already exists and has files
    statements_dir = Path("statements")
    if statements_dir.exists():
        existing_pdfs = list(statements_dir.glob("*.pdf"))
        if existing_pdfs:
            print(f"📂 Statements folder already exists with {len(existing_pdfs)} PDF files")
            response = input("Do you want to move additional PDFs from current directory? (y/n): ")
            if response.lower() != 'y':
                print("👍 No changes made. Your files are already organized!")
                return
    
    # Check if there are PDF files to move
    current_pdfs = list(Path(".").glob("*.pdf"))
    if not current_pdfs:
        print("📄 No PDF files found in current directory")
        if statements_dir.exists():
            existing_pdfs = list(statements_dir.glob("*.pdf"))
            print(f"📂 Statements folder has {len(existing_pdfs)} PDF files")
        return
    
    print(f"📄 Found {len(current_pdfs)} PDF files in current directory:")
    for pdf in current_pdfs[:5]:  # Show first 5
        print(f"   - {pdf.name}")
    if len(current_pdfs) > 5:
        print(f"   ... and {len(current_pdfs) - 5} more")
    
    print()
    response = input("Organize these files into statements folder? (y/n): ")
    
    if response.lower() == 'y':
        organize_pdfs()
    else:
        print("👍 No changes made to your files")

if __name__ == "__main__":
    main()
