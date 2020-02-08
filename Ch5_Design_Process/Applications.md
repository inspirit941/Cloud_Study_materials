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

## The photo service is slow

서비스가 Slow down 상태다. 뭘 할 수 있을까?
던져야 할 질문
* What is the cause?
* What can be done?
* What lessons does this offer for design?


Service Slow = User Experience Part라고 보면 된다.


<img width="922" alt="스크린샷 2020-02-08 오후 3 53 49" src="https://user-images.githubusercontent.com/26548454/74082182-e70c8d80-4a9a-11ea-9474-2669cff1ea78.png">


어디서 문제가 생기는지 segement / reduce the problem space.
Monitoring / logging 데이터가 있는지 보고, 만약 없거나 설정되어 있지 않으면 설정해둬야 한다. 
이런 데이터조차 없으면, actual data를 토대로 troubleshooting해야 함

-> do I have the ability to add more information to this, so I can troubleshoot this in the future?

<img width="927" alt="스크린샷 2020-02-08 오후 3 56 16" src="https://user-images.githubusercontent.com/26548454/74082189-eb38ab00-4a9a-11ea-94a7-95ebdc3b30dc.png">

Adding more infomation을 포함해서, 이 작업은 개인이 다룰 수 있는 범위를 넘어서는 경우가 많다. 그래서 collaborations, communication이 중요함.

Being a hero can lead to longer downtime. Closed-Group conversation은 협력보다는 반목의 가능성을 높인다. 

User experience를 돌아보면, 이미지 업로드 -> 저장 -> 처리 -> 결과물 저장 -> 반환 순서로 되어 있다. slow라는 건, 이 중 하나 이상이 뭔가 문제가 있다는 것.


<img width="922" alt="스크린샷 2020-02-08 오후 4 18 34" src="https://user-images.githubusercontent.com/26548454/74082219-29ce6580-4a9b-11ea-8e66-b2cf87d6ca67.png">


1. User Experience part
	- Web server is reponding? DNS 서버에 문제가 있나?
	- session handling에 문제가 있나?

2. Ingest
	- HTTP 프로토콜 사용. Disk IO 자체는 문제가 되지 않을 것이다. 엥간하면
	
3. Conversion : Computing power를 가장 많이 잡아먹는 곳, 디스크에서 메모리로 데이터 읽어온 뒤 메모리에서 처리하는 과정이라서 disk IO가 미치는 영향 자체는 적을 것.

4. 변환된 파일 저장 : 이미 원본이미지 + 새로 변환된 이미지 저장을 해야 하는 상황. File system을 체크해봐야 한다. 수많은 파일 전부를 keep track on 하는 데서 오는 부하는 없는가? (IO intensive … potential issue)



예시로 돌아오면
결국 User experience는 thumbnail conversion processing에 영향을 받는다.

띠라서 Web Server측에서 직접 conversion 작업을 처리하는 대신, 처리를 전담하는 다른 processing App server를 만드는 걸로 해결한다. 이렇게 되면 Web server의 cpu 사용량이나 메모리 양도 줄어들고, disk io도 크게 줄어든다. 

다시말해 Web server는 사용자와의 interface일 뿐, 어떤 작업도 직접 처리하지 않는 형태로 변경함

<img width="926" alt="스크린샷 2020-02-08 오후 4 24 07" src="https://user-images.githubusercontent.com/26548454/74082201-0d322d80-4a9b-11ea-8c8e-e2e74281e305.png">

구조를 변경했을 때, SLI나 SLO에 변동이 있는지?
-> performance-based SLI to the server 적용이 가능하다. 1분 이내에 사용자에게 서비스를 제공할 수 있다는 SLI는 그대로이고, 이걸 측정할 수 있는 indicator로 end-to-end latency를 추가할 수 있음.

---
## Challenge #1. Log aggregation

구조를 변경하면서, log system design에  변동이 생김. Separate logs will need to be aggregated onto a single system. 어떻게 디자인하는 게 좋을지?

<img width="926" alt="스크린샷 2020-02-08 오후 4 34 03" src="https://user-images.githubusercontent.com/26548454/74082205-115e4b00-4a9b-11ea-9da0-3faef91087af.png">

ID (log entry) | session ID | timestamp | payload (info about application On whats’ going on)

<img width="925" alt="스크린샷 2020-02-08 오후 4 35 30" src="https://user-images.githubusercontent.com/26548454/74082207-128f7800-4a9b-11ea-8ad0-93aea51bd6e4.png">

이제 로그를 생성하는 머신이 2개이므로, 2개 각각에서 생성되는 로그를 어떻게 합칠 것인지 봐야 한다. 여기서는 두 개의 session ID값이 같기 때문에, 이걸 활용할 수 있을 .

<img width="924" alt="스크린샷 2020-02-08 오후 4 37 45" src="https://user-images.githubusercontent.com/26548454/74082209-13c0a500-4a9b-11ea-8f9a-c0bd2deeea8a.png">

각각의 서버에서 로그파일 받은 뒤, append + transform + output log file 생성하는 logging Server를 생성한다. 하루 단위로 통합.


<img width="925" alt="스크린샷 2020-02-08 오후 4 41 55" src="https://user-images.githubusercontent.com/26548454/74082210-14593b80-4a9b-11ea-9f9c-d167f1655cd0.png">


두 개의 로그를 통합하는 게 Sizing 과정에서 매우 중요함. 일단 이 정도 로그 사이즈는 나쁘지 않다. 이후에 measurement을 정의할 때 유용하게 쓰일 예정

---
