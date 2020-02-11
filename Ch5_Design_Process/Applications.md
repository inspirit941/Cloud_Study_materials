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

## intermittent Outages


<img width="856" alt="스크린샷 2020-02-09 오전 11 51 11" src="https://user-images.githubusercontent.com/26548454/74095703-d827e880-4b37-11ea-850b-329d962d093d.png">

서비스가 제대로 작동하지 않는 상황. 랜덤하게 발생하는 이슈였는데, 점점 빈도가 잦아져서 사용자가 불편함을 느낄 정도라고 해 보자. 뭐가 문제일까.

<img width="923" alt="스크린샷 2020-02-09 오전 11 53 08" src="https://user-images.githubusercontent.com/26548454/74095706-dc540600-4b37-11ea-88b9-cfc32b2e8470.png">

Troubleshooting결과 persistent disk on application server cannot keep up with the scale of demand. 이런 경우는 VM의 cpu 파워만 올리는 걸로는 한계가 있기 마련이다. Scale up을 진행할 때, file system에서 제대로 파일 control을 하기 어려워하는 문제.

결과적으로 Capacity issue.

해결책으로 local file system에 저장하던 데이터를 GCS로 바꾸기로 . 로컬에서 파일을 불러오는 게 아니기 때문에, 이제 latency가 발생할 수 있다.


<img width="927" alt="스크린샷 2020-02-09 오전 11 56 29" src="https://user-images.githubusercontent.com/26548454/74095708-dd853300-4b37-11ea-92cc-4fc63922c009.png">

SRE 관점에서 해야 할 일 중 하나 = Error Budget. 에러 발생이 이 범위를 벗어나지 않도록 해야 한다. SRE 팀에서 이걸 관리하지만, 허용범위를 너무 많이 벗어날 경우에는 아예 서비스 잠깐 내리고 점검하는 게 낫다. Firefighter가 상시대기 상태로 있지만, 그렇다고 24시간 내내 불끄러 다니지는 않듯.


---
## Challenge #2 : Complication 

또 시스템을 바꿨으니, 로그 시스템도 바뀌어야 한다.



<img width="928" alt="스크린샷 2020-02-09 오후 12 15 42" src="https://user-images.githubusercontent.com/26548454/74095730-0ad1e100-4b38-11ea-897a-6dc665301f04.png">

2개의 sets of logs. Webserver + App log, Webserver + Data storage log. 두 개의 로그를 통해 앱 서버에 문제가 있었는지, 데이터 스토리지에 문제가 있었는지 확인할 수 있다.

로그 두 개를 만들어 troubleshooting하는 방식이 있다. 대신, 이렇게 하게 되면 logging server의 저장공간이 부족해진다. 그전까지는 single VM을 사용했지만, persistent drive로는 부족함.

<img width="923" alt="스크린샷 2020-02-09 오후 12 18 46" src="https://user-images.githubusercontent.com/26548454/74095732-0f969500-4b38-11ea-8e4d-7269d875c35c.png">

-> logging 서버도 그냥 storage에 쓰면 되지 않나? 라고 생각할 수 있지만, log의 format을 보자. Indexable, relational or index based data storage 형식이다. 그러면 BigTable도 괜찮은 선택지다.

Logging Storage에 필요한 사항들을 생각해보면
* Fast data ingest 지원. & scalability
* low latency & indexable
* session key : all values 형태로 데이터를 넣을 수도 있음

= BigTable 사용 가능

<img width="927" alt="스크린샷 2020-02-09 오후 12 23 22" src="https://user-images.githubusercontent.com/26548454/74095733-10c7c200-4b38-11ea-820b-68edf401feb7.png">

따라서, Logging Server가 ingest -> append -> transform 하는 과정 자체는 유지한 채 (transform 방법은 달라질 수 있겠지만) 저장을 local 대신 BigTable에 저장하는 형태로 변경할 수 있다.

물론 dataflow를 사용할 수도 있긴 하지만, 그렇게 되면 logging system 전체를 뜯어고쳐야 함.

---

## Periodic Slowdown in Application 

특정 상황에서는 속도가 매우 느리다가, 어느 순간에는 다시 빨라지는 상황.

<img width="920" alt="스크린샷 2020-02-09 오후 2 22 08" src="https://user-images.githubusercontent.com/26548454/74211086-b498a580-4cd1-11ea-836d-822f4f73021c.png">

협력 안 하는 회사를 가정한다면, 위와 같은 모양새가 나온다. Web팀은 App에 문제가 있다고 보고, App 팀은 Web server에 문제가 있다고 생각함. Operation team은 단지 deployment와 production에만 관여했기 때문에, 두 팀 중 어디가 문제인지 확인할 방법이 없음


