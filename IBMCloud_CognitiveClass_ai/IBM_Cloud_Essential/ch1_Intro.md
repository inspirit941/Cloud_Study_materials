## IBM Cloud / Compliance

Hybrid Cloud 형태로 클라우드 서비스가 사용될 전망. 어떤 건 public, 어떤 건 private, 어떤 건 on-prem에서 처리하는 식. Regulated industry의 경우 모든 서비스를 클라우드로 바꾸는 건 enterprise 특성상 하기 어렵다

IBM은 Secure / Compliant / Unique Capability라는 특징을 가지고 있다고 어필하는 내용.

## Cloud Deployment options

* Public : cloud hosted on IBM data center, accessible over internet

* Private : cloud delivered behind your firewall and in your data center

1. Hybrid Cloud

Shipment 회사인 Acme라는 가상의 회사 예시.

이 회사는 On-prem으로 ERP 서비스를 구동하고 있다. ERP는 다시 BFF (Backend for Frontend), ERP chunk (inventory, delivery, shipment 등), User Registry (Driver / .User 관련 정보).

BFF는 프론트엔드의 요청에 응답하고, 웹 대시보드 서비스가 원활히 작동하도록 만드는 것.
여기서 회사가 모바일 앱을 위한 BFF를 만들기로 했고, 이걸 Public cloud에 올리려 한다. Mobile BFF App만 Public으로 만들게 되면, on-prem의 ERP와 새로 만든 클라우드기반 모바일 앱의 interact이 필요함. 그래서 Tunnel을 하나 생성해 두 개의 서비스가 통신할 수 있도록 만듦. 

이게 interoperable이라는 하이브리드 클라우드의 특징. public / private cloud components are working in tandem.

---

여기까지는 좋았는데, 연휴 등 서비스 수요가 폭주할 때 서비스가 bogging down하는 문제점 발생. 회사 측에서는 'ERP를 microservice로 쪼개고, public cloud로 옮기자'는 결정을 내림. 그래서 여기 docker라는 리눅스 컨테이너 툴, 오케스트레이션 툴인 쿠버네티스가 등장함.

이렇게 옮기게 되면, seamlessly scale out application이 가능하게 됨. 이게 public cloud의 또 다른 특징.

그리고, 클라우드에서 제공하는 여러 프로그래밍 언어 / 오픈소스를 사용해서 portabilty를 확보할 수 있음. on-prem에서는 예컨대 자바 EE라던가.. 개발 가능한 스택에 종속적이지만, 클라우드는 선택지가 넓음.

Security. On-prem에서 클라우드로 옮기고 싶지 않은 것들 (유저 정보라던가)... 그대로 유지할 수 있음. 회사의 firewall을 그대로 활용한다거나

2. MultiCloud

하이브리드 클라우드와 멀티클라우드는 다른 개념임.

하이브리드 : workload가 working together across multiple cloud 형태. 앞서 설명한 interoperable / portability를 제공하는 형태.

멀티클라우드 : 컨테이너 개수의 증가 / 쿠버네티스 테크의 등장으로 enable the growth of multicloud.

멀티클라우드가 사용되는 이유?

- 99.999% Availability를 추구하는 기업이라고 해 보자. 설령 클라우드 하나가 기능을 못 하더라도, 다른 클라우드에서 작동하는 웹서비스를 구축할 수 있음.

- global 사용자에게 가장 regional 가까운 cloud 서비스로 라우팅하면, lower latency + UX 향상.

- 멀티클라우드 방식을 사용하면, private 클라우드에는 민감하거나 중요한 정보를 보호할 수 있게 됨.

1. Automation

퍼블릭 / 프라이빗 클라우드에 쿠버네티스 클러스터가 각각 하나씩 존재한다고 해 보자.

Devs와 Ops에서 Ops의 목적은 "Spin up new clusters as well as manage, see the different clusters that have been created." 따라서 이런 걸 확인할 수 있는 Control plane을 필요로 한다. 

Figure out the configuration -> go to control panel & tell it to spin up certain clusters 같은 식.

반대로 Dev의 경우, 새 application을 도커 형태로 생성했다고 가정하자. 서비스를 돌리려면 두 개의 클러스터에 전부 push해야 하는데, control plane의 존재가 없다면 authentication / configurations of different clouds... 등 귀찮아짐.

single Command로 두 개의 클러스터에 컨테이너를 spin up할 수 있는 게 장점.

2. visitbility

각자의 unique dashboard도 존재하는 상황에서, single unified way of managing이 가능하기 때문에 유용함. Control plane의 존재 덕분에 unified kind of approach + see the difference가 가능하게 됨. pods / deployments across multiple cloud 확인이 가능해진다.

3. Governance

