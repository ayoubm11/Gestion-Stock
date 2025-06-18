import { Stack } from 'expo-router';

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen 
        name="index" 
        options={{ title: 'Tableau de Bord' }} 
      />
      <Stack.Screen 
        name="about" 
        options={{ title: 'Fonctionnement' }} 
      />
      <Stack.Screen 
        name="settings" 
        options={{ title: 'Paramètres' }} 
      />
    </Stack>
  );
}