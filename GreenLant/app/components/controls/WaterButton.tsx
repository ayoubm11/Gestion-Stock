import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';

export default function WaterButton() {
  const handlePress = () => {
    // Logique pour déclencher l'arrosage
  };

  return (
    <TouchableOpacity style={styles.button} onPress={handlePress}>
      <Text style={styles.text}>💧 Arroser Maintenant</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 10,
    margin: 20,
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});