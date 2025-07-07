import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    try:
        print(f"\n{'='*50}")
        print(f"RUNNING: {description}")
        print(f"{'='*50}")
        
        result = subprocess.run([
            ".\.venv\Scripts\python.exe", 
            script_name
        ], capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {description} completed successfully!")
            return True
        else:
            print(f"❌ Error in {description}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Failed to run {description}: {str(e)}")
        return False

def main():
    print("🏦 HDFC Bank Statement Processing Suite")
    print("=" * 60)
    print("This will:")
    print("1. Consolidate your Excel files and organize by month")
    print("2. Categorize all transactions automatically")
    print("3. Create organized folder structure")
    print("=" * 60)
    
    # Step 1: Consolidate statements
    if not run_script("consolidate_statements.py", "Statement Consolidation"):
        print("\n❌ Consolidation failed. Please check the error messages above.")
        return
    
    # Step 2: Categorize transactions
    if not run_script("categorize_transactions.py", "Transaction Categorization"):
        print("\n❌ Categorization failed. Please check the error messages above.")
        return
    
    print("\n" + "="*60)
    print("🎉 ALL PROCESSING COMPLETE!")
    print("="*60)
    print("\n📁 Your files are now organized in:")
    print("   Organized_Statements/")
    print("   ├── Monthly_Files/          (individual monthly statements)")
    print("   ├── Consolidated_Files/     (complete consolidated data)")
    print("   ├── Categorized_Files/      (data organized by category)")
    print("   └── Periodic_Files/         (monthly analysis & summaries)")
    print("\n💡 You can now:")
    print("   • Analyze spending patterns by category")
    print("   • Track monthly expenses")
    print("   • Plan budgets based on historical data")
    print("   • Prepare for tax filing")
    
    print("\n🔄 To process new statements in the future:")
    print("   • Add new Excel files to this folder")
    print("   • Run this script again")
    print("   • Everything will be automatically updated!")

if __name__ == "__main__":
    main()
