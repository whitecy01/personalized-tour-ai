package com.backend.graduationwork.RequestDto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class ChatmessageRequest {
    private Long roomId;

    private Long userId;

    private String message;
}
