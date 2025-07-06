# Personal Finance CLI Application

A robust Java-based command-line application for managing personal finances with enterprise-grade architecture and design patterns.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)

## Overview

This Personal Finance CLI application is built using Java 24 and Gradle, following enterprise software development best practices. It provides a command-line interface for tracking expenses, generating financial summaries, and managing personal financial data with JSON-based persistence.

## Features

- ✅ **Expense Management**: Add, view, update, and delete expenses
- ✅ **Category-based Organization**: Organize expenses by categories
- ✅ **Date Range Filtering**: Filter expenses by date ranges
- ✅ **Financial Summaries**: Generate comprehensive financial reports
- ✅ **JSON Persistence**: File-based data storage with JSON format
- ✅ **Thread-Safe Operations**: Concurrent access support with read-write locks
- ✅ **Enterprise Logging**: Structured logging with SLF4J and Logback
- ✅ **Robust Error Handling**: Comprehensive exception handling and validation
- ✅ **Unit Testing**: Complete test coverage with JUnit 5 and Mockito

## Project Structure

```
personal-financing/
├── build.gradle                           # Gradle build configuration
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties      # Gradle wrapper configuration
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── enterprise/
│   │               └── personalfinance/
│   │                   ├── PersonalFinanceApplication.java      # Main application entry point
│   │                   ├── application/                         # Application layer
│   │                   │   └── service/
│   │                   │       ├── PersonalFinanceService.java  # Service interface
│   │                   │       └── impl/
│   │                   │           └── PersonalFinanceServiceImpl.java # Service implementation
│   │                   ├── domain/                              # Domain layer
│   │                   │   └── model/
│   │                   │       ├── Expense.java                 # Core expense entity
│   │                   │       └── FinancialSummary.java        # Financial summary value object
│   │                   ├── infrastructure/                      # Infrastructure layer
│   │                   │   └── repository/
│   │                   │       ├── ExpenseRepository.java       # Repository interface
│   │                   │       ├── RepositoryException.java     # Custom exception
│   │                   │       └── impl/
│   │                   │           └── FileBasedExpenseRepository.java # File-based implementation
│   │                   └── presentation/                        # Presentation layer
│   │                       └── cli/
│   │                           ├── PersonalFinanceCLI.java      # CLI interface
│   │                           ├── command/                     # Command pattern implementations
│   │                           └── util/
│   │                               └── CLIUtils.java            # CLI utilities
│   └── test/
│       └── java/
│           └── com/
│               └── enterprise/
│                   └── personalfinance/                         # Test packages mirror main structure
└── expenses.json                                               # Data file (created at runtime)
```

## Architecture

This application follows **Clean Architecture** principles with clear separation of concerns:

### Layers

1. **Domain Layer** (`domain/model/`)
   - Contains core business entities and value objects
   - No dependencies on external frameworks
   - Pure Java objects with business logic

2. **Application Layer** (`application/service/`)
   - Contains business use cases and orchestration logic
   - Defines service interfaces and implementations
   - Coordinates between domain and infrastructure layers

3. **Infrastructure Layer** (`infrastructure/repository/`)
   - Handles data persistence and external system interactions
   - Implements repository interfaces defined in the application layer
   - Contains framework-specific code (Jackson, file I/O)

4. **Presentation Layer** (`presentation/cli/`)
   - Handles user interaction and input/output
   - CLI commands and user interface logic
   - Converts between user input and domain objects

### Design Patterns

- **Repository Pattern**: Abstracts data access logic
- **Service Layer Pattern**: Encapsulates business logic
- **Command Pattern**: CLI command handling
- **Dependency Injection**: Loose coupling between components
- **Value Object Pattern**: Immutable domain objects

## Prerequisites

- **Java Development Kit (JDK) 24** or later
- **Gradle 8.5** or later (included via wrapper)
- **Visual Studio Code** with Java Extension Pack (recommended)

## Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd personal-financing
   ```

2. **Build the project:**
   ```bash
   ./gradlew build
   ```

3. **Run the application:**
   ```bash
   ./gradlew run
   ```

## Usage

### Running the Application

```bash
# Using Gradle
./gradlew run

