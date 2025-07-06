package com.enterprise.personalfinance.presentation.cli;

import com.enterprise.personalfinance.application.service.PersonalFinanceService;
import com.enterprise.personalfinance.domain.model.Expense;
import com.enterprise.personalfinance.domain.model.FinancialSummary;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

/**
 * Command-line interface for the Personal Finance application.
 * Provides interactive menu-driven interface for expense management.
 */
public class PersonalFinanceCLI {
    
    private static final Logger logger = LoggerFactory.getLogger(PersonalFinanceCLI.class);
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    
    private final PersonalFinanceService financeService;
    private final Scanner scanner;
    private boolean running;
    
    public PersonalFinanceCLI(PersonalFinanceService financeService) {
        this.financeService = financeService;
        this.scanner = new Scanner(System.in);
        this.running = true;
    }
    
    /**
     * Start the CLI application.
     */
    public void start() {
        logger.info("Starting Personal Finance CLI");
        System.out.println("=== Personal Finance Manager ===");
        System.out.println("Welcome to your personal expense tracker!");
        System.out.println();
        
        while (running) {
            try {
                displayMenu();
                int choice = getMenuChoice();
                handleMenuChoice(choice);
            } catch (Exception e) {
                logger.error("Error in CLI main loop", e);
                System.err.println("An error occurred: " + e.getMessage());
                System.out.println("Please try again.");
            }
        }
        
        System.out.println("Thank you for using Personal Finance Manager!");
        scanner.close();
    }
    
    private void displayMenu() {
        System.out.println("\n=== Main Menu ===");
        System.out.println("1. Add Expense");
        System.out.println("2. View All Expenses");
        System.out.println("3. View Expenses by Category");
        System.out.println("4. View Expenses by Date Range");
        System.out.println("5. Generate Financial Summary");
        System.out.println("6. View Expenses by Category Summary");
        System.out.println("7. Delete Expense");
        System.out.println("8. Delete All Expenses");
        System.out.println("9. Exit");
        System.out.print("\nSelect an option (1-9): ");
    }
    
    private int getMenuChoice() {
        try {
            String input = scanner.nextLine().trim();
            if (input.isEmpty()) {
                System.out.println("Please enter a choice.");
                return -1;
            }
            return Integer.parseInt(input);
        } catch (NumberFormatException e) {
            System.out.println("Invalid input. Please enter a number between 1 and 9.");
            return -1;
        }
    }
    
    private void handleMenuChoice(int choice) {
        switch (choice) {
            case 1 -> addExpense();
            case 2 -> viewAllExpenses();
            case 3 -> viewExpensesByCategory();
            case 4 -> viewExpensesByDateRange();
            case 5 -> generateFinancialSummary();
            case 6 -> viewExpensesByCategorySummary();
            case 7 -> deleteExpense();
            case 8 -> deleteAllExpenses();
            case 9 -> exitApplication();
            default -> System.out.println("Invalid option. Please select a number between 1 and 9.");
        }
    }
    
    private void addExpense() {
        System.out.println("\n=== Add New Expense ===");
        
        try {
            System.out.print("Enter category: ");
            String category = scanner.nextLine().trim();
            
            if (category.isEmpty()) {
                System.out.println("Category cannot be empty.");
                return;
            }
            
            System.out.print("Enter amount: ");
            String amountStr = scanner.nextLine().trim();
            BigDecimal amount = new BigDecimal(amountStr);
            
            if (amount.compareTo(BigDecimal.ZERO) <= 0) {
                System.out.println("Amount must be positive.");
                return;
            }
            
            System.out.print("Enter date (YYYY-MM-DD) or press Enter for today: ");
            String dateStr = scanner.nextLine().trim();
            LocalDate date = dateStr.isEmpty() ? LocalDate.now() : LocalDate.parse(dateStr, DATE_FORMATTER);
            
            System.out.print("Enter description (optional): ");
            String description = scanner.nextLine().trim();
            
            System.out.print("Enter tags (comma-separated, optional): ");
            String tagsStr = scanner.nextLine().trim();
            String[] tags = tagsStr.isEmpty() ? new String[0] : tagsStr.split(",");
            
            // Trim tags
            for (int i = 0; i < tags.length; i++) {
                tags[i] = tags[i].trim();
            }
            
            Expense expense = new Expense(category, amount, date, description, tags);
            financeService.addExpense(expense);
            
            System.out.println("✓ Expense added successfully!");
            System.out.println("Expense ID: " + expense.getId());
            
        } catch (NumberFormatException e) {
            System.out.println("Invalid amount format. Please enter a valid number.");
        } catch (DateTimeParseException e) {
            System.out.println("Invalid date format. Please use YYYY-MM-DD format.");
        } catch (Exception e) {
            System.out.println("Error adding expense: " + e.getMessage());
        }
    }
    
    private void viewAllExpenses() {
        System.out.println("\n=== All Expenses ===");
        
        List<Expense> expenses = financeService.getAllExpenses();
        
        if (expenses.isEmpty()) {
            System.out.println("No expenses found.");
            return;
        }
        
        displayExpenses(expenses);
        
        BigDecimal total = financeService.calculateTotalExpenses();
        System.out.println(String.format("\nTotal: $%.2f", total));
        System.out.println("Count: " + expenses.size() + " expenses");
    }
    
