import React from 'react';
import { TouchableOpacity, View, Text, Image, StyleSheet } from 'react-native';

interface DropdownSelectorProps {
  label: string;
  value: string;
  onPress: () => void;
}

export default function DropdownSelector({ label, value, onPress }: DropdownSelectorProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <TouchableOpacity style={[styles.button,  { paddingHorizontal: 8, minWidth: 50 }]} onPress={onPress}> 
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <Text>{value}</Text>
          <Image
            source={require('../assets/icon/polygon_4.png')}
            style={styles.arrowIcon}
            resizeMode="contain"
          />
        </View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', alignItems: 'center', marginBottom: 15 },
  label: { fontSize: 16, marginRight: 10, fontWeight: 'bold' },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    paddingVertical: 8,
    paddingHorizontal: 12,
    minWidth: 80,
  },
  arrowIcon: {
    width: 12,
    height: 12,
    marginLeft: 5,
  },
});
