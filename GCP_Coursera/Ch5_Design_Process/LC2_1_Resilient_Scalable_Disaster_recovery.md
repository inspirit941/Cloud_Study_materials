# Design for Resiliency, Scalability, Disaster recovery
## Overview
high - Availability (resiliency) = unexpected failure에도 제대로 작동할 수 있는 특성을 말함. 특정 instance in certain zone이나 특정 zone 자체가 죽더라도, resiliency application remain fault tolerant - 서비스는 죽지 않고, 자동으로 repair system 가동.


<img width="926" alt="스크린샷 2020-02-10 오후 3 44 48" src="https://user-images.githubusercontent.com/26548454/74210397-efe5a500-4cce-11ea-8e14-0e47ae49be0d.png">


## Failure due to loss

Error나 loss는 필연이다. 이걸 없애는 건 불가능함. 

<img width="924" alt="스크린샷 2020-02-10 오후 4 11 14" src="https://user-images.githubusercontent.com/26548454/74210405-fa07a380-4cce-11ea-8815-f4737fc07d4e.png">



그 어떤 것이라도 fail이 없을 수는 없다. 예측하고 대응하는 게 최선.
Communication part의 의미는, ‘누가 의도적으로 이런 fail이 나도록 만들었다거나 하는 식으로 의심하지 말라’는 것.


<img width="925" alt="스크린샷 2020-02-10 오후 4 13 40" src="https://user-images.githubusercontent.com/26548454/74210415-068bfc00-4ccf-11ea-9351-163905ab3c12.png">

Single Point of Failure. 어디에서든, 무엇에서든 발생 가능하다는 게 특징.


<img width="926" alt="스크린샷 2020-02-10 오후 4 15 00" src="https://user-images.githubusercontent.com/26548454/74210424-0e4ba080-4ccf-11ea-94e0-815cabaa757f.png">



최소 N+2. 업그레이드 / failure 대비용. 각각의 server에 너무 많은 권한이나 역할을 부여하지 마라. 각각의 unit을 interchangeable clone으로 만들어라.
Microservice / Container나 GCP에서 가능함.


<img width="925" alt="스크린샷 2020-02-10 오후 4 18 22" src="https://user-images.githubusercontent.com/26548454/74210426-0f7ccd80-4ccf-11ea-9c92-7441c437ce41.png">

Correlated Failure
하나 망가지면 연쇄적으로 영향을 받는 것. 연쇄적으로 전부 영향을 받는 모든 것들을 통칭 Failure Group이라고 한다.

이 Failure group을 어디까지로 정의할지에 따라서도 Design이 달라질 것.



<img width="924" alt="스크린샷 2020-02-10 오후 4 21 10" src="https://user-images.githubusercontent.com/26548454/74210427-11469100-4ccf-11ea-9780-1c2d34024a62.png">


Divide Business logic into services based on failure domains. 개별 component 뿐만이 아니라 entire failure domain 관점에서 보는 것.
Microservice 모델의 경우 각각의 모듈은 independent. communicate가 기본적으로 false 형태이므로, failover mechanism in case that workflow logic tends to fail 을 대비해둬야 한다.


### Failure due to overload

overload되면, 어느 순간에 시스템이 맛이 간다. Crash, thrash, stop responding, break adjacent resources at the service depends on. Loss로 인한 fail, overload로 인한 fail은 겹쳐 있거나 밀접한 관계인 경우가 많음.

메모리 초과, disk 용량 초과 등 overload 발생 -> 다른 곳에도 연쇄작용이 발생할 가능성이 매우 높아진다.

<img width="925" alt="스크린샷 2020-02-11 오전 10 58 08" src="https://user-images.githubusercontent.com/26548454/74210428-1277be00-4ccf-11ea-8369-5847033e143d.png">


예시 디자인. Failover design. Load balancing으로 traffic을 분할하고 있지만, 둘 중 하나라도 죽으면 하나의 서버가 한계용량 1000 중 960을 담당하는 형태다. 하지만 Failover가 아니어도 system growth로도 용량을 초과할 가능성이 존재함.

<img width="924" alt="스크린샷 2020-02-11 오전 11 01 14" src="https://user-images.githubusercontent.com/26548454/74210430-13105480-4ccf-11ea-84d7-7e2481df1c84.png">


