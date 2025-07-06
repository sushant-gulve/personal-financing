package com.enterprise.personalfinance.infrastructure.config;

import com.enterprise.personalfinance.application.service.PersonalFinanceService;
import com.enterprise.personalfinance.application.service.impl.PersonalFinanceServiceImpl;
import com.enterprise.personalfinance.infrastructure.di.DIContainer;
import com.enterprise.personalfinance.infrastructure.repository.ExpenseRepository;
import com.enterprise.personalfinance.infrastructure.repository.impl.FileBasedExpenseRepository;
import com.enterprise.personalfinance.presentation.cli.PersonalFinanceCLI;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Configuration class for setting up dependency injection.
 * This class centralizes all dependency configuration and wiring.
 */
public class ApplicationConfig {
    
    private static final Logger logger = LoggerFactory.getLogger(ApplicationConfig.class);
    
    /**
     * Configure and return a fully initialized DI container with all dependencies
     */
    public static DIContainer createContainer() {
        logger.info("Initializing dependency injection container");
        
        DIContainer container = new DIContainer();
        
        // Register repository as singleton - only one instance needed for the entire application
        logger.debug("Registering ExpenseRepository as singleton");
        container.registerSingleton(
            ExpenseRepository.class, 
            new FileBasedExpenseRepository()
        );
        
        // Register service as factory - creates new instance when requested (depends on repository)
        logger.debug("Registering PersonalFinanceService as factory");
        container.registerFactory(
            PersonalFinanceService.class,
            () -> {
                ExpenseRepository repository = container.getInstance(ExpenseRepository.class);
                return new PersonalFinanceServiceImpl(repository);
            }
        );
        
        // Register CLI as factory - creates new instance when requested (depends on service)
        logger.debug("Registering PersonalFinanceCLI as factory");
        container.registerFactory(
            PersonalFinanceCLI.class,
            () -> {
                PersonalFinanceService service = container.getInstance(PersonalFinanceService.class);
                return new PersonalFinanceCLI(service);
            }
        );
        
        logger.info("Dependency injection container initialized with {} registered types", 
                   container.getRegisteredTypesCount());
        
        return container;
    }
    
    /**
     * Validate that all required dependencies are registered
     */
    public static void validateContainer(DIContainer container) {
        logger.info("Validating dependency injection container");
        
        // Check that all required types are registered
        Class<?>[] requiredTypes = {
            ExpenseRepository.class,
            PersonalFinanceService.class,
            PersonalFinanceCLI.class
        };
        
        for (Class<?> type : requiredTypes) {
            if (!container.isRegistered(type)) {
                throw new IllegalStateException("Required dependency not registered: " + type.getName());
            }
        }
        
        // Test that instances can be created
        try {
            container.getInstance(ExpenseRepository.class);
            container.getInstance(PersonalFinanceService.class);
            container.getInstance(PersonalFinanceCLI.class);
            
            logger.info("All dependencies validated successfully");
        } catch (Exception e) {
            logger.error("Dependency validation failed", e);
            throw new IllegalStateException("Failed to create required dependencies", e);
        }
    }
}
