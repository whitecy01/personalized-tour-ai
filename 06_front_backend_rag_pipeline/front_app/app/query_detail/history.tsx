import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator } from 'react-native';
import axios from 'axios';

type QueryResponse = {
  queryId: number;
  age: string;
  friendType: string;
  reviewLength: number;
  reviewCountPreference: number;
  photoPreference: number;
  recentnessPreference: number;
  sentimentPreference: number;
  trustScoreThreshold: number;
  purposes: string[];
};
const EN_TO_KO_PURPOSE: { [key: string]: string } = {
  'Relaxation': '휴식',
  'Cultural Experience': '문화체험',
  'Food Tour': '맛집탐방',
  'Shopping': '쇼핑',
  'Photography': '사진',
  'Healing': '힐링',
};


export default function QueryHistoryScreen() {
  const [queryData, setQueryData] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const userId = 1; // 예: 로그인된 사용자 ID
  

  useEffect(() => {
    const fetchQueryHistory = async () => {
      try {
        const response = await axios.get<QueryResponse>(
          `http://52.78.195.74:8080/queries/${userId}`
        );
        console.log(response.data)

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
    const reviewLengthMap = ['없음', '짧고 간결한 리뷰', '적당한 길이의 리뷰', '자세하고 길게 작성된 리뷰'];
  const reviewCountMap = ['없음', '상관없음', '리뷰 수가 적어도 내용이 좋다면 신뢰함', '리뷰를 많이 작성한 사용자'];
  const photoMap = ['없음', '아니오', '예'];
  const recentnessMap = ['없음', '오래된 리뷰도 상관없다', '그렇다'];
  const sentimentMap = ['없음', '아니다', '중립적이다', '그렇다'];


  return (
    <View style={styles.container}>
      <Text style={styles.title}>사전 질의 내역</Text>
      <Text>나이: {queryData.age}</Text>
      <Text>동행 유형: {queryData.friendType}</Text>

      <Section title="여행 목적" data={queryData.purposes} />

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>개인화 질문 응답</Text>
        <View style={styles.itemRow}>
          <Text style={styles.bullet}>•</Text>
          <Text style={styles.itemLabel}>리뷰 길이 선호:</Text>
          <Text style={styles.itemValue}>{reviewLengthMap[queryData.reviewLength]}</Text>
        </View>
        <View style={styles.itemRow}>
          <Text style={styles.bullet}>•</Text>
          <Text style={styles.itemLabel}>리뷰 작성자 활동성:</Text>
          <Text style={styles.itemValue}>{reviewCountMap[queryData.reviewCountPreference]}</Text>
        </View>
        <View style={styles.itemRow}>
          <Text style={styles.bullet}>•</Text>
          <Text style={styles.itemLabel}>사진 포함 여부:</Text>
          <Text style={styles.itemValue}>{photoMap[queryData.photoPreference]}</Text>
        </View>
        <View style={styles.itemRow}>
          <Text style={styles.bullet}>•</Text>
          <Text style={styles.itemLabel}>리뷰 최신성:</Text>
          <Text style={styles.itemValue}>{recentnessMap[queryData.recentnessPreference]}</Text>
        </View>
        <View style={styles.itemRow}>
          <Text style={styles.bullet}>•</Text>
          <Text style={styles.itemLabel}>긍정 리뷰 선호도:</Text>
          <Text style={styles.itemValue}>{sentimentMap[queryData.sentimentPreference]}</Text>
        </View>
        <View style={styles.itemRow}>
          <Text style={styles.bullet}>•</Text>
          <Text style={styles.itemLabel}>신뢰 점수 기준:</Text>
          <Text style={styles.itemValue}>{Math.round(queryData.trustScoreThreshold * 100)}%</Text>
        </View>
      </View>

    </View>
  );
}

function Section({ title, data }: { title: string; data: string[] }) {
  const translated = data.map(item => EN_TO_KO_PURPOSE[item] || item);

  // return (
  //   <View style={styles.section}>
  //     <Text style={styles.sectionTitle}>{title}</Text>
  //     {data.length === 0 ? (
  //       <Text>선택 없음</Text>
  //     ) : (
  //       <FlatList
  //         data={data}
  //         keyExtractor={(item, index) => `${item}-${index}`}
  //         renderItem={({ item }) => <Text>- {item}</Text>}
  //       />
  //     )}
  //   </View>
  // );
    return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {translated.length === 0 ? (
        <Text>선택 없음</Text>
      ) : (
        <FlatList
          data={translated}
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
  itemRow: {
  flexDirection: 'row',
  alignItems: 'center',
  marginBottom: 6,
  flexWrap: 'wrap',
  },
  bullet: {
    fontSize: 16,
    marginRight: 6,
    color: '#7dbdf5',
  },
  itemLabel: {
    fontSize: 15,
    fontWeight: '600',
    marginRight: 4,
    color: '#333',
  },
  itemValue: {
    fontSize: 15,
    color: '#555',
  },
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
