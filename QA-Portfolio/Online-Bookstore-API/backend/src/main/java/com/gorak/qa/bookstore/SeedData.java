package com.gorak.qa.bookstore;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.math.BigDecimal;

@Configuration
public class SeedData {
 @Bean CommandLineRunner seedBooks(BookRepository repository) {
  return args -> {
   if(repository.count()==0) {
    repository.save(new Book("Clean Code","Robert C. Martin",new BigDecimal("499.00"),10));
    repository.save(new Book("The Pragmatic Programmer","Andrew Hunt and David Thomas",new BigDecimal("599.00"),8));
    repository.save(new Book("Designing Data-Intensive Applications","Martin Kleppmann",new BigDecimal("799.00"),5));
   }
  };
 }
}
