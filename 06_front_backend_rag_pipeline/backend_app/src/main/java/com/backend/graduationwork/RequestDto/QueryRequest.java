package com.backend.graduationwork.RequestDto;

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
    private String age;
    private String friendType;
    private List<String> purposes;
    private Long reviewLength;
    private Long reviewCountPreference;
    private Long photoPreference;
    private Long recentnessPreference;
    private Long sentimentPreference;
    private double trustScoreThreshold;


//    private List<String> interest;
//    private List<String> taste;
//    private List<String> location;
//    private List<String> amenity;
//    private String priority;


    // Getter, Setter
}