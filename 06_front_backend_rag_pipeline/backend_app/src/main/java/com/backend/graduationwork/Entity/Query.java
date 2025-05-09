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
    private String gender;

    @Column(nullable = false)
    private String friendType;

    @Column(nullable = false)
    private String priorities;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    // 연관관계: N:M 다중 선택 항목들
    //1. 여행 목적
    @ManyToMany
    @JoinTable(
            name = "query_purposes",
            joinColumns = @JoinColumn(name = "query_id"),
            inverseJoinColumns = @JoinColumn(name = "purpose_id")
    )
    private List<Purpose> purposes = new ArrayList<>();

    //2. 관심사
    @ManyToMany
    @JoinTable(
            name = "query_interests",
            joinColumns = @JoinColumn(name = "query_id"),
            inverseJoinColumns = @JoinColumn(name = "interest_id")
    )
    private List<Interest> interests = new ArrayList<>();

    //3. 음식 취향
    @ManyToMany
    @JoinTable(
            name = "query_tastes",
            joinColumns = @JoinColumn(name = "query_id"),
            inverseJoinColumns = @JoinColumn(name = "taste_id")
    )
    private List<Taste> tastes = new ArrayList<>();

    //4. 방문 희망 지역
    @ManyToMany
    @JoinTable(
            name = "query_locations",
            joinColumns = @JoinColumn(name = "query_id"),
            inverseJoinColumns = @JoinColumn(name = "location_id")
    )
    private List<Location> locations = new ArrayList<>();

    //5. 기타 편의 사항
    @ManyToMany
    @JoinTable(
            name = "query_amenities",
            joinColumns = @JoinColumn(name = "query_id"),
            inverseJoinColumns = @JoinColumn(name = "amenity_id")
    )
    private List<Amenity> amenities = new ArrayList<>();

    //6. 최우선 조건
//    @ManyToMany
//    @JoinTable(
//            name = "query_priorities",
//            joinColumns = @JoinColumn(name = "query_id"),
//            inverseJoinColumns = @JoinColumn(name = "priority_id")
//    )

}
