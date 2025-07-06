package com.enterprise.personalfinance.application.service;

import com.enterprise.personalfinance.domain.model.Expense;
import com.enterprise.personalfinance.domain.model.FinancialSummary;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Service interface for personal finance operations.
 * Defines the core business logic for expense management.
 */
public interface PersonalFinanceService {
    
    /**
     * Add a new expense.
     * 
     * @param expense the expense to add
     * @throws IllegalArgumentException if the expense is invalid
     */
    void addExpense(Expense expense);
    
    /**
     * Get an expense by its ID.
     * 
     * @param id the expense ID
     * @return an Optional containing the expense if found
     */
    Optional<Expense> getExpenseById(String id);
    
    /**
     * Get all expenses.
     * 
     * @return a list of all expenses
     */
    List<Expense> getAllExpenses();
    
    /**
     * Get expenses by category.
     * 
     * @param category the category to filter by
     * @return a list of expenses in the specified category
     */
    List<Expense> getExpensesByCategory(String category);
    
    /**
     * Get expenses within a date range.
     * 
     * @param startDate the start date (inclusive)
     * @param endDate the end date (inclusive)
     * @return a list of expenses within the date range
     */
    List<Expense> getExpensesByDateRange(LocalDate startDate, LocalDate endDate);
    
    /**
     * Calculate total expenses.
     * 
     * @return the total amount of all expenses
     */
    BigDecimal calculateTotalExpenses();
    
    /**
     * Calculate total expenses by category.
     * 
     * @return a map of category to total amount
     */
    Map<String, BigDecimal> calculateExpensesByCategory();
    
    /**
     * Calculate total expenses within a date range.
     * 
     * @param startDate the start date (inclusive)
     * @param endDate the end date (inclusive)
     * @return the total amount of expenses within the date range
     */
    BigDecimal calculateTotalExpenses(LocalDate startDate, LocalDate endDate);
    
    /**
     * Get financial summary for all expenses.
     * 
     * @return a financial summary
     */
    FinancialSummary getFinancialSummary();
    
    /**
     * Get financial summary for a specific date range.
     * 
     * @param startDate the start date (inclusive)
     * @param endDate the end date (inclusive)
     * @return a financial summary for the specified period
     */
    FinancialSummary getFinancialSummary(LocalDate startDate, LocalDate endDate);
    
    /**
     * Delete an expense by its ID.
     * 
     * @param id the expense ID
     * @return true if the expense was deleted, false if not found
     */
    boolean deleteExpense(String id);
    
    /**
     * Delete all expenses.
     */
    void deleteAllExpenses();
    
    /**
     * Get the count of all expenses.
     * 
     * @return the total number of expenses
     */
    long getExpenseCount();
}
