package com.backend.graduationwork.ResponseDto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class MessageResponse {
    private int code;
    private String message;
}
