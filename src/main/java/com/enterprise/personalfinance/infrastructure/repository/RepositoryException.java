package com.enterprise.personalfinance.infrastructure.repository;

/**
 * Exception thrown when repository operations fail.
 */
public class RepositoryException extends RuntimeException {
    
    public RepositoryException(String message) {
        super(message);
    }
    
    public RepositoryException(String message, Throwable cause) {
        super(message, cause);
    }
}
