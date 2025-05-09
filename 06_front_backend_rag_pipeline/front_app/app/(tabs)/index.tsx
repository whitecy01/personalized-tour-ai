// import React, { useState } from 'react';
// import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
// import { useRouter } from 'expo-router';
// import dayjs from 'dayjs';

// type Room = {
//   id: number;
//   title: string;
//   date: string;
// };

// export default function ChatListScreen() {
//   const router = useRouter();
//   // const [rooms, setRooms] = useState<Room[]>([]);
//   const [rooms, setRooms] = useState([
//     { id: 1, title: '크림 빵집 추천', date: '11월 8일(금) 14:30' },
//     { id: 2, title: '부산 관광 추천', date: '12월 9일(화) 09:15' },
//   ]);
  

//   const createNewRoom = () => {
//     const newId = rooms.length + 1;
//     // const dateStr = dayjs().format('YYYY-MM-DD HH:mm:ss');
//     const now = new Date();
//     const hours = now.getHours().toString().padStart(2, '0');
//     const minutes = now.getMinutes().toString().padStart(2, '0');

//     const dateStr = `${now.getMonth() + 1}월 ${now.getDate()}일(${['일', '월', '화', '수', '목', '금', '토'][now.getDay()]}) ${hours}:${minutes}`;
//     const newRoom: Room = { id: newId, title: `새 채팅방 ${newId}`, date: dateStr };
//     setRooms([...rooms, newRoom]);
//     router.push(`/chat/${newId}`);
//   };

//   return (
//     <View style={styles.container}>
//       <Text style={styles.title}>채팅 목록</Text>

//       <FlatList
//         data={rooms}
//         keyExtractor={(item) => item.id.toString()}
//         renderItem={({ item }) => (
//           <View style={styles.card}>
//             <Text style={styles.date}>{item.date}</Text>
//             <Text style={styles.cardTitle}>{item.title}</Text>
//             <TouchableOpacity
//               style={styles.button}
//               onPress={() => router.push(`/chat/${item.id}`)}
//             >
//               <Text style={styles.buttonText}>채팅하기</Text>
//             </TouchableOpacity>
//           </View>
//         )}
//       />

//       <TouchableOpacity style={styles.fab} onPress={createNewRoom}>
//         <Text style={styles.fabText}>+</Text>
//       </TouchableOpacity>
//     </View>
//   );
// }

import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import axios from 'axios';

type Room = {
  id: number;
  title: string;
  date: string;
};

export default function ChatListScreen() {
  const router = useRouter();
  const [rooms, setRooms] = useState<Room[]>([]);
  const userId = 1;  // 사용자 ID (로그인 구현 시 dynamic하게)

  // 처음에 서버에서 사용자의 채팅방 목록 불러오기
  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await axios.get(`http://192.168.1.193:8080/api/chat/${userId}/rooms`);
        
        const formattedRooms: Room[] = response.data.map((item: any) => ({
          id: item.id,
          title: item.name,
          date: formatDate(item.createdAt),
        }));
  
        setRooms(formattedRooms);
        console.log('서버에서 변환된 rooms:', formattedRooms);
      } catch (error) {
        console.error('채팅방 불러오기 실패:', error);
      }
    };
    fetchRooms();
  }, []);
  


  // 새로운 채팅방 생성
  const createNewRoom = async () => {
    try {
      const response = await axios.post(`http://192.168.1.193:8080/api/chat/${userId}`);
  
      const newRoom: Room = {
        id: response.data.id,
        title: response.data.name,
        date: formatDate(response.data.createdAt),
      };
  
      setRooms([...rooms, newRoom]);
      router.push(`/chat/${newRoom.id}`);
      console.log('새 채팅방 생성:', newRoom);
    } catch (error) {
      console.error('채팅방 생성 실패:', error);
    }
  };
  
  const formatDate = (createdAt: string) => {
    const date = new Date(createdAt);
    const dayNames = ['일', '월', '화', '수', '목', '금', '토'];
    const day = dayNames[date.getDay()];
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const dayOfMonth = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
  
    return `${month}월 ${dayOfMonth}일(${day}) ${hour}:${minute}`;
  };
  

  return (
    <View style={styles.container}>
      <Text style={styles.title}>채팅 목록</Text>

      <FlatList
        data={rooms}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.date}>{item.date}</Text>
            <Text style={styles.cardTitle}>{item.title}</Text>
            <TouchableOpacity
              style={styles.button}
              onPress={() => router.push(`/chat/${item.id}`)}
            >
              <Text style={styles.buttonText}>채팅하기</Text>
            </TouchableOpacity>
          </View>
        )}
      />

      <TouchableOpacity style={styles.fab} onPress={createNewRoom}>
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>
    </View>
  );
}


const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f5f5f5' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  card: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 15,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
    elevation: 3,
  },
  date: { fontSize: 14, color: '#999', marginBottom: 5 },
  cardTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 15 },
  button: {
    borderWidth: 1,
    borderColor: '#ccc',
    paddingVertical: 10,
    borderRadius: 6,
    alignItems: 'center',
  },
  buttonText: { fontSize: 16, color: '#333' },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 30,
    backgroundColor: '#007bff',
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
  },
  fabText: { color: '#fff', fontSize: 30, lineHeight: 30 },
});
