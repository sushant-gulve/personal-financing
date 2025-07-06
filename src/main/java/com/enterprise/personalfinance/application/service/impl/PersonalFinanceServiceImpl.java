package com.enterprise.personalfinance.application.service.impl;

import com.enterprise.personalfinance.application.service.PersonalFinanceService;
import com.enterprise.personalfinance.domain.model.Expense;
import com.enterprise.personalfinance.domain.model.FinancialSummary;
import com.enterprise.personalfinance.infrastructure.repository.ExpenseRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Implementation of PersonalFinanceService.
 * Provides business logic for expense management and financial calculations.
 */
public class PersonalFinanceServiceImpl implements PersonalFinanceService {
    
    private static final Logger logger = LoggerFactory.getLogger(PersonalFinanceServiceImpl.class);
    
    private final ExpenseRepository expenseRepository;
    
    public PersonalFinanceServiceImpl(ExpenseRepository expenseRepository) {
        this.expenseRepository = expenseRepository;
    }
    
    @Override
    public void addExpense(Expense expense) {
        if (expense == null) {
            throw new IllegalArgumentException("Expense cannot be null");
        }
        
        logger.debug("Adding expense: {}", expense);
        expenseRepository.save(expense);
        logger.info("Successfully added expense with ID: {}", expense.getId());
    }
    
    @Override
    public Optional<Expense> getExpenseById(String id) {
        if (id == null || id.trim().isEmpty()) {
            return Optional.empty();
        }
        
        return expenseRepository.findById(id);
    }
    
    @Override
    public List<Expense> getAllExpenses() {
        return expenseRepository.findAll();
    }
    
    @Override
    public List<Expense> getExpensesByCategory(String category) {
        if (category == null || category.trim().isEmpty()) {
            return List.of();
        }
        
        return expenseRepository.findByCategory(category.trim());
    }
    
    @Override
    public List<Expense> getExpensesByDateRange(LocalDate startDate, LocalDate endDate) {
        if (startDate == null || endDate == null) {
            throw new IllegalArgumentException("Start date and end date cannot be null");
        }
        
        if (startDate.isAfter(endDate)) {
            throw new IllegalArgumentException("Start date cannot be after end date");
        }
        
        return expenseRepository.findAll().stream()
                .filter(expense -> !expense.getDate().isBefore(startDate) && !expense.getDate().isAfter(endDate))
                .collect(Collectors.toList());
    }
    
    @Override
    public BigDecimal calculateTotalExpenses() {
        return expenseRepository.findAll().stream()
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    @Override
    public Map<String, BigDecimal> calculateExpensesByCategory() {
        return expenseRepository.findAll().stream()
                .collect(Collectors.groupingBy(
                        Expense::getCategory,
                        Collectors.reducing(BigDecimal.ZERO, Expense::getAmount, BigDecimal::add)
                ));
    }
    
    @Override
    public BigDecimal calculateTotalExpenses(LocalDate startDate, LocalDate endDate) {
        return getExpensesByDateRange(startDate, endDate).stream()
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    @Override
    public FinancialSummary getFinancialSummary() {
        List<Expense> allExpenses = expenseRepository.findAll();
        
        if (allExpenses.isEmpty()) {
            return new FinancialSummary(
                    BigDecimal.ZERO,
                    BigDecimal.ZERO,
                    null,
                    null,
                    0
            );
        }
        
        BigDecimal total = allExpenses.stream()
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        BigDecimal average = total.divide(
                BigDecimal.valueOf(allExpenses.size()), 
                2, 
                RoundingMode.HALF_UP
        );
        
        LocalDate earliest = allExpenses.stream()
                .map(Expense::getDate)
                .min(LocalDate::compareTo)
                .orElse(null);
        
        LocalDate latest = allExpenses.stream()
                .map(Expense::getDate)
                .max(LocalDate::compareTo)
                .orElse(null);
        
        return new FinancialSummary(total, average, earliest, latest, allExpenses.size());
    }
    
    @Override
    public FinancialSummary getFinancialSummary(LocalDate startDate, LocalDate endDate) {
        List<Expense> filteredExpenses = getExpensesByDateRange(startDate, endDate);
        
        if (filteredExpenses.isEmpty()) {
            return new FinancialSummary(
                    BigDecimal.ZERO,
                    BigDecimal.ZERO,
                    startDate,
                    endDate,
                    0
            );
        }
        
        BigDecimal total = filteredExpenses.stream()
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        BigDecimal average = total.divide(
                BigDecimal.valueOf(filteredExpenses.size()), 
                2, 
                RoundingMode.HALF_UP
        );
        
        return new FinancialSummary(total, average, startDate, endDate, filteredExpenses.size());
    }
    
    @Override
    public boolean deleteExpense(String id) {
        if (id == null || id.trim().isEmpty()) {
            return false;
        }
        
        boolean deleted = expenseRepository.deleteById(id);
        if (deleted) {
            logger.info("Successfully deleted expense with ID: {}", id);
        } else {
            logger.warn("Expense with ID {} not found for deletion", id);
        }
        
        return deleted;
    }
    
    @Override
    public void deleteAllExpenses() {
        expenseRepository.deleteAll();
        logger.info("Successfully deleted all expenses");
    }
    
    @Override
    public long getExpenseCount() {
        return expenseRepository.count();
    }
}
