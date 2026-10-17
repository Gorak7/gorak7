package com.gorak.qa.bookstore;

import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@RestController @RequestMapping("/api") @CrossOrigin(origins="*")
public class BookController {
 private final BookRepository books;
 public BookController(BookRepository books){this.books=books;}
 @GetMapping("/health") public Map<String,String> health(){return Map.of("status","UP","service","bookstore");}
 @GetMapping("/books") public List<Book> all(@RequestParam(defaultValue="") String q){
  return q.isBlank()?books.findAll():books.findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCase(q,q);
 }
 @GetMapping("/books/{id}") public Book one(@PathVariable long id){return books.findById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Book not found"));}
 @PostMapping("/books") @ResponseStatus(HttpStatus.CREATED) public Book create(@Valid @RequestBody BookRequest b){return books.save(new Book(b.title(),b.author(),b.price(),b.stock()));}
 @PutMapping("/books/{id}") public Book update(@PathVariable long id,@Valid @RequestBody BookRequest b){
  Book existing=one(id);existing.setTitle(b.title());existing.setAuthor(b.author());existing.setPrice(b.price());existing.setStock(b.stock());return books.save(existing);
 }
 @DeleteMapping("/books/{id}") @ResponseStatus(HttpStatus.NO_CONTENT) public void delete(@PathVariable long id){books.delete(one(id));}
 @PostMapping("/orders") @ResponseStatus(HttpStatus.CREATED) public Map<String,Object> order(@Valid @RequestBody OrderRequest request){
  Book book=one(request.bookId());
  if(book.getStock()<request.quantity())throw new ResponseStatusException(HttpStatus.CONFLICT,"Insufficient stock");
  book.setStock(book.getStock()-request.quantity());books.save(book);
  BigDecimal total=book.getPrice().multiply(BigDecimal.valueOf(request.quantity()));
  return Map.of("orderReference","BOOK-"+System.currentTimeMillis(),"bookId",book.getId(),"quantity",request.quantity(),"total",total,"status","SIMULATED");
 }
 public record BookRequest(@NotBlank @Size(max=180) String title,@NotBlank @Size(max=120) String author,@NotNull @DecimalMin(value="0.01") BigDecimal price,@NotNull @Min(0) Integer stock){}
 public record OrderRequest(@Positive long bookId,@Positive int quantity){}
}
