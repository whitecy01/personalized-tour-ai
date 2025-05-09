package com.backend.graduationwork.Controller;

import com.backend.graduationwork.Repository.PurposeRepository;
import com.backend.graduationwork.Repository.QueryRepository;
import com.backend.graduationwork.Repository.UserRepository;
import com.backend.graduationwork.RequestDto.QueryRequest;
import com.backend.graduationwork.ResponseDto.QuerySelectResponse;
import com.backend.graduationwork.Service.QueryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/queries")
public class QueryController {

    @Autowired
    QueryService queryService;
    @PostMapping("/create")
    public ResponseEntity<QueryRequest> createQuery(@RequestBody QueryRequest request) {
        return queryService.createQuery(request);
    }

    @GetMapping("/{userId}")
    public ResponseEntity<QuerySelectResponse> getAllQuery(@PathVariable("userId") Long userId) {
        return queryService.getAllQuery(userId);
    }

}
