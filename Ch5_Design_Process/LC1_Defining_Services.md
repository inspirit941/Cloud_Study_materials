# Design and Process
실제로 How to start, utilize a design and process the follows the best practices.

<img width="924" alt="스크린샷 2020-02-06 오후 1 55 40" src="https://user-images.githubusercontent.com/26548454/74001768-2316f400-49b0-11ea-8e45-96875d3172ae.png">


<img width="921" alt="스크린샷 2020-02-06 오후 2 05 01" src="https://user-images.githubusercontent.com/26548454/74001843-683b2600-49b0-11ea-86ae-53f562ac69d3.png">

강의 구성

1. Lecture, introducing architect concepts and principles.
2. Application of those principles to a real world design
3. Related application problem.
4. Compare it with standard solutions

---
## Lecture 1. Defining the Service

### Overview

<img width="927" alt="스크린샷 2020-02-06 오후 2 15 54" src="https://user-images.githubusercontent.com/26548454/74001854-6cffda00-49b0-11ea-9cc2-3b55b36de9eb.png">

Automated Deployments are the foundation of SRE and design process. 강의보다는 lab 형태로 가르쳐야 하는 부분.

### Module Overview.

* State, measurement, and requirement (Design과 Cloud Architecture에 가장 중요한 세 가지 Concept)

1. Defining the Service
처음엔 Rough하게 시작해라. 원래 처음에는 아무리 경험있고 경력있어도 다 비슷한 출발선이다. Involve the team going through that design process -> take a more structured design approach. 

몇 가지 질문으로 계속 생각을 다듬고 정리한다.
	- Is this going to handle Specific Scenarios?
	- Do we have proper budeget? Etc

Define measurable instruments that we allow us to define.
	- Are we succeeding the goals that we’ve set out?
	- What are exactly our service level objectives, and how do we create service level indicators to measure those?

등등을 거친 뒤, Three-tier Architecture로 넘어간다.

2. Three-tier Architecture

<img width="927" alt="스크린샷 2020-02-06 오후 2 26 30" src="https://user-images.githubusercontent.com/26548454/74001857-6ec99d80-49b0-11ea-92f4-265972f33f42.png">

* Presentation Layer : that’s the networking and you’ll notice everything Google, especially Google Cloud, nothing happens we don’t create a data center, without laying out that network, and as unfun as it may be, or especially if you’re inexperienced, this is something you have to really consider early on. (?)

* Business Logic : What exactly our service going to be? 어떤 종류의 component가 Logic의 어떤 부분을 담당해야 하는지.

* Data Layer : 데이터는 어떻게 되어야 하나? RDB? Static Storage? NoSQL? Global relational databases? 등등
보통 Business logic이 명확하고 어떤 요구사항이 필요한지 확실해지면, What our storage layer is going to look like도 금방 정해진다.

5. Resiliency, Scalability, DS

<img width="925" alt="스크린샷 2020-02-06 오후 2 31 39" src="https://user-images.githubusercontent.com/26548454/74001861-712bf780-49b0-11ea-9d29-23fa67c15ce5.png">

* Resiliency, scalability, disaster recovery

6. Security
그 다음으로 고민할 사항이 Security. 어쨌든 인터넷에 뭔가를 올리고 노출할 거면 보안은 매우 중요한 이슈다. 보통 이거는 anything goes online 이전에 built-in 해야 하는 process

단순히 protecting data만을 의미하는 게 아니다. Inadvertent attack 등에 견딜 수 있는지 (DoS 공격이라거나)

7. Capacity planning and cost optimization
예산 제약과 목적달성 사이의 균형잡기

8. Deployment, monitoring, alerting, incident response.

Deployment process는 뭘 쓸 건가 -> Continuous deployment? Blue-green deployment, Rolling deployment, Canary deployment 등등…

무엇을, 어떻게 Monitoring 할 것인가. 필요하면 Alert를 받을 건가? 문제 발생 시 어떻게 handle할 건가? -> proactive / reactive 항목을 정하는 문제.

