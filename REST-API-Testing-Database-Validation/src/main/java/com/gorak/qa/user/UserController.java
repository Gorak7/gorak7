package com.gorak.qa.user;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
public class UserController {
 private final UserRepository repo;
 @Value("${qa.api-key}") private String apiKey;
 public UserController(UserRepository repo){this.repo=repo;}
 private void auth(String key){if(key==null || !apiKey.equals(key)) throw new ResponseStatusException(HttpStatus.UNAUTHORIZED,"Missing or invalid X-API-Key");}
 @GetMapping public List<UserRecord> all(@RequestHeader(value="X-API-Key",required=false) String key){auth(key);return repo.findAll();}
 @GetMapping("/{id}") public UserRecord one(@PathVariable Long id,@RequestHeader(value="X-API-Key",required=false) String key){auth(key);return repo.findById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"User not found"));}
 @PostMapping @ResponseStatus(HttpStatus.CREATED)
 public UserRecord create(@Valid @RequestBody UserRecord in,@RequestHeader(value="X-API-Key",required=false) String key){
  auth(key); if(repo.existsByEmailIgnoreCase(in.getEmail())) throw new ResponseStatusException(HttpStatus.CONFLICT,"Email already exists");
  in.setName(in.getName().trim());in.setEmail(in.getEmail().trim().toLowerCase());in.setRole(in.getRole().trim());return repo.save(in);
 }
 @PutMapping("/{id}") public UserRecord replace(@PathVariable Long id,@Valid @RequestBody UserRecord in,@RequestHeader(value="X-API-Key",required=false) String key){
  auth(key);UserRecord cur=repo.findById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"User not found"));
  if(!cur.getEmail().equalsIgnoreCase(in.getEmail())&&repo.existsByEmailIgnoreCase(in.getEmail()))throw new ResponseStatusException(HttpStatus.CONFLICT,"Email already exists");
  cur.setName(in.getName().trim());cur.setEmail(in.getEmail().trim().toLowerCase());cur.setRole(in.getRole().trim());return repo.save(cur);
 }
 @PatchMapping("/{id}") public UserRecord patch(@PathVariable Long id,@RequestBody Map<String,Object> changes,@RequestHeader(value="X-API-Key",required=false) String key){
  auth(key);UserRecord cur=repo.findById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND,"User not found"));
  if(changes.isEmpty())throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"At least one editable field is required");
  if(changes.containsKey("name")){Object v=changes.get("name");if(!(v instanceof String s)||s.isBlank()||s.length()>80)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"name must be a non-empty string up to 80 characters");cur.setName(s.trim());}
  if(changes.containsKey("email")){Object v=changes.get("email");if(!(v instanceof String s)||s.isBlank()||!s.matches("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")||s.length()>160)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"email must be valid");if(!cur.getEmail().equalsIgnoreCase(s)&&repo.existsByEmailIgnoreCase(s))throw new ResponseStatusException(HttpStatus.CONFLICT,"Email already exists");cur.setEmail(s.trim().toLowerCase());}
  if(changes.containsKey("role")){Object v=changes.get("role");if(!(v instanceof String s)||s.isBlank()||s.length()>40)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"role must be a non-empty string up to 40 characters");cur.setRole(s.trim());}
  return repo.save(cur);
 }
 @DeleteMapping("/{id}") @ResponseStatus(HttpStatus.NO_CONTENT)
 public void delete(@PathVariable Long id,@RequestHeader(value="X-API-Key",required=false) String key){auth(key);if(!repo.existsById(id))throw new ResponseStatusException(HttpStatus.NOT_FOUND,"User not found");repo.deleteById(id);}
}
