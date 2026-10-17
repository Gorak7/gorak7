package com.gorak.qa.ecommerce;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.math.BigDecimal;

@Configuration
public class SeedData {
    @Bean
    CommandLineRunner seedProducts(ProductRepository repository) {
        return args -> {
            if (repository.count() == 0) {
                repository.save(new Product("Wireless Mouse", "Ergonomic wireless mouse", new BigDecimal("799.00"), 25));
                repository.save(new Product("Mechanical Keyboard", "Compact mechanical keyboard", new BigDecimal("2499.00"), 12));
                repository.save(new Product("USB-C Hub", "Seven-port USB-C hub", new BigDecimal("1599.00"), 18));
            }
        };
    }
}
