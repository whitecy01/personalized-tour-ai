import { View, Text, ScrollView, StyleSheet, Button, TextInput, ActivityIndicator} from 'react-native';
import { useState } from 'react';
import DropdownSelector from '../../components/DropdownSelector';
import PickerModal from '../../components/PickerModal';
import { TouchableOpacity } from 'react-native';
import axios from 'axios';


type CheckItemMap = { [key: string]: boolean };

export default function NewQueryScreen() {


  const [checkedItems, setCheckedItems] = useState<CheckItemMap>({});
  const [selectedAge, setSelectedAge] = useState('40대');
  const [ageModalVisible, setAgeModalVisible] = useState(false);
  const [selectedfrined, setSelectedfrined] = useState('혼자');
  const [friendModalVisible, setfriendModalVisible] = useState(false);

  // 리뷰 길이 신뢰도 선택
  const [reviewLengthPref, setReviewLengthPref] = useState<number>();

  //작성자 리뷰수
  const [reviewCountPreferencePref, setReviewCountPreferencePref] = useState<number>();

  //사진 포함 여부
  const [photoPreferencePref, setPhotoPreferencePref] = useState<number>();

  //리뷰 작성 시점
  const [recentnessPreferencePref, setRecentnessPreferencePref] = useState<number>();

  //감정분석 점수
  const [sentimentPreferencePref, setSentimentPreferencePref] = useState<number>();

  //선택지(리뷰 신뢰 점수 기준)
  const [trustScoreThresholdPref, setTrustScoreThresholdPref] = useState<number>();

  //스피너
  const [loading, setLoading] = useState(false);

  //모든 값
  const [validationModalVisible, setValidationModalVisible] = useState(false);
  const [validationMessage, setValidationMessage] = useState('');

  
  const toggleCheck = (key: string) => {
    setCheckedItems((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };


  return (
    <>
    <ScrollView style={styles.container} contentContainerStyle={{ flexGrow: 1, paddingBottom: 40 }}>
      <Text style={styles.sectionTitle}>1. 기본 정보를 입력해주세요</Text>
      <View style={styles.row}>
        <DropdownSelector label="나이" value={selectedAge} onPress={() => setAgeModalVisible(true)} />
        <View style={{ width: 20 }} />
        {/* <DropdownSelector label="성별" value={selectedGender} onPress={() => setGenderModalVisible(true)} /> */}
      </View>

      <Text style={styles.sectionTitle}>2. 관광 스타일을 입력해주세요</Text>
      <View>
        <DropdownSelector label="동행 유형" value={selectedfrined} onPress={() => setfriendModalVisible(true)} />
      </View>

      <Text style={styles.sectionTitle_third}>여행 목적</Text>
      <Text style={styles.subNote}>복수선택 가능</Text>
      <View style={styles.checkboxRow}>
        {['휴식', '문화체험', '맛집탐방', '쇼핑', '사진', '힐링'].map((item) => (
          <TouchableOpacity key={item} style={styles.circleItem} onPress={() => toggleCheck(item)}>
            <View style={[styles.circle, checkedItems[item] && styles.circleChecked]} />
            <Text style={styles.circleLabel}>{item}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle}>3. 개인화 추천을 위한 질문</Text>

      <Text style={styles.sectionTitle_four}>작성된 리뷰에서는 어떤 것이 신뢰가 가시나요?</Text>
      <View style={styles.radioGroup}>
        {[
          { label: '짧고 간결한 리뷰', value: 1 },
          { label: '적당한 길이의 리뷰', value: 2 },
          { label: '자세하고 길게 작성된 리뷰', value: 3 },
        ].map((item) => (
          <TouchableOpacity
            key={item.value}
            style={styles.radioItem}
            onPress={() => setReviewLengthPref(item.value)}
          >
            <View style={[styles.radioCircle, reviewLengthPref === item.value && styles.radioCircleSelected]} />
            <Text style={styles.circleLabel}>{item.label}</Text>
          </TouchableOpacity>
        ))}
      </View>
      
      <Text style={styles.sectionTitle_four}>리뷰 작성자가 활동적일수록 신뢰가 가나요?</Text>
      <View style={styles.radioGroup}>
        {[
          { label: '상관없음', value: 1 },
          { label: '리뷰 수가 적어도 내용이 좋다면 신뢰함', value: 2 },
          { label: '리뷰를 많이 작성한 사용자', value: 3 },
        ].map((item) => (
          <TouchableOpacity
            key={item.value}
            style={styles.radioItem}
            onPress={() => setReviewCountPreferencePref(item.value)}
          >
            <View style={[styles.radioCircle, reviewCountPreferencePref === item.value && styles.radioCircleSelected]} />
            <Text style={styles.circleLabel}>{item.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>사진이 포함된 리뷰를 더 선호하시나요?</Text>
      <View style={styles.radioGroup}>
        {[
          { label: '아니오', value: 1 },
          { label: '예', value: 2 },
        ].map((item) => (
          <TouchableOpacity
            key={item.value}
            style={styles.radioItem}
            onPress={() => setPhotoPreferencePref(item.value)}
          >
            <View style={[styles.radioCircle, photoPreferencePref === item.value && styles.radioCircleSelected]} />
            <Text style={styles.circleLabel}>{item.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>최신 리뷰가 더 중요하신가요?</Text>
      <View style={styles.radioGroup}>
        {[
          { label: '오래된 리뷰도 상관없다', value: 1 },
          { label: '그렇다', value: 2 },
        ].map((item) => (
          <TouchableOpacity
            key={item.value}
            style={styles.radioItem}
            onPress={() => setRecentnessPreferencePref(item.value)}
          >
            <View style={[styles.radioCircle, recentnessPreferencePref === item.value && styles.radioCircleSelected]} />
            <Text style={styles.circleLabel}>{item.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>긍정적인 리뷰가 많을수록 신뢰가 간다고 생각하시나요?</Text>
      <View style={styles.radioGroup}>
        {[
          { label: '아니다', value: 1 },
          { label: '중립적이다', value: 2 },
          { label: '그렇다', value: 3 }
        ].map((item) => (
          <TouchableOpacity
            key={item.value}
            style={styles.radioItem}
            onPress={() => setSentimentPreferencePref(item.value)}
          >
            <View style={[styles.radioCircle, sentimentPreferencePref === item.value && styles.radioCircleSelected]} />
            <Text style={styles.circleLabel}>{item.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>리뷰 신뢰점수 기준을 선택해주세요</Text>
      <View style={styles.radioGroup}>
        {[
          { label: '신뢰도 70% 이상 리뷰만 볼래요', value: 0.7 },
          { label: '신뢰도 60% 이상이면 괜찮아요', value: 0.6 },
          { label: '모든 리뷰 중 가장 적절한 것만 보여주세요', value: 0.5 }
        ].map((item) => (
          <TouchableOpacity
            key={item.value}
            style={styles.radioItem}
            onPress={() => setTrustScoreThresholdPref(item.value)}
          >
            <View style={[styles.radioCircle, trustScoreThresholdPref === item.value && styles.radioCircleSelected]} />
            <Text style={styles.circleLabel}>{item.label}</Text>
          </TouchableOpacity>
        ))}
      </View>


      {/* 완료 버튼 */}
      <TouchableOpacity
        disabled={loading}
        style={[styles.customButton, loading && { opacity: 0.5 }]}
        onPress={async () => {
            if (!reviewLengthPref || !reviewCountPreferencePref || !photoPreferencePref || !recentnessPreferencePref || !sentimentPreferencePref || !trustScoreThresholdPref) {
              setValidationMessage("모든 질문 항목을 선택해주세요.");
              setValidationModalVisible(true);
              return;
            }

            // if (!reviewLengthPref || !reviewCountPreferencePref || !photoPreferencePref || !recentnessPreferencePref || !sentimentPreferencePref || !trustScoreThresholdPref) {
            //   alert("모든 질문 항목을 선택해주세요.");
            //   return;
            // }

        const purposeMap: Record<string, string> = {
          휴식: 'Relaxation',
          문화체험: 'Cultural Experience',
          맛집탐방: 'Food Tour',
          쇼핑: 'Shopping',
          사진: 'Photography',
          힐링: 'Healing',
        };

          // const selectedPurposes = Object.keys(checkedItems).filter((key) => checkedItems[key]);
          const selectedPurposes = Object.keys(checkedItems)
            .filter((key) => checkedItems[key])
            .map((korean) => purposeMap[korean] || korean);  // 매핑이 
          
          console.log(selectedPurposes);
          const requestBody = {
            userId: 1,
            age: selectedAge,
            friendType: selectedfrined,
            purposes: selectedPurposes,
            reviewLength: reviewLengthPref || 0,
            reviewCountPreference: reviewCountPreferencePref || 0,
            photoPreference: photoPreferencePref || 0,
            recentnessPreference: recentnessPreferencePref || 0,
            sentimentPreference: sentimentPreferencePref || 0,
            trustScoreThreshold: trustScoreThresholdPref || 0
          };
          console.log(requestBody.purposes);

          setLoading(true); // 로딩 시작
          try {
            const response = await axios.post('http://52.78.195.74:8080/queries/create', requestBody);
            console.log('서버 응답:', response.data);
            alert('저장이 완료되었습니다!');
          } catch (error) {
            console.error('저장 중 오류 발생:', error);
            alert('저장 중 오류가 발생했습니다.');
          } finally {
            setLoading(false); // 로딩 종료
          }
        }}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>완료</Text>
        )}
      </TouchableOpacity>
      {/* <TouchableOpacity
        style={styles.customButton}
        onPress={async () => {
          const selectedPurposes = Object.keys(checkedItems).filter((key) => checkedItems[key]);

          const requestBody = {
            userId: 1,
            age: selectedAge,
            friendType: selectedfrined,
            purposes: selectedPurposes,
            reviewLength: reviewLengthPref || 0,
            reviewCountPreference: reviewCountPreferencePref || 0,
            photoPreference: photoPreferencePref || 0,
            recentnessPreference: recentnessPreferencePref || 0,
            sentimentPreference: sentimentPreferencePref || 0,
            trustScoreThreshold: trustScoreThresholdPref || 0
          };

          console.log(requestBody);
          try {
            const response = await axios.post('http://52.78.195.74:8080/queries/create', requestBody);
            console.log('서버 응답:', response.data);
            alert('저장이 완료되었습니다!');
          } catch (error) {
            console.error('저장 중 오류 발생:', error);
            alert('저장 중 오류가 발생했습니다.');
          }
        }}
      >
        <Text style={styles.customButtonText}>완료</Text>
      </TouchableOpacity> */}

      <PickerModal visible={ageModalVisible} selectedValue={selectedAge} onValueChange={setSelectedAge} onClose={() => setAgeModalVisible(false)} items={['10대', '20대', '30대', '40대', '50대 이상']} />
      {/* <PickerModal visible={genderModalVisible} selectedValue={selectedGender} onValueChange={setSelectedGender} onClose={() => setGenderModalVisible(false)} items={['남', '여', '기타']} /> */}
      <PickerModal visible={friendModalVisible} selectedValue={selectedfrined} onValueChange={setSelectedfrined} onClose={() => setfriendModalVisible(false)} items={['혼자', '친구', '연인', '가족', '아이 동반']} />
    </ScrollView>
      {loading && (
      <View style={styles.modalOverlay}>
        <View style={styles.modalContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.modalText}>리뷰 데이터를 최적화 중입니다.{'\n'}시간이 다소 소요될 수 있습니다.</Text>
        </View>
      </View>
    )}

    {validationModalVisible && (
      <View style={styles.modalOverlay}>
        <View style={styles.modalContainer}>
          <Text style={styles.modalText}>{validationMessage}</Text>
          <TouchableOpacity onPress={() => setValidationModalVisible(false)} style={styles.customButton}>
            <Text style={styles.buttonText}>확인</Text>
          </TouchableOpacity>
        </View>
      </View>
    )}

  </>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', marginBottom: 15 },
  sectionTitle_four: { fontSize: 16, fontWeight: 'bold', marginBottom: 6 },
  sectionTitle_third: { fontSize: 16, fontWeight: 'bold', marginVertical: 3 },
  row: { flexDirection: 'row', alignItems: 'center', marginBottom: 5 },
  checkboxRow: { flexDirection: 'row', flexWrap: 'wrap', marginBottom: 10 },
  circleItem: { flexDirection: 'row', alignItems: 'center', marginRight: 15, marginBottom: 10 },
  circle: { width: 20, height: 20, borderRadius: 10, borderWidth: 2, borderColor: '#ccc', justifyContent: 'center', alignItems: 'center', marginRight: 5 },
  circleChecked: { borderColor: '#007bff', backgroundColor: '#007bff' },
  circleLabel: { fontSize: 14 },
  // customButton: { backgroundColor: '#7dbdf5', paddingVertical: 12, paddingHorizontal: 30, borderRadius: 8, alignItems: 'center', width: '100%', marginTop: 3 },
  customButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  subNote: { fontSize: 12, color: '#888', marginBottom: 5 },
  radioGroup: { marginVertical: 8 },
  radioItem: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  radioCircle: { width: 16, height: 16, borderRadius: 8, borderWidth: 2, borderColor: '#ccc', marginRight: 8 },
  radioCircleSelected: { borderColor: '#007bff', backgroundColor: '#007bff' },


  customButton: {
    backgroundColor: '#007AFF',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 20
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  modalOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 999,
  },
  modalContainer: {
    backgroundColor: 'white',
    padding: 25,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  modalText: {
    marginTop: 15,
    fontSize: 15,
    textAlign: 'center',
    color: '#333',
  },
  
  
});
