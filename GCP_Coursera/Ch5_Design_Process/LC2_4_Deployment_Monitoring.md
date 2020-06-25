# Deploying, Monitoring, Alerting, incident Response
## Overview

강의 내내 언급되던 사항이지만, system stabilize를 위해서는 needs to be surrounded by properly prepared and designed behavior.

Same Measures, discipline of iterative reviewing will also help determine when the circumstances have changed.

---

## Deployment

당연한 소리들 할 거다. Make a checklist, automate processes, use an infrastructure orchestration framework. 당연한 일이라고 과소평가하면 안 된다. Stable solution의 필수 요소이기 때문.



<img width="926" alt="스크린샷 2020-02-12 오후 1 18 56" src="https://user-images.githubusercontent.com/26548454/74306465-eaa75980-4da5-11ea-8d3a-a3b3e9fabf3f.png">


CheckList 만들기.

need to define our dependencies, any shared infrastructure, any external or third-party dependencies. 
Being able to plan for capacity, so verify that we’ve dealt with any overload handling procedures. 
We’re in plus two everywhere we can. Are there any single point of failures before we deploy?

Security and access control. Have we done a security audit, verify our attack shields? 

And then defining our roll out plan. We’re going to do gradual, will it be a staged or a phased rollout, or is it going to be for a percentage of users? 
How are we going to design maybe a canary deployment? So it could be blue, green, many different options here.


<img width="925" alt="스크린샷 2020-02-12 오후 1 21 11" src="https://user-images.githubusercontent.com/26548454/74306473-f004a400-4da5-11ea-9e24-c73572edfb53.png">

체크리스트 설정이 다 끝나면, Launch automation 작업.
* Reliability is the fundamental Features. And Reliability comes from consistency.
* self-service release process -> allows you to promote high velocity team that can create code and simply automatically deploy.
* Access Control. 필요한 사람에게 올바른 권한부여 했는지.


<img width="922" alt="스크린샷 2020-02-12 오후 1 27 51" src="https://user-images.githubusercontent.com/26548454/74306475-f1ce6780-4da5-11ea-89ce-c660e6e6dae8.png">



## Monitoring and Alerting


<img width="924" alt="스크린샷 2020-02-12 오후 1 36 45" src="https://user-images.githubusercontent.com/26548454/74306477-f266fe00-4da5-11ea-958b-681302c08368.png">

구글의 SRE pyramid. 맨 바닥에 Monitoring이 있다. Monitoring과 alerting이 있어야 incident에 반응하고 postmortem을 작성할 수 있을 것. 이걸 토대로 다시 testing -> deployment까지 이루어진다는 걸 감안했을 때, Monitoring과 alerting의 역할은 중요함.

* Reveals what needs urgent attention
* identify what trends exist, which will help with forecasting and planning
* identify any potential improvement.

- White box Monitoring : Actual System 자체를 monitoring하는 것.
- Black box Monitoring : 백엔드에 아무것도 없다고 가정하는 것. Customer facing point of view 관점.


2 Types of Metrics.


<img width="921" alt="스크린샷 2020-02-12 오후 1 42 38" src="https://user-images.githubusercontent.com/26548454/74306479-f2ff9480-4da5-11ea-905e-1e6969f4e337.png">

* Push base : send out alert이 전부임. 예컨대 디스크 꽉 찼으면 ‘디스크 공간 부족’이라는 push 알림을 보내는 식.
* Pull from the outside 

보통 push - pull을 periodically 반복한다고 함. 정상적으로 다들 잘 작동하고 있는지 확인하는 차원에서.


<img width="922" alt="스크린샷 2020-02-12 오후 1 43 56" src="https://user-images.githubusercontent.com/26548454/74306481-f3982b00-4da5-11ea-9420-b45753a91391.png">

Black box monitoring은 User experience에만 관심을 갖는다. 여기서 문제가 감지되면, white box monitoring으로 가서 business logic 어디에 문제가 생겼는지를 확인해야 한다.


<img width="923" alt="스크린샷 2020-02-12 오후 1 45 07" src="https://user-images.githubusercontent.com/26548454/74306483-f3982b00-4da5-11ea-9845-46d7ab2033e9.png">

