package com.enterprise.personalfinance;

import com.enterprise.personalfinance.infrastructure.config.ApplicationConfig;
import com.enterprise.personalfinance.infrastructure.di.DIContainer;
import com.enterprise.personalfinance.presentation.cli.PersonalFinanceCLI;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main application class for the Personal Finance CLI application.
 * Uses dependency injection for managing dependencies and loose coupling.
 */
public class PersonalFinanceApplication {
    
    private static final Logger logger = LoggerFactory.getLogger(PersonalFinanceApplication.class);
    
    public static void main(String[] args) {
        try {
            logger.info("Starting Personal Finance Application with Dependency Injection");
            
            // Initialize dependency injection container
            DIContainer container = ApplicationConfig.createContainer();
            
            // Validate that all dependencies are properly configured
            ApplicationConfig.validateContainer(container);
            
            // Get the CLI instance from the container (all dependencies will be injected automatically)
            PersonalFinanceCLI cli = container.getInstance(PersonalFinanceCLI.class);
            
            logger.info("All dependencies initialized successfully, starting CLI");
            
            // Start the CLI application
            cli.start();
            
            logger.info("Personal Finance Application terminated successfully");
            
        } catch (Exception e) {
            logger.error("Fatal error in Personal Finance Application", e);
            System.err.println("A fatal error occurred: " + e.getMessage());
            System.err.println("Please check the logs for more details.");
            System.exit(1);
        }
    }
}