<img width="926" alt="스크린샷 2020-02-09 오후 2 24 37" src="https://user-images.githubusercontent.com/26548454/74211092-ba8e8680-4cd1-11ea-8f30-1ddad4e84176.png">


사람 탓하지 마라. 사람은 잘못이 없다. 보통은 세 개 - system, processes, behavior - 중에 원인이 있다.



<img width="921" alt="스크린샷 2020-02-09 오후 2 38 30" src="https://user-images.githubusercontent.com/26548454/74211093-bbbfb380-4cd1-11ea-9928-65ae0b693f57.png">

나중에 비슷한 일이 발생했을 때를 대비한 report 제작. Recovert process에서 필수적으로 만들어둬야 한다.



<img width="924" alt="스크린샷 2020-02-09 오후 2 39 53" src="https://user-images.githubusercontent.com/26548454/74211101-bfebd100-4cd1-11ea-8f65-12a5cca5a8c0.png">


사용량 많을 땐 cpu 사용량이 100%여서 그렇다는 결론.
cf. 다만, cpu 사용량은 SLI로 사용할 수 없다.

어쨌든 scalability issue인 건 맞음. 백엔드의 썸네일 프로세싱 작업을 수행하는 부분의 scale이 필요한 상황.


<img width="924" alt="스크린샷 2020-02-09 오후 2 41 33" src="https://user-images.githubusercontent.com/26548454/74211102-c11cfe00-4cd1-11ea-96f3-c17b0432e939.png">


MSA의 장점이 드러나는 부분인데, storage를 GCS로 isolated해둔 상태이므로, same code 그대로 여러 instnace에 적용할 수 있다. Upload server와 썸네일 처리하는 서버 사이에 internal load balancer를 두는 식으로. 해당 cpu 사용량의 80%를 넘으면 traffic distribution을 시행하도록 작업할 수 있다.

<img width="924" alt="스크린샷 2020-02-09 오후 2 52 12" src="https://user-images.githubusercontent.com/26548454/74211104-c24e2b00-4cd1-11ea-9af1-e431b619f101.png">



다만, 이 작업을 수행한다고 해서 SLI나 SLO가 바뀔 일은 없다. 여전히 주된 measurement는 end-to-end latency, error rate일 거다.


---

## Challenge #3. Growth

다시 Logging 문제. Load balanced auto scaling server가 등장했다는 건, 이제 여러 대의 서버에서 동시에 log 데이터가 발생한다는 걸 말한다. 이걸 어떻게 처리할 것인지?

<img width="925" alt="스크린샷 2020-02-09 오후 2 57 56" src="https://user-images.githubusercontent.com/26548454/74211039-85823400-4cd1-11ea-95d8-2b32a4d6db50.png">

해결책 : logging server에도 load balancer를 달고, multiple instance로 처리하자.

<img width="927" alt="스크린샷 2020-02-09 오후 3 07 37" src="https://user-images.githubusercontent.com/26548454/74211032-7bf8cc00-4cd1-11ea-9680-d177de1b6dd5.png">


---

## Out of service!

서비스가 죽은 경우.

- 가정: 모든 백엔드 서버가 single zone + region. Zone이 잠깐 죽어버린 상황.
-> 사람 문제나 business logic 문제가 아니다. Design problem.


<img width="923" alt="스크린샷 2020-02-11 오후 1 43 32" src="https://user-images.githubusercontent.com/26548454/74213165-5cff3780-4cdb-11ea-8cf0-ef3504002c76.png">

1. 책임자를 한 명 선정. 이 사람의 총괄로 작업을 처리할 수 있게끔 한다. 적임자를 정하거나 on-call rotation 등등.
2. Identify teams that are going to be affected. Establish exactly who the key individuals from those teams are. 어중이떠중이 다 모여서 같은 작업 반복하는 일은 피해야 한다
3. Postmortem report 준비. (사후보고서)


<img width="923" alt="스크린샷 2020-02-11 오후 1 44 14" src="https://user-images.githubusercontent.com/26548454/74213169-64bedc00-4cdb-11ea-8384-505702cd9f0f.png">

Multiple Zone으로 server 분리하는 작업. Cloud load Balancing에서 natively support it.


<img width="921" alt="스크린샷 2020-02-11 오후 1 48 07" src="https://user-images.githubusercontent.com/26548454/74213174-67b9cc80-4cdb-11ea-96e6-6ae0f49f31ff.png">


SLI나 SLO는 바뀌지 않는다. User experience는 변하지 않기 때문.


<img width="922" alt="스크린샷 2020-02-11 오후 1 48 41" src="https://user-images.githubusercontent.com/26548454/74213177-6a1c2680-4cdb-11ea-8ab2-3201741133d4.png">


