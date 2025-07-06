package com.enterprise.personalfinance.application.service.impl;

import com.enterprise.personalfinance.application.service.PersonalFinanceService;
import com.enterprise.personalfinance.domain.model.Expense;
import com.enterprise.personalfinance.domain.model.FinancialSummary;
import com.enterprise.personalfinance.infrastructure.repository.ExpenseRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for PersonalFinanceServiceImpl.
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("Personal Finance Service Tests")
class PersonalFinanceServiceImplTest {
    
    @Mock
    private ExpenseRepository expenseRepository;
    
    private PersonalFinanceService financeService;
    
    @BeforeEach
    void setUp() {
        financeService = new PersonalFinanceServiceImpl(expenseRepository);
    }
    
    @Test
    @DisplayName("Should add expense successfully")
    void shouldAddExpenseSuccessfully() {
        // Given
        Expense expense = createTestExpense("Food", "25.50", LocalDate.of(2025, 7, 1));
        
        // When
        financeService.addExpense(expense);
        
        // Then
        verify(expenseRepository).save(expense);
    }
    
    @Test
    @DisplayName("Should throw exception when adding null expense")
    void shouldThrowExceptionWhenAddingNullExpense() {
        // When & Then
        assertThatThrownBy(() -> financeService.addExpense(null))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Expense cannot be null");
        
        verify(expenseRepository, never()).save(any());
    }
    
    @Test
    @DisplayName("Should get expense by ID")
    void shouldGetExpenseById() {
        // Given
        String expenseId = "test-id";
        Expense expense = createTestExpense("Food", "25.50", LocalDate.of(2025, 7, 1));
        when(expenseRepository.findById(expenseId)).thenReturn(Optional.of(expense));
        
        // When
        Optional<Expense> result = financeService.getExpenseById(expenseId);
        
        // Then
        assertThat(result).isPresent().contains(expense);
        verify(expenseRepository).findById(expenseId);
    }
    
    @Test
    @DisplayName("Should return empty when expense not found")
    void shouldReturnEmptyWhenExpenseNotFound() {
        // Given
        String expenseId = "non-existent-id";
        when(expenseRepository.findById(expenseId)).thenReturn(Optional.empty());
        
        // When
        Optional<Expense> result = financeService.getExpenseById(expenseId);
        
        // Then
        assertThat(result).isEmpty();
        verify(expenseRepository).findById(expenseId);
    }
    
    @Test
    @DisplayName("Should get all expenses")
    void shouldGetAllExpenses() {
        // Given
        List<Expense> expenses = Arrays.asList(
                createTestExpense("Food", "25.50", LocalDate.of(2025, 7, 1)),
                createTestExpense("Transport", "15.00", LocalDate.of(2025, 7, 2))
        );
        when(expenseRepository.findAll()).thenReturn(expenses);
        
        // When
        List<Expense> result = financeService.getAllExpenses();
        
        // Then
        assertThat(result).hasSize(2).containsExactlyElementsOf(expenses);
        verify(expenseRepository).findAll();
    }
    
    @Test
    @DisplayName("Should calculate total expenses")
    void shouldCalculateTotalExpenses() {
        // Given
        List<Expense> expenses = Arrays.asList(
                createTestExpense("Food", "25.50", LocalDate.of(2025, 7, 1)),
                createTestExpense("Transport", "15.00", LocalDate.of(2025, 7, 2)),
                createTestExpense("Entertainment", "30.00", LocalDate.of(2025, 7, 3))
        );
        when(expenseRepository.findAll()).thenReturn(expenses);
        
        // When
        BigDecimal total = financeService.calculateTotalExpenses();
        
        // Then
        assertThat(total).isEqualTo(new BigDecimal("70.50"));
        verify(expenseRepository).findAll();
    }
    
    @Test
    @DisplayName("Should return zero when no expenses exist")
    void shouldReturnZeroWhenNoExpensesExist() {
        // Given
        when(expenseRepository.findAll()).thenReturn(Arrays.asList());
        
        // When
        BigDecimal total = financeService.calculateTotalExpenses();
        
        // Then
        assertThat(total).isEqualTo(BigDecimal.ZERO);
        verify(expenseRepository).findAll();
    }
    
