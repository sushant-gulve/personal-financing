package com.enterprise.personalfinance.infrastructure.di;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Simple dependency injection container for managing application dependencies.
 */
public class DIContainer {
    
    private final Map<Class<?>, Object> singletons = new HashMap<>();
    private final Map<Class<?>, Supplier<?>> factories = new HashMap<>();
    
    /**
     * Register a singleton instance
     */
    public <T> void registerSingleton(Class<T> type, T instance) {
        singletons.put(type, instance);
    }
    
    /**
     * Register a factory for creating instances
     */
    public <T> void registerFactory(Class<T> type, Supplier<T> factory) {
        factories.put(type, factory);
    }
    
    /**
     * Get an instance of the specified type
     */
    @SuppressWarnings("unchecked")
    public <T> T getInstance(Class<T> type) {
        // Check if singleton exists
        Object singleton = singletons.get(type);
        if (singleton != null) {
            return (T) singleton;
        }
        
        // Check if factory exists
        Supplier<?> factory = factories.get(type);
        if (factory != null) {
            return (T) factory.get();
        }
        
        throw new IllegalArgumentException("No registration found for type: " + type.getName());
    }
    
    /**
     * Check if a type is registered
     */
    public boolean isRegistered(Class<?> type) {
        return singletons.containsKey(type) || factories.containsKey(type);
    }
    
    /**
     * Get all registered types
     */
    public int getRegisteredTypesCount() {
        return singletons.size() + factories.size();
    }
}
