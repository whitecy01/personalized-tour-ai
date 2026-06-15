package com.backend.graduationwork.Entity;

import jakarta.persistence.*;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@Setter
@Table(name = "queries")
public class Query {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String age;

    @Column(nullable = false)
    private String friendType;

    //리뷰 길이
    @Column(nullable = false)
    private Long reviewLength = 0L;

    //리뷰 작성자 활동적
    @Column(nullable = false)
    private Long reviewCountPreference = 0L;

    //사진 유무
    @Column(nullable = false)
    private Long photoPreference = 0L;

    //리뷰 최신성
    @Column(nullable = false)
    private Long recentnessPreference = 0L;

    //긍정적 리뷰 선호
    @Column(nullable = false)
    private Long sentimentPreference = 0L;

    //신뢰도 필터 기준
    @Column(nullable = false)
    private double trustScoreThreshold = 0L;




    @ManyToOne
    @JoinColumn(name = "user_id")
    private Users user;


//    @Column(nullable = false)
//    private String gender;


//    @Column(nullable = false)
//    private String priorities;

    // 연관관계: N:M 다중 선택 항목들
//    //1. 여행 목적
    @ManyToMany
    @JoinTable(
            name = "query_purposes",
            joinColumns = @JoinColumn(name = "query_id"),
            inverseJoinColumns = @JoinColumn(name = "purpose_id")
    )
    private List<Purpose> purposes = new ArrayList<>();



//
//    //2. 관심사
//    @ManyToMany
//    @JoinTable(
//            name = "query_interests",
//            joinColumns = @JoinColumn(name = "query_id"),
//            inverseJoinColumns = @JoinColumn(name = "interest_id")
//    )
//    private List<Interest> interests = new ArrayList<>();
//
//    //3. 음식 취향
//    @ManyToMany
//    @JoinTable(
//            name = "query_tastes",
//            joinColumns = @JoinColumn(name = "query_id"),
//            inverseJoinColumns = @JoinColumn(name = "taste_id")
//    )
//    private List<Taste> tastes = new ArrayList<>();
//
//    //4. 방문 희망 지역
//    @ManyToMany
//    @JoinTable(
//            name = "query_locations",
//            joinColumns = @JoinColumn(name = "query_id"),
//            inverseJoinColumns = @JoinColumn(name = "location_id")
//    )
//    private List<Location> locations = new ArrayList<>();


}
