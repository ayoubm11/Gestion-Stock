import React from 'react';
import { LineChart } from 'react-native-chart-kit';

export default function HumidityChart() {
  const data = {
    labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
    datasets: [{
      data: [65, 59, 80, 81, 56, 55, 40],
      color: (opacity = 1) => `rgba(0, 128, 0, ${opacity})`,
    }]
  };

  return (
    <LineChart
      data={data}
      width={Dimensions.get('window').width - 32}
      height={220}
      chartConfig={{
        backgroundColor: '#f0f8ff',
        backgroundGradientFrom: '#f0f8ff',
        backgroundGradientTo: '#e0f0e0',
        decimalPlaces: 0,
        color: (opacity = 1) => `rgba(0, 100, 0, ${opacity})`,
      }}
    />
  );
}