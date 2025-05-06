package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Amenity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AmenityRepository extends JpaRepository<Amenity, Long> {
    List<Amenity> findByNameIn(List<String> names);
}
