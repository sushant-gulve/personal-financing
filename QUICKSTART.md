# Personal Finance CLI Application - Quick Start Guide

## Prerequisites

Before running this application, ensure you have:
1. **Java 24** or later installed (required)
2. **Gradle Wrapper** is included (no need to install Gradle separately)

## Quick Setup

### Option 1: Using Gradle Wrapper (Recommended)

The project includes a Gradle wrapper, so you don't need to install Gradle separately.

1. Navigate to the project directory:
```powershell
cd "c:\Users\SG2952\Desktop\projects\personal financing"
```

2. Build the project:
```powershell
.\gradlew.bat build
```

3. Run tests to verify everything works:
```powershell
.\gradlew.bat test
```

4. Run the application (Note: For interactive CLI, see Option 3):
```powershell
.\gradlew.bat run
```

### Option 2: Using Gradle (if installed)

1. Navigate to the project directory:
```powershell
cd "c:\Users\SG2952\Desktop\projects\personal financing"
```

2. Build the project:
```powershell
gradle build
```

3. Run the application:
```powershell
gradle run
```

### Option 3: Direct JAR Execution (Best for Interactive CLI)

After building the project, run the JAR directly for proper terminal interaction:

1. Build the project:
```powershell
.\gradlew.bat build
```

2. Run the application directly:
```powershell
java -jar build\libs\personal-financing-1.0.0.jar
```

### Option 4: Using VS Code

1. Open the project in VS Code
2. Install the Java Extension Pack if not already installed
3. Use Ctrl+Shift+P and run "Java: Build Projects"
4. Use Ctrl+Shift+P and run "Java: Run Application"

### Option 5: Direct Java Compilation

If you don't have Gradle installed, you can compile and run the project directly with Java:

1. Create the classes directory:
```powershell
mkdir build\classes -Force
```

2. Compile the Java files (you'll need the dependencies in a lib directory):
```powershell
javac -d build\classes -cp "lib\*" (Get-ChildItem -Recurse -Filter "*.java" src\main\java).FullName
```

3. Run the application:
```powershell
java -cp "build\classes;lib\*" com.enterprise.personalfinance.PersonalFinanceApplication
```

## Gradle Wrapper Information

This project includes a complete Gradle wrapper setup:
- **gradlew.bat** - Windows batch script to run Gradle
- **gradle/wrapper/gradle-wrapper.jar** - Gradle wrapper JAR
- **gradle/wrapper/gradle-wrapper.properties** - Wrapper configuration

The wrapper uses **Gradle 8.5** and will automatically download and cache Gradle if needed.

## Running the Application

### Recommended Method (Interactive CLI)

For the best interactive experience, run the JAR directly:

```powershell
# Build the project first
.\gradlew.bat build

# Run the application
java -jar build\libs\personal-financing-1.0.0.jar
```

### Alternative Methods

1. **Using Gradle wrapper:**
   ```powershell
   .\gradlew.bat run
   ```
   *Note: Interactive input may not work properly through Gradle*

2. **Using VS Code:**
   - Use the Run/Debug buttons in the editor
   - Or use Command Palette: "Java: Run Application"

### Building and Testing

```powershell
# Clean and build
.\gradlew.bat clean build

# Run tests only
.\gradlew.bat test

# View test results
.\gradlew.bat test --info
```

## Application Usage

Once the application starts, you'll see a menu with the following options:

1. **Add Expense** - Record a new expense
2. **View All Expenses** - Display all recorded expenses
3. **View Expenses by Category** - Filter by category
4. **View Expenses by Date Range** - Filter by date range
5. **Generate Financial Summary** - Show financial overview
6. **View Expenses by Category Summary** - Category totals
7. **Delete Expense** - Remove a specific expense
8. **Delete All Expenses** - Clear all data
9. **Exit** - Close the application

## Data Storage

- Expenses are stored in `expenses.json` in the project root directory
- The file is created automatically on first run
- Data persists between application sessions

## Troubleshooting

### Java Version Issues
```bash
java -version
```
Ensure you're running Java 24 or later.

### Compilation Issues
Make sure all dependencies are in the classpath and the source files are properly structured.

### File Permission Issues
Ensure the application has write permissions in the project directory for creating the expenses.json file.

## Example Session

```
=== Personal Finance Manager ===
Welcome to your personal expense tracker!

=== Main Menu ===
1. Add Expense
2. View All Expenses
3. View Expenses by Category
4. View Expenses by Date Range
5. Generate Financial Summary
6. View Expenses by Category Summary
7. Delete Expense
8. Delete All Expenses
9. Exit

Select an option (1-9): 1

=== Add New Expense ===
Enter category: Food
Enter amount: 25.50
Enter date (YYYY-MM-DD) or press Enter for today: 2025-07-01
Enter description (optional): Lunch at downtown cafe
Enter tags (comma-separated, optional): restaurant, lunch, downtown
✓ Expense added successfully!
Expense ID: a1b2c3d4-e5f6-7890-1234-567890abcdef
```

This application provides a robust foundation for personal finance tracking with enterprise-grade architecture and best practices.
