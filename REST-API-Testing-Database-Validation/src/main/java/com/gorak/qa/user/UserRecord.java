package com.gorak.qa.user;
import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
@Entity
@Table(name="user_records", uniqueConstraints=@UniqueConstraint(columnNames="email"))
public class UserRecord {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
 @NotBlank(message="Name is required") @Size(max=80) @Column(nullable=false,length=80) private String name;
 @NotBlank(message="Email is required") @Email(message="Email must be valid") @Size(max=160) @Column(nullable=false,unique=true,length=160) private String email;
 @NotBlank(message="Role is required") @Size(max=40) @Column(nullable=false,length=40) private String role;
 public UserRecord() {}
 public Long getId(){return id;}
 public String getName(){return name;} public void setName(String v){name=v;}
 public String getEmail(){return email;} public void setEmail(String v){email=v;}
 public String getRole(){return role;} public void setRole(String v){role=v;}
}