Overload 문제로 서버가 죽는 경우. Upload server의 single point of failure 문제다.

<img width="924" alt="스크린샷 2020-02-11 오후 1 51 08" src="https://user-images.githubusercontent.com/26548454/74213235-aea7c200-4cdb-11ea-8b5c-c4a9b10c3166.png">

Frontend Server Scale. 백엔드 서버에서는 Network Load balancer를 썼지만, frontend에서는 HTTP load balancer를 써야 한다. Presentation Layer (web based)에서 오는 요청이기 때문.

Multiple upload server가 작동하려면, servers should be stateless. Single server면 모든 걸 추적할 수 있지만, multiple server에서는 tracking 작업이 매우 복잡하기 때문.



<img width="924" alt="스크린샷 2020-02-11 오후 1 54 07" src="https://user-images.githubusercontent.com/26548454/74213243-b4050c80-4cdb-11ea-8e24-5fa66afb0400.png">

Overload 문제 해결작업을 수행했으면 test를 해봐야 한다. 사실 자금여유 있으면 production에서 발생할 수 있는 상황과 동일한 테스트 해보는게 이상적. Preemptible VM that last for 24 hours -> easily clone and do automated deployment of an isolated environment.



<img width="922" alt="스크린샷 2020-02-11 오후 1 57 04" src="https://user-images.githubusercontent.com/26548454/74213245-b5363980-4cdb-11ea-961d-49f565352c6e.png">

Stateless Server 만들기. = break the state out of upload server. 따라서 isolated state로 프로세스를 분리하는 작업이 필요하다.


<img width="923" alt="스크린샷 2020-02-11 오후 1 58 23" src="https://user-images.githubusercontent.com/26548454/74213246-b5ced000-4cdb-11ea-8f02-8ac447b777f4.png">

State를 분절한 다음 저장하는 것 -> GCS로 처리할 수 있다. 


<img width="923" alt="스크린샷 2020-02-11 오후 2 00 17" src="https://user-images.githubusercontent.com/26548454/74213249-b6fffd00-4cdb-11ea-9e39-1420ae185c15.png">


매번 작업할 때마다 SLI / SLO 확인해봐야 한다. 이제 Single upload server에서 벗어났으므로 availability는 이전보다 상승할 수 있다. Maintain 99.9% availability를 하기 위해서는 deployment 방법을 바꿔야 하고, deploy 과정에서의 downtime도 원치 않으면 downtime budget은 only 43 min per month.

---

## Challenge #4. Redesign for time

서버가 crashed되면, troubleshooting에 시간이 오래 걸린다. Aggregating log need for troubleshooting도 그렇고, 여러 곳에서 꼬리물듯 문제가 계속 터지면 그 로그들도 aggregating하느라 시간이 더 걸린다.

Log system redesign, to eliminate the bottlenecks?


<img width="927" alt="스크린샷 2020-02-11 오후 2 05 17" src="https://user-images.githubusercontent.com/26548454/74213250-b7989380-4cdb-11ea-8453-fdb1ef40b887.png">


현재의 로그 시스템은 24시간 delay가 존재함. downtime을 43 min 이하로 줄이기 위해서는 어떻게 구조를 바꿔야 할까?


<img width="925" alt="스크린샷 2020-02-11 오후 2 06 31" src="https://user-images.githubusercontent.com/26548454/74213251-b8c9c080-4cdb-11ea-9405-c1fa16ba6fc2.png">


12 factor 요소 중 하나가 ‘treat logs as event streams’ 였다. log를 batch process로 처리하는 방법은 service troubleshooting을 처리해주지 못함.


<img width="928" alt="스크린샷 2020-02-11 오후 2 13 16" src="https://user-images.githubusercontent.com/26548454/74213253-b9625700-4cdb-11ea-8a0c-f03885c2ac24.png">


Dataflow를 사용할 수도 있지만, 이 서비스의 담당자는 java에 익숙함. Nodejs로 변경하기에는 어려움. Microprocessing Design을 적용해보자.

모든 데이터 로그를 Cloud pub / sub로 보낸다. 여기에 cloud function을 붙여서 처리하면 사실상 realtime으로 작업이 가능해진다. function으로 처리한 작업은 다시 pub / sub을 타고 BigTable로 저장되도록 flow를 생성.

Stream processing으로 변환하면서 scalability도 확보.


---


## Intentional Attack

<img width="928" alt="스크린샷 2020-02-11 오후 8 34 47" src="https://user-images.githubusercontent.com/26548454/74234853-2512e700-4d11-11ea-9566-18ab75bc7e3a.png">

해커의 공격이 있다고 가정할 경우, 두 가지 중요한 이슈를 해결해야 한다.

1. How does the system keep users data private
2. How does the system protect against a DoS attack.



