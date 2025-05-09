package com.backend.graduationwork.Controller;

import com.backend.graduationwork.Entity.Chatmessage;
import com.backend.graduationwork.RequestDto.ChatmessageRequest;
import com.backend.graduationwork.ResponseDto.ChatmessageLLMRequest;
import com.backend.graduationwork.ResponseDto.ChatroomResponse;
import com.backend.graduationwork.Service.ChatService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
public class ChatController {

    @Autowired
    private ChatService chatService;

    @PostMapping("/send")
    public ResponseEntity<ChatmessageLLMRequest> sendMessage(
            @RequestBody ChatmessageRequest chatmessageRequest
            ) {
        return chatService.sendMessage(chatmessageRequest.getRoomId(), chatmessageRequest.getUserId(), chatmessageRequest.getMessage());
    }

    //채팅방 전체 조회
    @GetMapping("/{userId}/rooms")
    public ResponseEntity<List<ChatroomResponse>> getUserChatrooms(@PathVariable("userId") Long userId) {
        return chatService.getUserChatrooms(userId);
    }

    //채팅방의 메시지들 반환
    @GetMapping("/{roomId}")
    public ResponseEntity<List<Chatmessage>> getMessages(@PathVariable("roomId") Long roomId) {
        return chatService.getChatMessages(roomId);
    }

    //채팅방 만들기
    @PostMapping("/{userId}")
    public ResponseEntity<ChatroomResponse> createChatroom(@PathVariable("userId") Long userId) {
        return chatService.createChatroom(userId);
    }
}
