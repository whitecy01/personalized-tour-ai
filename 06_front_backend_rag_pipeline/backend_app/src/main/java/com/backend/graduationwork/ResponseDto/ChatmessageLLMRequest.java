package com.backend.graduationwork.ResponseDto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class ChatmessageLLMRequest {
    private Long roomId;

    private Long userId;

    private String userMessage;

    private String botMessage;
}
