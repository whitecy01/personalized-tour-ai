import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator } from 'react-native';
import axios from 'axios';

type QueryResponse = {
  id: number;
  age: string;
  gender: string;
  friendType: string;
  purposes: string[];
  interests: string[];
  tastes: string[];
  locations: string[];
  amenities: string[];
  priorities: string;
};

export default function QueryHistoryScreen() {
  const [queryData, setQueryData] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const userId = 1; // 예: 로그인된 사용자 ID

  useEffect(() => {
    const fetchQueryHistory = async () => {
      try {
        const response = await axios.get<QueryResponse>(
          `http://192.168.1.193:8080/queries/${userId}`
        );
        setQueryData(response.data);
      } catch (error) {
        console.error('데이터 불러오기 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchQueryHistory();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#7dbdf5" />
      </View>
    );
  }

  if (!queryData) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>데이터가 없습니다.</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>사전 질의 내역</Text>
      <Text>나이: {queryData.age}</Text>
      <Text>성별: {queryData.gender}</Text>
      <Text>동행 유형: {queryData.friendType}</Text>

      <Section title="여행 목적" data={queryData.purposes} />
      <Section title="관심사" data={queryData.interests} />
      <Section title="음식 취향" data={queryData.tastes} />
      <Section title="방문 희망 지역" data={queryData.locations} />
      <Section title="기타 편의 사항" data={queryData.amenities} />
      <Section title="최우선 조건" data={[queryData.priorities]} />
    </View>
  );
}

function Section({ title, data }: { title: string; data: string[] }) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {data.length === 0 ? (
        <Text>선택 없음</Text>
      ) : (
        <FlatList
          data={data}
          keyExtractor={(item, index) => `${item}-${index}`}
          renderItem={({ item }) => <Text>- {item}</Text>}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  section: { marginTop: 15 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 5 },
});


// import { View, Text, StyleSheet } from 'react-native';

// export default function QueryHistoryScreen() {
//   return (
//     <View style={styles.container}>
//       <Text style={styles.title}>사전 질의 내역 화면</Text>
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
//   title: { fontSize: 24, fontWeight: 'bold' },
// });
