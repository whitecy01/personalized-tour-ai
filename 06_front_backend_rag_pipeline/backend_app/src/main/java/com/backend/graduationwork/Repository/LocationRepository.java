package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Location;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LocationRepository extends JpaRepository<Location, Long> {
    List<Location> findByNameIn(List<String> names);
}
