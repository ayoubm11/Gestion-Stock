import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { getWeatherForecast } from '../../services/weatherService';

// Mappage des icônes météo aux emojis
const weatherIcons: Record<string, string> = {
  '01d': '☀️', // soleil
  '01n': '🌙', // lune
  '02d': '⛅', // peu nuageux jour
  '02n': '⛅', // peu nuageux nuit
  '03d': '☁️', // nuageux
  '03n': '☁️', // nuageux
  '04d': '☁️', // très nuageux
  '04n': '☁️', // très nuageux
  '09d': '🌧️', // pluie
  '09n': '🌧️', // pluie
  '10d': '🌦️', // pluie légère
  '10n': '🌦️', // pluie légère
  '11d': '⛈️', // orage
  '11n': '⛈️', // orage
  '13d': '❄️', // neige
  '13n': '❄️', // neige
  '50d': '🌫️', // brouillard
  '50n': '🌫️', // brouillard
};

const WeatherWidget = () => {
  const [weather, setWeather] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWeather = async () => {
      const data = await getWeatherForecast('Paris'); // Remplacez par votre ville
      setWeather(data);
      setLoading(false);
    };
    
    fetchWeather();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <Text>Chargement météo...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Météo Actuelle</Text>
      </View>
      
      <View style={styles.weatherInfo}>
        <Text style={styles.weatherIcon}>
          {weatherIcons[weather.icon] || '🌡️'}
        </Text>
        
        <View style={styles.weatherDetails}>
          <Text style={styles.temperature}>{weather.temp}°C</Text>
          <Text style={styles.description}>{weather.description}</Text>
        </View>
      </View>
      
      {weather.willRain ? (
        <View style={styles.rainWarning}>
          <Text style={styles.warningText}>🌧️ Pluie prévue demain</Text>
          <Text style={styles.warningText}>L'arrosage automatique sera suspendu</Text>
        </View>
      ) : (
        <Text style={styles.noRainText}>☀️ Aucune pluie prévue - Arrosage normal</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#e3f2fd',
    borderRadius: 12,
    padding: 16,
    margin: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  header: {
    borderBottomWidth: 1,
    borderBottomColor: '#bbdefb',
    paddingBottom: 8,
    marginBottom: 12,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1565c0',
    textAlign: 'center',
  },
  weatherInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  weatherIcon: {
    fontSize: 48,
    marginRight: 16,
  },
  weatherDetails: {
    alignItems: 'center',
  },
  temperature: {
    fontSize: 32,
    fontWeight: 'bold',
  },
  description: {
    fontSize: 16,
    color: '#555',
    textTransform: 'capitalize',
  },
  rainWarning: {
    backgroundColor: '#ffebee',
    padding: 10,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#f44336',
  },
  warningText: {
    color: '#d32f2f',
    textAlign: 'center',
    fontWeight: 'bold',
  },
  noRainText: {
    color: '#2e7d32',
    textAlign: 'center',
    fontWeight: 'bold',
    padding: 8,
  },
});

export default WeatherWidget;