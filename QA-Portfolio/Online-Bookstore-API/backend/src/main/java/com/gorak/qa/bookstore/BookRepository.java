package com.gorak.qa.bookstore;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
public interface BookRepository extends JpaRepository<Book,Long> {
 List<Book> findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCase(String title,String author);
}
