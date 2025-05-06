package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Interest;
import com.backend.graduationwork.Entity.Taste;
import com.backend.graduationwork.Entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface TasteRepository extends JpaRepository<Taste, Long> {
    List<Taste> findByNameIn(List<String> names);
}