regulatory + compliance policy becomes increasingly strict / the differ from geography to geography. Operation Team에서 compliance policy를 multiple cloud에 등록하고 싶을 때, Control plane으로 multiple cluster에 등록할 수 있다.

single command로 security policy for compliance -> 가능함.

---

## IaaS, PaaS, SaaS

* IaaS

Infrastructure는 크게 세 가지로 나뉜다.
1. Compute - Processors. Compute, GPU, HPC 등
2. Storage - Object, blocks, files. 
object storage가 보편적인 형태의 storage (web server에서 보통 사용하는 형태. 사진 / document 등등). 
block과 file storaged는 network storage의 한 형태이며, attached specific way. block의 경우 attaches with iSCSI, file의 경우 NFS. 
3. Network - 위의 두 개를 아우르는 컴포넌트. 두 개를 연결하는 파이프라고 생각하면 된다. 메가바이트 단위 정보를 전송할 수 있는 작은 파이프에서부터 기가바이트 단위로 전송할 수 있는 파이프. 전송에 필요한 bandwidth / throughput에 따라 비용이 다르고, 비용 측정방식도 a set period of time으로 설정가능.

이런 특징들이 다 합쳐진 것 중 하나로 AI workload를 들 수 있다.

- billion pictures in the Object storage
- train model on GPU servers
- 여기서 gpu 서버 자체는 local storage가 없기 때문에 block storage와 계속 통신하는 식으로 storage를 사용한다.
- 학습이 끝난 후 모든 결과는 object storage에 저장한다.

* As a Service

여기서 중요한 건 네 가지.
1. shared
multi-tenant 형태.
2. hourly/monthly
각각의 서비스마다 비용 측정 방식이 조금씩 다름. 예컨대 storage의 경우 cents per Gig, 네트워크의 경우 size of pipe - pay per month / 데이터 전송량 - cent per gig per months.
3. contract가 딱히 없음.
필요한 만큼 쓰고, 필요없으면 get rid of. On-demand라는 특징.
4. Self-service.
웹사이트에서 payment detail 입력하면 as-a-service 형태의 서비스를 사용할 수 있음. 따로 configure setup time이 필요하거나 하지 않다.

* PaaS

IaaS의 Persona가 System Admin (IT admin)의 형태라면, PaaS는 virtualized resource인 IaaS를 토대로 사용자가 일일이 manage할 필요 없도록 구축한 서비스를 말함. 보통 Dev팀이 Persona.

(IaaS - car lease. 차 스펙과 사양 등을 면밀히 따져서 차를 운행하고, 운행에 필요한 기름값같은 건 사용자가 낸다. PaaS - car rent. 여행지같은 곳에서 렌트카 회사 가면, 차 스펙이나 사양을 디테일하게 따지지 않고 차 빌려 쓴다. 차 매니지할 필요 자체가 없지만, 운행하면서 드는 기름값은 내가 낸다.)

PaaS 장점
- Fast and easy to get an app up / running. create / delete 과정이 쉬움
- cost / benefit. full time으로 돈내는 개념이 아님.
- tools. API 마켓 플레이스에서 plug in 형태로 적용하기 쉬움

단점
- lack of controls. fine tuning이 불가능
- vendor lock-in. (migrate PaaS from one cloud to another... 가 어려운 편. 따라서 cloud provider 처음에 잘 골라서 써야 함)
- performance at scale issue.

---

### 3 Types of Account in IBM Cloud

1. Lite

    - 무료
    - PoC / Light Dev work용
    - 사용가능한 서비스 제한. 한 번에 하나의 인스턴스만 생성가능
    - 하나의 Cloud Foundry managed service in one Region 만 생성가능. 해당 Foundry는 256MB 메모리제한.
    - 열흘간 활동 없으면 만들었던 app은 sleep 상태로 변경. 30일 활동 없으면 자동삭제.

2. Paygo

    - credit card 등록하면 자동발동
    - 모든 종류의 서비스 사용 가능.
    - 쓴 만큼 내는 시스템이며, lite 서비스도 사용 가능 (무료).
    - 비용은 매달 청구되고, 업그레이드 시 $200 credit 제공


3. Subscription
    - production 레벨에서 적용 가능함. IBM측에 문의한 후 등록
    - commitment to a combined min spending amount per month.
    - subscription discount 적용됨

## Cost Estimation

Estimator tool 존재. estimates / quotations for service & infra. pdf형태로 저장 가능. 카탈로그 -> estimate 들어가보면 된다.

## What is Cloud Native?

Monolitic App vs Microservice Cloud App이 있다고 하자.

기본적으로 시스템은 크게 5가지 Layer로 구분됨. 하단 -> 상단 순으로 서술

1. Cloud / Infrastructure. 이건 Public이든 private이든 상관없다. 보통 Multicloud / Hybrid Cloud가 여기 해당됨.

