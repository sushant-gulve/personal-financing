@echo off
cd /d "c:\Users\SG2952\Desktop\projects\personal financing\statements\HDFC"
echo Running transaction categorization...
".\.venv\Scripts\python.exe" categorize_transactions.py
echo.
echo Categorization completed! Check the Consolidated_Statements folder for results.
echo Press any key to close...
pause > nul
