package com.gorak.ecommerce;
import jakarta.persistence.*;
import java.time.Instant;
@Entity @Table(name="customer_orders") public class Order {
@Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
private String customerName; private String email; private String items; private double total; private Instant createdAt=Instant.now();
protected Order() {}
public Order(String customerName,String email,String items,double total){this.customerName=customerName;this.email=email;this.items=items;this.total=total;this.createdAt=Instant.now();}
public Long getId(){return id;} public String getCustomerName(){return customerName;} public String getEmail(){return email;} public String getItems(){return items;} public double getTotal(){return total;} public Instant getCreatedAt(){return createdAt;}
}
