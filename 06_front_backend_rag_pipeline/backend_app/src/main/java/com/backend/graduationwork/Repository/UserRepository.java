package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Users;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<Users, Long> {
    // userId와 password가 일치하는 사용자 찾기
    Optional<Users> findByUserIdAndPassword(String userId, String password);
}
