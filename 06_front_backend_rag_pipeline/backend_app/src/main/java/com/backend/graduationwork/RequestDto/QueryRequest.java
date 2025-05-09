package com.backend.graduationwork.RequestDto;

import com.backend.graduationwork.Entity.Priority;
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
    private String gender;
    private String age;
    private String friendType;
    private List<String> purposes;
    private List<String> interest;
    private List<String> taste;
    private List<String> location;
    private List<String> amenity;
    private String priority;


    // Getter, Setter
}