만약 둘 중 하나가 죽어서 다른 서버가 허용치 이상의 traffic을 받았을 때 생길 수 있는 오류들. 수많은 오류가 연쇄적으로 발생하기 때문에 cascading failureㄹ고 부른다. 이 수많은 오류가 발생할 때,뭐가 처음 문제였는지 확인하기 위해서라도 logging이 중요한 거다.



<img width="925" alt="스크린샷 2020-02-11 오전 11 13 17" src="https://user-images.githubusercontent.com/26548454/74210548-831eda80-4ccf-11ea-8c08-1a23783cb248.png">


Safety Size 설정 및 준수. 극한상황까지 오기 전에 미리 관리하는 게 핵심. 


<img width="923" alt="스크린샷 2020-02-11 오전 11 18 34" src="https://user-images.githubusercontent.com/26548454/74210557-887c2500-4ccf-11ea-81af-05faec7301d9.png">

이런 형태의 Incase bottleneck도 발생할 수 있다. 백엔드 서버를 auto scale하는 건 좋은데, 그 많은 백엔드 서버의 response를 하나의 frontend server가 처리하게 될 경우


<img width="922" alt="스크린샷 2020-02-11 오전 11 20 00" src="https://user-images.githubusercontent.com/26548454/74210561-8b771580-4ccf-11ea-9617-b9962e67bfa9.png">

구글 BigQuery에서도 사용하는 방법. Tree 형태로 노드를 관리하는 방식으로 incasf failure를 방지한다.


<img width="926" alt="스크린샷 2020-02-11 오전 11 20 58" src="https://user-images.githubusercontent.com/26548454/74210565-8d40d900-4ccf-11ea-83e0-623514c4cf98.png">

이런 형태의 error도 있다. Feedback loop을 도는 형식. Business logic이 resouce overconsumption을 일으키는 경우 발생한다. 쿼리를 요청하는데 받아줄 resource가 없어서 쿼리가 계속 도는 현상.

<img width="928" alt="스크린샷 2020-02-11 오전 11 21 26" src="https://user-images.githubusercontent.com/26548454/74210569-8e720600-4ccf-11ea-844a-9cdc9ebdcbf2.png">

시스템의 reliability를 높이기 위해 query를 반복하는 건 좋지만, 어느 순간을 넘어서면 system overload로 간주하는 로직이 필요하다. 구글의 route dampenlingd이 하나의 사례.

<img width="925" alt="스크린샷 2020-02-11 오전 11 35 50" src="https://user-images.githubusercontent.com/26548454/74210571-8fa33300-4ccf-11ea-9cd7-05266247fd3a.png">

아니면, early warning system을 도입하는 것도 괜찮다. (Canaries) 미리 single server를 만든 뒤 테스트해보는 것. 


### Coping with failure


Failure는 어느 시점에서든 발생하니까, limit the impact하는 게 중요함.

<img width="924" alt="스크린샷 2020-02-11 오전 11 41 15" src="https://user-images.githubusercontent.com/26548454/74210574-903bc980-4ccf-11ea-99c6-6e51e015ef12.png">


- planned rotating outages. (Forest fire : reactive, controlled burn : proactive) DR팀을 만들어서 test production system to see if they can actually fail over. -> loss fail인지 overload인지, hw문제인지 business logic 문제인지 확인할 수 있다.



- SLI나 SLO에 failure를 통합하는 것도 좋은 방법이다. 목적이 뭔지 알고 measurement도 명확히 정한다는 건, prevent for happening할 수 있다는 것. Over-engineering을 방지할 수 있다. 
- Establish a margin of safety, incorporate downtime as a potental. 


<img width="924" alt="스크린샷 2020-02-11 오전 11 46 24" src="https://user-images.githubusercontent.com/26548454/74210785-81094b80-4cd0-11ea-9725-51215474bce7.png">


- Meeting. 관계자들과 한 달에 한 번 정도는 모여서 SLI나 service level, objectives and production 상황을 공유하는 것도 좋다. Objective는 잘 맞추고 있는지, achieving이라는 걸 확인할 measurement는 잘 있는지 등등.

Goal = to develop procedures to test resilience of solution and an overload condition. Pre-production deployment라면, degraded service나 service outage 상황을 정의하고 그 때에 맞는 business process를 정의하는 게 좋다.


