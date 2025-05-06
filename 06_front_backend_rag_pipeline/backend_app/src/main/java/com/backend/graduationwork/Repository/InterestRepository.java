package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Interest;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;



@Repository
public interface InterestRepository extends JpaRepository<Interest, Long> {
    List<Interest> findByNameIn(List<String> names);
}
