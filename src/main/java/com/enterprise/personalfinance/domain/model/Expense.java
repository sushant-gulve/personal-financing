package com.enterprise.personalfinance.domain.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Objects;
import java.util.UUID;

/**
 * Domain model representing a financial expense.
 * Immutable value object with enterprise-grade validation and formatting.
 */
public class Expense {
    
    @JsonProperty("id")
    private final String id;
    
    @JsonProperty("category")
    private final String category;
    
    @JsonProperty("amount")
    private final BigDecimal amount;
    
    @JsonProperty("date")
    @JsonFormat(pattern = "yyyy-MM-dd")
    private final LocalDate date;
    
    @JsonProperty("description")
    private final String description;
    
    @JsonProperty("tags")
    private final String[] tags;
    
    // Default constructor for Jackson
    public Expense() {
        this.id = UUID.randomUUID().toString();
        this.category = "";
        this.amount = BigDecimal.ZERO;
        this.date = LocalDate.now();
        this.description = "";
        this.tags = new String[0];
    }
    
    public Expense(String category, BigDecimal amount, LocalDate date, String description) {
        this(UUID.randomUUID().toString(), category, amount, date, description, new String[0]);
    }
    
    public Expense(String category, BigDecimal amount, LocalDate date, String description, String[] tags) {
        this(UUID.randomUUID().toString(), category, amount, date, description, tags);
    }
    
    public Expense(String id, String category, BigDecimal amount, LocalDate date, String description, String[] tags) {
        if (category == null || category.trim().isEmpty()) {
            throw new IllegalArgumentException("Category cannot be null or empty");
        }
        if (amount == null || amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Amount cannot be null or negative");
        }
        if (date == null) {
            throw new IllegalArgumentException("Date cannot be null");
        }
        
        this.id = id != null ? id : UUID.randomUUID().toString();
        this.category = category.trim();
        this.amount = amount;
        this.date = date;
        this.description = description != null ? description.trim() : "";
        this.tags = tags != null ? tags.clone() : new String[0];
    }
    
    public String getId() {
        return id;
    }
    
    public String getCategory() {
        return category;
    }
    
    public BigDecimal getAmount() {
        return amount;
    }
    
    public LocalDate getDate() {
        return date;
    }
    
    public String getDescription() {
        return description;
    }
    
    public String[] getTags() {
        return tags.clone();
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Expense expense = (Expense) o;
        return Objects.equals(id, expense.id);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
    
    @Override
    public String toString() {
        return String.format("Expense{id='%s', category='%s', amount=%s, date=%s, description='%s'}", 
                           id, category, amount, date, description);
    }
}
