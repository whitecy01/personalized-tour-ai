import { Tabs } from 'expo-router';
import { Image } from 'react-native';

export default function Layout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: '채팅',
          tabBarIcon: ({ color, size }) => (
            <Image source={require('../../assets/images/majesticons_chat-line.png')} style={{ width: size, height: size, tintColor: color }} />
          ),
        }}
      />
      <Tabs.Screen
        name="query"
        options={{
          title: '사전 질의',
          tabBarIcon: ({ color, size }) => (
            <Image source={require('../../assets/images/Group_128.png')} style={{ width: size, height: size, tintColor: color }} />
          ),
        }}
      />
    </Tabs>
  );
}
