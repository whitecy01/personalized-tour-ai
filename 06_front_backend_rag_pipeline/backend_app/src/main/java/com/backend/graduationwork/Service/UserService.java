package com.backend.graduationwork.Service;

import com.backend.graduationwork.Entity.User;
import com.backend.graduationwork.Repository.UserRepository;
import com.backend.graduationwork.RequestDto.SignupRequest;
import com.backend.graduationwork.ResponseDto.MessageResponse;
import com.backend.graduationwork.ResponseDto.UserResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.Optional;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public ResponseEntity<UserResponse> Signup(@RequestBody SignupRequest signupRequest){
        User user = User.of(signupRequest.getUserId(), signupRequest.getPassword());
        userRepository.save(user);

        UserResponse userResponse = new UserResponse(user.getId(), user.getUserId(), user.getPassword());
        return ResponseEntity.ok(userResponse);
    }

    public ResponseEntity<Object> Signin(@RequestBody SignupRequest signupRequest){
        Optional<User> optionalUser = userRepository.findByUserIdAndPassword(
                signupRequest.getUserId(),
                signupRequest.getPassword()
        );

        if (optionalUser.isPresent()) {
            User user = optionalUser.get();
            UserResponse response = new UserResponse(user.getId(), user.getUserId(), user.getPassword());
            return ResponseEntity.ok(response);
        }

        MessageResponse errorResponse = new MessageResponse(404, "로그인 실패");
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorResponse);
    }
}
