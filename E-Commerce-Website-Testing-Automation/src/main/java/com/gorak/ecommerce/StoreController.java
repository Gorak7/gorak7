package com.gorak.ecommerce;
import jakarta.validation.Valid; import jakarta.validation.constraints.*; import org.springframework.http.HttpStatus; import org.springframework.web.bind.annotation.*; import org.springframework.web.server.ResponseStatusException; import java.util.*;
@RestController @RequestMapping("/api") public class StoreController {
private final OrderRepository orders; private final List<Product> products=List.of(new Product(1L,"Wireless Headphones","Comfortable over-ear headphones",2499.00,"Audio"),new Product(2L,"Mechanical Keyboard","Compact mechanical keyboard",3299.00,"Accessories"),new Product(3L,"USB-C Hub","Seven-port USB-C hub",1799.00,"Accessories"),new Product(4L,"Smart Watch","Everyday fitness smartwatch",4599.00,"Wearables"));
public StoreController(OrderRepository orders){this.orders=orders;}
@GetMapping("/health") public Map<String,String> health(){return Map.of("status","UP");}
@GetMapping("/products") public List<Product> products(){return products;}
@PostMapping("/orders") @ResponseStatus(HttpStatus.CREATED) public Map<String,Object> createOrder(@Valid @RequestBody CheckoutRequest req){double total=0;StringJoiner names=new StringJoiner(", ");if(req.productIds().isEmpty())throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Cart must contain at least one product");for(Long id:req.productIds()){Product p=products.stream().filter(x->x.id().equals(id)).findFirst().orElseThrow(()->new ResponseStatusException(HttpStatus.BAD_REQUEST,"Unknown product id: "+id));total+=p.price();names.add(p.name());}Order saved=orders.save(new Order(req.name().trim(),req.email().trim(),names.toString(),total));return Map.of("orderId",saved.getId(),"customerName",saved.getCustomerName(),"items",saved.getItems(),"total",saved.getTotal(),"status","CONFIRMED");}
@GetMapping("/orders/{id}") public Order getOrder(@PathVariable Long id){return orders.findById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Order not found"));}
public record CheckoutRequest(@NotBlank String name,@NotBlank @Email String email,@NotEmpty List<Long> productIds){}
}
