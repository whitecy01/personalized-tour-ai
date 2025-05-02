import { View, Text, StyleSheet } from 'react-native';

export default function QueryHistoryScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>사전 질의 내역 화면</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
});
