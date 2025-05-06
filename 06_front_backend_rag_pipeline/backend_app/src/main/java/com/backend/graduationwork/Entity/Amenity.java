package com.backend.graduationwork.Entity;

import jakarta.persistence.*;
import lombok.Getter;

@Entity
@Table(name = "amenities")
@Getter
public class Amenity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
}
