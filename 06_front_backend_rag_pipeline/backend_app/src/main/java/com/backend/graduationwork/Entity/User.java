package com.backend.graduationwork.Entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import jakarta.persistence.Id;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@Table(name = "user")
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String userId;

    @Column(nullable = false)
    private String password;


    private User() {};

    public User(String userId, String password) {
        this.userId = userId;
        this.password = password;
    }

    public static User of(String userId, String password){
        return new User(userId,password);
    }

//    // 연관관계
//    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
//    private List<Folders> folders;
}
