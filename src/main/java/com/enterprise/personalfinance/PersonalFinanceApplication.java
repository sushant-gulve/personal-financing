package com.enterprise.personalfinance;

import com.enterprise.personalfinance.application.service.PersonalFinanceService;
import com.enterprise.personalfinance.application.service.impl.PersonalFinanceServiceImpl;
import com.enterprise.personalfinance.infrastructure.repository.ExpenseRepository;
import com.enterprise.personalfinance.infrastructure.repository.impl.FileBasedExpenseRepository;
import com.enterprise.personalfinance.presentation.cli.PersonalFinanceCLI;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main application class for the Personal Finance CLI application.
 * Sets up dependency injection and starts the application.
 */
public class PersonalFinanceApplication {
    
    private static final Logger logger = LoggerFactory.getLogger(PersonalFinanceApplication.class);
    
    public static void main(String[] args) {
        try {
            logger.info("Starting Personal Finance Application");
            
            // Initialize dependencies using manual dependency injection
            ExpenseRepository expenseRepository = new FileBasedExpenseRepository();
            PersonalFinanceService financeService = new PersonalFinanceServiceImpl(expenseRepository);
            PersonalFinanceCLI cli = new PersonalFinanceCLI(financeService);
            
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