2. Orchestration / Scheduling. 쿠버네티스가 여기 해당됨.
3. Application / Data Service Layer. Backing Service가 보통 포함되고, integrate application code on existing services on other cloud or on-prem.
4. Application Runtime. 보통 middleware라고 통칭했던 부분.
5. Application Code = Cloud Native Part.

cloud native를 위해서는 Application code의 Design, build, deliver가 달라지게 됨.
- Enable Innovation
- Business Agility
- Tech차원에서 Commonditization.

-> Enterprice / Engineering At scale.

standardize logging / events가 필요함 (to commodify)

<?>
Commoditize 가능한 Layer 
- Orchestration. Istio, Knatives 같은 tech. embedded in control panal.
<?>

---

## Cloud Foundry / IAM Admin 101

1. Account Owner.

- Master admin역할. can see / charge everything.
- 얘 빼고 나머지 모든 계정은 granted access / privileges가 필요하다.

사람의 이메일 계정에 등록한다면, 해당 사람이 퇴사하거나 자리를 옮기는 등의 일이 생기면 매번 계정권한을 변경해줘야 함. 따라서 ServiceID에 이 권한을 부여하는 걸 권장한다.

2. Cloud Foundry / IAM

= 2 models to manage user access.

- Cloud Foundry : organizations and spaces를 관리하는 management. 2014년에 등장. 단, graunlar한 구분은 지원하고 있지 않다. running in same region에 있는 Service에만 connect 가능함. 따라서 권한 세분화가 필요한 거대 애플리케이션이나 Geographically separated 서비스를 사용해야 할 경우 제약이 큰 편.

- IAM : 2017년. granular access control over geographical abstraction. Cloud Foundry 권한에 있는 것들도 IAM 통제에 놓일 수 있게 이양중이라고 함. 

두 개는 서로 Separated Manage Module이라는 점에 유의할 것. 만약 특정 사용자가 이미 admin (under Cloud Foundry) -> no access to IAM managed Resources.

### Cloud Foundry

https://www.youtube.com/watch?time_continue=1152&v=w2AyDVS2SSM

- Organizations and spaces.
특정 Organization 안에 여러 개의 space가 존재하는 식. 기본적으로 계정 하나당 1 org + 1 space이지만, Paygo 계정부터는 이 제한이 깨진다. 

Space는 tied to a geographical Region. 한 번 생성하면 다른 region으로 옮기는 건 불가능하다. 지우고 recreate하는 식으로 작업해야 함. 다른 organization으로 이동하는 것도 불가능.

-> 즉 특정 space 안에 생성한 Service는 다른 space로 이동시킬 수 없다. 해당 service가 different space의 service와 통신하는 것도 불가능. "you can only connect Cloud Foundry managed services to Cloud Foundry managed application in the same space."

사용자의 권한도 space based로 주어지는 듯. Dev space / Test space / Production space가 있을 때, 각각의 space마다 접근권한을 다르게 설정할 수 있음.

Cloud Foundry managed Service를 사용할 경우, 기본적으로 same region의 space에서만 작동할 수 있다.

Organization은 multiple region의 space를 보유할 수 있는 구조. (logical constructs that group spaces) 

- Security Model

Split into Org Role / Space Role.
* Org Role
    - Manager : create space / invite users + set access
    - Billing Admin : billing info.
    - Auditor : resource 보는건 가능, not modify
* Space Role : 특정 region + 특정 space
    - Manager : 해당 space manager
    - Developer : resource purchase 가능
    - Auditor : view 가능, 수정 불가능.

### IAM

- Resoure Groups.
More granular Access. Resource의 Region 제한이 없다.

계정에는 기본적으로 1개의 resource group이 부여됨 (default)
lite는 1개 Resource group만 보유 가능하며, paygo부터는 제한 풀린다.

IAM 통제하에 있는 resource는 geographical 제한 없이 Cloud Foundry 리소스와 통신 가능함. far more secure / precise한 통제가 가능하다.

billing - resourse group level.

- Security Model
    - Assign Access to Resource group
        - Admin : 모든 권한
        - Editor : 리소스 통제는 가능하지만 account 관련 권한은 없음
        - Viewer
    - Service Access
        - All IAM Managed Service
        - Particular Service Type : Platform access role, Service access role

Platform Access Role / Service Access Role도 각각 구분됨.

- Platform access Role
    - admin : access policy 설정 가능.
    - editor : resource 생성변경 가능, account 설정불가
    - Operator : 특정 service 관련 설정권한 존재
    - viewer
- Service Access role (서비스마다 있는 것도 / 없는 것도 있음)
    - Manager
    - Writer : create / edit 
    - Reader : read only

IAM Access Group

Group User나 특정 Service ID에게 동일한 권한을 대량 부여하는 것. Individual 설정하는 대신 사용







