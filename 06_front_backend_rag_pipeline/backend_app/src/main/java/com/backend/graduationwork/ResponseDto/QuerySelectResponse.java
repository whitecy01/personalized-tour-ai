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
    private String gender;
    private String friendType;
    private List<String> purposes;
    private List<String> interests;
    private List<String> tastes;
    private List<String> locations;
    private List<String> amenities;
    private String priorities;

    // 생성자, getter, setter 작성
}
