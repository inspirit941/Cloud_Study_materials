## Things for Post Cloud Native

이제는 클라우드를 적용하는 기업이 많이 늘었고, 클라우드로 전환해서 효과를 보고 있는 기업도 있다. 아직까지는 '전환'에 전체적인 방점이 찍혀 있다고 볼 수 있지만, 변화는 서서히 일어나고 있다.

그렇다면 클라우드 '전환' 다음 단계는 무엇일까? Cloud Native의 의미는 무엇인지, Cloud Native의 끝은 무엇일까?

<img width="1513" alt="스크린샷 2021-11-18 오후 2 18 16" src="https://user-images.githubusercontent.com/26548454/142356436-2fe1acb8-05ac-4295-b71e-0c5991092000.png">

클라우드를 적용하는 정도, 수준을 진단해볼 수 있는 지표로 CMMI가 있다.

- Level 1 : 불확실한 상태에서 PoC 또는 가볍게 시도해보는 정도의 단계. '찍먹'
- Level 2 : 도입을 조금씩 확대해가는 단계.
- Level 3 : '표준화' 단계. 개발자 사이에서의 약속이 확립되는 시기라고 보면 된다. 개발 플랫폼이나 개발 언어로 무엇을 사용할 것인지 규칙이 정해지는 단계.
- Level 4 : 표준이 정해졌으니 누가 얼만큼 사용하고 있는지 파악해야 하기 때문에 '측정'이 중요해지기 시작하는 단계.
- Level 5 : 표준화되어 있던 프로세스 자체를 개선하려는 시도가 등장하는 단계.

Level 3. 즉 '표준'이 되었다고 말할 만한 단계가 되려면 '제공하고 있는 서비스 중 클라우드 기반으로 동작하는 서비스의 비중'을 확인하면 된다. 50%를 넘으면 Level 3이라고 생각하면 됨.


![스크린샷 2021-11-18 오후 3 54 02](https://user-images.githubusercontent.com/26548454/142366873-87c126de-cf11-4f8e-b257-1fabe33aeee5.png)

Level 4.

회사 내부에서 클라우드로 전환되는 것들이 많아질수록, 이런저런 이슈가 많이 발생한다. 
- '효율적으로 쓰고 있는 게 맞나?' 라는 의문이 들고,
- 효율을 파악하기 위해 측정하고 기록하기 시작하는 단계.
- 카카오는 각 클러스터의 cpu / memory / network 사용량을 토대로, 여유가 있을 때 새로운 프로세스를 실행하도록 하는 "Black Pearl" 이라는 제품을 개발해 쓰고 있음.
  - 유휴 리소스를 측정하고, 자동으로 알림을 주고, 불필요한 경우에는 suspend / delete를 진행해 주고 있음.


![스크린샷 2021-11-18 오후 3 59 20](https://user-images.githubusercontent.com/26548454/142367550-1f8575e7-8f08-44e7-91bd-880ce099ea3b.png)

Level 5.

측정된 것들을 토대로 '효율'을 보다 깊게 고민하게 되는 단계.
- 네트워크 아키텍처, 시스템 구조, 데이터 시스템 등을 다시 들여다보는 단계.
- 오픈소스에만 의존하는 대신, **필요한 제품을 직접 개발해 사용하는 단계.**




![스크린샷 2021-11-18 오후 4 01 57](https://user-images.githubusercontent.com/26548454/142367837-13eab43e-f185-4b8e-acee-80780e89c193.png)

필요한 제품을 직접 개발해 쓰는 단계까지 온 이유? -> 관리할 게 너무 많았다. 
- 카카오는 컨테이너 숫자만 100만 개. 리소스에 직접 로그인해서 log를 보는 등의 작업을 할 수 없음.
- 클라이언트의 요청을 MSA로 처리 -> 요청 처리 과정에서 생산되는 데이터 양을 감당할 수 없을 만큼 많아짐.


![스크린샷 2021-11-18 오후 4 13 26](https://user-images.githubusercontent.com/26548454/142369489-ad8b29b6-027b-4e4a-9b4c-eb27a4d120fa.png)

Resource / Dependency 관리를 위한 SaaS 개발.

- 멀티 클러스터 + 멀티 서비스 형태로 운영 -> 모니터링을 위한 서비스 (SaaS) 개발
- 멀티 클러스터 + 멀티 서비스 형태로 배포할 수 있는 SaaS 개발.


<img width="1483" alt="스크린샷 2021-11-18 오후 4 24 21" src="https://user-images.githubusercontent.com/26548454/142370776-d41f068d-4e61-4d12-a525-3354d0dc9581.png">

Data 관리를 위한 SaaS 등장
- 대표적이고 기본적인 RDB
- Key-value DB
- Time series DB
- log stream - threshold 기준치 이상 시 알림이라던가..

그라파나 등 기존의 모니터링 서비스와 연계될 수 있는 형태의 As a Service 등장.

특히 Time Series DB의 경우 오픈소스의 복잡도가 높고, 비용을 요구하는 경우가 많아서 내부에서 개발.

<img width="1467" alt="스크린샷 2021-11-18 오후 4 24 29" src="https://user-images.githubusercontent.com/26548454/142370773-95f68336-7811-40f7-9c14-db306d0c3771.png">


기존 서비스들을 Event 기반으로 연결하기 위한 Event Pub/Sub 서비스의 등장.
- 개발자가 모든 event를 직접 관리하는 대신
  - 담당하는 프로덕트에서 만드는 이벤트를 publish하고
  - 필요한 이벤트만 subscribe하는 형태로 점차 움직일 것.

카카오의 경우 내부적으로 여러 서비스의 이벤트를 KEAP이라는 pub/sub을 토대로 연결하고 있음.


<img width="1461" alt="스크린샷 2021-11-18 오후 4 24 38" src="https://user-images.githubusercontent.com/26548454/142370770-a23a789d-f965-4c0d-819c-3b50a03b7066.png">


결과적으로, As a Service 형태의 프로덕트가 만들어지고, 서비스들을 연결하기 위한 As a Service가 만들어지는 패턴이 발생한다.

클라우드 기반, 컨테이너 기반의 프로덕트를 만들 때 
- 어떻게 개발할 것인가
- 어떻게 관리할 것인가

를 고민하면서 나아가다 보니 도달하게 된 흐름이라고 생각함.

<img width="1472" alt="스크린샷 2021-11-18 오후 4 24 48" src="https://user-images.githubusercontent.com/26548454/142370753-ad4142d2-8d66-485b-9cd2-c6eb70d720d0.png">

결론적으로, Cloud Native 흐름이 이어질 때의 종착지는 "As a Service" 의 조합과 연결이 된다고 생각함.

On Premise에서 개발하던 프로덕트건, Public Cloud에서 사용하던 프로덕트건 결국 연결하고 조합해서 사용하게 될 것이고, SaaS Mixture Computing 형태가 Cloud Native Computing의 최종 모습일 것이다.

물론, SaaS Mixture Computing이 보편화된 시대가 오면, 그 시대에 적응하기 위한 개발 방법이나 논의가 이루어질 것이다. 

지금 Cloud Native의 성숙도를 판단하기 위한 CMMI 지표가 있는 것처럼, 그 시대의 성숙도를 판단하기 위한 지표로 다시 CMMI 지표를 사용할 수도 있을 것이다.


https://if.kakao.com/session/34
