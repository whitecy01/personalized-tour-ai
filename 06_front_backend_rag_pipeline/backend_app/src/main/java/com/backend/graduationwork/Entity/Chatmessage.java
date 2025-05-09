package com.backend.graduationwork.Entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "chatmessage")
@Setter
@Getter
public class Chatmessage {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String sender;  // "USER" or "BOT" → 누가 보냈는지 구분

    @Column(columnDefinition = "TEXT", nullable = false)
    private String message;

    @Column(nullable = false)
    @CreationTimestamp
    private LocalDateTime createdAt;

    @ManyToOne
    @JoinColumn(name = "room_id")
    private Chatroom room;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;  // 메시지 보낸 사용자


}
