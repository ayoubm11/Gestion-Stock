import axios from 'axios';
import moment from 'moment';

const API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'; // Obtenez gratuitement sur openweathermap.org

export interface WeatherData {
  temp: number;
  humidity: number;
  description: string;
  icon: string;
  willRain: boolean;
  rainAmount?: number;
}

export const getWeatherForecast = async (city: string): Promise<WeatherData> => {
  try {
    const response = await axios.get(
      `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${API_KEY}&units=metric&lang=fr`
    );

    // Données actuelles
    const current = response.data.list[0];
    const currentWeather: WeatherData = {
      temp: Math.round(current.main.temp),
      humidity: current.main.humidity,
      description: current.weather[0].description,
      icon: current.weather[0].icon,
      willRain: false
    };

    // Vérifier s'il va pleuvoir dans les prochaines 24 heures
    const now = moment();
    const tomorrow = moment().add(24, 'hours');
    
    const rainForecast = response.data.list.some((item: any) => {
      const forecastTime = moment.unix(item.dt);
      return forecastTime.isBetween(now, tomorrow) && 
             item.weather[0].main.toLowerCase().includes('rain');
    });

    currentWeather.willRain = rainForecast;

    return currentWeather;
  } catch (error) {
    console.error('Erreur météo:', error);
    return {
      temp: 20,
      humidity: 60,
      description: 'Ensoleillé',
      icon: '01d',
      willRain: false
    };
  }
};