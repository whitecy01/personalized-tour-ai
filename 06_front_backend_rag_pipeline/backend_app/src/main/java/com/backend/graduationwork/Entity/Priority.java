package com.backend.graduationwork.Entity;

import jakarta.persistence.*;

@Entity
@Table(name = "Priorities")
public class Priority {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
}

