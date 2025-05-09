package com.backend.graduationwork.Repository;

import com.backend.graduationwork.Entity.Chatmessage;
import com.backend.graduationwork.Entity.Chatroom;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ChatmessageRepository extends JpaRepository<Chatmessage, Long> {
    List<Chatmessage> findByRoomOrderByCreatedAtAsc(Chatroom room);
}