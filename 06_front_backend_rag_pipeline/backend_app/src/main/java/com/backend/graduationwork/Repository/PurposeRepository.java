package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Purpose;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository

public interface PurposeRepository extends JpaRepository<Purpose, Long> {
    List<Purpose> findByNameIn(List<String> names);
}

