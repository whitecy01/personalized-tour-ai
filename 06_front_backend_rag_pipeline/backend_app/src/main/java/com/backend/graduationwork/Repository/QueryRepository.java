package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Query;
import com.backend.graduationwork.Entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface QueryRepository extends JpaRepository<Query, Long> {
    Optional<Query> findByUser(User user);
}
