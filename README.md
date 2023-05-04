<h1> alarm_generator </h1> 

<h3> new Version - 2.1.2.230504 </h3>


[new] 2.2.1.230504 - Update release note

1. table 자동 저장 오류 해결
2. thread 동작중 save 파일 변경시 자동으로 약 5분뒤 detect 하도록 설정
   1. 수동으로 start, stop으로 설정 가능
3. detect 도중 stop 버튼을 누르면 늦게 프로세스가 멈추는 현상 해결
4. 프로그램 속성 업데이트

- readme 작성자: jh choi


-----------------------------------------------

2.2.0.230503 - Update release note

1. UI Update
2. 일부 오류 해결 
3. git 오류로 인한 thread remake

- readme 작성자: jh choi

-----------------------------------------------

2.1.0.230427 - Update release note

1. IP 추가 방식 업데이트 - 기존 txt -> json 형식 
2. Login 버튼 추가
   1. 해당 버튼을 눌러야 모든 버튼 활성화
   2. ip 변경(추가, 수정, 삭제)시 해당 버튼을 눌러야 활성화
3. Save 버튼 추가
   1. ip 변경(추가, 수정, 삭제)시 버튼 누르면 저장
   2. 어느한 버튼을 눌러도 자동 저장이 되도록 설정
4. Alarm Control 기능 추가
   1. Status 확인 기능
   2. 모든 알람을 한번에 동작 제어 버튼을 추가
5. Model 선택 추가
6. Thread 를 한개만 동작 하도록 process 수정
7. Sound ON 기능 추가
   1. 기존에는 USB 경광등을 부착하여야 소리가 발생
   2. wav 파일을 추가하여 화재 발생 알람이 발생
8. Test 버튼 추가
   1. 단일 버튼으로 활성화, 비활성화 설정

- readme 작성자: jh choi