# Or using the custom task
./gradlew runApp

# Or run the JAR directly
java -jar build/libs/personal-financing-1.0.0.jar
```

### CLI Commands

The application provides an interactive command-line interface with the following options:

1. **Add Expense**: Record a new expense with category, amount, date, and description
2. **View All Expenses**: Display all recorded expenses
3. **View by Category**: Filter expenses by category
4. **View by Date Range**: Filter expenses within a specific date range
5. **Financial Summary**: Generate comprehensive financial reports
6. **Delete Expense**: Remove a specific expense by ID
7. **Exit**: Close the application

### Example Usage

```
=== Personal Finance Manager ===
1. Add Expense
2. View All Expenses
3. View Expenses by Category
4. View Expenses by Date Range
5. Generate Financial Summary
6. Delete Expense
7. Exit

Select an option: 1
Enter category: Food
Enter amount: 25.50
Enter date (YYYY-MM-DD): 2025-07-01
Enter description: Lunch at cafe
Expense added successfully!
```

## Development

### Building the Project

```bash
# Clean and build
./gradlew clean build

# Run tests
./gradlew test

# Generate test report
./gradlew test jacocoTestReport
```

### Project Configuration

The project uses:
- **Gradle** for build automation
- **Jackson** for JSON serialization/deserialization
- **SLF4J + Logback** for logging
- **JUnit 5** for testing
- **Mockito** for mocking in tests
- **AssertJ** for fluent assertions

### Dependencies

Key dependencies defined in `build.gradle`:

```gradle
dependencies {
    // JSON processing
    implementation 'com.fasterxml.jackson.core:jackson-databind:2.16.1'
    implementation 'com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.16.1'
    
    // Logging
    implementation 'org.slf4j:slf4j-api:2.0.9'
    implementation 'ch.qos.logback:logback-classic:1.4.14'
    
    // Testing
    testImplementation 'org.junit.jupiter:junit-jupiter'
    testImplementation 'org.mockito:mockito-core:5.8.0'
    testImplementation 'org.assertj:assertj-core:3.24.2'
}
```

## Testing

### Running Tests

```bash
# Run all tests
./gradlew test

# Run tests with verbose output
./gradlew test --info

# Run specific test class
./gradlew test --tests "*ExpenseRepositoryTest"
```

### Test Structure

Tests are organized to mirror the main source structure:
- Unit tests for domain models
- Service layer tests with mocking
- Repository integration tests
- CLI component tests

### Test Coverage

The project includes comprehensive test coverage for:
- Domain model validation and behavior
- Service layer business logic
- Repository persistence operations
- Error handling and edge cases

## Contributing

### Code Style

- Follow Java naming conventions
- Use meaningful variable and method names
- Add comprehensive JavaDoc for public APIs
- Maintain consistent indentation (4 spaces)
- Keep methods focused and single-purpose

### Development Workflow

1. Create feature branch from main
2. Implement changes with tests
3. Run full test suite
4. Update documentation if needed
5. Submit pull request

### Adding New Features

When adding new features:
1. Start with domain models if needed
2. Define service interfaces
3. Implement service logic
4. Add repository methods if required
5. Update CLI interface
6. Write comprehensive tests

## Configuration

### Data Storage

- Default storage: `expenses.json` in the application root
- JSON format with pretty printing enabled
- Automatic file creation on first run
- Thread-safe concurrent access

### Logging

- Default log level: INFO
- Logs written to console
- Debug logging available for troubleshooting
- Configure in `src/main/resources/logback.xml`

## Troubleshooting

### Common Issues

1. **Java Version**: Ensure Java 24+ is installed and configured
2. **File Permissions**: Verify write permissions in the application directory
3. **JSON Corruption**: Delete `expenses.json` to reset data (backup first!)
4. **Memory Issues**: Increase JVM heap size for large datasets

### Debug Mode

Enable debug logging by setting:
```bash
java -Dlogging.level.com.enterprise.personalfinance=DEBUG -jar app.jar
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please:
1. Check existing issues in the project repository
2. Create a new issue with detailed description
3. Include steps to reproduce for bugs
4. Provide system information (Java version, OS, etc.)