해커가 공격한 정황이 보인다면
- Design 방법을 토대로 현재 어떤 방어조치가 취해져 있는가.
- 데이터가 위험하지 않도록 추가로 보완할 사항은?
- what additional design changes will reduce the “attack surface”?


<img width="926" alt="스크린샷 2020-02-11 오후 8 38 44" src="https://user-images.githubusercontent.com/26548454/74234860-293f0480-4d11-11ea-96f2-598d2450e259.png">


현재 시스템 구조만 놓고 보면, 딱히 위협이 될 상황은 없다. Bulit-in security with the network, Global load balancing and Network load balancing. 하지만 뭐, 아직 internal IP address나 private network, firewall 등은 다루지 않은 상태.



<img width="924" alt="스크린샷 2020-02-11 오후 8 41 07" src="https://user-images.githubusercontent.com/26548454/74234861-2a703180-4d11-11ea-8b98-2268a887584f.png">


Firewall rule 설정이 없으면 port open은 불가능하다. 물론, 기본적으로 firewall rule은 default로 설정되어 있긴 하지만.



<img width="922" alt="스크린샷 2020-02-11 오후 8 44 52" src="https://user-images.githubusercontent.com/26548454/74234864-2b08c800-4d11-11ea-8ab2-676b96e01287.png">

DDoS 공격이 왔다.
1. 현재 방어상태는 어떤지
2. 공격 방어하기
3. Evolve the design to protect against DDoS.


<img width="924" alt="스크린샷 2020-02-11 오후 8 46 01" src="https://user-images.githubusercontent.com/26548454/74235206-d3b72780-4d11-11ea-8640-8e0029e72e3b.png">



* 일단 Google CDN을 쓴다. 
-> 구글이 제공하는 전 세계 120여 개의 Edge에 썸네일과 static 데이터를 캐시한다. 
* Google DNS 적용. 100% uptime (Dyn DNS)


<img width="923" alt="스크린샷 2020-02-11 오후 8 48 51" src="https://user-images.githubusercontent.com/26548454/74235222-d9147200-4d11-11ea-8600-dead070de7d8.png">

* Implement Autoscale. Managed instance group을 사용하고 있으므로 handle fail levels이 가능함. 따라서 공격으로 서버까지 접근했으면 Autoscale 작업으로 개별 서버에 들어가는 부하를 줄인다.



<img width="919" alt="스크린샷 2020-02-11 오후 8 50 31" src="https://user-images.githubusercontent.com/26548454/74235225-d9ad0880-4d11-11ea-8cbb-1614c902f2ee.png">


프론트 쪽은 이렇게 막았다고 치자. 하지만 현재 설정만으로는 백엔드가 취약하다. 아무런 보안장치를 해두지 않았으니까. 우회해 들어올 경우의 해결방안은?



<img width="924" alt="스크린샷 2020-02-11 오후 8 56 00" src="https://user-images.githubusercontent.com/26548454/74235229-da459f00-4d11-11ea-9de0-c3ca9ff7b2af.png">


백엔드 서버들을 internal network로 바꿔버리면 된다. 백엔드 서버에 접근하려면 반드시 upload server를 통하게끔 만들어놓으면 됨


<img width="924" alt="스크린샷 2020-02-11 오후 8 56 30" src="https://user-images.githubusercontent.com/26548454/74235233-dade3580-4d11-11ea-8fa5-d02548cabed2.png">

기타등등 취할 수 있는 기능들.


## Challenge #5. Defense in Depth

Log에 사용자 정보와 event 정보가 기록된다. 만약 로그 서버가 보안이 취약하면, 데이터 다 뚫림.

<img width="924" alt="스크린샷 2020-02-11 오후 9 05 54" src="https://user-images.githubusercontent.com/26548454/74237520-15969c80-4d17-11ea-9ca1-d55db18541ed.png">


<img width="922" alt="스크린샷 2020-02-11 오후 9 06 56" src="https://user-images.githubusercontent.com/26548454/74237526-1a5b5080-4d17-11ea-935c-b72f448560cd.png">



해결책.
- Web Server / App Server가 logging server로 데이터를 보낼 때 IAM으로 Service Account를 사용한다.
- Logging Server에서 bigtable로 데이터를 전송할 때 Service Account를 사용한다.

- Private Network를 사용한다.
	* Web, Data storage, App log 생성하는 세 개를 전부 private network로 분리한 다음, 셋을 하나의 VPC로 묶는다. 이 세 개는 각각 통신할 이유가 딱히 없으므로 isolation 해도 괜찮음.
	* logging server와 통신할 수 있게 한다.



#컴퓨터공학쪽지식/Coursera/GCP/ch5_infra_design_process/application