1. Redesign : 문제가 될 법한 부분을 재디자인하는 것. 가장 좋지만, 매번 가능한 해결방법은 아니기 마련
2. Prevention : 해당 문제가 발생하지 않을 수 있도록 take the necessary steps.
3. Detection and Mitigation : 문제가 생겼다는 걸 탐지하고, 해당 문제가 만들어낼 수 있는 영향력이나 파급력을 줄이는 작업
4. Graceful Degration : 한 번에 박살나는 걸 막고, handle stress + return to full service once issue passes. (Cloud 환경이면 상대적으로 이게 쉽다. Scale out이든 up이든 미봉책을 세워놓은 다음 Repair 작업할 수 있으므로)
5. Repair.
6. Recovery



###  Business Continuity and Disaster Recovery

Business Continuity의 핵심은, ‘No Surprise’다. 뭔 일이 있더라도 recovery가 가능한 시스템이 기반이 된다. 그러면, recovery system이 제대로 작동하긴 하는지, 작동한 시스템이 unchanged이며 문제없이 작동하는 걸 어떻게 확인할 수 있나?
-> level of testing / exercise of the recovery systems을 알아야 한다.



<img width="924" alt="스크린샷 2020-02-11 오후 12 10 40" src="https://user-images.githubusercontent.com/26548454/74210789-86669600-4cd0-11ea-86c0-227095aa11eb.png">


* Cloud DNS
First entry way to any application service on the Web. 이게 맛탱이가 가면 아무것도 시작할 수 없음. 단 cloud DNS는 100% uptime gurantee. Cloud에서 100% 보장하는 서비스는 많지 않은데, 얘는 모든 서비스의 출발지점에 해당하기 때문에 중요함. Built-in recovery system도 내장되어 있다.


앞서 설명했듯, 사용자에게는 data integrity가 중요하다. 데이터의 accuracy나 accessibility를 확보하지 못하면, 사용자 입장에서는 system failure. 즉 lost integrity에 해당한다.

이걸 일으키는 원인이 시스템일 수도 있지만, 사람일 수도 있다.


<img width="926" alt="스크린샷 2020-02-11 오후 12 16 18" src="https://user-images.githubusercontent.com/26548454/74210790-86ff2c80-4cd0-11ea-936a-42eb6a7d5759.png">


Lazy Deletion. 어떤 형태로든 시스템에서 data가 permanently delete되는 상황을 최대한 늦추는 것. Sys admininistrator의 삽질을 복구할 수 있는 방법이기도 하다.


<img width="927" alt="스크린샷 2020-02-11 오후 12 19 15" src="https://user-images.githubusercontent.com/26548454/74210791-8797c300-4cd0-11ea-9455-0d47ffd60403.png">

포인트는 ‘복구’ 다. 복구할 수 없는 형태의 backup / archive는 의미가 없다. 다들 restore strategy라고는 말 안하고 backup strategy라 말한다. 그리고 실제로 restore가 필요할 때는, 제대로 작동 안 하는 backup strategy였다는 걸 자각하는 경우도 많음

* Periodic testing = 해당 backup으로 복구가 가능한 건지 정기적으로 테스트 진행.
* 아니면 아예 automate restore from backups.



<img width="928" alt="스크린샷 2020-02-11 오후 12 22 07" src="https://user-images.githubusercontent.com/26548454/74210792-88305980-4cd0-11ea-9d5a-2b63c09614a8.png">


여러 단계의 tier로 resiliency 대비를 해놓는 게 일반적이다. 2nd tier는 disk-to-disk 형태고, 3rd tier에 Nearline이나 Coldline storage 등을 적용함.


<img width="924" alt="스크린샷 2020-02-11 오후 12 27 05" src="https://user-images.githubusercontent.com/26548454/74210794-88c8f000-4cd0-11ea-8dd1-004607b47cf3.png">


Cloud Storage는 Lifecycle Management와 Versioning을 제공함. 

<img width="925" alt="스크린샷 2020-02-11 오후 12 35 35" src="https://user-images.githubusercontent.com/26548454/74210795-89618680-4cd0-11ea-8341-38eda0500531.png">




### Scalable and Resilient Design


Vertical Scaling은 components bigger -> single point of failure로 작동할 여지가 있음. Horizontal scaling이 resilient를 확보하는 데에는 더 좋은 방법.


