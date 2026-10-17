package com.gorak.qa.bookstore;
import jakarta.persistence.*;
import java.math.BigDecimal;
@Entity @Table(name="books")
public class Book {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 @Column(nullable=false,length=180) private String title;
 @Column(nullable=false,length=120) private String author;
 @Column(nullable=false,precision=10,scale=2) private BigDecimal price;
 @Column(nullable=false) private Integer stock=0;
 public Book() {}
 public Book(String title,String author,BigDecimal price,Integer stock){this.title=title;this.author=author;this.price=price;this.stock=stock;}
 public Long getId(){return id;} public String getTitle(){return title;} public String getAuthor(){return author;} public BigDecimal getPrice(){return price;} public Integer getStock(){return stock;}
 public void setId(Long id){this.id=id;} public void setTitle(String title){this.title=title;} public void setAuthor(String author){this.author=author;} public void setPrice(BigDecimal price){this.price=price;} public void setStock(Integer stock){this.stock=stock;}
}
