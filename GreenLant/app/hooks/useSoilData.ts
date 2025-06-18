import { useState, useEffect } from 'react';
import { getSoilData } from '../services/esp32Service';

export default function useSoilData(refreshInterval = 60000) {
  const [soilData, setSoilData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    const data = await getSoilData();
    setSoilData(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, refreshInterval);
    return () => clearInterval(interval);
  }, []);

  return { soilData, loading, refresh: fetchData };
}