package com.backend.graduationwork.Service;

import com.backend.graduationwork.Entity.*;
import com.backend.graduationwork.Repository.ChatmessageRepository;
import com.backend.graduationwork.Repository.ChatroomRepository;
import com.backend.graduationwork.Repository.QueryRepository;
import com.backend.graduationwork.Repository.UserRepository;
import com.backend.graduationwork.ResponseDto.ChatmessageLLMRequest;
import com.backend.graduationwork.ResponseDto.ChatroomResponse;
import com.backend.graduationwork.ResponseDto.QuerySelectResponse;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class ChatService {
    @Autowired
    private ChatmessageRepository chatmessageRepository;

    @Autowired
    private ChatroomRepository chatroomRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private QueryRepository queryRepository;

    public ResponseEntity<ChatmessageLLMRequest> sendMessage(Long roomId, Long userId, String messageText) {
        Chatroom room = chatroomRepository.findById(roomId).orElseThrow();
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        // 사용자 메시지 저장
        Chatmessage userMsg = new Chatmessage();
        userMsg.setRoom(room);
        userMsg.setUser(user);
        userMsg.setSender("USER");
        userMsg.setMessage(messageText);
        chatmessageRepository.save(userMsg);

        // LLM에 메시지 전송 후 응답 받기
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
        ObjectMapper mapper = new ObjectMapper();
        try {
            String json = mapper.writeValueAsString(response);
            System.out.println("[QuerySelectResponse] " + json);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }




//        String llmResponse = callLLM(messageText);
        String llmResponse = callLLM(response, messageText);

        // BOT 메시지 저장
        Chatmessage botMsg = new Chatmessage();
        botMsg.setUser(user);
        botMsg.setRoom(room);
        botMsg.setSender("BOT");
        botMsg.setMessage(llmResponse);
        chatmessageRepository.save(botMsg);

        // 전체 메시지 반환
        ChatmessageLLMRequest chatmessageLLMRequest = new ChatmessageLLMRequest(roomId, userId, messageText, llmResponse);
        return ResponseEntity.ok(chatmessageLLMRequest);
    }

//    private String callLLM(String prompt) {
//        // 실제 LLM 호출 로직 (예: OpenAI API 호출)
//        return "임시 응답: " + prompt + "에 대한 답변입니다.";
//    }

    private String callLLM(QuerySelectResponse response, String userMessage) {
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // request body 생성
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("survey", response);
        requestBody.put("message", userMessage);

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

        // Python API 호출
        ResponseEntity<Map> responseEntity = restTemplate.exchange(
                "http://localhost:8000/llm-recommend",  // Python 서버 주소
                HttpMethod.POST,
                entity,
                Map.class
        );

        // 응답에서 "response" 키의 값 가져오기
        Map<String, Object> responseBody = responseEntity.getBody();
        return (String) responseBody.get("response");
    }



    public ResponseEntity<List<ChatroomResponse>> getUserChatrooms(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("사용자를 찾을 수 없습니다."));

        List<Chatroom> rooms = chatroomRepository.findByUser(user);

        return ResponseEntity.ok(rooms.stream()
                .map(room -> new ChatroomResponse(room.getId(), room.getName(), room.getCreatedAt()))
                .collect(Collectors.toList()));
    }

    public ResponseEntity<List<Chatmessage>> getChatMessages(Long roomId) {
        Chatroom room = chatroomRepository.findById(roomId)
                .orElseThrow(() -> new RuntimeException("채팅방이 존재하지 않습니다."));

        List<Chatmessage> messages = chatmessageRepository.findByRoomOrderByCreatedAtAsc(room);

        return ResponseEntity.ok(messages);
    }

    //채팅방 생성
    public ResponseEntity<ChatroomResponse> createChatroom(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("사용자를 찾을 수 없습니다."));

        Chatroom chatroom = new Chatroom();
        chatroom.setName("새로운 채팅방");  // 기본 이름, 필요 시 프론트에서 받아도 OK
        chatroom.setUser(user);  // 사용자 연결

        Chatroom savedRoom = chatroomRepository.save(chatroom);

        return ResponseEntity.ok(new ChatroomResponse(savedRoom.getId(), savedRoom.getName(), savedRoom.getCreatedAt()));
    }


}
