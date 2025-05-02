import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function ChatListScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>채팅 목록</Text>

      <View style={styles.card}>
        <Text style={styles.date}>11월 8일(금)</Text>
        <Text style={styles.cardTitle}>크림 빵집 추천</Text>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>채팅하기</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.card}>
        <Text style={styles.date}>12월 9일(화)</Text>
        <Text style={styles.cardTitle}>부산 관광 추천</Text>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>채팅하기</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
    paddingHorizontal: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
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
  date: {
    fontSize: 14,
    color: '#999',
    marginBottom: 5,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  button: {
    borderWidth: 1,
    borderColor: '#ccc',
    paddingVertical: 10,
    borderRadius: 6,
    alignItems: 'center',
  },
  buttonText: {
    fontSize: 16,
    color: '#333',
  },
});

