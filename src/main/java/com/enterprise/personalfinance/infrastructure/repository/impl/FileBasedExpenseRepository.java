package com.enterprise.personalfinance.infrastructure.repository.impl;

import com.enterprise.personalfinance.domain.model.Expense;
import com.enterprise.personalfinance.infrastructure.repository.ExpenseRepository;
import com.enterprise.personalfinance.infrastructure.repository.RepositoryException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * File-based implementation of ExpenseRepository using JSON for persistence.
 * Thread-safe implementation with proper error handling and logging.
 */
public class FileBasedExpenseRepository implements ExpenseRepository {
    
    private static final Logger logger = LoggerFactory.getLogger(FileBasedExpenseRepository.class);
    private static final String DEFAULT_FILENAME = "expenses.json";
    
    private final Path filePath;
    private final ObjectMapper objectMapper;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    
    public FileBasedExpenseRepository() {
        this(DEFAULT_FILENAME);
    }
    
    public FileBasedExpenseRepository(String filename) {
        this.filePath = Paths.get(filename);
        this.objectMapper = createObjectMapper();
        initializeFileIfNotExists();
    }
    
    private ObjectMapper createObjectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        mapper.enable(SerializationFeature.INDENT_OUTPUT);
        return mapper;
    }
    
    private void initializeFileIfNotExists() {
        lock.writeLock().lock();
        try {
            if (!Files.exists(filePath)) {
                Files.createDirectories(filePath.getParent() != null ? filePath.getParent() : Paths.get("."));
                objectMapper.writeValue(filePath.toFile(), new ArrayList<Expense>());
                logger.info("Initialized new expense file: {}", filePath);
            }
        } catch (IOException e) {
            throw new RepositoryException("Failed to initialize expense file: " + filePath, e);
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    @Override
    public void save(Expense expense) {
        if (expense == null) {
            throw new IllegalArgumentException("Expense cannot be null");
        }
        
        lock.writeLock().lock();
        try {
            List<Expense> expenses = loadExpenses();
            
            // Remove existing expense with same ID if present
            expenses.removeIf(e -> e.getId().equals(expense.getId()));
            expenses.add(expense);
            
            saveExpenses(expenses);
            logger.debug("Saved expense: {}", expense.getId());
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    @Override
    public void saveAll(List<Expense> expenses) {
        if (expenses == null) {
            throw new IllegalArgumentException("Expenses list cannot be null");
        }
        
        lock.writeLock().lock();
        try {
            saveExpenses(new ArrayList<>(expenses));
            logger.debug("Saved {} expenses", expenses.size());
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    @Override
    public Optional<Expense> findById(String id) {
        if (id == null) {
            return Optional.empty();
        }
        
        lock.readLock().lock();
        try {
            return loadExpenses().stream()
                    .filter(expense -> id.equals(expense.getId()))
                    .findFirst();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    @Override
    public List<Expense> findAll() {
        lock.readLock().lock();
        try {
            return new ArrayList<>(loadExpenses());
        } finally {
            lock.readLock().unlock();
        }
    }
    
    @Override
    public List<Expense> findByCategory(String category) {
        if (category == null) {
            return new ArrayList<>();
        }
        
        lock.readLock().lock();
        try {
            return loadExpenses().stream()
                    .filter(expense -> category.equalsIgnoreCase(expense.getCategory()))
                    .toList();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    @Override
    public boolean deleteById(String id) {
        if (id == null) {
            return false;
        }
        
        lock.writeLock().lock();
        try {
            List<Expense> expenses = loadExpenses();
            boolean removed = expenses.removeIf(expense -> id.equals(expense.getId()));
            
            if (removed) {
                saveExpenses(expenses);
                logger.debug("Deleted expense: {}", id);
            }
            
            return removed;
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    @Override
    public void deleteAll() {
        lock.writeLock().lock();
        try {
            saveExpenses(new ArrayList<>());
            logger.debug("Deleted all expenses");
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    @Override
    public long count() {
        lock.readLock().lock();
        try {
            return loadExpenses().size();
        } finally {
            lock.readLock().unlock();
        }
    }
    
    private List<Expense> loadExpenses() {
        try {
            if (!Files.exists(filePath)) {
                return new ArrayList<>();
            }
            
            return objectMapper.readValue(filePath.toFile(), new TypeReference<List<Expense>>() {});
        } catch (IOException e) {
            logger.error("Failed to load expenses from file: {}", filePath, e);
            throw new RepositoryException("Failed to load expenses from file: " + filePath, e);
        }
    }
    
    private void saveExpenses(List<Expense> expenses) {
        try {
            objectMapper.writeValue(filePath.toFile(), expenses);
        } catch (IOException e) {
            logger.error("Failed to save expenses to file: {}", filePath, e);
            throw new RepositoryException("Failed to save expenses to file: " + filePath, e);
        }
    }
}