White box는 individual service에 집중한다. 이 중 어느 business logic 부분에 문제가 있었길래 user experience 에 영향을 줬는지 확인함



<img width="924" alt="스크린샷 2020-02-12 오후 1 50 16" src="https://user-images.githubusercontent.com/26548454/74306484-f4c95800-4da5-11ea-9a61-3e87f8c745a6.png">

사람이 눈으로 보고 문제가 있다고 파악하는 식으로 운영하면 안 된다. 프로그래밍으로 어떤 condition이 fail인지 확인해야 함. 중대한 오류와 사소한 오류는 사람이 구분하는 것.

대개 이렇게 구분한다
- Alert : availability에 영향을 크게 주는 이슈, 사람이 빨리 처리해야 하는 것들
- Tickets : user experience에 바로 영향을 주지는 않지만, 사람이 보고 처리해야 하는 것들. 우선순위가 alert보다는 낮다
- logging : 일단 다 저장하도록 monitoring system에서 날림. Stack driver같은 곳으로. 나중에 진단하고 troubleshooting할 때 쓰도록



<img width="922" alt="스크린샷 2020-02-12 오후 1 53 47" src="https://user-images.githubusercontent.com/26548454/74306561-35c16c80-4da6-11ea-9d09-bb2de36bc063.png">

12 Factor를 GCP에서는 어떻게 디자인으로 적용할 수 있는가
* treat logs as event streams. -> stackdriver를 쓰면 log을 stream 형태로 사용할 수 있다. Queryable, BigTable이나 GCS로 넘길 수 있다.
* admin과 manage task를 one-off process로 처리해라 -> Service Account가 major function을 실행할 수 있게 권한설정을 해놓는 식으로. 사람에게 root 권한을 주는 게 아니라. 
얘도 stackdriver 써서 end-to-end 작업이 가능함. (Monitoring, error report, cloud tracing, debugging 등등.)


<img width="924" alt="스크린샷 2020-02-12 오후 1 56 40" src="https://user-images.githubusercontent.com/26548454/74306563-378b3000-4da6-11ea-9eb0-a04fa7e913f7.png">

Stackdriver는 collection of tools that are unified together.
App engine에서 error reporting, trace, debugging 다 가능하다.

stackdriver는 initial deployment의 경우 eventual consistency를 사용함. 따라서 처음에 VM을 인지하고 monitoring 시작하는 데 시간이 좀 걸린다.



<img width="921" alt="스크린샷 2020-02-12 오후 2 01 06" src="https://user-images.githubusercontent.com/26548454/74306565-3823c680-4da6-11ea-97de-161a7720b3b1.png">

얘 원래는 AWS에서 쓰려고 만든 3rd party 프로그램들 집합체임. 따라서 AWS connector 기능이 있다. 물론 separate account by itself, and separate authentication mechanism으로 연결해야 함


<img width="920" alt="스크린샷 2020-02-12 오후 2 03 06" src="https://user-images.githubusercontent.com/26548454/74306566-38bc5d00-4da6-11ea-8a1a-042f5c2fe21d.png">


Error Allocation for months 용도로 많이 쓴다. 시각화 용으로도 좋음.
Health condition은 뭘 의미하는지부터 여러 가지로 정의할 수 있음.

<img width="918" alt="스크린샷 2020-02-12 오후 2 04 38 1" src="https://user-images.githubusercontent.com/26548454/74306567-3954f380-4da6-11ea-8a46-1f1bcd1344f2.png">

Health condition에 부합하지 않게 될 경우 alert 설정을 할 수 있다.
Documentation 부분 = 일종의 error explanation. 뭐가 문제인지를 명시하는 부분. 



<img width="924" alt="스크린샷 2020-02-12 오후 2 08 03" src="https://user-images.githubusercontent.com/26548454/74306568-3a862080-4da6-11ea-8c51-fdc366ebef82.png">


Dynamic Chart 제공한다. script로 stackdriver 설치할 수 있음.


## Incident Response

Incident response는 사람이 담당해야 할 영역. SRE 모델에서, 그리고 그동안 해왔던 실습에서는 어떤 식으로 작업했는지가 곧 정답임.



