@echo off
cd /d "c:\Users\SG2952\Desktop\projects\personal financing\statements\HDFC"
echo.
echo ============================================================
echo   HDFC Bank Statement Processing Suite
echo ============================================================
echo.
echo This will organize your Excel files into separate folders:
echo   - Monthly Files (individual monthly statements)
echo   - Consolidated Files (complete data and summaries)
echo   - Categorized Files (organized by spending category)
echo   - Periodic Files (monthly analysis and trends)
echo.
echo Starting processing...
echo.

".\.venv\Scripts\python.exe" process_all_statements.py

echo.
echo ============================================================
echo Processing completed! Check the Organized_Statements folder
echo ============================================================
echo.
echo Press any key to open the results folder...
pause > nul
explorer "Organized_Statements"
