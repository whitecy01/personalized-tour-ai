import { Stack } from 'expo-router';

export default function QueryDetailsLayout() {
  return (
    <Stack screenOptions={{ title: '바꾸기', headerBackTitle: '뒤로가기' }}>
      <Stack.Screen name="new" options={{ 
        headerShown: false, 
        headerTitle: '바꾸기',
        headerBackTitle: '뒤로가기',

        }}  />
      {/* <Stack.Screen name="history" options={{ title: '사전 질의 내역' }} /> */}
      <Stack.Screen name="history" options={{ headerShown: false }}  />
    </Stack>
  );
}
