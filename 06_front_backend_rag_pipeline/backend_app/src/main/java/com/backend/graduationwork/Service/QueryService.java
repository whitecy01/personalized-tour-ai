package com.backend.graduationwork.Service;

import com.backend.graduationwork.Entity.*;
import com.backend.graduationwork.Entity.Purpose;
import com.backend.graduationwork.Repository.*;
import com.backend.graduationwork.RequestDto.QueryRequest;
import com.backend.graduationwork.RequestDto.TrustScoreUpdateRequest;
import com.backend.graduationwork.ResponseDto.QuerySelectResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Optional;

@Service
public class QueryService {

    @Autowired
    private UserRepository userRepository;
    @Autowired
    private QueryRepository queryRepository;
    @Autowired
    private PurposeRepository purposeRepository;


    public ResponseEntity<QueryRequest> createQuery(QueryRequest request) {
        Users users = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        // 기존 Query 찾기 (user 기준)
        Optional<Query> existingQueryOpt = queryRepository.findByUser(users);

        Query query = existingQueryOpt.orElse(new Query());
        query.setUser(users);
        query.setAge(request.getAge());
        query.setFriendType(request.getFriendType());
        query.setReviewLength(request.getReviewLength());
        query.setReviewCountPreference(request.getReviewCountPreference());
        query.setPhotoPreference(request.getPhotoPreference());
        query.setRecentnessPreference(request.getRecentnessPreference());
        query.setSentimentPreference(request.getSentimentPreference());
        query.setTrustScoreThreshold(request.getTrustScoreThreshold());

        // 1. 여행 목적
        if (query.getPurposes() != null) {
            query.getPurposes().clear();  // 중간 테이블 데이터 제거
        }
        
        List<Purpose> purposes = purposeRepository.findByNameIn(request.getPurposes());
        System.out.println("입력값 : " + request.getPurposes());
        System.out.println("조회된 목적 수: " + purposes.size());
        System.out.println("조회된 목적 목록: " + purposes);

        query.setPurposes(purposes);
        System.out.println("목적 : " + purposes);
        queryRepository.save(query);

        // Python 서버에 요청
        RestTemplate restTemplate = new RestTemplate();
        // 원본 값 (0이면 기본값으로 대체)
        double reviewLength = request.getReviewLength() > 0 ? request.getReviewLength() : 0.2;
        double reviewCount = request.getReviewCountPreference() > 0 ? request.getReviewCountPreference() : 0.3;
        double sentiment = request.getSentimentPreference() > 0 ? request.getSentimentPreference() : 0.25;
        double photo = request.getPhotoPreference() > 0 ? request.getPhotoPreference() : 0.2;
        double recentness = request.getRecentnessPreference() > 0 ? request.getRecentnessPreference() : 0.05;

        // 정규화
        double total = reviewLength + reviewCount + sentiment + photo + recentness;
        double normalizedReviewLength = reviewLength / total;
        double normalizedReviewCount = reviewCount / total;
        double normalizedSentiment = sentiment / total;
        double normalizedPhoto = photo / total;
        double normalizedRecentness = recentness / total;
        System.out.println("정규화 후 가중치:");
        System.out.println("reviewLength = " + normalizedReviewLength);
        System.out.println("reviewCount = " + normalizedReviewCount);
        System.out.println("sentiment = " + normalizedSentiment);
        System.out.println("photo = " + normalizedPhoto);
        System.out.println("recentness = " + normalizedRecentness);

        TrustScoreUpdateRequest updateRequest = new TrustScoreUpdateRequest(
                normalizedReviewLength,
                normalizedReviewCount,
                normalizedSentiment,
                normalizedPhoto,
                normalizedRecentness,
                request.getTrustScoreThreshold()
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<TrustScoreUpdateRequest> entity = new HttpEntity<>(updateRequest, headers);
        System.out.println("API 요청 전");
        try {
            System.out.println("API 요청");
            ResponseEntity<String> response = restTemplate.postForEntity(
//                    "http://fastapi:8000/update-trust-score",
                    "http://fastapi-server:8000/update-trust-score", entity, String.class
            );

            if (response.getStatusCode().is2xxSuccessful()) {
                System.out.println("Python 응답: " + response.getBody());
            } else {
                System.err.println("응답 실패: " + response.getStatusCode());
            }

        } catch (Exception e) {
            System.err.println("Python 서버 호출 실패: " + e.getMessage());
        }




        return ResponseEntity.ok(new QueryRequest(
                request.getUserId(),
                request.getAge(),
                request.getFriendType(),
                request.getPurposes(),
                request.getReviewLength(),
                request.getReviewCountPreference(),
                request.getPhotoPreference(),
                request.getRecentnessPreference(),
                request.getSentimentPreference(),
                request.getTrustScoreThreshold()
        ));
    }

    public ResponseEntity<QuerySelectResponse> getAllQuery(Long userId) {
        Users user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Query query = queryRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Query not found"));

        QuerySelectResponse response = new QuerySelectResponse(
                query.getId(),
                query.getAge(),
                query.getFriendType(),
                query.getPurposes().stream().map(Purpose::getName).toList(),
                query.getReviewLength(),
                query.getReviewCountPreference(),
                query.getPhotoPreference(),
                query.getRecentnessPreference(),
                query.getSentimentPreference(),
                query.getTrustScoreThreshold()
        );
        return ResponseEntity.ok(response);
    }

}