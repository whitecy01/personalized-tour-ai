import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  Linking,
} from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import axios from 'axios';

type ChatMessage = {
  id: string;
  text: string;
  sender: 'user' | 'bot';
};

export default function ChatRoomScreen() {
  const { roomId } = useLocalSearchParams();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(true);
  const userId = 1; // 임시 userId

  // BOT 메시지 파싱 함수
  const renderBotMessage = (message: string) => {
    const lines = message.split('\n');

    return lines.map((line, index) => {
      const trimmed = line.trim();

      // 리뷰 제목과 링크 추출
      const match = trimmed.match(/-\s?\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/);
      if (match) {
        const label = match[1];
        const url = match[2];
        return (
          <TouchableOpacity key={index} onPress={() => Linking.openURL(url)}>
            <Text style={{ color: 'blue', textDecorationLine: 'underline', marginBottom: 4 }}>
              - {label}
            </Text>
          </TouchableOpacity>
        );
      }

      // 마지막에 [리뷰 페이지](링크) 형태 처리
      const lastLink = trimmed.match(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)$/);
      if (lastLink) {
        const label = lastLink[1];
        const url = lastLink[2];
        return (
          <TouchableOpacity key={index} onPress={() => Linking.openURL(url)}>
            <Text style={{ color: 'blue', textDecorationLine: 'underline', marginBottom: 4 }}>
            {'   -'} 리뷰 링크로 이동하기
            </Text>
          </TouchableOpacity>
        );
      }

      return (
        <Text key={index} style={{ marginBottom: 4 }}>
          {line}
        </Text>
      );
    });
  };

  // 메시지 불러오기
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get(`http://52.78.195.74:8080/api/chat/${roomId}`);
        const loadedMessages = response.data.map((msg: any) => ({
          id: msg.id.toString(),
          text: msg.message,
          sender: msg.sender.toLowerCase() as 'user' | 'bot',
        }));
        setMessages(loadedMessages);
        console.log('불러온 메시지:', loadedMessages);
      } catch (error) {
        console.error('메시지 불러오기 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMessages();
  }, [roomId]);

  // 메시지 전송
  const handleSend = async () => {
    if (inputText.trim() === '') return;

    try {
      const response = await axios.post(`http://52.78.195.74:8080/api/chat/send`, {
        roomId: Number(roomId),
        userId: userId,
        message: inputText,
      });

      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        text: response.data.userMessage,
        sender: 'user',
      };

      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: response.data.botMessage,
        sender: 'bot',
      };

      setMessages([...messages, userMessage, botMessage]);
      setInputText('');
      console.log('전송 후 메시지 추가:', userMessage, botMessage);
    } catch (error) {
      console.error('메시지 전송 실패:', error);
    }
  };

  if (loading) {
    return (
      <View style={styles.centeredContainer}>
        <ActivityIndicator size="large" color="#007bff" />
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={90}
    >
      <FlatList
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View
            style={[
              styles.messageBubble,
              item.sender === 'user' ? styles.userBubble : styles.botBubble,
            ]}
          >
            {item.sender === 'bot' ? renderBotMessage(item.text) : <Text>{item.text}</Text>}
          </View>
        )}
        contentContainerStyle={{ padding: 16 }}
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="메시지를 입력하세요"
          value={inputText}
          onChangeText={setInputText}
        />
        <TouchableOpacity style={styles.sendButton} onPress={handleSend}>
          <Text style={styles.sendButtonText}>전송</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  centeredContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  messageBubble: {
    padding: 10,
    marginBottom: 10,
    borderRadius: 10,
    maxWidth: '80%',
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#e1f5fe',
  },
  botBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#f1f1f1',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 8,
    borderTopWidth: 1,
    borderColor: '#ddd',
    backgroundColor: '#fff',
    marginBottom: 10,
  },
  input: {
    flex: 1,
    height: 40,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 20,
  },
  sendButton: {
    backgroundColor: '#007bff',
    paddingHorizontal: 16,
    justifyContent: 'center',
    borderRadius: 20,
    marginLeft: 8,
  },
  sendButtonText: { color: '#fff', fontWeight: 'bold' },
});



