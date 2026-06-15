package com.backend.graduationwork.ResponseDto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
public class QuerySelectResponse {
    private Long queryId;
    private String age;
    private String friendType;
    private List<String> purposes;
    private Long reviewLength;
    private Long reviewCountPreference;
    private Long photoPreference;
    private Long recentnessPreference;
    private Long sentimentPreference;
    private double trustScoreThreshold;

    // 생성자, getter, setter 작성
}
