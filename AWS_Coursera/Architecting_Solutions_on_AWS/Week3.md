## Designing a hybrid solution for container based workloads on AWS

### Customer #3 - requirements

전체 workload의 절반은 on-prem으로, 나머지 절반은 AWS로 이전하고자 하는 상황
- AWS와 on-prem workload 간 통신이 필요하며, **Lowest Latency / High Throughput이 최우선 요구사항**.
- on-prem에서 생성한 파일 시스템을 AWS workload에서 읽어야 하고, 점차적으로 AWS에서 파알 생성하도록 할 예정.
- 모든 workload는 DB 제외하고 전부 Container.
  - container workload는 전부 internal access. 인터넷에서 접근하면 안 됨
  - DB는 Postgres로, AWS로 DB migration 생각 있음. migration을 위한 코드작업은 하고 싶지 않으므로, on-prem에서 하던 것과 동일한 방식으로 동작했으면 함
- management / orchestration tool은 on-prem과 aws가 동일했으면 좋겠음.

Requirement를 정리하면
- Host a PostgreSQL DB on AWS (migration)
- Use Common tooling across environments when possible. (on-prem의 orchestration tool과 같은 걸 쓰고 싶다.)
- Store data generated on-prem in AWS with minimal refactoring
- optimize for resilience (fault-tolerance)

소스코드 변경을 원하지 않으므로, 가급적 많은 부분을 lift-and-shift 방식으로 해결하고자 함

### Hybrid Networking and Connectivity Service

Customers' on-prem과 AWS 간 Network 통신이 필요한 상황. <br>

on-prem과 통신할 수 있도록 하는 컴포넌트로는 VPC를 제공. 강의에서는 1 VPC / 1 AWS Account / 1 Region을 상정하고 설명한다.
- customer가 리소스를 할당받을 Subnet이 필요함. requirements에서 '외부 통신이 필요없는 서비스'를 migration 예정이므로, private subnet이 필요할 듯.

AWS와 on-prem 간 통신을 위해 사용할 수 있는 컴포넌트
- Public internet: throughput / 보안 면에서 X
  - Non-Encrpyted connections are not secure.
  - 모든 인터넷 사용자와 Throughput share.

<img width="986" alt="스크린샷 2023-06-17 오전 11 34 30" src="https://github.com/inspirit941/inspirit941/assets/26548454/a77a6cc4-6633-4b29-a4d4-c34e898fbb3b">
<img width="980" alt="스크린샷 2023-06-17 오전 11 35 04" src="https://github.com/inspirit941/inspirit941/assets/26548454/12c1150f-82d7-4546-938d-b27d75caf740">

- AWS Managed VPN: 2개의 컴포넌트로 구성됨
  - AWS Site-to-Site VPN: on-prem의 DataCenter와 AWS VPC 간 통신을 지원하는 컴포넌트.
  - AWS Client VPN: 개발자나 admin이 노트북으로 VPC에 접근하기 위한 용도로 쓰임

위 예시에 부합하는 건 Site-to-Site VPN. 단, VPN도 결국 public internet 기반 통신이므로, throughtput을 안정적으로 보장하지는 못한다.

<img width="986" alt="스크린샷 2023-06-17 오전 11 37 49" src="https://github.com/inspirit941/inspirit941/assets/26548454/adf6d666-6846-4df1-a4cd-9d6365e0b11c">
<Br>

- AWS Direct Connect
  - Hosted private, Dedicated Connection을 Delivery Partner 또는 AWS 자체적으로 제공하는 것
  - AWS Global Network를 사용하며, public internet을 쓰지 않음 -> 안정적인 throughtput, latency 보장
  - Consists of a "Single Dedicated Connection btwn ports on your router / AWS Direct Connect Device."
    - Redundancy 위해서 second connection도 구축하는 것을 권장한다.


