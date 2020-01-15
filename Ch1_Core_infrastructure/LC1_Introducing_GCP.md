# 기본적인 권한설정이나 특징들
## Introducing GCP
GCP는 기본적으로 네 가지 서비스를 제공한다.
- Compute
- Storage
- Big Data
- ML

이 강의에서는 Compute와 Storage를 다룰 예정.
기본적으로 클라우드는 네트워크과 연결되어 있어야 하며, 클라우드를 사용하면 Application을 운용하고 데이터를 저장하는 과정에서의 수많은 Overhead Chore를 처리할 수 있다.

---
### What is Cloud Computing?

A way of using IT that has five equally important traits.

- Get computing Resources on-demand and self-service. (No need for human intervention
- Can access these resources over the net, from anywhere you want.
- Provider는 Big pool을 가지고 있으며 allocates them to customers out of the pool. - 규모의 경제.
- Elastic Resources. 필요하면 더 받고, 필요없으면 반납.
- 사용한 만큼만 비용 지불.

---
### Why is this system compelling?

1. colocation. 비싼 데이터센터를 직접 짓는 대신 rent space in shared facilities.
2. virtualization.  서버 / 데이터센터 등이 하드웨어와 분리됨.
= 두 가지 모두 flexibility, efficiency 확보에 도움이 되었음
… 단, virtualization만으로는 사업 확장이 어렵다는 판단 (구글) (can’t move fast enough)
= container based Architecture. (Automated elastic 3rd wave cloud)
3. Cloud. (Serverless). 필요한 서비스를 자동으로 provision / configure to run google familiar applications.

---
### GCP computing architecture

Virtualized Data center -> Infrastructure as a Service, Platform as a Service 두  가지를 제공한다.

- IaaS
raw compute, storage, network 제공. 
Pay for what you allocate

- PaaS
application code that you write -> libraries that give access to the infrastructure your application needs를 bind하는 역할. 따라서 application code에만 집중할 수 있도록 만들어 준다.
Pay for what you use.

= 불확실한 예측을 토대로 미리 구매해야만 했던 과거의 방식보다는 훨씬 낫다.
“Managed infrastructure / Managed Services”로 흐름이 바뀌는 중.

cf. SaaS는?? -> 구글이 제공하는 검색 / 구글드라이브 / 지메일 등 여러 Software 서비스들은 인터넷으로 directly 제공되는 중. G suite는 이 강의에서 다루지 않는 주제임.

---
### Google Network

잘은 몰라도, 전세계에 퍼져 있는 건 확실하다.
만약 사용자가 구글에게 request를 요청하면, 구글은 가장 latency가 작은 edge network location을 활용해 respone을 해준다.

---
### GCP Zone

Zone : 가장 하위 레벨. deployment area from GCP Platform Resources.

사용자가 예컨대 GCP Compute Engine을 사용한다고 하면, 이걸 할당하고 작동하는 게 Zone이다. Data Center라고 이해하기도 하지만, 꼭 그렇진 않다. Zone이 반드시 Single Physical building에 매칭되는 건 아니기 때문.

Zone이 모여 하나의 Region이 된다. Independent Geographic area라고 지칭. GCP를 사용할 때 어느 Region의 Resource를 사용할지 선택할 수 있다.

Zone within a Region = Fast Connectivity를 제공한다. Round Trip network latencies under 5 ms.

Fault Tolerance를 위해서는 동일한 Region 내 여러 Zone에서 Resources를 가져오는 걸 권장한다.

Different Region에서 Resources를 할당받는 경우도 많다. 보통 세계 각국의 User에게 서비스해야 할 경우. 유저와 가까운 지역의 Region에서 할당받는 식임.

몇몇 GCP Service는 placing Resources in Multi-Region를 지원한다. 예컨대 ‘Europe’이라는 Multi-Region에  GCP Storage를 등록할 경우, 최소 두 개의 geographical Location에 데이터를 저장하는 식. (최소 160km 떨어진 지점에.)
---
### Environmental Responsibility

Virtual Infrastructure라 해도 결국 Physical infra 위에 지어진 것들이다. 이걸 운영하는 데엔 많은 에너지원이 필요하기 마련. 지구상의 데이터센터가 전 세계 에너지 소모의 약 2%를 차지할 만큼 많다. 따라서 구글은 환경에 대한 책임을 통감하고 있음. 최대한 효율적이고 환경친화적으로 운영하려고 한 노력들을 서술함

핀란드의 경우 냉각수로 바닷물을 사용한다던가. 태양열 등 대체에너지를 쓰고, Carbon-neutral Since 07, 데이터센터에 사용할 에너지원으로 Renewable Energy를 쓰려고 노력중.

뭐 아무튼, 환경친화적인 Customer라면 구글 정책과 맞닿는 부분이 있을 거라는 얘기

---
### Customer Friendly pricing

Fine-grain (가는 결, 미립자) billing 시스템. Billed by the second.

Compute System의 경우 Automatically applied sustained use discounts. (If you run virtual machine instance for a significant portion of the billing month.)

만약 instance를 more than 25% of a month -> every incremental minutes마다 discount 적용함.

Compute Engine Custom Virtual Machine type -> fine tune virtual machine on your apps. 가격정보를 추적할 수 있다는 듯.

---
### Open APIs

Google gives customers the ability to run their apps elsewhere. (만약 더 이상 구글을 best provider로 쓰고 싶지 않은 경우라면)
즉, feeling locked-in 하지 않도록 지원한다는 게 골자다.

GCP Services는 Open Sources와 호환된다. (구글의 Bigtable -> apache HBase와 호환, Hadoop과 호환…) 즉 꼭 구글꺼 안 써도 상관없다는 의미.
Ex) 텐서플로우