    private void viewExpensesByCategory() {
        System.out.println("\n=== Expenses by Category ===");
        System.out.print("Enter category: ");
        String category = scanner.nextLine().trim();
        
        if (category.isEmpty()) {
            System.out.println("Category cannot be empty.");
            return;
        }
        
        List<Expense> expenses = financeService.getExpensesByCategory(category);
        
        if (expenses.isEmpty()) {
            System.out.println("No expenses found for category: " + category);
            return;
        }
        
        displayExpenses(expenses);
        
        BigDecimal total = expenses.stream()
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        System.out.println(String.format("\nTotal for '%s': $%.2f", category, total));
        System.out.println("Count: " + expenses.size() + " expenses");
    }
    
    private void viewExpensesByDateRange() {
        System.out.println("\n=== Expenses by Date Range ===");
        
        try {
            System.out.print("Enter start date (YYYY-MM-DD): ");
            String startDateStr = scanner.nextLine().trim();
            LocalDate startDate = LocalDate.parse(startDateStr, DATE_FORMATTER);
            
            System.out.print("Enter end date (YYYY-MM-DD): ");
            String endDateStr = scanner.nextLine().trim();
            LocalDate endDate = LocalDate.parse(endDateStr, DATE_FORMATTER);
            
            List<Expense> expenses = financeService.getExpensesByDateRange(startDate, endDate);
            
            if (expenses.isEmpty()) {
                System.out.println(String.format("No expenses found between %s and %s.", startDate, endDate));
                return;
            }
            
            displayExpenses(expenses);
            
            BigDecimal total = financeService.calculateTotalExpenses(startDate, endDate);
            System.out.println(String.format("\nTotal for period %s to %s: $%.2f", startDate, endDate, total));
            System.out.println("Count: " + expenses.size() + " expenses");
            
        } catch (DateTimeParseException e) {
            System.out.println("Invalid date format. Please use YYYY-MM-DD format.");
        } catch (Exception e) {
            System.out.println("Error retrieving expenses: " + e.getMessage());
        }
    }
    
    private void generateFinancialSummary() {
        System.out.println("\n=== Financial Summary ===");
        
        FinancialSummary summary = financeService.getFinancialSummary();
        
        if (summary.getTransactionCount() == 0) {
            System.out.println("No expenses recorded yet.");
            return;
        }
        
        System.out.println(String.format("Total Expenses: $%.2f", summary.getTotalExpenses()));
        System.out.println(String.format("Average Expense: $%.2f", summary.getAverageExpense()));
        System.out.println("Transaction Count: " + summary.getTransactionCount());
        
        if (summary.getPeriodStart() != null && summary.getPeriodEnd() != null) {
            System.out.println("Period: " + summary.getPeriodStart() + " to " + summary.getPeriodEnd());
        }
    }
    
    private void viewExpensesByCategorySummary() {
        System.out.println("\n=== Expenses by Category Summary ===");
        
        Map<String, BigDecimal> categoryTotals = financeService.calculateExpensesByCategory();
        
        if (categoryTotals.isEmpty()) {
            System.out.println("No expenses found.");
            return;
        }
        
        System.out.println(String.format("%-20s %s", "Category", "Total"));
        System.out.println("".repeat(35));
        
        categoryTotals.entrySet().stream()
                .sorted(Map.Entry.<String, BigDecimal>comparingByValue().reversed())
                .forEach(entry -> {
                    System.out.println(String.format("%-20s $%.2f", entry.getKey(), entry.getValue()));
                });
        
        BigDecimal grandTotal = categoryTotals.values().stream()
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        System.out.println("".repeat(35));
        System.out.println(String.format("%-20s $%.2f", "TOTAL", grandTotal));
    }
    
    private void deleteExpense() {
        System.out.println("\n=== Delete Expense ===");
        System.out.print("Enter expense ID: ");
        String id = scanner.nextLine().trim();
        
        if (id.isEmpty()) {
            System.out.println("Expense ID cannot be empty.");
            return;
        }
        
        boolean deleted = financeService.deleteExpense(id);
        
        if (deleted) {
            System.out.println("✓ Expense deleted successfully!");
        } else {
            System.out.println("Expense not found with ID: " + id);
        }
    }
    
    private void deleteAllExpenses() {
        System.out.println("\n=== Delete All Expenses ===");
        System.out.print("Are you sure you want to delete ALL expenses? (yes/no): ");
        String confirmation = scanner.nextLine().trim().toLowerCase();
        
        if ("yes".equals(confirmation) || "y".equals(confirmation)) {
            financeService.deleteAllExpenses();
            System.out.println("✓ All expenses deleted successfully!");
        } else {
            System.out.println("Operation cancelled.");
        }
    }
    
    private void exitApplication() {
        System.out.println("\nExiting application...");
        running = false;
    }
    
    private void displayExpenses(List<Expense> expenses) {
        System.out.println(String.format("%-8s %-15s %-10s %-12s %s", "ID", "Category", "Amount", "Date", "Description"));
        System.out.println("".repeat(80));
        
        for (Expense expense : expenses) {
            String shortId = expense.getId().substring(0, Math.min(8, expense.getId().length()));
            String shortCategory = expense.getCategory().length() > 15 ? 
                    expense.getCategory().substring(0, 12) + "..." : expense.getCategory();
            String shortDescription = expense.getDescription().length() > 30 ? 
                    expense.getDescription().substring(0, 27) + "..." : expense.getDescription();
            
            System.out.println(String.format("%-8s %-15s $%-9.2f %-12s %s", 
                    shortId, shortCategory, expense.getAmount(), expense.getDate(), shortDescription));
        }
    }
}
