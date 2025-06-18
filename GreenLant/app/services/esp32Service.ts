import axios from 'axios';

const ESP32_IP = '192.168.1.100'; // Adresse IP de votre ESP32

export const getSoilData = async () => {
  try {
    const response = await axios.get(`http://${ESP32_IP}/sensors`);
    return response.data;
  } catch (error) {
    console.error('Erreur ESP32:', error);
    return null;
  }
};

export const triggerWatering = async (duration: number) => {
  try {
    await axios.post(`http://${ESP32_IP}/water`, { duration });
    return true;
  } catch (error) {
    console.error('Erreur arrosage:', error);
    return false;
  }
};