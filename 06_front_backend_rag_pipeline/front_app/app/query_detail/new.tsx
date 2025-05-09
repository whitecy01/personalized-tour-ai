import { View, Text, ScrollView, StyleSheet, Button, TextInput } from 'react-native';
import { useState } from 'react';
import DropdownSelector from '../../components/DropdownSelector';
import PickerModal from '../../components/PickerModal';
import { TouchableOpacity } from 'react-native';
import axios from 'axios';

type CheckItemMap = { [key: string]: boolean };

export default function NewQueryScreen() {
  const [checkedItems, setCheckedItems] = useState<CheckItemMap>({});
  const [selectedAge, setSelectedAge] = useState('40대');
  const [selectedGender, setSelectedGender] = useState('남');
  const [ageModalVisible, setAgeModalVisible] = useState(false);
  const [genderModalVisible, setGenderModalVisible] = useState(false);

  const [selectedfrined, setSelectedfrined] = useState('혼자');
  const [friendModalVisible, setfriendModalVisible] = useState(false);

  const [interestCheckedItems, setInterestCheckedItems] = useState<CheckItemMap>({});
  const [TasteCheckedItems, setTasteCheckedItems] = useState<CheckItemMap>({});
  const [checkedItemsLocation, setCheckedItemsLocation] = useState<CheckItemMap>({});
  const [amenitiesItemsLocation, setCheckedItemsAmenities] = useState<CheckItemMap>({});
  const [selectedPriority, setSelectedPriority] = useState('');

  const toggleCheck = (key: string) => {
    setCheckedItems((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const interstToggleCheck = (key: string) => {
    setInterestCheckedItems((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const tasteToggleCheck = (key: string) => {
    setTasteCheckedItems((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const locationToggleCheck = (key: string) => {
    setCheckedItemsLocation((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const amenitiesToggleCheck = (key: string) => {
    setCheckedItemsAmenities((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ flexGrow: 1, paddingBottom: 40 }}>
      <Text style={styles.sectionTitle}>1. 기본 정보를 입력해주세요</Text>
      <View style={styles.row}>
        <DropdownSelector label="나이" value={selectedAge} onPress={() => setAgeModalVisible(true)} />
        <View style={{ width: 20 }} />
        <DropdownSelector label="성별" value={selectedGender} onPress={() => setGenderModalVisible(true)} />
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

      <Text style={styles.sectionTitle_four}>3. 관심사를 입력해주세요</Text>
      <Text style={styles.subNote}>복수선택 가능</Text>
      <View style={styles.checkboxRow}>
        {['카페', '활동', '해변', '전통시장', '감성'].map((item) => (
          <TouchableOpacity key={item} style={styles.circleItem} onPress={() => interstToggleCheck(item)}>
            <View style={[styles.circle, interestCheckedItems[item] && styles.circleChecked]} />
            <Text style={styles.circleLabel}>{item}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>4. 음식 취향을 입력해주세요</Text>
      <Text style={styles.subNote}>복수선택 가능</Text>
      <View style={styles.checkboxRow}>
        {['달달한', '고소한', '매운', '단백한'].map((item) => (
          <TouchableOpacity key={item} style={styles.circleItem} onPress={() => tasteToggleCheck(item)}>
            <View style={[styles.circle, TasteCheckedItems[item] && styles.circleChecked]} />
            <Text style={styles.circleLabel}>{item}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>5. 방문 희망 지역을 입력해주세요</Text>
      <Text style={styles.subNote}>복수선택 가능</Text>
      <View style={styles.checkboxRow}>
        {['송정', '남포동', '서면', '광안리','사상','하단','구포','동래','해운대','기장', '영도','강서구','수영구'].map((item) => (
          <TouchableOpacity key={item} style={styles.circleItem} onPress={() => locationToggleCheck(item)}>
            <View style={[styles.circle, checkedItemsLocation[item] && styles.circleChecked]} />
            <Text style={styles.circleLabel}>{item}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>6. 기타 편의 사항을 입력해주세요</Text>
      <Text style={styles.sectionTitle_third}>알레르기/음식 제한</Text>
      <Text style={styles.subNote}>복수선택 가능</Text>
      <View style={styles.checkboxRow}>
        {['유제품', '견과류', '갑각류', '글루텐'].map((item) => (
          <TouchableOpacity key={item} style={styles.circleItem} onPress={() => amenitiesToggleCheck(item)}>
            <View style={[styles.circle, amenitiesItemsLocation[item] && styles.circleChecked]} />
            <Text style={styles.circleLabel}>{item}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.sectionTitle_four}>7. 최우선 조건을 입력해주세요</Text>
      <View style={styles.checkboxRow}>
        {['동행 유형', '가격', '음식', '분위기'].map((item) => (
          <TouchableOpacity key={item} style={styles.circleItem} onPress={() => setSelectedPriority(item)}>
            <View style={[styles.circle, selectedPriority === item && styles.circleChecked]} />
            <Text style={styles.circleLabel}>{item}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity
        style={styles.customButton}
        onPress={async () => {
          const selectedInterests = Object.keys(interestCheckedItems).filter((key) => interestCheckedItems[key]);
          const selectedPurposes = Object.keys(checkedItems).filter((key) => checkedItems[key]);
          const selectedTastes = Object.keys(TasteCheckedItems).filter((key) => TasteCheckedItems[key]);
          const selectedLocations = Object.keys(checkedItemsLocation).filter((key) => checkedItemsLocation[key]);
          const selectedAmenities = Object.keys(amenitiesItemsLocation).filter((key) => amenitiesItemsLocation[key]);

          const requestBody = {
            userId: 1,
            gender: selectedGender,
            age: selectedAge,
            friendType: selectedfrined,
            purposes: selectedPurposes,
            interest: selectedInterests,
            taste: selectedTastes,
            location: selectedLocations,
            amenity: selectedAmenities,
            priority: selectedPriority,
          };

          console.log(requestBody);
          try {
            const response = await axios.post('http://192.168.1.193:8080/queries/create', requestBody);
            console.log('서버 응답:', response.data);
            alert('저장이 완료되었습니다!');
          } catch (error) {
            console.error('저장 중 오류 발생:', error);
            alert('저장 중 오류가 발생했습니다.');
          }
        }}
      >
        <Text style={styles.customButtonText}>완료</Text>
      </TouchableOpacity>

      <PickerModal visible={ageModalVisible} selectedValue={selectedAge} onValueChange={setSelectedAge} onClose={() => setAgeModalVisible(false)} items={['10대', '20대', '30대', '40대', '50대 이상']} />
      <PickerModal visible={genderModalVisible} selectedValue={selectedGender} onValueChange={setSelectedGender} onClose={() => setGenderModalVisible(false)} items={['남', '여', '기타']} />
      <PickerModal visible={friendModalVisible} selectedValue={selectedfrined} onValueChange={setSelectedfrined} onClose={() => setfriendModalVisible(false)} items={['혼자', '친구', '연인', '가족', '아이 동반']} />
    </ScrollView>
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
  customButton: { backgroundColor: '#7dbdf5', paddingVertical: 12, paddingHorizontal: 30, borderRadius: 8, alignItems: 'center', width: '100%', marginTop: 3 },
  customButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  subNote: { fontSize: 12, color: '#888', marginBottom: 5 },
});

// 기타 버튼 있음
// import { View, Text, ScrollView, StyleSheet, Button, TextInput } from 'react-native';
// import { useState } from 'react';
// import DropdownSelector from '../../components/DropdownSelector';
// import PickerModal from '../../components/PickerModal';
// import { TouchableOpacity } from 'react-native';
// import axios from 'axios';

// type CheckItemMap = { [key: string]: boolean };

// export default function NewQueryScreen() {
//   const [checkedItems, setCheckedItems] = useState<CheckItemMap>({});
//   const [selectedAge, setSelectedAge] = useState('40대');
//   const [selectedGender, setSelectedGender] = useState('남');
//   const [ageModalVisible, setAgeModalVisible] = useState(false);
//   const [genderModalVisible, setGenderModalVisible] = useState(false);

//   // 관광 스타일
//   const [selectedfrined, setSelectedfrined] = useState('혼자');
//   const [friendModalVisible, setfriendModalVisible] = useState(false);

//   // 관심사
//   const [interestCheckedItems, setInterestCheckedItems] = useState<CheckItemMap>({});
//   const [showOtherInput, setShowOtherInput] = useState(false);
//   const [otherInterest, setOtherInterest] = useState('');

//   // 음식 취향
//   const [TasteCheckedItems, setTasteCheckedItems] = useState<CheckItemMap>({});
//   const [showOtherInputTaste, setShowOtherInputTaste] = useState(false);
//   const [otherTaste, setOtherTaste] = useState('');


//   //방문 희망 지역
//   const [checkedItemsLocation, setCheckedItemsLocation] = useState<CheckItemMap>({});

//   //기타 편의 사항
//   const [amenitiesItemsLocation, setCheckedItemsAmenities] = useState<CheckItemMap>({});

//   //최우선 조건
//   // const [priorityItemsLocation, setCheckedItemsPriority] = useState<CheckItemMap>({});1
//   const [selectedPriority, setSelectedPriority] = useState('');

  


//   const toggleCheck = (key: string) => {
//     setCheckedItems((prev) => ({
//       ...prev,
//       [key]: !prev[key],
//     }));
//   };

//   const interstToggleCheck = (key: string) => {
//     setInterestCheckedItems((prev) => ({
//       ...prev,
//       [key]: !prev[key],
//     }));
//   };

//   const tasteToggleCheck = (key: string) => {
//     setTasteCheckedItems((prev) => ({
//       ...prev,
//       [key]: !prev[key],
//     }));
//   };

//   const locationToggleCheck = (key: string) => {
//     setCheckedItemsLocation((prev) => ({
//       ...prev,
//       [key]: !prev[key],
//     }));
//   };

//   const amenitiesToggleCheck = (key: string) => {
//     setCheckedItemsAmenities((prev) => ({
//       ...prev,
//       [key]: !prev[key],
//     }));
//   };

//   // const priorityToggleCheck = (key: string) => {
//   //   setCheckedItemsPriority((prev) => ({
//   //     ...prev,
//   //     [key]: !prev[key],
//   //   }));
//   // };

  

  

//   return (
//     <ScrollView style={styles.container}
//     contentContainerStyle={{ flexGrow: 1, paddingBottom: 40 }}
//     >
//       {/* 기본정보 */}
//       <Text style={styles.sectionTitle}>1. 기본 정보를 입력해주세요</Text>
//       <View style={styles.row}>
//         <DropdownSelector label="나이" value={selectedAge} onPress={() => setAgeModalVisible(true)} />
//         <View style={{ width: 20 }} />
//         <DropdownSelector label="성별" value={selectedGender} onPress={() => setGenderModalVisible(true)} />
//       </View>


//       {/* 관광 */}
//       <Text style={styles.sectionTitle}>2. 관광 스타일을 입력해주세요</Text>
//       <View>
//         <DropdownSelector label="동행 유형" value={selectedfrined} onPress={() => setfriendModalVisible(true)} />
//       </View>

//       <Text style={styles.sectionTitle_third}>여행 목적</Text>
//       <Text style={styles.subNote}>복수선택 가능</Text>
//       <View style={styles.checkboxRow}>
//         {['휴식', '문화체험', '맛집탐방', '쇼핑', '사진', '힐링'].map((item) => (
//           <TouchableOpacity
//             key={item}
//             style={styles.circleItem}
//             onPress={() => toggleCheck(item)}
//           >
//             <View style={[
//               styles.circle,
//               checkedItems[item] && styles.circleChecked
//             ]} />
//             <Text style={styles.circleLabel}>{item}</Text>
//           </TouchableOpacity>
//         ))}
//       </View>

//       {/* 관심사 */}
//       <Text style={styles.sectionTitle_four}>3. 관심사를 입력해주세요</Text>
//       <Text style={styles.subNote}>복수선택 가능</Text>
//       <View style={styles.checkboxRow}>
//         {['카페', '활동', '해변', '전통시장', '감성', '기타'].map((item) => (
//           <TouchableOpacity
//             key={item}
//             style={styles.circleItem}
//             onPress={() => {
//               if (item === '기타') {
//                 setShowOtherInput(!showOtherInput);
//               } else {
//                 interstToggleCheck(item);
//               }
//             }}
//           >
//             <View style={[
//               styles.circle,
//               item === '기타'
//                 ? showOtherInput
//                   ? styles.circleChecked
//                   : null
//                 : interestCheckedItems[item] && styles.circleChecked
//             ]} />
//             <Text style={styles.circleLabel}>{item}</Text>
//           </TouchableOpacity>
//         ))}
//         {showOtherInput && (
//           <View style={styles.otherInputContainer}>
//             <Text style={styles.otherInputLabel}>기타 입력:</Text>
//             <TextInput
//               style={styles.otherInput}
//               placeholder="관심사를 입력해주세요"
//               value={otherInterest}
//               onChangeText={(text) => {
//                 console.log('입력됨:', text);
//                 setOtherInterest(text);
//               }}
//             />
//           </View>
//         )}
//       </View>

//       {/* 음식 취향 */}
//       <Text style={styles.sectionTitle_four}>4. 음식 취향을 입력해주세요</Text>
//       <Text style={styles.subNote}>복수선택 가능</Text>
//       <View style={styles.checkboxRow}>
//         {['달달한', '고소한', '매운', '단백한', '기타'].map((item) => (
//           <TouchableOpacity
//             key={item}
//             style={styles.circleItem}
//             onPress={() => 
//             {
//               if (item === '기타') {
//                 setShowOtherInputTaste(!showOtherInputTaste);
//               } else {
//                 tasteToggleCheck(item);
//               }
//             }}
//           >
//             <View style={[
//               styles.circle,
//               // TasteCheckedItems[item] && styles.circleChecked
//               item === '기타'
//               ? showOtherInputTaste
//                 ? styles.circleChecked
//                 : null
//               : TasteCheckedItems[item] && styles.circleChecked
//             ]} />
//             <Text style={styles.circleLabel}>{item}</Text>
//           </TouchableOpacity>
//         ))}
//         {showOtherInputTaste && (
//           <View style={styles.otherInputContainer}>
//             <Text style={styles.otherInputLabel}>기타 입력:</Text>
//             <TextInput
//               style={styles.otherInput}
//               placeholder="음식 취향을 입력해주세요"
//               value={otherTaste}
//               onChangeText={(text) => {
//                 console.log('입력됨:', text);
//                 setOtherTaste(text);
//               }}
//             />
//           </View>
//         )}
//       </View>

//       {/* 방문 희망 지역 */}
//       <Text style={styles.sectionTitle_four}>5. 방문 희망 지역을 입력해주세요</Text>
//       <Text style={styles.subNote}>복수선택 가능</Text>
//       <View style={styles.checkboxRow}>
//         {['송정', '남포동', '서면', '광안리','사상','하단','구포','동래','해운대','기장', '영도','강서구','수영구'].map((item) => (
//           <TouchableOpacity
//             key={item}
//             style={styles.circleItem}
//             onPress={() => locationToggleCheck(item)}
//           >
//             <View style={[
//               styles.circle,
//               checkedItemsLocation[item] && styles.circleChecked
//             ]} />
//             <Text style={styles.circleLabel}>{item}</Text>
//           </TouchableOpacity>
//         ))}
//       </View>

//       {/* 기타 편의 사항 */}
//       <Text style={styles.sectionTitle_four}>6. 기타 편의 사항을 입력해주세요</Text>
//       <Text style={styles.sectionTitle_third}>알레르기/음식 제한</Text>
//       <Text style={styles.subNote}>복수선택 가능</Text>
//       <View style={styles.checkboxRow}>
//         {['유제품', '견과류', '갑각류', '글루텐'].map((item) => (
//           <TouchableOpacity
//             key={item}
//             style={styles.circleItem}
//             onPress={() => amenitiesToggleCheck(item)}
//           >
//             <View style={[
//               styles.circle,
//               amenitiesItemsLocation[item] && styles.circleChecked
//             ]} />
//             <Text style={styles.circleLabel}>{item}</Text>
//           </TouchableOpacity>
//         ))}
//       </View>

//       {/* 최우선 조건 */}
//       <Text style={styles.sectionTitle_four}>7. 최우선 조건을 입력해주세요</Text>
//       <View style={styles.checkboxRow}>
//         {['동행 유형', '가격', '음식', '분위기'].map((item) => (
//           <TouchableOpacity
//             key={item}
//             style={styles.circleItem}
//             onPress={() => setSelectedPriority(item)}  // 하나만 선택
//           >
//             <View style={[
//               styles.circle,
//               selectedPriority === item && styles.circleChecked  // 선택 표시
//             ]} />
//             <Text style={styles.circleLabel}>{item}</Text>
//           </TouchableOpacity>
//         ))}
//       </View>

//       {/* <Text style={styles.sectionTitle_four}>7. 최우선 조건을 입력해주세요</Text>
//       <View style={styles.checkboxRow}>
//         {['동행 유형','가격','음식','분위기'].map((item) => (
//           <TouchableOpacity
//             key={item}
//             style={styles.circleItem}
//             onPress={() => priorityToggleCheck(item)}
//           >
//             <View style={[
//               styles.circle,
//               priorityItemsLocation[item] && styles.circleChecked
//             ]} />
//             <Text style={styles.circleLabel}>{item}</Text>
//           </TouchableOpacity>
//         ))}
//       </View> */}



//       {/* 완료 버튼 */}
//       <TouchableOpacity
//         style={styles.customButton}
//         onPress={async () => {
//           const selectedInterests = Object.keys(interestCheckedItems).filter(
//             (key) => interestCheckedItems[key]
//           );

//           if (showOtherInput && otherInterest.trim() !== '') {
//             selectedInterests.push(otherInterest.trim());
//           }
      
//           // 여행 목적
//           const selectedPurposes = Object.keys(checkedItems).filter(
//             (key) => checkedItems[key]
//           );
      
//           // 음식 취향
//           const selectedTastes = Object.keys(TasteCheckedItems).filter(
//             (key) => TasteCheckedItems[key]
//           );
//           if (showOtherInputTaste && otherTaste.trim() !== '') {
//             selectedTastes.push(otherTaste.trim());
//           }
      
//           // 방문 희망 지역
//           const selectedLocations = Object.keys(checkedItemsLocation).filter(
//             (key) => checkedItemsLocation[key]
//           );
      
//           // 기타 편의 사항
//           const selectedAmenities = Object.keys(amenitiesItemsLocation).filter(
//             (key) => amenitiesItemsLocation[key]
//           );
      
//           // 최우선 조건
//           // const selectedPriorities = Object.keys(priorityItemsLocation).filter(
//           //   (key) => priorityItemsLocation[key]
//           // );
      
//           console.log('=== 선택된 값들 ===');
//           console.log('나이:', selectedAge);
//           console.log('성별:', selectedGender);
//           console.log('동행 유형:', selectedfrined);
//           console.log('여행 목적:', selectedPurposes);
//           console.log('관심사:', selectedInterests);
   
//           console.log('음식 취향:', selectedTastes);
//           console.log('방문 희망 지역:', selectedLocations);
//           console.log('기타 편의 사항:', selectedAmenities);
//           // console.log('최우선 조건:', selectedPriorities);
//           console.log('최우선 조건:', selectedPriority);
//           // api 요청 코드
//           const requestBody = {
//             userId: 1, // 예: 테스트용 userId, 실제 로그인 연동 시 교체
//             gender: selectedGender,
//             age: selectedAge,
//             friendType: selectedfrined,
//             purposes: selectedPurposes,
//             interest: selectedInterests,
//             taste: selectedTastes,
//             location: selectedLocations,
//             amenity: selectedAmenities,
//             // prioritie: selectedPriorities,
//             priority: selectedPriority,
//           };
//           console.log(requestBody);
//           try {
//             const response = await axios.post(
//               'http://192.168.1.193:8080/queries/create',
//               requestBody
//             );
//             console.log('서버 응답:', response.data);
//             alert('저장이 완료되었습니다!');
//           } catch (error) {
//             console.error('저장 중 오류 발생:', error);
//             alert('저장 중 오류가 발생했습니다.');
//           }

//         }}
//       >
//         <Text style={styles.customButtonText}>완료</Text>
//       </TouchableOpacity>

//       {/* 기본 정보 */}
//       <PickerModal
//         visible={ageModalVisible}
//         selectedValue={selectedAge}
//         onValueChange={setSelectedAge}
//         onClose={() => setAgeModalVisible(false)}
//         items={['10대', '20대', '30대', '40대', '50대 이상']}
//       />

//       <PickerModal
//         visible={genderModalVisible}
//         selectedValue={selectedGender}
//         onValueChange={setSelectedGender}
//         onClose={() => setGenderModalVisible(false)}
//         items={['남', '여', '기타']}
//       />

//       {/* 관광 */}
//       <PickerModal
//         visible={friendModalVisible}
//         selectedValue={selectedfrined}
//         onValueChange={setSelectedfrined}
//         onClose={() => setfriendModalVisible(false)}
//         items={['혼자', '친구', '연인', '가족', '아이 동반']}
//       />



//     </ScrollView>
//   );
// }

// const styles = StyleSheet.create({
//   container: { flex: 1, padding: 20, backgroundColor: '#fff' },
//   sectionTitle: { fontSize: 16, fontWeight: 'bold', marginBottom : 15},
//   sectionTitle_four: { fontSize: 16, fontWeight: 'bold', marginBottom : 6},
//   sectionTitle_third :  { fontSize: 16, fontWeight: 'bold', marginVertical: 3 },
//   row: { flexDirection: 'row', alignItems: 'center', marginBottom: 5 },
//   detail_row : {flexDirection: 'row', alignItems: 'center', marginBottom: 5 },
//   checkboxRow: { flexDirection: 'row', flexWrap: 'wrap', marginBottom: 10 },
//   checkboxItem: { marginRight: 10, marginBottom: 5 },
//   buttonContainer: { marginTop: 20 },
//   subNote: { fontSize: 12, color: '#888', marginBottom: 5 },
//   label: { fontSize: 14, marginRight: 10 },
//   circleItem: { flexDirection: 'row', alignItems: 'center', marginRight: 15, marginBottom: 10 },
//   circle: {
//     width: 20,
//     height: 20,
//     borderRadius: 10,
//     borderWidth: 2,
//     borderColor: '#ccc',
//     justifyContent: 'center',
//     alignItems: 'center',
//     marginRight: 5,
//   },
//   circleChecked: {
//     borderColor: '#007bff',
//     backgroundColor: '#007bff',
//   },
//   circleLabel: { fontSize: 14 },
//   otherInputContainer: {
//     flexDirection: 'row',  // ← row → column으로 변경
//     // alignItems: 'flex-start', // 왼쪽 정렬
//     width: '50%',            // 전체 너비 사용
//     marginBottom: 10,
//     alignItems: 'center',   // ← 중앙 정렬
//   },
//   otherInputLabel: {
//     marginRight: 10,
//     fontSize: 14,
//   },
//   otherInput: {
//     flex: 1,
//     minWidth: 150,         // 최소 너비 추가
//     minHeight: 15,         // 최소 높이 추가 (기본 입력창 높이)
//     borderWidth: 1,
//     borderColor: '#ccc',
//     borderRadius: 5,
//     padding: 8,
//   },
//   customButton: {
//     backgroundColor: '#7dbdf5',  // 연한 파란색
//     paddingVertical: 12,
//     paddingHorizontal: 30,
//     borderRadius: 8,
//     alignItems: 'center',
//     width: '100%',
//     marginTop: 3,
//   },
//   customButtonText: {
//     color: '#fff',
//     fontSize: 16,
//     fontWeight: 'bold',
//   },
// });


