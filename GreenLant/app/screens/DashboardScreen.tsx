import React from 'react';
import { View, ScrollView, Text } from 'react-native';
import WeatherWidget from '../components/weather/WeatherWidget';
// ... autres imports

export default function DashboardScreen() {
  return (
    <ScrollView>
      <WeatherWidget />
      
      {/* ... vos autres composants ... */}
    </ScrollView>
  );
}