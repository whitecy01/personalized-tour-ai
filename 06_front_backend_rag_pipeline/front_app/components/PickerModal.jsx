import React from 'react';
import { Modal, View, Button, StyleSheet } from 'react-native';
import { Picker } from '@react-native-picker/picker';

export default function PickerModal({ visible, selectedValue, onValueChange, onClose, items }) {
  return (
    <Modal visible={visible} transparent animationType="slide">
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <Picker selectedValue={selectedValue} onValueChange={onValueChange}>
            {items.map((item) => (
              <Picker.Item key={item} label={item} value={item} />
            ))}
          </Picker>
          <Button title="선택 완료" onPress={onClose} />
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.3)',
  },
  modalContent: {
    backgroundColor: '#fff',
    paddingBottom: 20,
  },
});
