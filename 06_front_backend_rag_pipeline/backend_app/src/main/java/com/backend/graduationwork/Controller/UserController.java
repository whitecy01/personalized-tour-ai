package com.backend.graduationwork.Controller;

import com.backend.graduationwork.RequestDto.SignupRequest;
import com.backend.graduationwork.ResponseDto.UserResponse;
import com.backend.graduationwork.Service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {

    private UserService userService;

    @GetMapping("/ping")
    public String ping() {
        return "pong";
    }


    @PostMapping("/signup")
    public ResponseEntity<UserResponse> Signup(@RequestBody SignupRequest signupRequest){
        return userService.Signup(signupRequest);
    }

    @PostMapping("/signin")
    public ResponseEntity<Object> Signin(@RequestBody SignupRequest signupRequest){
        return userService.Signin(signupRequest);
    }

}

