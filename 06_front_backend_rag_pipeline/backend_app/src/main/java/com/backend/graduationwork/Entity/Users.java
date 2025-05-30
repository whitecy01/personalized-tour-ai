package com.backend.graduationwork.Entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import jakarta.persistence.Id;

@Entity
@Getter
@Setter
@Table(name = "users")
@AllArgsConstructor
public class Users {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String userId;

    @Column(nullable = false)
    private String password;


    private Users() {};

    public Users(String userId, String password) {
        this.userId = userId;
        this.password = password;
    }

    public static Users of(String userId, String password){
        return new Users(userId,password);
    }

//    // 연관관계
//    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
//    private List<Folders> folders;
}