    @Test
    @DisplayName("Should get expenses by date range")
    void shouldGetExpensesByDateRange() {
        // Given
        LocalDate startDate = LocalDate.of(2025, 7, 1);
        LocalDate endDate = LocalDate.of(2025, 7, 3);
        
        List<Expense> allExpenses = Arrays.asList(
                createTestExpense("Food", "25.50", LocalDate.of(2025, 6, 30)), // Before range
                createTestExpense("Transport", "15.00", LocalDate.of(2025, 7, 1)), // In range
                createTestExpense("Entertainment", "30.00", LocalDate.of(2025, 7, 2)), // In range
                createTestExpense("Shopping", "50.00", LocalDate.of(2025, 7, 5)) // After range
        );
        when(expenseRepository.findAll()).thenReturn(allExpenses);
        
        // When
        List<Expense> result = financeService.getExpensesByDateRange(startDate, endDate);
        
        // Then
        assertThat(result).hasSize(2);
        assertThat(result.get(0).getCategory()).isEqualTo("Transport");
        assertThat(result.get(1).getCategory()).isEqualTo("Entertainment");
        verify(expenseRepository).findAll();
    }
    
    @Test
    @DisplayName("Should throw exception when start date is after end date")
    void shouldThrowExceptionWhenStartDateIsAfterEndDate() {
        // Given
        LocalDate startDate = LocalDate.of(2025, 7, 5);
        LocalDate endDate = LocalDate.of(2025, 7, 1);
        
        // When & Then
        assertThatThrownBy(() -> financeService.getExpensesByDateRange(startDate, endDate))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Start date cannot be after end date");
        
        verify(expenseRepository, never()).findAll();
    }
    
    @Test
    @DisplayName("Should generate financial summary")
    void shouldGenerateFinancialSummary() {
        // Given
        List<Expense> expenses = Arrays.asList(
                createTestExpense("Food", "20.00", LocalDate.of(2025, 7, 1)),
                createTestExpense("Transport", "30.00", LocalDate.of(2025, 7, 2)),
                createTestExpense("Entertainment", "50.00", LocalDate.of(2025, 7, 3))
        );
        when(expenseRepository.findAll()).thenReturn(expenses);
        
        // When
        FinancialSummary summary = financeService.getFinancialSummary();
        
        // Then
        assertThat(summary.getTotalExpenses()).isEqualTo(new BigDecimal("100.00"));
        assertThat(summary.getAverageExpense()).isEqualTo(new BigDecimal("33.33"));
        assertThat(summary.getTransactionCount()).isEqualTo(3);
        assertThat(summary.getPeriodStart()).isEqualTo(LocalDate.of(2025, 7, 1));
        assertThat(summary.getPeriodEnd()).isEqualTo(LocalDate.of(2025, 7, 3));
        verify(expenseRepository).findAll();
    }
    
    @Test
    @DisplayName("Should delete expense successfully")
    void shouldDeleteExpenseSuccessfully() {
        // Given
        String expenseId = "test-id";
        when(expenseRepository.deleteById(expenseId)).thenReturn(true);
        
        // When
        boolean result = financeService.deleteExpense(expenseId);
        
        // Then
        assertThat(result).isTrue();
        verify(expenseRepository).deleteById(expenseId);
    }
    
    @Test
    @DisplayName("Should return false when deleting non-existent expense")
    void shouldReturnFalseWhenDeletingNonExistentExpense() {
        // Given
        String expenseId = "non-existent-id";
        when(expenseRepository.deleteById(expenseId)).thenReturn(false);
        
        // When
        boolean result = financeService.deleteExpense(expenseId);
        
        // Then
        assertThat(result).isFalse();
        verify(expenseRepository).deleteById(expenseId);
    }
    
    private Expense createTestExpense(String category, String amount, LocalDate date) {
        return new Expense(category, new BigDecimal(amount), date, "Test expense");
    }
}