<img width="912" alt="스크린샷 2020-02-06 오후 2 41 53" src="https://user-images.githubusercontent.com/26548454/74001863-72f5bb00-49b0-11ea-8b19-64ee3b4e0513.png">


유의점
- iterative process로 good idea가 탄생한다. 처음에 별로거나 잘 안 된다 해도 실망하지 마라
- No universal Solution. Only contextual solutions.
- Recency bias : tendency to grab onto new ideas, because it is hot and popular… (+try to use everything.)
새롭다고 다 뛰어들지 말고, Consider which designs and tools work best in which context.


<img width="920" alt="스크린샷 2020-02-06 오후 2 46 34" src="https://user-images.githubusercontent.com/26548454/74001864-7426e800-49b0-11ea-8f8a-40cd85398e31.png">

### Defining the Service : State and Solution

* State : any action in the system that depends on the memory of a preceding action.
* State information : data that must be remembered

이전 정보를 기억해야 할 경우 stateful, 이전 정보를 기억할 필요가 없을 경우 stateless라고 한다.

해당 시스템이 stateless / stateful 여부에 따라 디자인 자체가 달라지며, 특히 Where to Store state information, how to retrieve it, what to do if it’s lost를 결정할 때.

<img width="672" alt="스크린샷 2020-02-06 오후 2 59 10" src="https://user-images.githubusercontent.com/26548454/74001910-a6d0e080-49b0-11ea-8db5-e6c0fa21a74b.png">

State과 Solution에서부터 접근을 출발하는 게 좋다. state의 경우 모든 cloud-based design의 주춧돌이기 때문.

* Where state information is located in the system, and how it’s going to be maintained.

<img width="912" alt="스크린샷 2020-02-06 오후 3 01 35" src="https://user-images.githubusercontent.com/26548454/74001917-aafcfe00-49b0-11ea-9d83-acea099f6f38.png">

* Stateful (왼쪽)
장점: Easy to troubleShoot. (해당 부분에만 focusing하면 되기 때문. 이슈 발견도 쉽다.)
단점:  Scalabiliy 확장이 매우 어렵다. 어디 하나만 잘못되어 시스템 전체가 박살남 (single point of failure)

* Stateless (오른쪽)
Assembly line 같은 시스템. 

장점 : scale도 용이하면서 troubleshooting하기도 편하다.
단점: 중앙화된 형태의 시스템이 stateless와 결합할 경우, 어느 한 부분만 Fail이 발생해도 시스템 전체가 박살나게 될 개연성이 크다.
(작업에 필요한 모든 데이터가 한 곳에만 있을 경우… 데이터 요청 과정에서 혼선이 생기지 않아야 하고, 수많은 종류의 데이터 요청이 들고나는 과정에서 fail이나 problem이 생기는 순간, 중앙화된 데이터 시스템 자체가 Single point of Failure로 작동할 수 있다.)


<img width="912" alt="스크린샷 2020-02-06 오후 3 05 45" src="https://user-images.githubusercontent.com/26548454/74001919-acc6c180-49b0-11ea-916c-ef99f888a40b.png">

데이터가 Centralized인 경우… (Centralized Ctrl System 사용 시) -> 그 자체로도 choke point나 single point of failure로 작동할 가능성이 있다. (Ex -> data discrepancy나 DB corruption 발생 시 대안이 없다.)

따라서, Storing Stateful information이 중요한 이슈가 됨.

<img width="911" alt="스크린샷 2020-02-06 오후 3 09 34" src="https://user-images.githubusercontent.com/26548454/74001920-ad5f5800-49b0-11ea-89fd-f53ea2c3da19.png">

결론적으로, State는 ‘No state’가 최상이다. 
- Workers를 새로 부여하기도 쉽고
- task relocation도 용이하며
- fault tolerance, recovery에서 강하다

Source of State (어디에 저장할 것인가)
-> 목적 따라 알아서. 메모리에 저장하는 경우는 보통 ‘세션’같은 것들. Tracking Cookie같은 경우라면 key-value 자체.

Critical State
What is the best way to implement and manage it?


