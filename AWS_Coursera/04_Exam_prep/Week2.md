## Design Resilient Architecture

### Scalable / Loosely coupled architecture

under load / failure가 발생해도 서비스 영향이 최소화될 수 있도록 설계한다.

![스크린샷 2023-09-10 오후 3 40 24](https://github.com/inspirit941/inspirit941/assets/26548454/c4a20b11-67cf-4d98-b387-4aceecb440f0)
<br>

- horizontal / vertical scaling.
- Elasticity: 일반적으로 autoscaling 개념과 함께 쓰이며, match capacity with your demand.
  - demand는 ever-changing. linear하지 않다.
  - AWS는 configuration / autoscaling 지원. 필요하면 resource 투입을 늘리고, 필요 없어지면 줄이거나 0으로도 변경한다.
  - performance efficiency, operational excellence, cost optimization

AWS Autoscaling / EC2 autoscaling의 기능? EC2 autoscaling에서 적용할 수 있는 policy는?


![스크린샷 2023-09-10 오후 3 46 39](https://github.com/inspirit941/inspirit941/assets/26548454/9f68c32e-b305-4f66-9101-ea206cb00646)
<br>

Compute Workload 종류: containers, serverless, virtualization
- 어떤 상황에서 무엇을 쓰는 게 적절한지. 각각의 benefits / limitations?
  - 예컨대 EC2는 목적에 맞게 다양한 종류의 instance type을 제공한다. (CPU / Memory)

![스크린샷 2023-09-10 오후 5 54 38](https://github.com/inspirit941/inspirit941/assets/26548454/d69e460a-20a0-4030-afc6-ece9eb7ace64)
<br>

Storage Service for multi-tier architecture

- DynamoDB: NoSQL DB for low latency performance at extreme scale
- RDS: managed RDBMS
  - read replica: performance / availability.
    - Cache와 개념이 다름. DB와 통신하는 데서 오는 overhead는 그대로이기 때문.
  - Multi-AZ designs: scale을 지원하지는 않음. high availability.
- Aurora: cloud native RDB
- Redshift: for data warehouse needs

Cache
- AWS CloudFront
- ElastiCache
- DynamoDB Accelerator

cf. RDS Proxy를 사용해서 application scalability를 확보하고, DB failure resilient / secure 확보할 수 있다.
<br>

AWS Edge networking services; CloudFront, Route53, AWS Global Accelarator.
- transmit your data securely / improve latency

위와 같은 서비스들을 활용해서 불필요한 network hop 제거, encrypt data, control application access which helps resiliency / performance.

---

![스크린샷 2023-09-10 오후 5 57 47](https://github.com/inspirit941/inspirit941/assets/26548454/7ec19ea9-b166-4171-9666-9f208bd45905)
<br>

예시: file transfer service
- do not have to host / manage your own file transfer service. 모든 종류의 operation overhead를 최소화한다.

AWS Transfer Family: create, automate, monitor file processing workflows without your own code or infrastructure.
- support up to 3 AZs
- backed by autoscaling
- redundant fleet (fault tolerance) for your connection / transfer request


<img width="955" alt="스크린샷 2023-09-11 오전 9 37 33" src="https://github.com/inspirit941/inspirit941/assets/26548454/dc71a3bc-3fbc-4081-84dc-ebd6b640c905">
<br>

- Service-oriented architecture: making SW Components reusable via service interfaces
- microservice architecture: go further to make components smaller / simpler
- distributed system: rely on communication networks to interconnect components
  - distributed system의 컴포넌트는 다른 컴포넌트의 동작에 영향을 주지 않는 구조.

microservice 기반 approach / design -> well-defined APIs.
- API-driven
- Event-driven
- data streaming

AWS의 managed / serverless service 활용해서 구축할 수 있다.

<img width="955" alt="스크린샷 2023-09-11 오전 9 57 09" src="https://github.com/inspirit941/inspirit941/assets/26548454/17de38ff-0d5f-46fd-ab73-d007faa7dadf">
<br>

serverless
- operational model with no infrastructure provision or manage.
- automatically scales by unit of consumption.
- pay for value billing mode.
- built-in availability and fault tolerance.

AWS API Gateway: Scales automatically, many api usecases do not require management. <br>

AWS Lambda: serverless, event-driven compute service, that gives you the ability to run code for virtually any type of application or backend service.
- scale-related terms: concurrency / transaction

AWS SQS: high-throughput queue.
- 예컨대 BE와 FE 성능차이가 나서 scale independently 필요할 경우, async / durable msg stores 용도로 사용 가능.
  - request ingestion / response를 분리한다.


<img width="959" alt="스크린샷 2023-09-11 오전 10 23 34" src="https://github.com/inspirit941/inspirit941/assets/26548454/1f140550-2ab9-4b17-86a9-36100d2c14ed">
<br>

Decoupling
- components remaining autonomous / unaware of each other as they complete their work, as part of a larger system.
- design scalable / loosely coupled architectures.
- Synchronous decoupling: 서비스 동작을 위해서는 항상 available해야 하는 컴포넌트가 있는 경우
- Asynchronous decoupling: durable한 컴포넌트를 사용해서 통신하는 경우

### Walkthrough Question 2.1

<img width="958" alt="스크린샷 2023-09-11 오전 10 34 24" src="https://github.com/inspirit941/inspirit941/assets/26548454/faff2cd2-d054-46c6-ac62-b7ef06eec621">
<br>

Answer: D. FIFO는 exactly once processing. 메시지 순서가 보장되고, consumer process -> delete할 때까지 queue에 메시지가 남아 있다.
- A. kinesis는 duplicate data stream이 발생할 수 있다. producer retry / consumer retry 이슈.
- B. A와 마찬가지.
- C. SNS는 queue 서비스가 아님.


### Design HA / fault-tolerant architecture

<img width="679" alt="스크린샷 2023-09-11 오후 1 30 15" src="https://github.com/inspirit941/inspirit941/assets/26548454/e0692b63-a6eb-499d-88db-2636a8784961">
<BR>

High Availability: keep your system up and running, and providing service as often as possible.
- 장애가 발생하더라도 replace / fix ASAP. downtime이나 outage를 완전히 예방하는 건 아님.
- reduce outage / stay operational fast / automatic recovery

Fault tolerance: actual ability of a system to keep operating in the event of a failure.
- 특정 component에서 문제가 발생하더라도, 해당 컴포넌트를 제외한 나머지는 정상 동작한다.
- minimize failure, continue operate through failure. 따라서 이 형태의 system design은 HA design보다 expensive

Disaster Recovery: disaster 발생 시의 plan / process.
- onsite(or AWS) backup to switch your environment
- CloudFormation templates to provision your environment inside AWS after that disaster.
- ensuring redundancy of your normal operational components (servers / DB)
  - 이외에도 서비스 동작에 필요한 data replication, traffic management, failure detection 등의 작업도 고려사항에 넣어야 함

<img width="686" alt="스크린샷 2023-09-11 오후 1 37 30" src="https://github.com/inspirit941/inspirit941/assets/26548454/0048f91a-792e-41c7-b8d1-87f0d03abacd">
<img width="681" alt="스크린샷 2023-09-11 오후 1 38 42" src="https://github.com/inspirit941/inspirit941/assets/26548454/a7b30336-e822-4a10-9916-076899ec07a8">
<br>

recovery strategy에 참고할 수 있는 Disaster recovery Objectives
- Recovery Point Objectives (RPO)
- Recovery Time Objectives (RTO)

RPO: max amount of time since the last data recovery point.
- how often does the data need to be backed up?

RTO: max acceptable delay btwn interruption & restoration.
- application이 unavailable할 수 있는 최대 허용시간?

<img width="953" alt="스크린샷 2023-09-11 오후 1 39 45" src="https://github.com/inspirit941/inspirit941/assets/26548454/24d7cc81-6ac7-423d-a9aa-0b6c2baf1072">
<Br>

Active / Passive
- Backup & Restore
- Pilot Light
- Warm Standby

Active / Active
- multi-site active / active

각각의 전략이 어느 정도 수준의 RTO와 RPO를 보장하는지 확인해서, 적절한 전략을 선택하면 된다.
- Object Storage: S3
- File Storage: EFS / Amazon FSx
- RDS의 경우 Multi-AZ deployment. primary DB 죽으면 failover 진행. -> access downtime은?
- Aurora의 경우 Cross Region failure에 어떻게 대응하는가? failover에 걸리는 시간은?
- DynamoDB는 어떤가?

Cloud Native가 아닌 legacy 서비스의 경우... AWS Elastic Disaster Recovery 적용이 가능함.
- EC2: AMI와 EC2 image builder를 disaster recovery strategy에 포함할 수 있다.

<img width="956" alt="스크린샷 2023-09-11 오후 1 51 26" src="https://github.com/inspirit941/inspirit941/assets/26548454/650613ee-24ae-4bb2-9dc8-2d9e7238f1ce">
<br>

- how routing tables work
- VPC peering connection
- AWS Transit Gateways
- AWS Site-to-Site VPNs
- AWS Direct Connect locations
- AWS Direct Connect Gateways
- AWS Route53 resolver

automate deployment에 사용될 수 있는 서비스들
- VMs: Beanstalk / CloudFormation / OpsWorks
- Container based: ECS / EKS

코드 내의 취약점이나 보안관련 이슈 탐지
- AWS Inspector
- Amazon CodeGuru

Handle SPOF of EC2 Instance / entire AZs
- ELB across multi AZs, with EC2 autoscaling Groups
- automatic failover to other region
  - Route53을 활용한 DNS routing
- Global Accelerator 활용한 availability / performance 향상
- RDS Proxy 활용한 HA / managed DB proxy. makes applications scalable.
  - serverless application은 spiky DB Connection 발생 가능. DB 리소스를 일시적으로 고갈시킬 수 있다.
  - RDS proxy는 pull / share connections established with DB. improving DB efficiency and application scalability.
  - RDS proxy 적용 시 Aurora / RDS DB의 failover time이 66%까지 감소. 
  - DB 관련 credentials는 Secret Manager / IAM으로 관리할 수 있다.

서비스의 continual improvement: track and respond to key metrics for applications / infrastructures in your environment.
- AWS CloudWatch / AWS X-ray
- initiate automated actions based on key metrics using cloudwatch alarms
- 변경사항을 near real-time으로 확인하기 위한 EventBridge

AWS Polly도 최근에 시험에 나온다고 함.


### Walkthrough Question 2.2

![스크린샷 2023-09-12 오후 8 54 01](https://github.com/inspirit941/inspirit941/assets/26548454/ef799de0-b0b7-4cde-93d8-9e799ddaf3cd)
<br>

Answer: C. 
- A. HA는 multi-AZs에 배포해야 함
- B. Peer VPC는 HA 요구사항과 직접적인 관련이 없음
- D. ELB는 Single Region의 multi-AZs 대상으로 구성할 수 있음.


### Wrap up

![스크린샷 2023-09-13 오전 9 58 29](https://github.com/inspirit941/inspirit941/assets/26548454/700bdf57-befd-47e2-8faa-1be110873c4f)
<br>

AWS 장점 중 하나가 capacity 고민할 필요가 없다는 것. 
- needs에 따라 autoscale 가능.
- 사용한 만큼만 비용 지불

HA와 fault-tolerance / disaster recovery 개념 구분하기.
- resilient workloads across AZs
- single Region multi-AZ 단위: SPOF 방어를 위한 ELB / EC2 autoscaling groups
- cross-Region resilience: Route53 routing / latency-based routing. AWS Global Accelerator

monitoring workloads: cloudwatch / X-ray

