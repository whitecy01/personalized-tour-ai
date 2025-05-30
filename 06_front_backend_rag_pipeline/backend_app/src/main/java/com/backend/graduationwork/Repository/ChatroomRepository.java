package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Chatroom;
import com.backend.graduationwork.Entity.Users;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;


public interface ChatroomRepository extends JpaRepository<Chatroom, Long> {
    List<Chatroom> findByUser(Users user);
}