<img width="915" alt="스크린샷 2020-02-06 오후 3 27 09" src="https://user-images.githubusercontent.com/26548454/74001921-ad5f5800-49b0-11ea-9c1c-fcd28d55938b.png">

하지 말아야 할 것 1. Hotspot

예컨대 Frontend Server에 state storing 작업을 해뒀을 경우.
-> load balancing system이 항상 완벽할 수는 없다. Stateful transaction이 특정 frontend에 몰릴 경우 overloaded될 가능성이 높음. 
(Same User Request는 같은 frontend에서 처리할 수밖에 없는 구조이기 때문)

<img width="913" alt="스크린샷 2020-02-06 오후 3 34 15" src="https://user-images.githubusercontent.com/26548454/74001922-adf7ee80-49b0-11ea-87f2-043de3adfd66.png">

따라서 state 처리 자체를 백엔드에 두는 게 안정적이다. 
여기서 생각할 수 있는 방법 중 하나가
* Master State -> keep track of everything을 두고, Cache it해서 사용하는 방법.

단, 캐시된 데이터가 Master state와 일치하지 않는 경우 (outdated) 문제점이 발생할 수 있다. 

<img width="908" alt="스크린샷 2020-02-06 오후 3 37 00" src="https://user-images.githubusercontent.com/26548454/74001923-ae908500-49b0-11ea-9faf-ef61c165d1a1.png">

State 자체를 distribute 하는 경우.
- Cloud Load balancing의 기능을 그대로 사용할 수 있다. replication을 만드는 것
- 여기서도, additional latency는 존재한다. 따라서 replication 간 state가 달라졌을 경우 무엇을 truth로 봐야 하는지… 를 고려해야 하는데, 이 문제 자체도 꽤 이슈가 됨

그럼에도 불구하고 이전까지 발생했던 문제들을 다수 해결할 수 있는 방법임.

<img width="906" alt="스크린샷 2020-02-06 오후 3 41 27" src="https://user-images.githubusercontent.com/26548454/74001925-afc1b200-49b0-11ea-9327-19e34337ed14.png">

신뢰할 만한 만병통치약 (Penacea). 물론 모든 경우에 맞아떨어지는 건 아니고, 대부분의 경우 통하는 방식

1. Frontend (Cloud DNS 등) + cloud load balancer
2. Stateless Server. 이 서버는 State를 저장하지 않기 때문에 can fail very quickly. 
강사는 여기를 preemptive server (up to 80% discount) 활용하라고 하는데, ‘interrupted anytime within 24 hour period 상황에서 service가 돌아가도록 만드는 방법’을 고민해야 한다. 
-> 이 방법을 쓰려면, static stateful Cluster (dedicate resources to) 를 백엔드에 몇 개 설정한다. 이렇게 될 경우, 많은 백엔드 서버를 preemptive로 만들어도 동작한다.

이렇게 생성할 경우
장점: no single point of failure, Scalable (no state required), easy to troubleshoot application code.

단점: understanding application logic. 워낙 거쳐가는 통신이 많기 때문. 하지만 state만 보겠다면 dedicated cluster maintaining state만 보면 된다. Sharded, replicated된 state information을 저장하고 있기 때문.

이 디자인이 현재 구글에서도 쓰이는 방식.

---
### Defining the Service : Measurement

Measurement : Key to creating a stable, manageable system. 
Architect는 단순히 design + implement만 하는 게 아니라 stick around for some time after the implementation to stabilize system + make sure it is operated / maintained.

바닥부터 designing을 하게 된다면, identifying indicators to be measured / objectives to compare them against.

<img width="914" alt="스크린샷 2020-02-06 오후 4 08 40" src="https://user-images.githubusercontent.com/26548454/74002111-5efe8900-49b1-11ea-826d-c33e46ed692b.png">


* Service Level : Tell your users ‘what can you expect from this service in terms of reliability and performance’ 를 말함.

