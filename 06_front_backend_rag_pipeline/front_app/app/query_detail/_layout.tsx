import { Stack } from 'expo-router';

export default function QueryDetailsLayout() {
  return (
    <Stack screenOptions={{ title: '사전 질의', headerBackTitle: '뒤로가기' }}>
      <Stack.Screen name="new" options={{ 
        headerShown: false, 
        headerTitle: '사전 질의하기',
        headerBackTitle: '뒤로가기',

        }}  />
      {/* <Stack.Screen name="history" options={{ title: '사전 질의 내역' }} /> */}
      <Stack.Screen name="history" options={{ 
        headerShown: false,
        headerTitle: '사전 질의 내역'
        }}  />
    </Stack>
  );
}
