package com.backend.graduationwork.ResponseDto;


import lombok.AllArgsConstructor;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@AllArgsConstructor
public class ChatroomResponse {
    private Long id;
    private String name;
    private LocalDateTime createdAt;
}