Service Level는 크게 세 가지.
1. Service Level indicator (SLI) : 웹페이지 속도나, 사용자의 action 시 웹페이지의 반응속도 등등
2. 해당 SLI의 threshold of pain (Service Level Objective - SLO). 즉 어떤 지점에서 사용자가 ‘this service works properly’라고 느끼는지 정의하는 것.
3. 특정 서비스는 Formal business agreement가 provider / user 사이에 존재할 수 있다. (Guarantee a specific behavior, compensate the user if the service fails to meet this expectation). -> SLA (Service Level Agreement)

<img width="908" alt="스크린샷 2020-02-06 오후 4 10 49" src="https://user-images.githubusercontent.com/26548454/74002115-63c33d00-49b1-11ea-9e9e-f6b777762dbd.png">

Service Level은 해당 서비스나 product가 어떤 일을 해야 하는지 정의한 것들이다. 이걸 정의하기 위한 항목들도 다양한 편
Ex) availability나 perform specification (99.99 uptime / min response time of 1 sec) 등

이걸 정의한다는 건, User의 expectation을 설정하고, Service Design 과정에서 이 기대치를 계속 유지한다는 milestone.

 1. SLI : 사용자가 직관적으로 볼 수 있고 측정할 수 있는 지표. 따라서 Internal System Metrics는 의미 없다. 
(시스템 사용량 같은 거. 시스템 사용량은 Service 품질에 영향을 주는 건 아니고, Auto-scaler가 consistent user experience를 제공하기 위해 확인해야 할 지표.)
 2. SLO : threshold value of SLI. 보통 lowest / poorest level of service를 말한다. 이 상황에서도 사용자가 ‘시스템이 정상적으로 작동한다’고 여길 수 있을 정도의 마지노선.
 3. SLA : SLO를 충족하지 못할 경우 사용자가 큰 손해를 볼 수 있는 시스템 (Air traffic ctrl이라던가..) 에서도 보장해야 하는 SLO 기준이라고 보면 된다. SLO와 달리 SLA는 contract이며, 이걸 어겼을 때에는 provider 측에서 사용자에게 배상해야 한다.

따라서 보통 provider는 SLO 기준을 지키려고 하기 마련. SLO를 지키면 SLA는 당연히 충족되기 때문

<img width="910" alt="스크린샷 2020-02-06 오후 4 20 35" src="https://user-images.githubusercontent.com/26548454/74002284-201d0300-49b2-11ea-849b-642586130523.png">



<img width="912" alt="스크린샷 2020-02-06 오후 4 21 47" src="https://user-images.githubusercontent.com/26548454/74002285-20b59980-49b2-11ea-886c-4203e3f5c3f6.png">

SLA. 아무튼 사용자가 측정할 수 있고 서비스 품질에 직접적으로 영향을 미치는 요소여야 함. Stick with values that are both meaningful to users / tied to the core functionality of the service.

-> What functions or behavior do the user care about?
-> How do the user Quantify a good / bad experience?


<img width="910" alt="스크린샷 2020-02-07 오후 12 36 57" src="https://user-images.githubusercontent.com/26548454/74002288-21e6c680-49b2-11ea-9cc0-3ca436b192c4.png">

SLI 설정에서 고려할 다른 사항들.
-> 정확히는 ‘User experience 입장에서의 지표’를 봐야 한다. 예컨대 Latency라고 하면, 사용자 입장에서의 Latency 측정을 위해서는 다른 시스템 지표들도 봐야 한다.

Latency 예시 -> latency of Load balancer + data server까지 포함. 사용자와의 인터넷 연결유무는 No visibility이니 제외한다 쳐도, Latency를 측정하기 위해서는 “frontend Load balancer -> data server -> 다시 frontend load balancer”까지 돌아올 때까지 걸리는 시간으로 보는 게 일반적이다.



<img width="910" alt="스크린샷 2020-02-07 오후 12 45 00" src="https://user-images.githubusercontent.com/26548454/74002291-227f5d00-49b2-11ea-8066-e2318f74110b.png">


SLO : the point you must do something to improve the reliability or performance of the service. 단지 fixing component만 의미하는 건 아니다. 문제 해결을 위해 devote engineering을 수행하거나, update 작업 등의 작업도 전부 포함.

