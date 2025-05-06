package com.backend.graduationwork.DTO;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class QueryRequest {
    private Long userId;
    private String queryText;
    private List<Long> purposes;  // 선택된 Purpose ID 리스트

    // Getter, Setter
}