“쿠버네틱스” - Gives Customers the ability to mix and match MicroServices running Differenct Clouds.
Google StackDriver … Let Customers monitor workload across multiple cloud providers.

Cf. 오픈소스 이용해서 서비스 만들어 팔아먹는 거 대단하다..

---
### Why Choose GCP

GCP -> Computing / Storage / Big Data / ML / Application Service를 Mobile, Back-end Solution, Analytics 등으로 지원한다.

정리하자면
GCP의 Product / Services는 크게 네 가지로 요약된다.

1. Compute
2. Storage
3. Big data
4. Machine Learning / networking / operations & tools.

---
### Multi-layered Security approach

전세계 사람들이 사용하는 서비스 최소 7개. 따라서 구글의 서비스는 Design for Security is pervasive. -> Throughout the infrastructure, GCP & Google Services run-on. 

1. HardWare Infrastructure. 
구글의 Server Board / Networking equipment in Google Data Center는 전부 Custom Designed by Google. 하드웨어 보안 Chip인 Titan도 구글이 제작했으며, 현재 Server와 peripherals (주변부)에 전부 사용되고 있다.
Server Machine은 Cryptographic Signature로 ‘booting the correct software’ 여부를 검증함.

구글 데이터센터는 Multiple Layers of physical Security Protection가 통합된 Design이며, 극소수의 구글 엔지니어만 데이터센터 접근 권한이 허용되어 있다.

Google Infrastructure provides Cryptographic privacy & integrity for remote procedure called “Data-on-the-Network”. This is how google Services communicate with each other.

Infrastructure automatically encrypts our PC traffic in transit btwn data centers.

보통 구글 로그인 페이지로 알려져 있는 Google Central Identity Service는 단순히 아이디 + password만 요구하고 끝나진 않는다. 구글이 설정한 risk factor (비슷한 장소, 동일한 디바이스에서 로그인했는가 등)를 토대로 Challenging Question이나 Certification을 요구하기도 한다.

구글에서 제공하는 대부분의 Application은 Physical Storage에 직접 접근하지 않는 형태다. Storage Services를 통해 접근하며, 각각의 Services마다 Encryption이 기본적으로 적용되어 있다.

구글 서비스 중에 Internet을 활용해 서비스를 제공하는 것들은 구글 내의 ‘Google Front-End’라는 infrastructure 서비스에 등록되어 있다. 이 서비스는 check incoming network connections for correct certificates and best practices.
GFE 서비스는 Denial of Services attack 방어를 지원하고,

Sheer Scale of its infrastructure (인프라 자체의 규모) 때문에 Denial of Service Attack의 많은 부분은 타격받지 않고 흡수할 수 있으며, 그 뒤에 multi-tier, multi-layer denial of service protection으로 공격의 위험성을 최소화하고 있다.

구글 내 Red Team은 모의 시뮬레이션으로 공격받았을 시의 피해를 예측 및 최소화하고 효과적으로 반응하기 위한 팀이다.

구글 내에서 혹시 접근권한을 가진 Employee의 계정을 해킹하는 것으로 보안을 뚫을 수도 있다. 이 때문에 구글은 infrastructure에 접근권한을 가지고 있는 직원 계정을 Actively Monitor하고 있으며, Employee Account는 반드시 U2F compatible Security Key를 요구하도록 되어 있다.

코드 자체의 보안을 위해서는, 구글은 모든 Source Code를 Centrally하게 관리하며 2 Party review of new code가 의무화되어 있다. 외부적으로는, 버그나 보안취약점을 발견하는 사람에게 보상을 주고 있음.

---
### Budgets and Billings

혹시 실수로 뭘 실행해서 Big GCP Bill을 받지는 않을까? 이런 걱정을 해소하기 위해 구글은 4 tools를 제공한다.
- Budgets and alerts
- billing export
- reports and quotas

Budgets -> billing account별 / GCP 프로젝트별로 나눌 수 있다. Fixed Limit을 설정하거나 tie it to another metric (이전 달 사용량의 몇 % 같은 기준 등). 예산 제한에 어느 정도 근접하면 Alert 메세지를 발송한다.

Billing Exports -> Bill 관련 정보들 확인 가능. Detailed Analysis

Reports -> Visual Tool to monitor Expenditure
Quotas -> Account Owner나 GCP community as a whole로도 적용되는 사항. 에러 또는 외부의 공격 때문에 Resource over-consumption가 발생하는 걸 막기 위한 조치. 
Rate quotas, allocation quotas 두 가지가 있으며, 프로젝트 단위로 적용 가능하다. rate의 경우 특정 시간대별로 초기화된다. (쿠버네티스의 경우 100초마다 제한 초기화) allocation의 경우 프로젝트가 할당받을 수 있는 자원의 개수를 제한하는 식이다.

Google Cloud Support를 통해 quotas를 변경할 수 있다.