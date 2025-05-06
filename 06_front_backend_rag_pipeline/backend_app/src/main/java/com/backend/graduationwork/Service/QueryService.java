package com.backend.graduationwork.Service;

import com.backend.graduationwork.Entity.*;
import com.backend.graduationwork.Repository.*;
import com.backend.graduationwork.RequestDto.QueryRequest;
import com.backend.graduationwork.ResponseDto.QuerySelectResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

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

    @Autowired
    private InterestRepository interestRepository;

    @Autowired
    private TasteRepository tasteRepository;

    @Autowired
    private LocationRepository locationRepository;

    @Autowired
    private AmenityRepository amenityRepository;

    public ResponseEntity<QueryRequest> createQuery(QueryRequest request) {
        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        // 기존 Query 찾기 (user 기준)
        Optional<Query> existingQueryOpt = queryRepository.findByUser(user);

        Query query = existingQueryOpt.orElse(new Query());
        query.setUser(user);
        query.setAge(request.getAge());
        query.setGender(request.getGender());
        query.setFriendType(request.getFriendType());
        // 6. 최우선 조건
        query.setPriorities(request.getPriority());

        // 1. 여행 목적
        List<Purpose> purposes = purposeRepository.findByNameIn(request.getPurposes());
        query.setPurposes(purposes);

        // 2. 관심사
        List<Interest> interest = interestRepository.findByNameIn(request.getInterest());
        query.setInterests(interest);

        // 3. 음식 취향
        List<Taste> taste = tasteRepository.findByNameIn(request.getTaste());
        query.setTastes(taste);

        // 4. 방문 희망 지역
        List<Location> location = locationRepository.findByNameIn(request.getLocation());
        query.setLocations(location);

        // 5. 기타 편의 사항
        List<Amenity> amenities = amenityRepository.findByNameIn(request.getAmenity());
        query.setAmenities(amenities);

        queryRepository.save(query);

        return ResponseEntity.ok(new QueryRequest(
                request.getUserId(),
                request.getAge(),
                request.getGender(),
                request.getFriendType(),
                request.getPurposes(),
                request.getInterest(),
                request.getTaste(),
                request.getLocation(),
                request.getAmenity(),
                request.getPriority()
        ));
    }

    public ResponseEntity<QuerySelectResponse> getAllQuery(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Query query = queryRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Query not found"));

        QuerySelectResponse response = new QuerySelectResponse(
                query.getId(),
                query.getAge(),
                query.getGender(),
                query.getFriendType(),
                query.getPurposes().stream().map(Purpose::getName).toList(),
                query.getInterests().stream().map(Interest::getName).toList(),
                query.getTastes().stream().map(Taste::getName).toList(),
                query.getLocations().stream().map(Location::getName).toList(),
                query.getAmenities().stream().map(Amenity::getName).toList(),
                query.getPriorities()
        );
        return ResponseEntity.ok(response);
    }

}