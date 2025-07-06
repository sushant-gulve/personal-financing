package com.enterprise.personalfinance.domain.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Objects;

/**
 * Domain model representing financial summary information.
 */
public class FinancialSummary {
    
    private final BigDecimal totalExpenses;
    private final BigDecimal averageExpense;
    private final LocalDate periodStart;
    private final LocalDate periodEnd;
    private final int transactionCount;
    
    public FinancialSummary(BigDecimal totalExpenses, BigDecimal averageExpense, 
                           LocalDate periodStart, LocalDate periodEnd, int transactionCount) {
        this.totalExpenses = totalExpenses != null ? totalExpenses : BigDecimal.ZERO;
        this.averageExpense = averageExpense != null ? averageExpense : BigDecimal.ZERO;
        this.periodStart = periodStart;
        this.periodEnd = periodEnd;
        this.transactionCount = transactionCount;
    }
    
    public BigDecimal getTotalExpenses() {
        return totalExpenses;
    }
    
    public BigDecimal getAverageExpense() {
        return averageExpense;
    }
    
    public LocalDate getPeriodStart() {
        return periodStart;
    }
    
    public LocalDate getPeriodEnd() {
        return periodEnd;
    }
    
    public int getTransactionCount() {
        return transactionCount;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        FinancialSummary that = (FinancialSummary) o;
        return transactionCount == that.transactionCount &&
               Objects.equals(totalExpenses, that.totalExpenses) &&
               Objects.equals(averageExpense, that.averageExpense) &&
               Objects.equals(periodStart, that.periodStart) &&
               Objects.equals(periodEnd, that.periodEnd);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(totalExpenses, averageExpense, periodStart, periodEnd, transactionCount);
    }
    
    @Override
    public String toString() {
        return String.format("FinancialSummary{totalExpenses=%s, averageExpense=%s, periodStart=%s, periodEnd=%s, transactionCount=%d}",
                           totalExpenses, averageExpense, periodStart, periodEnd, transactionCount);
    }
}
