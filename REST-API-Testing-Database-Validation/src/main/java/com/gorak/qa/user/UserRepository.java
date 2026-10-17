package com.gorak.qa.user;
import org.springframework.data.jpa.repository.JpaRepository;
public interface UserRepository extends JpaRepository<UserRecord,Long> {
 boolean existsByEmailIgnoreCase(String email);
}
