package com.enterprise.personalfinance.domain.model;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.assertj.core.api.Assertions.*;

/**
 * Unit tests for the Expense domain model.
 */
@DisplayName("Expense Domain Model Tests")
class ExpenseTest {
    
    @Test
    @DisplayName("Should create expense with valid parameters")
    void shouldCreateExpenseWithValidParameters() {
        // Given
        String category = "Food";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Lunch at cafe";
        String[] tags = {"restaurant", "lunch"};
        
        // When
        Expense expense = new Expense(category, amount, date, description, tags);
        
        // Then
        assertThat(expense.getCategory()).isEqualTo(category);
        assertThat(expense.getAmount()).isEqualTo(amount);
        assertThat(expense.getDate()).isEqualTo(date);
        assertThat(expense.getDescription()).isEqualTo(description);
        assertThat(expense.getTags()).containsExactly("restaurant", "lunch");
        assertThat(expense.getId()).isNotNull().isNotEmpty();
    }
    
    @Test
    @DisplayName("Should throw exception when category is null")
    void shouldThrowExceptionWhenCategoryIsNull() {
        // Given
        String category = null;
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Test expense";
        
        // When & Then
        assertThatThrownBy(() -> new Expense(category, amount, date, description))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Category cannot be null or empty");
    }
    
    @Test
    @DisplayName("Should throw exception when category is empty")
    void shouldThrowExceptionWhenCategoryIsEmpty() {
        // Given
        String category = "   ";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Test expense";
        
        // When & Then
        assertThatThrownBy(() -> new Expense(category, amount, date, description))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Category cannot be null or empty");
    }
    
    @Test
    @DisplayName("Should throw exception when amount is null")
    void shouldThrowExceptionWhenAmountIsNull() {
        // Given
        String category = "Food";
        BigDecimal amount = null;
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Test expense";
        
        // When & Then
        assertThatThrownBy(() -> new Expense(category, amount, date, description))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Amount cannot be null or negative");
    }
    
    @Test
    @DisplayName("Should throw exception when amount is negative")
    void shouldThrowExceptionWhenAmountIsNegative() {
        // Given
        String category = "Food";
        BigDecimal amount = new BigDecimal("-10.00");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Test expense";
        
        // When & Then
        assertThatThrownBy(() -> new Expense(category, amount, date, description))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Amount cannot be null or negative");
    }
    
    @Test
    @DisplayName("Should throw exception when date is null")
    void shouldThrowExceptionWhenDateIsNull() {
        // Given
        String category = "Food";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = null;
        String description = "Test expense";
        
        // When & Then
        assertThatThrownBy(() -> new Expense(category, amount, date, description))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Date cannot be null");
    }
    
    @Test
    @DisplayName("Should handle null description gracefully")
    void shouldHandleNullDescriptionGracefully() {
        // Given
        String category = "Food";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = null;
        
        // When
        Expense expense = new Expense(category, amount, date, description);
        
        // Then
        assertThat(expense.getDescription()).isEmpty();
    }
    
    @Test
    @DisplayName("Should handle null tags gracefully")
    void shouldHandleNullTagsGracefully() {
        // Given
        String category = "Food";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Test expense";
        String[] tags = null;
        
        // When
        Expense expense = new Expense(category, amount, date, description, tags);
        
        // Then
        assertThat(expense.getTags()).isEmpty();
    }
    
    @Test
    @DisplayName("Should trim whitespace from category and description")
    void shouldTrimWhitespaceFromCategoryAndDescription() {
        // Given
        String category = "  Food  ";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "  Test expense  ";
        
        // When
        Expense expense = new Expense(category, amount, date, description);
        
        // Then
        assertThat(expense.getCategory()).isEqualTo("Food");
        assertThat(expense.getDescription()).isEqualTo("Test expense");
    }
    
    @Test
    @DisplayName("Should implement equals based on ID")
    void shouldImplementEqualsBasedOnId() {
        // Given
        String id = "test-id";
        String category = "Food";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Test expense";
        String[] tags = new String[0];
        
        Expense expense1 = new Expense(id, category, amount, date, description, tags);
        Expense expense2 = new Expense(id, "Different Category", new BigDecimal("100.00"), date, "Different description", tags);
        
        // When & Then
        assertThat(expense1).isEqualTo(expense2);
        assertThat(expense1.hashCode()).isEqualTo(expense2.hashCode());
    }
    
    @Test
    @DisplayName("Should have meaningful toString representation")
    void shouldHaveMeaningfulToStringRepresentation() {
        // Given
        String category = "Food";
        BigDecimal amount = new BigDecimal("25.50");
        LocalDate date = LocalDate.of(2025, 7, 1);
        String description = "Lunch at cafe";
        
        Expense expense = new Expense(category, amount, date, description);
        
        // When
        String toString = expense.toString();
        
        // Then
        assertThat(toString)
                .contains("Expense{")
                .contains("category='Food'")
                .contains("amount=25.50")
                .contains("date=2025-07-01")
                .contains("description='Lunch at cafe'")
                .contains("id='" + expense.getId() + "'");
    }
}
