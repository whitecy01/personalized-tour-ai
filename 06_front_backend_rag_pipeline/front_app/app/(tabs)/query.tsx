import { useRouter } from 'expo-router';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function QueryMainScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>

      <TouchableOpacity style={styles.button} onPress={() => router.navigate('/query_detail/new')}>
        <Text style={styles.buttonText}>사전 질의 하기</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={() => router.push('/query_detail/history')}>
        <Text style={styles.buttonText}>사전 질의 내역 확인하기</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 30 },
  button: {
    backgroundColor: '#4db8ff',
    paddingVertical: 12,
    paddingHorizontal: 30,
    borderRadius: 8,
    marginVertical: 10,
    width: '80%',
    alignItems: 'center',
  },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
});
