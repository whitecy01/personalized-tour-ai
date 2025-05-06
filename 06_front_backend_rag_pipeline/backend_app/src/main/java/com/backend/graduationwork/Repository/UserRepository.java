package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    // userId와 password가 일치하는 사용자 찾기
    Optional<User> findByUserIdAndPassword(String userId, String password);
}