<img width="924" alt="스크린샷 2020-02-12 오후 2 13 23" src="https://user-images.githubusercontent.com/26548454/74306569-3c4fe400-4da6-11ea-8b28-7c8b03676331.png">

사용자에게 신뢰를 얻으려면
* outage 최소화하고
* 문제 생겼으면 우리가 뭐 했는지 해결과정을 투명하게 공개하고
* 빠르게 대응해야 함


<img width="925" alt="스크린샷 2020-02-12 오후 2 16 18" src="https://user-images.githubusercontent.com/26548454/74306571-3d811100-4da6-11ea-8544-b2d779840bc9.png">



대응 매뉴얼 같은 걸 설계해야 함.

누가 뭐 해야 하는지 명확하게 정의해서, 같은 일 두 번 하는 식의 낭비나 혼선이 없도록

So, knowing exactly what the steps are once we have identified the process and identifying what the communication is. Even if we haven’t fully identified it, having the steps in place to say this is our first level communication, this is our conclusion once we’re backup in line and then follow up with a postmortem, that’s a typical three-step response.


이게 3 step response라고 함.

<img width="925" alt="스크린샷 2020-02-12 오후 2 19 09" src="https://user-images.githubusercontent.com/26548454/74306623-6903fb80-4da6-11ea-96ee-31cc6806b1ba.png">

3 step response에 들어갈 첫 번째: monitoring dashboard.

* Metrics -> 문제의 범위를 좁히고 뭐가 영향을 받았는지 확인하는 용도
* Alerting regimen. 사용자에겐 어떻게 notify, 누가 on-call인지 등등




 
<img width="918" alt="스크린샷 2020-02-12 오후 2 27 14" src="https://user-images.githubusercontent.com/26548454/74306625-6a352880-4da6-11ea-9d79-1aef5fb90ec6.png">

Incident Response -> 결국 우리가 배웠던 모든 것들

Business logic layer : root cause analysis의 시작점
Testing and release : production 과정에서의 resiliency 확보
release가 완료되면, 사용자의 데이터를 토대로 forecasting capacity


<img width="925" alt="스크린샷 2020-02-12 오후 2 30 11" src="https://user-images.githubusercontent.com/26548454/74306628-6b665580-4da6-11ea-81d6-6851e6f62548.png">

포켓몬 고의 사례는 이걸 충실히 따른 케이스로, 들여다보기 좋다



<img width="924" alt="스크린샷 2020-02-12 오후 2 31 17" src="https://user-images.githubusercontent.com/26548454/74306617-63a6b100-4da6-11ea-85be-5d1f8d48bd51.png">


몇 가지 subjects on incident response
12 factor의 ‘admin / management task는 한 번에 처리해야 한다’

-> 사람이 할 수 있는 일 / 아닌 일을 분리하는 작업이 필요함.
segregate Control plane functions from data plane functions.

예컨대 baston host 라던가 creating private subnetworks 같은 것,
Business / user logic과 troubleshooting에 필요한 management을 분리하는 게 중요함


<img width="921" alt="스크린샷 2020-02-12 오후 2 36 11" src="https://user-images.githubusercontent.com/26548454/74306632-6c978280-4da6-11ea-9476-300fd7322d9f.png">

매뉴얼 만들기.


<img width="913" alt="스크린샷 2020-02-12 오후 2 37 40" src="https://user-images.githubusercontent.com/26548454/74306636-6d301900-4da6-11ea-9d8b-c2be362a9beb.png">

일종의 encapsulate 느낌인데, inside process 신경 안 써도 되게끔 만들라는 것



<img width="926" alt="스크린샷 2020-02-12 오후 2 39 20" src="https://user-images.githubusercontent.com/26548454/74306639-6e614600-4da6-11ea-99e5-a5bfec76f0d7.png">


Interrupt (문제 생겼다!) 대응에 집중할수록 project driven 작업에 소홀해지기 마련. On-call rotation을 권장함

Reduce noise. 모든 alert마다 사람이 달라붙어야 하도록 시스템을 만들지 마라.


