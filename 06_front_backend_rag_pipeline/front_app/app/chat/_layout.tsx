import { Stack } from 'expo-router';
import React from 'react';

export default function ChatLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="[roomId]"
        options={{
          title: '채팅방',
          headerShown: false, // ← 헤더를 보여줘야 뒤로가기 버튼도 나옵니다
          headerBackTitle: '목록으로', // ← 뒤로가기 버튼 이름 지정
        }}
      />
    </Stack>
  );
}
