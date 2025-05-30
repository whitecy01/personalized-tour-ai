package com.backend.graduationwork.ResponseDto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Setter
@Getter
@AllArgsConstructor
public class LLMQueryRequest {
    private Long queryId;
    private String age;
    private String friendType;
    private List<String> purposes;
}
