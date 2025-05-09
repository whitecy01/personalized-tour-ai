package com.backend.graduationwork.Entity;

import jakarta.persistence.*;
import lombok.Getter;

@Entity
@Table(name = "interest")
@Getter
public class Interest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
}
