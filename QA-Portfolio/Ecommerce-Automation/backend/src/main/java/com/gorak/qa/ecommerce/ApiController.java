package com.gorak.qa.ecommerce;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Positive;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import java.math.BigDecimal;
import java.util.Map;
import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ApiController {
    private final ProductRepository products;
    public ApiController(ProductRepository products) { this.products = products; }

    @GetMapping("/health")
    public Map<String, String> health() { return Map.of("status", "UP", "service", "ecommerce"); }

    @GetMapping("/products")
    public List<Product> all(@RequestParam(defaultValue = "") String q) {
        return q.isBlank() ? products.findAll() : products.findByNameContainingIgnoreCase(q);
    }

    @PostMapping("/orders")
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, Object> createOrder(@Valid @RequestBody OrderRequest request) {
        BigDecimal total = BigDecimal.ZERO;
        for (OrderLine line : request.items()) {
            Product product = products.findById(line.productId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "Unknown product"));
            if (product.getStock() < line.quantity())
                throw new ResponseStatusException(HttpStatus.CONFLICT, "Insufficient stock");
            total = total.add(product.getPrice().multiply(BigDecimal.valueOf(line.quantity())));
        }
        return Map.of("orderReference", "QA-" + System.currentTimeMillis(),
                      "email", request.email(), "total", total, "status", "SIMULATED");
    }

    public record OrderRequest(@Email @NotBlank String email, @NotEmpty List<@Valid OrderLine> items) {}
    public record OrderLine(@Positive long productId, @Positive int quantity) {}
}