![fdBpU3qHQomQaVN6h2KJmQ_5babb5fe652b475bbce85464b4b258f1_Reading3 1A](https://github.com/inspirit941/inspirit941/assets/26548454/02dac0db-7e86-4e7f-940d-e0a4311fef73)
<br>

**cf. Virtual Private Gateway**

![tKB8WdT4TgSgfFnU-F4EvA_62ad51e38fc04d57a7c17e714cd4ddf1_Reading3 1B](https://github.com/inspirit941/inspirit941/assets/26548454/6ba55b3b-9c13-43b8-ae4c-2142e1bc9c28)
![EW63c5vRTgmut3Ob0V4Jiw_09dccfe3d3d04c4a9da1111c36bb45f1_Reading3 1C](https://github.com/inspirit941/inspirit941/assets/26548454/ec68180c-62fc-4bd1-9128-3039822868ea)
<br>

VPN Concentrator on the AWS Side of the Site-To-Site VPN Connection.
- VPC를 만들고 VPG를 앞단에 붙여서 on-prem DataCenter와 통신을 활성화하는 역할로 쓴다.
- Automate Redundancy / Failover 지원.
- on-prem 쪽의 Customer Gateway 여러 개와 연결할 수 있다.

<br>

![HGzQY3xrQSes0GN8azEn9Q_bc1d4d4485084aa7b83ea9be22c82bf1_Reading3 1H](https://github.com/inspirit941/inspirit941/assets/26548454/e2806a75-d5f8-43ce-bd1e-c72b9ced4fed)
![H3s0Jz18Qdm7NCc9fOHZFA_2231cac1874d452dbe80ddbae3ce67f1_Reading3 1I](https://github.com/inspirit941/inspirit941/assets/26548454/f6b21096-0aba-4900-98c9-1f3e5208441d)
<br>

만약 AWS Account / Region이 여러 개 있고 Direct Connection으로 연결해야 할 경우 AWS Transit Gateway 같은 컴포넌트가 추가로 필요하다.
- 일종의 hub for connection btwn Different Networks.
- route table 생성해서 network connection in a more centralized manner로 구축 가능

### Running Containers on AWS


- EKS : Kubernetes 자체의 management (클러스터 제공).
- ECS : Network / Security Concern은 AWS가 담당.
  - Native integration with other AWS Services.
    - 예컨대 LB가 필요하면 AWS에서 제공하는 것에 붙이면 된다.

Run on Where? 

![kDg2QE-ZRwG4NkBPmVcBfw_2d34f74a7edf4de89f81b9478fc639f1_Reading3 2A](https://github.com/inspirit941/inspirit941/assets/26548454/b4ae591d-a9c8-4bda-b464-be6abaee02b7)
<br>

EC2: Flexibility & Control
- ECS가 container orchestration할 수 있도록, ECS Agent가 EC2 인스턴스에 설치됨.
- image 타입, patching / scaling 자유도 제공, ssh access 스스로 설정

![Yavcd9PSSNmr3HfT0ujZBw_19d287d0c9ca4a429c46873bfff172f1_Reading3 2B](https://github.com/inspirit941/inspirit941/assets/26548454/4140f358-1538-477b-ad40-d2ba50de4288)
<br>

Fargate: Managed Serverless.
  - Serverless. Managed Scaling / Managed Runtime environment
  - no ssh access

requirements 체크
- k8s 안쓰고 있는데 modern platform으로 옮길 의향 있음. 단 k8s learning curve가 부담스러움. 학습에 따로 투자할 여력이 없음
- container 관련 복잡한 기능은 필요 없음. Just A large Quantity running at the same time.
- day-today operation에 ssh access가 필요한가?
  - yes. 지금은 own image를 클러스터에 배포 접근하기 위해 써야 하고, 개별 server에도 ssh 접근이 가능해야 함.
  - 바꾸면 좋긴 한데, 당장 다 바꾸고 싶진 않고 one change at a time.

<img width="987" alt="스크린샷 2023-06-17 오후 12 31 18" src="https://github.com/inspirit941/inspirit941/assets/26548454/986335b0-90d5-4404-9513-0ce02754271d">
<img width="980" alt="스크린샷 2023-06-17 오후 12 07 14" src="https://github.com/inspirit941/inspirit941/assets/26548454/93730394-8241-4d30-950c-7aee59d33c1a">
<br>

따라서 요구사항에 부합하는 contaier 서비스 조합은 ECS + EC2 instance.
- ECS 서비스를 두고, EC2 instance는 VPC 내부에 정의한다.
  - EC2 인스턴스 자체는 ingress / egress로 internet이 필요 없으므로 Private Subnet에 구축한다
- 단, bootup 같은 특수한 상황에서는 외부로부터 데이터를 받아와야 함. 사용자가 정의한 script같은 것들.
  - 따라서 Public Subnet에 **NAT (network address translation) gateway**를 설치한다.
  - NAT gateway를 통해서, backend 노출 없이도 외부로부터 필요한 리소스를 받아올 수 있음.

**NAT Service (NAT Gateway)**

NAT Gateway 와 NAT Instance 두 가지 종류가 있음.
- NAT Instance: NAT 기능을 수행하는 EC2 인스턴스. NAT 성능이 underlying EC2 instance 성능에 달렸다.
  - managed service가 아니므로 scale에 어려움이 있지만, small workload의 경우 NAT Gateway보다 cost-effective할 수 있음.
  - redundancy 처리 / failover 대비는 알아서 해야 함
- NAT Gateway: Managed service.
  - scaling / throughput 지원
  - Deploy one Gateway per AZ for redundancy

### AWS Relational Database Service

Relational DB 서비스에서 Resilience / fault tolerance 보강하는 방법 설명.

<img width="987" alt="스크린샷 2023-06-17 오후 12 39 41" src="https://github.com/inspirit941/inspirit941/assets/26548454/22cda5af-a00f-4376-b464-f3fdfd9eb4c9">
<img width="982" alt="스크린샷 2023-06-17 오후 12 42 36" src="https://github.com/inspirit941/inspirit941/assets/26548454/d56cb838-5bff-4512-b978-dc6d1f7b5b88">
<br>

Resilience가 중요한 시스템 설계할 때, 컴포넌트 추가할 때마다 '이거 죽으면 어떻게 되지?'를 계속 확인해야 한다.
- RDS에서 single instance로 RDS 생성했을 때 instance가 죽으면, 자동으로 fix instance 해주는 장치는 아무것도 없다.


![0F3Aqh7URX6dwKoe1PV-1w_acc1991f8ec04c5bb0fd55023a2cf2f1_Reading3 3B](https://github.com/inspirit941/inspirit941/assets/26548454/b4990487-2dcf-43c4-9761-ce474125cf56)
<br>

RDS Multi-AZ Deployment 기능
- primary / secondary instance가 각 AZ에 배포됨.
- DB와 통신하고자 하는 서비스는 DNS 조회해서 primary instance로 routing되는 DNS 주소값을 받는다.
- primary가 failover될 경우, DNS 주소는 동일하지만 second instance가 자동으로 primary로 변경된다.

<img width="983" alt="스크린샷 2023-06-17 오후 12 47 48" src="https://github.com/inspirit941/inspirit941/assets/26548454/06ce5b96-5db7-44c5-9277-e97579c0722a">
<br>

Read-Replica 기능
- 예컨대 PostgreSQL을 사용한 BI 서비스가 있다고 하자. Complex SQL로 돌아가는 BI 특성상 DB에서 SQL 처리를 위한 리소스 사용량이 많음.
  - SQL연산 처리하느라 DB에 리소스 여유분이 부족하다면, BI 서비스도 영향을 받는다.
- 따라서 일반적으로 Write보다 쿼리수가 많은 Read 작업은 별도의 Replica에서 따로 처리하도록 만드는 것.
  - Read Replica는 primary DB에서 비동기로 Sync.
- RDS에서 제공하는 DBMS Engine 대부분이 이 기능을 지원하며, 몇몇 Engine은 Cross-Regino Read Replica 기능도 된다

Scaling RDS instance
- 최초 생성시 instance type / size 선택 가능. 나중에 scale up 필요하면 늘릴 수 있다.
- CPU는 필요하지만 Memory 필요 없다면 Read Replica 기능을 사용할 수 있음.
- Memory 필요하지만 CPU 필요 없다면 scale out. RDS storage autoscaling 옵션을 활성화하면 된다.
  - provisioned 설정값과 실제 사용량이 다를 경우에 대응하기 편함. desired max Storage limit만 설정하면 된다.
  - actual storage consumption 확인 / 사용량이 provisioned storage capacity 도달할 경우 capacity up.

Storage Types
- General Purpose SSD: 
- Provisioned IOPS: designed to meet the needs fo I/O intensive workload that require I/O latency & consistent throughput
- 

---


Migration?
- 보통 migration은 1. Schema를 RDS 인스턴스에 등록한다 / 2. migrate Data 순으로 이루어진다.
- DB kept in Sync, all the way up to the point of cutover.

![erzlMicwTTC85TInME0wxg_de4379e908dd477193c4a8f4996235f1_Reading3 3D](https://github.com/inspirit941/inspirit941/assets/26548454/9698aa38-3bba-479e-9d15-0f3924df8ef5)
![6LQRhKcNRCi0EYSnDXQoVQ_f50de5644e5e44c390beafe9fee6b5f1_Reading3 3E](https://github.com/inspirit941/inspirit941/assets/26548454/9e8e0d4d-0b74-458a-ae4d-836f4c02f6d9)
<br>


AWS Data Migration Service (DMS) 사용을 권장.
- Source: on-prem DB, Target: AWS RDS 등으로 설정 가능.
- source / target 설정되면, migration 도중에 발생하는 source DB의 변경사항도 target DB에 자동 반영된다.
  - 즉 Migration 작업 돌려놓고도 source DB를 operational 용도로 사용할 수 있다
- homogeneous DB migration: source DB와 target DB의 DBMS Engine이 동일한 경우
- heterogeneous DB migration: source와 target DBMS가 다른 경우. 
  - AWS Schema Conversion tool을 써서 Schema 변환해야 한다.

일반적인 활용사례
- Dev / Test DB의 형상을 'production DB'와 sync 맞추는 것. 테스트 환경에서 쓰는 데이터가 실제 prod 데이터의 복사본이도록 유지하는 것
- DB Consolidation - migrating multiple DB instances to One RDS Instance.
- Continuous DB Replication - disaster recovery 등으로 활용 가능


cf. RDS 생성 화면에서
- EC2 instance storage Type을 설정할 수 있다.
  - General Purpose SSD (gp2) - performance baseline. 한 자릿수 ms의 latency / 3000 IOPS for extended period of time. volume size에 따라 상세한 성능은 다름
  - Provisioned IOPS SSD (io1) - RW Throughput이 gp2보다 높다.
  - Magnetic: 가장 느린 성능, 가장 낮은 비용

### Where should our Customer Store their Data?

S3
- Object Storage: written infrequently / read often에 적합.
  - 파일 변경이 있을 경우 파일 전체를 덮어쓰는 식으로 업데이트하기 때문.
- REST API to store / access data
- Serverless, Managed storage service
- Objects up to 5TB / Bucket has virtually no size limit

EFS (Elastic File System Storage)
- Managed file storage / use NFS protocol
  - 여러 개의 instance (VM / container)가 동시에 접근할 수 있음.
- Scale automatically
  - suitable for hosting file system with low operational overhead

FSx
- Managed file storage, support for certain file system
  - NetApp ONTOP, OpenZFS, Window File server / Lustre

EBS(Elastic Block Storage)
- Block Storage (Virtaul Hard Drives). Attachable to EC2 Instance
  - 따라서 autoscale은 지원하지 않음
- 여러 Size / Types가 있고, 필요한 걸 사용자가 스스로 선택해야 함

---

Customer 요구사항 파악하기
- 지금 데이터는 on-prem에서 file 형태로 생성됨. 한번 생성된 데이터는 바뀌지 않고, 다른 애플리케이션에서 참조하는 용도.
- 데이터는 분석 / 머신러닝 목적으로 사용.
- 생성 후 일주일 정도는 자주 쓰지만, 1년 정도 지나면 안 씀. 안쓰는 파일은 low-cost로 저장할 수 있었으면 좋겠음
- 리눅스 파일 시스템 사용중. 따라서 NFS 프로토콜 사용중이며, 클라우드에서도 그대로 쓸 수 있었으면 좋겠음
- latency requirement: lowest latency for writing files.

사용자의 요구에 부합하는 솔루션은 EFS로 보임.
- NFS 프로토콜 사용한 파일 시스템
- Direct Connect 사용해서 on-prem 컴포넌트가 접근 가능.
- Lifecycle Policy 지원.
- 문제는, AWS에 저장하기까지의 Latency. 
  - EFS를 쓰게 되면 Direct Connect를 쓰더라도 on-prem과 AWS 간 통신을 해야 하므로...

![rz4neyU3QOu-J3slN5DrtQ_14ed9f0304fb415c9d9ebd7c9eb058f1_Reading3 4A](https://github.com/inspirit941/inspirit941/assets/26548454/e45ee0fe-b2d4-4652-8795-4e7c13942248)
<br>

이 경우, hybrid solution인 AWS Storage Gateway를 적용할 수 있다. (https://aws.amazon.com/ko/storagegateway/)
- on-prem Application이 Cloud Storage에 접근할 수 있도록 지원하는 솔루션. 
- near-seamless integration with data security features btwn on-prem & AWS storage infrastructure.
- Low latency Writing + efficient Data Transfer to S3 bucket.
  - File System: NFS / SMB 프로토콜 지원.
  - Volume Gateway: iSCSI 프로토콜 지원.
  - Tape Gateway: iSCSI VTL 프로토콜 지원

AWS S3 File Gateway
- file interface into AWS S3.
- store / retrieve objects in S3 using file protocol (NFS, SMB (Server Message Block))
- on-prem application에 VM으로 실행됨. (VMware, Hyper-V, KVM 등)
- s3에 저장된 데이터를 file mount된 것처럼 사용 가능.


![스크린샷 2023-07-21 오후 12 41 09](https://github.com/inspirit941/inspirit941/assets/26548454/d398f838-aad8-43e7-b94d-a95dcacd4ec2)
<br>

- on-prem의 애플리케이션이 NFS를 활용해 storage gateway에 file write를 수행한다.
  - storage gateway 자체는 local device이므로, on-prem의 애플리케이션이 low-latency로 read / write 수행할 수 있다.  
- storage gateway는 async 방식으로 s3에 데이터를 저장한다.
  - file gateway의 경우 local data cache가 저장되므로, s3로 저장된 데이터를 read할 경우 low-latency 확보할 수 있다.

Storage gateway를 사용하면, s3의 lifecycle policy를 사용한 storage tiering이 가능하다.

![스크린샷 2023-07-22 오후 1 21 47](https://github.com/inspirit941/inspirit941/assets/26548454/7703778d-68b3-472b-8036-3c7ca990f6e6)


### Hybrid Solutions on AWS

migration을 진행할 때, Operational tool은 on-prem에서 쓰던 걸 그대로 유지하고 싶은 경우가 있음.
- AWS는 hybrid deployment을 지원하는 여러 서비스가 있다. https://aws.amazon.com/ko/hybrid/

**Compute** 중 소개할 만한 것들
- AWS outposts: AWS 서비스를 on-prem의 hardware racks / server에 실행할 수 있도록 하는 서비스.
  - super-low latency가 필요해서 traversing through internet 자체가 불가능한 경우.
  - 데이터가 반드시 특정 region의 데이터센터에 저장되어야 하는 등 Regulation 이슈가 있을 때.

**Containers** Orchestration tool
- AWS ECS / EKS AnyWhere: ECS / EKS 서비스를 AWS Cloud가 아니라 on-prem 환경에서 실행할 수 있다.
  - redundant effort / cost 를 줄일 수 있음.
  - ECS를 도입할 경우.. 보통 on-prem에 배포된 deployments를 AWS에 다시 배포해야 함. 필요시 코드를 변경해야 할 수도 있음.

![스크린샷 2023-07-22 오후 3 09 30](https://github.com/inspirit941/inspirit941/assets/26548454/195d9ed4-521a-4df0-903e-cd3041242e22)
<br>

ECS Anywhere를 도입할 경우 대략적인 사용방법
- Create Activation key. 이 key를 사용해서 on-prem에 있는 VM을 AWS ECS Anywhere 서비스에 등록한다.
- on-prem의 VM에 AWS의 System Manager Agent (SSM Agent)와 ECS Agent를 설치한다. 이 Agent는 앞서 만든 activation key를 사용한다.
- Application을 Deploy한다. 그럼 배포된 container는 ECS가 관리하게 된다.

**Storage**
- AWS Backup: Centralize Data protection management / compliance.
  - i.e. on-prem과 AWS에서 운영하는 VMware workload / data stored on AWS Storage gateway
- manage backup **across Environments.** on-prem과 AWS 둘다 활용해야 할 경우 도입을 고려할 만한 서비스.


**Networking**
- AWS Direct Connect

**Management**
- AWS Directory Service: 사용자가 MS Active Directory 서비스를 사용해서 AWS resource와 on-prem을 연결할 때 사용
- AWS IAM
- AWS CloudWatch / X-ray
- AWS Systems Manager
  - secure, end-to-end management solution for hybrid cloud environments.
  - helps manage & operate your resources **at scale**.

<img width="953" alt="스크린샷 2023-07-22 오후 5 02 40" src="https://github.com/inspirit941/inspirit941/assets/26548454/8f2dc1bd-bb05-4e7b-ac4c-5fbd2d11ef6c">
<br>

- 예컨대 on-prem과 AWS에 수많은 인스턴스가 있다고 할 때
- 모든 인스턴스에 특정 스크립트를 실행하는 작업을 자동화하는 Run Command라는 기능을 사용할 수 있다.
  - 관리 대상이 될 인스턴스는 전부 SSM Agent가 설치되어 있어야 한다
  - System Manager에서 tag나 metadata 등 특정 기준으로 인스터스를 group으로 묶어서 관리할 수 있다.
- SSM Agent가 리소스 management 기능을 수행하고, ECS Anywhere 서비스가 SSM Agent를 활용해서 on-prem VM의 container orchestration을 수행하는 것.
- System Manager에서 제공하는 기능이 진짜 많음. 
  - management에 필요한 여러 기능과 서비스의 집합이기 때문
  - Docs를 보는 것을 추천한다.

![6D-k_j1iTX-_pP49Ym1_Hg_d1cb53d39cc24dc09e9e2e7ccd8078f1_Reading3 5B](https://github.com/inspirit941/inspirit941/assets/26548454/ea4e005e-468f-42eb-a6f5-4383c8a11193)
<Br>

대략적인 구조
1. Access System Manager: AWS CLI나 web console로 접근
2. Choose System Manager Capabilities: resource에 어떤 작업을 수행할 것인지 선택. Run command 이외에도 여러 기능을 선택할 수 있다.
3. Verification and processing: 2에서 선택한 action을 수행할 권한이 있는지 IAM에서 확인한다. SSM Agent가 설치되어 있고 manage 기능이 활성화된 노드라면, 해당 작업을 수행한다.
4. Reporting: action 수행 결과를 기록한다.
5. System Manager operations management capabilities: 이 기능을 활성화하면 (Explorer, OpsCenter, incident manager 등) operational insight와 troubleshooing을 위한 automated remediation solutions을 제공한다.



<img width="938" alt="스크린샷 2023-07-22 오후 5 08 14" src="https://github.com/inspirit941/inspirit941/assets/26548454/e00205df-ba6f-4bcd-81a8-de0012fbf532">
<Br>

최종 아키텍처 구조는 위와 같다.
- On-Prem
  - AWS System Manager
  - AWS Backup
  - AWS ECS AnyWhere
  - AWS Storage Gateway
- AWS Cloud
  - AWS System Manager
  - AWS Backup
  - AWS ECS
  - AWS Storage Gateway
  - AWS DMS
  - AWS S3
  - VPC
    - NAT Gateway
    - AWS EC2
    - AWS RDS

### Solution Overview

<img width="940" alt="스크린샷 2023-07-22 오후 5 17 54" src="https://github.com/inspirit941/inspirit941/assets/26548454/dbb092ec-ad6c-4959-9154-65cee9f4a57e">
<br>

아키텍처 설명
- Network Connectivity: 
  - AWS Direct Connect: on-prem 데이터센터와 AWS Cloud 간 통신 목적. Send high volume of data / consistent Throughput 요구사항 반영.
  - NAT Gatway: AWS에 올라간 workload는 Private Subnet. 따라서 public internet과 통신이 가능하도록 public subnet에 NAT Gateway를 설치했다.
    - 외부로부터 리소스 다운로드는 가능하되, 외부에 workload 정보가 노출되지 않음.
- Workload
  - AWS ECS (AnyWhere): container workload는 migration 여부와 상관없이 ECS로 관리 가능. container 설정이나 코드 변경 없이 할 수 있다.
  - AWS ECR: Container Registry는 지금처럼 Dockerhub 유지할 수 있음. 필요 시 migrate 가능.
  - EC2 Cluster Group: container를 구동할 AWS Cloud 리소스. EC2를 사용했으므로 필요한 AMI는 직접 관리할 수 있고, ssh 통신도 가능하다.
    - 일단 EC2 Volume의 증감은 EC2 Autoscaler를 적용했다. container autoscale은 좀 다른 이야기이므로 여기선 제외.
  - Application Load Balancer.
- DB
  - AWS RDS: multi-AZ deployment (1 instance, 2 AZs) for fault-tolerance.

On-Prem Requirements
- AWS Storage gateway: on-Prem에서 AWS로 데이터를 저장하기 위한 요구사항. latency 문제 해결.
  - NFS 방식으로 파일을 저장하면
  - local cache가 on-prem에 남고, async 방식으로 s3 storage에 저장됨.
- AWS System Manager: on-prem과 AWS 리소스를 같은 interface로 manage할 목적.
  - run script / patch...
- AWS Backup: on-prem과 AWS 리소스의 백업본을 관리하기 위한 용도

### Wrap up - Archtecture Next Level

<img width="938" alt="스크린샷 2023-07-22 오후 5 08 14" src="https://github.com/inspirit941/inspirit941/assets/26548454/be3818bb-a211-42ac-a936-df00986b7322">
<br>

- Network Connectivity
  - VPN over the Internet 도입: Direct Connect에 문제가 생길 경우를 대비. for redundancy / resilience
    - Direct Connect 자체는 2 AZ에 연결하기 위해 2개의 endpoint를 관리한다. 따라서 AWS cloud 내부에서의 physical 이슈가 생길 가능성이 낮음.
    - on-prem 쪽에서 router 문제로 Direct Connect와의 통신에 문제가 생길 수 있음
- AWS RDS: DB instance 자체는 managed service의 autoscale이 적용되지 않음. auto storage scaling을 적용하면 underlying storage mechanism을 DB 관리자가 수동으로 관리할 필요 없어지게 됨.
- Secondary AWS Region 구성 for failover. (enterprise customer이므로)
  - AWS에서 제공하는 failover 방법은 매우 많음. https://aws.amazon.com/ko/blogs/tech/disaster-recovery-dr-architecture-on-aws-part-i-strategies-for-recovery-in-the-cloud-3/
  - IaaS 방식으로 구성하는 것이 필요.
  - AWS S3의 lifecycle policy에서 Cross-Region Replication 도입.
    - 백업용 S3에는 storage cost를 낮추기 위해 automate tiering을 같이 도입하는 것도 좋다.
  - Multi-region Aurora가 아니라면, AWS DMS로 Data Replication도 가능. Read Replica, for resiliency.
- ECS에서 Container의 scale 여부를 관리하는 건 EC2 Autoscale과 완전히 다른 로직. 따라서 ECS의 autoscaling 기능을 알아두는 것도 필요하다


