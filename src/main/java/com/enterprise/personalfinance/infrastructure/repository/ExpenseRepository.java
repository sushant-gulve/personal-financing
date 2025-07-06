package com.enterprise.personalfinance.infrastructure.repository;

import com.enterprise.personalfinance.domain.model.Expense;

import java.util.List;
import java.util.Optional;

/**
 * Repository interface for expense data persistence operations.
 * Follows enterprise patterns for data access abstraction.
 */
public interface ExpenseRepository {
    
    /**
     * Save an expense to the data store.
     * 
     * @param expense the expense to save
     * @throws RepositoryException if the save operation fails
     */
    void save(Expense expense);
    
    /**
     * Save multiple expenses to the data store.
     * 
     * @param expenses the list of expenses to save
     * @throws RepositoryException if the save operation fails
     */
    void saveAll(List<Expense> expenses);
    
    /**
     * Find an expense by its ID.
     * 
     * @param id the expense ID
     * @return an Optional containing the expense if found, empty otherwise
     */
    Optional<Expense> findById(String id);
    
    /**
     * Find all expenses.
     * 
     * @return a list of all expenses
     */
    List<Expense> findAll();
    
    /**
     * Find expenses by category.
     * 
     * @param category the category to search for
     * @return a list of expenses in the specified category
     */
    List<Expense> findByCategory(String category);
    
    /**
     * Delete an expense by its ID.
     * 
     * @param id the ID of the expense to delete
     * @return true if the expense was deleted, false if it wasn't found
     */
    boolean deleteById(String id);
    
    /**
     * Delete all expenses.
     */
    void deleteAll();
    
    /**
     * Get the count of all expenses.
     * 
     * @return the total number of expenses
     */
    long count();
}
