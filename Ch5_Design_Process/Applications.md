# Application : 썸네일 photo Service
강의 내내 사용할 예시

## Introducing an example Photo Application Service

<img width="925" alt="스크린샷 2020-02-07 오후 2 05 35" src="https://user-images.githubusercontent.com/26548454/74080164-4dd27c80-4a84-11ea-9712-04c1ed21b0db.png">

새로운 서비스라서, 얼마나 popular할지는 아무도 모르는 상태.
1. 사용자 : 아마 인터넷 쓰겠지
2. Speed : 로컬 컴퓨터에서 1분 이내로 걸린다. 그거보다 빠르면 족함
3. Resources : 몰라. 사용자 얼마나 있을지도 알 수 없음
4. Scale : 작게. Single VM으로, 일단 Vertical Size up으로 생각하자. (Add power)
5. Size : 사용자 지역분포 모른다. 일단 Central US 어딘가로 잡자
6. Availability : 몰라


<img width="927" alt="스크린샷 2020-02-07 오후 2 09 02" src="https://user-images.githubusercontent.com/26548454/74080166-52973080-4a84-11ea-8393-cbb154fc00bc.png">

Business Layer Logic.

- User Experience : 아마 Frontend (웹사이트 / 앱) 가 될 거고
- 이미지 받아서 저장 = 어디에 어떻게 저장할지 일단은 중요하지 않다
- 변환
- 변환된 결과물을 어딘가에 저장 -> 사용자에게 반환.


<img width="925" alt="스크린샷 2020-02-07 오후 2 11 18" src="https://user-images.githubusercontent.com/26548454/74080168-532fc700-4a84-11ea-81a0-25a4f70ca0ad.png">

SLO 정의하기

- 23시간 available. 1시간은 take offline 설정 = 95.83% availability
- 사용자 측면에서 이해할 수 있으려면 -> Service online / offline 여부. (SLI)

서비스의 첫 디자인은 위 그림과 같음. 
Single App Server를 하드웨어에 올리고, Log file은 하드웨어에 저장한다. 즉, App is separated from the Log data it’s generating.

<img width="924" alt="스크린샷 2020-02-07 오후 2 14 51" src="https://user-images.githubusercontent.com/26548454/74080171-53c85d80-4a84-11ea-9875-330ec4f69284.png">

로컬에서 돌려보고, 돌아가면 그 세팅 그대로 Cloud에 올려 실행한다고 가정했을 때

반드시 해야 할 과정들 -> Testing.
- 특히 System Test는, 서로 다른 환경에서 개발한 뒤 통합할 때 매우 중요하다. Containerization이 됐으면, 꼭 중요하지는 않음
- Stress test = Can it work to the scale that we anticipated? 어디가 bottleneck인지 확인하는 작업 등등

Production Test 레벨에서는

- Rolled out.  Deploy it to small number of customers -> 작동하면 점점 사용자 수를 확장해가는 식
- Red-green / AB test. = ‘turn whole things off and put on version 2’ 같은 식
- canary deployment = test if it works. 되면 simply switch everything out.

Testing 부분은 scale에 따라 방법도 많고, 사용자에게 들어가는 interruption도 다 다르다.

---