SLA와 다른 점은, SLO는 user의 pain tolerance to performance or availability issues를 정의했다는 것. SLA는 Legal Contract로, 사용자에게 반드시 사전에 고지되어야 한다.


<img width="913" alt="스크린샷 2020-02-07 오후 1 00 44" src="https://user-images.githubusercontent.com/26548454/74002292-2317f380-49b2-11ea-9e22-285c48154971.png">

SLO가 반드시 Maximum performance를 지칭할 필요 없다. 비즈니스 레벨에서의 appropriate level of performance or reliability provider can offer without making the service too available or too responsive.

SLO 설정할 때 확인해야 할 SLA 4가지 golden monitoring signals: Latency, traffic, errors, resource saturation (usage). 예시처럼.


Error budget Methodology. 구글에서 시행하는 정책 중 하나. Service는 언제든 에러가 발생할 수 있으므로, 일종의 error budget을 설정한 뒤 해당 budget을 초과할 경우 outage (정전)으로 간주하는 것. 서비스의 목표는 ‘error 발생량이 budget 이내가 되도록’ 만드는 것. 매달 replenished.

아무튼 SLO 자체도 ‘user experience’ 기반으로 설정해야 한다. 예컨대 새벽 3시에 system unavailable 상태가 잠깐 된다 해도 사용자에게 아무런 문제가 없다면, 굳이 24-hour 내내 high-level의 성능보장을 강제할 필요는 없을 수도 있다.

<img width="925" alt="스크린샷 2020-02-07 오후 1 12 08" src="https://user-images.githubusercontent.com/26548454/74002465-7ab65f00-49b2-11ea-9ec9-f434d667bf17.png">

SLA. NOT a Minimun point at which a service is considered usable. 
Mission-Critical (반드시 성능보장을 해야 하며, 안 그랬을 경우 사용자가 손실 보게 되는 경우) 일 경우 보통 사용하며, 이 성능보장을 하지 뭇하게 될 경우 provider가 compensate.

*Not all Services have SLAs, But ALL Services should have SLOs*

cf. 사용자를 모르면서, 사용자를 위한 서비스를 어떻게 만드나? -> Marketing Concept for developing user interface 과정인 ‘User Persona’를 사용한다. 어떤 종류의 사용자가 이 서비스를 사용할지를 추상적 형태로 정의한 것.

User persona를 토대로 SLI와 SLO로 무엇을 정의할지 실마리를 얻을 수 있다.

---
### Defining the Service : Gathering Requirements

Objective가 뭔지 알았다면, 여기에 맞는 Requirement를 찾아야 한다.

<img width="926" alt="스크린샷 2020-02-07 오후 1 20 57" src="https://user-images.githubusercontent.com/26548454/74002475-8013a980-49b2-11ea-8a90-6b429217380f.png">

-> set up expectation, define and achieve end goals.


<img width="927" alt="스크린샷 2020-02-07 오후 1 37 43" src="https://user-images.githubusercontent.com/26548454/74002479-80ac4000-49b2-11ea-915c-b409a998e427.png">

-> defining how much time / data / users we will allow to be done.

사용자가 원하는 조건이나 기능에 맞게 resource를 어떻게 사용할 것인지

<img width="926" alt="스크린샷 2020-02-07 오후 1 39 51" src="https://user-images.githubusercontent.com/26548454/74002481-8144d680-49b2-11ea-9340-8f2a9cfe74b2.png">

Unexpected growth 발생 시 어떻게 대처할 것인지. What resource constraints are going to be important to pay attention to? (State / Data storage / resources (servers?)

<img width="927" alt="스크린샷 2020-02-07 오후 1 41 20" src="https://user-images.githubusercontent.com/26548454/74002484-81dd6d00-49b2-11ea-86e5-67b01a9253ed.png">

Overbuy product which may not necessary 방지 / grow 시 scaling 고려 등등.
Ex) MySQL로 출발할 경우 … 얘는 scale이 안 된다. Horizontal Scaling이 필요하다면 NoSQL이 더 나을 수도 있다. (Horizontal : Add more machine, Vertical : Add more Power)

---