<img width="922" alt="스크린샷 2020-02-11 오후 12 37 59" src="https://user-images.githubusercontent.com/26548454/74210796-89618680-4cd0-11ea-8896-f8fec6e12f88.png">


<img width="921" alt="스크린샷 2020-02-11 오후 12 38 38" src="https://user-images.githubusercontent.com/26548454/74210907-f9700c80-4cd0-11ea-9254-4177ab85ab9d.png">


Health check로 instance에 이상이 생겼다면, restart 등 상응하는 조치를 취하는 것. Startup script나 instance group template 등등을 이용할 수 있다.

<img width="925" alt="스크린샷 2020-02-11 오후 12 40 10" src="https://user-images.githubusercontent.com/26548454/74210916-fd9c2a00-4cd0-11ea-8e7e-7d2c9276a623.png">

Cloud 기반 storage를 사용한다면, 여기 책임은 구글이 지는 것. Storage / SQL 등의 서비스.


<img width="923" alt="스크린샷 2020-02-11 오후 12 41 52" src="https://user-images.githubusercontent.com/26548454/74210917-fe34c080-4cd0-11ea-865d-01517c2cb29c.png">

네트워크 관리. 구글의 load balancer는 HW가 아니라 소프트웨어 기반 네트워크임. Multiple load balancer 쓸 필요도 없고, protocol 관련 문제나 failover 고민할 필요 없다

Location : spanner 같은 꼉우 알아서 configure nodes across multiple zones.


<img width="925" alt="스크린샷 2020-02-11 오후 12 44 04" src="https://user-images.githubusercontent.com/26548454/74210919-fecd5700-4cd0-11ea-9c19-bae05f70ec70.png">


언급한 모든 것들을 적용한 형태의 디자인.
1. Load balancer가 traffic을 할당한다. 각 zone 안에는 instance group 형태로 instance가 존재함. 따라서 얘네는 autoscale up / down이 가능. Health check도 in-place.
2. 필요한 데이터는 Cloud SQL에 저장. (state나 기타 데이터들). 두 개의 Cloud SQL로 데이터 replication. GCS에도 multi-region 형태로 데이터 저장.


- 만약 instance 하나가 죽으면 -> instance group에서 새로운 instance 생성.
- zone 전체가 죽으면 -> load balancer가 아직 살아있는 다른 zone으로 자동 연결, zone 복구되면 다시 traffic 분배.
- lose RDB -> resilient copy본으로 복구
- 만약 region 전체가 죽을 경우 (아직 그런 적은 없었지만) -> image repository, snapshot 등으로 현재 region 설정 그대로 다른 Region에 생성할 수 있다.
이 경우 Deployment Manager로 rebuild load balancer, VM, Data in SQL 등등… 을 automate 작업할 수 있다.



<img width="921" alt="스크린샷 2020-02-11 오후 12 55 11" src="https://user-images.githubusercontent.com/26548454/74210922-fffe8400-4cd0-11ea-888c-e7be26c22920.png">


Microservices design for streaming 사례.
Cloud Pub / sub으로 streaming data를 받고 있다. 받은 데이터를 토대로 cloud function이 작동. Function 기능으로 storage에 데이터를 저장하거나, output data directly back to pub / sub도 가능함.


<img width="921" alt="스크린샷 2020-02-11 오후 12 57 41" src="https://user-images.githubusercontent.com/26548454/74210923-fffe8400-4cd0-11ea-92f4-a31e08d041ad.png">

12 factor design system이 Google Cloud와 어떻게 연결되는지.


<img width="922" alt="스크린샷 2020-02-11 오후 12 59 36" src="https://user-images.githubusercontent.com/26548454/74210924-012fb100-4cd1-11ea-9ba0-2d4d4c9baf9f.png">



This module covered several related design goals, including reliability, scalability, and disaster recovery. 

The first subject was availability and reliability. A key concept is that planning for failure and dealing with failure in your design leads to improved reliability. 
Failure can occur due to the loss of a resource or it can occur due to overload. You must be careful when making adjustments to a system, that you don’t accidentally create the potential for an overload failure when you’re trying to improve resiliency to a loss failure. 

The second subject was disaster recovery. You learned that planning for disaster and preparing for recovery is key. 

The third was scalable and resilient design. That brings together many of the design principles you’ve seen in the previous modules, and shows how they all fit together into a general resilient solution.

