## Design High-Performing Architecture

### Determine high-performing, scalable storage solutions

![스크린샷 2023-09-13 오후 10 23 03](https://github.com/inspirit941/inspirit941/assets/26548454/b41d4ce8-70ae-453e-bcbb-fb9307e24840)
<br>

AWS에서 제공하는 storage 타입은 크게 세 가지. object / block / file
- access method / patterns, required throughput, frequency of access / updates, durability, availability별로 결정됨.
- 이외에도 각 solution의 scale 여부나 동작방식에 따라서도 다름.
  - EBS는 구조상 scaling / performing 방식이 S3나 EFS와 완전히 다름. 
    - 예컨대 EC2 file system으로 EBS를 쓰고 있다면, scale하기 위해서는 volume을 수동으로 변경해야 한다.
    - 대신 life configuration changes 옵션을 제공함
  - EFS는 파일을 추가할 때, 공간이 부족하면 자동으로 scale 진행함. 따라서 operational support를 적게 하고 싶다면 EBS보다 EFS가 파일 시스템으로는 적합할 수 있다.


EBS에서 type 선택하기
- DAS
- SAN
- Persistent Storage for EC2
  - EC2는 instant storage / Persistent Storage 선택이 가능함.

EBS snapshot: backup / disaster recovery에 사용할 수 있는 기능.
- S3에 저장되므로 Region resilient


EFS: network-based file systems, NFS, hybrid access (access via VPN / Direct Connect)
- shared file system; great for large repositories, dev environment, media stores / directories..
- types: General Purpose, Max IO
- cost optimization lifecycle policies
- cf. AWS Storage Gateway도 hybrid storage solution에 적합한 서비스.

FSx: EFS와 비슷하지만, managed windows file system / shared drive
- supports SMB / windows NTFS
- supports active directory integration
- HA, scalable -> Great solution for hybrid storage

![스크린샷 2023-09-14 오후 8 10 09](https://github.com/inspirit941/inspirit941/assets/26548454/ff30f3b2-36bd-4b39-aa21-8d85491d66bc)
<br>

Lifecycle policy: 데이터가 쌓이는 속도나 빈도에 따라 결정이 필요함
- storage에서 감당할 수 있는 upper bound 고려해서 선택해야 함
  - 예컨대 지금은 3TB가 필요하지만, 향후 5년간 100TB까지 증가할 수 있는 서비스라면?
- low latency가 필요하다면?
  - EBS volume은 latency가 낮고 performance도 나쁘지 않음. usecase와 IOPs 참고해서 적절한 타입 선택
- 성능 향상을 위해 다른 서비스와 연계할 수도 있음.
  - S3 Accelerator, caching with cloudfront


### Walkthrough question 3.1

![스크린샷 2023-09-14 오후 8 54 56](https://github.com/inspirit941/inspirit941/assets/26548454/6493375f-88af-4ef1-8652-b39782361d1b)
<br>

Answer: B. 일반적으로는 파일 크기가 100MB를 넘어가면 multipart upload를 권장함. throughput / quick recovery가 되기 때문. AWS S3의 copy command는 file size에 따라 자동으로 이 기능이 실행된다.
- A: multipart upload를 수행하려면 파일 사이즈가 100MB 넘어야 함. 5MB로 분할할 필요 없음. 또한 업로드 이전에 5MB 단위로 쪼개뒀으므로, reassemble to original file size가 안 됨. B보다 시간도 오래 걸림.
- C: console로 업로드하는 로직은 network protection 지원하지 않고, multipart upload도 지원하지 않음.
- D: SFTP로 업로드할 수는 있으나 요구사항인 resume failed upload easily를 지원하지 않고, 다른 선택지보다 품이 더 드는 불편한 작업임.


### Design high-performing and elastic compute solutions

![스크린샷 2023-09-15 오전 10 35 46](https://github.com/inspirit941/inspirit941/assets/26548454/65c9d6e1-6bc7-4db6-bf63-04a2e8c5683c)
<br>

compute solution은 크게 세 가지. instance (VM) / containers / functions
- instance (EC2): 요구사항에 맞게 다양한 type을 선택할 수 있음. 각 type마다 cpu/memory 뿐만 아니라 network bandwidth, resource rations, 기타 다양한 features가 있다는 걸 고려해서 선택해야 함
- containers: ECS, EKS
  - ECS: accepts containers with instructions on where / how to run the containers 
    - Fargate: serverless compute for containers.
    - EC2: 컨테이너가 동작할 환경으로 VM 선택할 수 있음.
  - EKS: AWS-powered k8s on EC2
- functions: small piece of code, starts the code running without EC2 instances.
  - 이벤트가 발생할 때 invoke. timeout은 최대 15분
  - 15분 이상의 execution time이 필요하면 step function 사용을 권장.
  - all cloudFront의 edge location에 전부 배포하면 globally execute가 가능하다. 반응성 강화.

![스크린샷 2023-09-15 오후 1 21 37](https://github.com/inspirit941/inspirit941/assets/26548454/4a18805e-5b52-4ea0-b21a-a3d00c0d4541)
<br>

architecting solution
- ELB나 SQS를 붙여서 decouple the workloads
- visibility to scale. - cloudwatch metrics, alarms, dashboards
  - EC2 autoscaling에서 metrics가 어떻게 사용되는지.
  - not available by default: amount of EC2 memory usage on EC2 instance
- application needs가 주어지면, 적절한 EC2 타입 선택.
  - instance family 이해하기.
- 굳이 EC2가 아니어도, performance requirements와 scalable 등 application 조건에 부합하는 AWS Service를 선택할 수 있어야 함
  - 예컨대 backend Web Service인데 usage가 vary throughout the day -> HA / elastic한 구조가 by EC2 autoscaling, ELB


### Walkthrough question 3.2

![스크린샷 2023-09-15 오후 1 36 39](https://github.com/inspirit941/inspirit941/assets/26548454/53b68092-3279-4294-ab7c-c242b6a0b590)
<BR>

Answer: C. processing layer가 peak time에 scale up이 빠르게 되지 않아서 발생. SQS를 Layer 사이에 두고, queue reaches certain depth일 때 scale할 수 있도록 한다. 추가로, queue라서 메시지 유실 방지할 수 있다.
- A. 퍼포먼스 증가는 맞지만, cost도 증가함. 프로세스 처리가 없는 저녁이나 밤 시간대에는 Idle상태로 비용만 나간다. instance size를 높이는 게 processing을 증가시킨다는 보장도 없다.
- B. spot instance는 scalable / available을 보장하는 방식이 아니고, on-demand instance라 한들 ec2 instance와 스펙 자체는 동일하기 때문에 성능 향상을 기대할 수 없음.
- D. lambda의 execution time은 max 15 minutes.

### Determine high-performing DB solutions

![스크린샷 2023-09-15 오후 1 47 41](https://github.com/inspirit941/inspirit941/assets/26548454/70649ea3-8c12-4d5f-93d8-d0b5b647f9b0)
<br>

- AWS에서는 여러 종류의 DB를 지원한다 - relational, in-memory, key-value, document, graph, time-series, ledger.
- DB provisioning / backup, recovery 등은 AWS가 담당한다. self-healing storage / automated scaling
- Availability, Consistency, Fault-tolerance, Latency, Durability, Scalability, Query capability 등 다양한 조건 중 usecase 요구사항에 부합하는 걸 선택하면 됨.
  - 좀더 고민한다면, RDBMS 선택했을 때 performance를 어떻게 향상시킬 수 있는지
  - traffic의 대부분이 read operation이라면?
  - how to configure read replicas on RDS
  - read replica와 multi-AZ deployment의 차이.

![스크린샷 2023-09-15 오후 2 28 44](https://github.com/inspirit941/inspirit941/assets/26548454/5cae9cff-17d6-47bb-a808-af72113841ea)
<br>

Aurora: improved version in RDS family.
- cluster 기반 아키텍처. single primary instance + 0 or more read replicas.
  - Aurora read replica는 read / multi-AZ 장점 둘 다 있음. availability / read operation 둘 다 가능.
- Aurora Storage는 RDS와 다름. local storage를 쓰지 않고, shared cluster volume을 쓰기 때문
  - faster provisioning, availability, better performance

---

usecase에 맞는 DB service 선택하기
- consistent single-digit ms performance와 extreme high volumes가 필요하다면
  - DynamoDB
    - 한 자릿수 ms performance regardless of loading, without tuning effort. 
    - data replicated multiple nodes by default. 
    - fast & backed by SSD. 
    - handles backup - point-in-time recovery
    - encryption at rest
    - support event-driven integration to take actions
- regional failover 발생 시
  - RDS는 regional resilient service. AZ failover
  - Aurora는 global resilient. Region Failover.
- DB Throughput 높이기 위한 방법
  - ElastiCache: managed in-memory cache (redis, memcached)
  - DAX: DynamoDB Accelerator로, access data in ms & cache (item, query)
  - RDS proxy: reduce the stress of compute / memory resources
    - 예컨대 functions -> DB 방식이라면, functions invoke할 때마다 DB connection이 발생함.
    - RDS proxy를 써서 large number / frequency of connection 지원할 수 있음.
  - RDS의 autoscaling 기능도 있긴 한데
    - storage increment가 max storage threshold 이상은 되어야 trigger된다.
- Aurora Serverless
  - On-demand autoscaling configuration이므로, simple / cost-effective options for infrequent / intermittent / unpredictable workloads.
  - Aurora DB의 version 관리를 해줌 - provisioning 자동.
  - provides the same shared cluster storage; six copies of your data across 3 AZs
  - Aurora ACU (access capacity units): 일정량의 compute / memory 지급.
    - 사용자가 min / max ACU를 지정할 수 있음. 지정한 범위 내에서 scale.
    - ACU는 scale to 0가 가능하고, 일정 시간 Inactivity -> paused 가능.
    - paused되면, storage하는 만큼만 비용을 내면 된다.

### Walkthrough question 3.3


![스크린샷 2023-09-16 오후 4 17 44](https://github.com/inspirit941/inspirit941/assets/26548454/b91b8e94-b6ce-4ad6-a675-e9faa11c991c)
<br>

Answer: A, D. key-value store + scaleable로는 DynamoDB가 적합하고, Kinesis Data stream은 DynamoDB의 item-level change를 감지해서 변경사항을 Data lake에 저장하는 등의 작업을 수행할 수 있다.
- B: DocumentDB는 key-value DB 아님
- C: lambda function으로도 할 수는 있으나, 코드를 작성해야 한다는 점에서 more operational overhead.
- E: kinesis -> Redshift로 전송하는 게 가능하지만, S3로 데이터를 저장하는 게 더 나은 방식. S3에서는 combine data from different sources for analysis를 지원하므로 data lake의 Operational overhead가 더 적다.


### Determine high-performing / scalable network architecture

![스크린샷 2023-09-16 오후 4 25 41](https://github.com/inspirit941/inspirit941/assets/26548454/8fe97748-c0c5-4611-8102-b7e343d4b0b5)
<br>

architecture 간 통신에서 반드시 쓰이는 서비스들이므로 중요함.
- AWS에서 네트워크 서비스는 전부 virtualized & available in different types / configurations.
- 따라서 bandwidth, latency, jitter, throughput 요구사항에 맞게 선택할 수 있음.
  - optimize network traffic: EBS-optimized instances / S3 transfer Acceleration / Cloudfront
  - reduce network distance or jitter: Route53 latency routing, VPC Endpoints, Direct Connect, Global Accelerator

Integrate storage services / data transfer methods / networking options to build solutions that protect your data with unmatched durability, security. <br>

![스크린샷 2023-09-16 오후 5 50 53](https://github.com/inspirit941/inspirit941/assets/26548454/c0a9fc21-66f4-44b7-91b0-d175a6b42001)
<br>

VPC: regional resilience service.
- custom VPC는 Private, without explicit configuration.
- build order: VPC, subnet, route tables, internet gateway, network ACLs, security groups. 여기까지 한 이후에 custom VPC
  - update security groups, add resources (i.e. NAT gateway), peer to another VPC, create endpoints

![스크린샷 2023-09-16 오후 5 56 07](https://github.com/inspirit941/inspirit941/assets/26548454/4ad19d77-7177-428b-ad88-7f611e900236)
<br>

Hybrid model, with AWS VPC & on-prem DataCenter
- privately communicate to transfer data & messages across system
  - design global architecture across 2 or more regions.
- Connect: through VPN Connections / Direct Connect같은 service 이용
  - 각각의 throughput / performance 를 알아야 요구사항에 맞는 걸 선택할 수 있다.
  - transit Gateway: connect multiple VPC to a remote network. (VPN이나 Direct Connect에 같이 적용할 수 있다.)
  - cloudHub: help you create 'hub & spoke model' for connecting networks.

Connection btwn VPCs: VPC peering, Transit Gateway, Direct Connect gateway

![스크린샷 2023-09-16 오후 6 32 28](https://github.com/inspirit941/inspirit941/assets/26548454/4e4f15f4-556b-4753-bc8c-2bb20f06dd5a)
<br>

private connection을 제공하는 endpoint service: PrivateLink, VPC Endpoints
- privateLink: 다른 VPC에 있는 애플리케이션과 통신해야 하는데, public으로 오픈하고 싶지 않거나 VPC peering을 쓰고 싶진 않을 때.
- gateway endpoints: AWS public service에 붙여서, sit inside public zone.
  - S3나 DynamoDB같은 public service를 NAT gateway 같은 설정이 없는 private instance / subnet에서 접근하려고 할 때 사용할 수 있음.

![스크린샷 2023-09-16 오후 7 20 14](https://github.com/inspirit941/inspirit941/assets/26548454/a1e52f70-4eb5-4ed8-8efd-26314cde2cec)
<br>

public resource에 send request / establish connection할 수 있는 방법은 여러 가지. 각각의 feature에 맞는 방법을 선택해야 한다.
- 예컨대 2 different region에 배포된 backend web server. website에 접근하려는 사용자의 지리적 위치에 가장 근접한 region으로 트래픽을 routing하려면
  - Route53의 routing policy를 이해해야 한다. 이 경우 route53의 geoproximity routing policy를 적용하면 됨
- Route53에서 제공하는 기능의 이해.
  - record type you can create / why you need to use Route53

![스크린샷 2023-09-16 오후 7 23 31](https://github.com/inspirit941/inspirit941/assets/26548454/2e5e4162-926b-4e05-8dd3-765a1a1e6f6b)
<br>

Global Accelerator: 애플리케이션의 network performance의 최적화를 위한 AWS 서비스. <br>

network performance를 높이는 다른 방법 중 하나: cache assets closer to your end users.
- AWS edge location의 장점 최대한 활용 - CloudFront

![스크린샷 2023-09-17 오후 1 09 39](https://github.com/inspirit941/inspirit941/assets/26548454/3288e2c3-5e16-4546-b76f-1b88f025c46f)
<br>

Data Migration / Ingestion을 위한 network performance.
- AWS DataSync, AWS SnowFamily, AWS Transfer Family, AWS Database Migration Service 등등..
- Amount / Type of Data, source & destination of data migration에 따라 적용에 적합한 서비스는 다름.


![스크린샷 2023-09-17 오후 2 48 41](https://github.com/inspirit941/inspirit941/assets/26548454/ae22fe67-2072-4a00-a4fd-458262d30022)
<br>

- know the layer of OSI model for each LB
  - OSI model이 network fundamental에 포함하는 방향을 권장.

![스크린샷 2023-09-17 오후 2 50 21](https://github.com/inspirit941/inspirit941/assets/26548454/0bc20f2e-6626-49c8-92d1-37e4fd4edd23)
<br>

scalability 관련 예시: 예컨대 위 구조에서 real-time 요구사항이 있어서 availbility 보장 수치를 99.9 -> 99.999% 로 올려야 한다면?
- load balance cluster for active-standby pairs
- Route53 provides a global DNS service that can be used as a public / private endpoint
- DNS healthchecks to route traffic to healthy endpoints / independently monitor the health of your applications.
- autoscaling, lifecycle hooks with cloudWatch events, route53, lambda functions 등을 사용할 수 있음

어쨌든 원칙을 지키면 됨
- no SPoF
- use automated monitoring / failure detection / failover mechanisms for both stateless & stateful components


![스크린샷 2023-09-17 오후 4 56 36](https://github.com/inspirit941/inspirit941/assets/26548454/3e5387f7-5783-409a-901a-8b6dcd6d729c)
<br>

how to build a global, highly scalable serverless solutions in this architecture?
- S3 website hosting: serve static content
  - route53 latency / failover routing - for optimal performance with some built-in resiliency
- DynamoDB global tables: low latency, performance, cross-region data replication.

여기에 추가할 수 있는 것?
- add CloudFront: performance, reliability, security, and add a cache
- Gloabl Accelerator: S3 multi-region access points (buckets in multiple regions) -> reliability, security, performance

### Walkthrough question 3.4

![스크린샷 2023-09-17 오후 5 01 41](https://github.com/inspirit941/inspirit941/assets/26548454/e1bd4618-1a73-4c70-a04a-1dee5cf1815f)
<br>

Answer: C. AWS privateLink connection 세팅 방법으로, privateLink는 one or more consumer VPCs 와 통신할 수 있는 client server를 설정함. directional access to a specific service, or set of instances in the service provider VPC.
- 위 문제의 경우 shared service와 통신해야 하는 consumer가 여러 개. 따라서 privateLink가 가장 적절한 선택지
- privateLink를 설정하려면
  - Network LB 생성하고
  - service Consumer Role을 IAM에 생성해주고
  - shared service가 배포된 VPC에 endpoint connection을 설정하고, auto accept를 설정해준다
  - creat consumer endpoint in each VPCs trying to access the shared VPC, and point to the network LB in the shared service VPC
- A: CAA를 설정하는 건 which certificate authorities can issue a certificate for a domain or subdomain을 의미함. 이게 requirement에 도움 안 됨.
- B: VPC peering은 number of connection에 제한이 있다. 1 VPC 하나에 최대 125개까지만 가능함. 문제를 보면 account가 50개 정도, 하나의 account에는 4 VPC가 있음. 제한을 초과하므로, shared VPC에서 peer connection이 불가능하다.
- D: VPN으로 VPC 간 connection을 생성하는 건 가능하지만, maintain / operate VPN connection의 overhead가 privateLink 구성하는 것보다 훨씬 더 크다.


### Determine high-performing data ingestion / transformation solutions

![스크린샷 2023-09-17 오후 8 36 50](https://github.com/inspirit941/inspirit941/assets/26548454/b6a0fdd3-6ced-4280-bff4-a12c43168510)
<br>

data ingestion: process of getting data; collecting & curating & preparing data from the source system to AWS for storage / data lakes / ML, etc <br>

패턴은 크게 두 가지
- homogeneous: move the data to the destination in the same format / storage engine as the source.
  - 보통 transfer speed, data protection for serving the integrity, automating continuous ingestion
  - cloud-based ETL services; AWS Athena, Amazon EMR 사용.
- heterogeneous: destination data storage에 저장할 때 data transformation이 수행되는 것
  - data type / format을 destination requirements에 맞게 작업.
  - Streaming data; AWS kinesis, Amazon Managed Streaming for Apache Kafka. 
    - provide the collection / processing / analysis of data.
  - kinesis data streams: real-time data streaming with Scalability, durability
    - producer는 data push - group of stored data units **'record'**. pipeline에서 처리할 수 있는 단위.
    - continuous capturing multi-GBs of data every second
  - kinesis data firehose: loading data streams into data stores.
    - simplest approach for capturing, transforming, loading data streams into stores.
  - kinesis data analytics: includes basic data transformation options

![스크린샷 2023-09-18 오후 4 38 54](https://github.com/inspirit941/inspirit941/assets/26548454/639ab478-79ce-4953-b854-325679f7dd2f)
<br>

Data transformation <br>
ETL을 거친 데이터는 feed to ML 등 여러 용도로 쓸 수 있다. 보통 이걸 더 편리하게 하려고 organized / cataloged.
- Optimizing these process; AWS EMR, AWS Glue, AWS Lake Formation
  - S3에 저장된 데이터의 경우 EMR / Glue 사용할 수 있음. S3가 scale horizontal이기 때문에, EMR / Glue를 사용하면 massive scale / highly distributed process 적용할 수 있다.
- Data Lake on S3, using EMR cluster
  - transform your data to Parquet (column-based) / use lambda functions to transfer your data in a data lake (S3)

![스크린샷 2023-09-18 오후 4 39 05](https://github.com/inspirit941/inspirit941/assets/26548454/889369b1-d609-4e28-95b8-d338f46e1b61)
<br>

Data Analytics: AWS Athena, AWS Lake Formation, AWS QuickSight
- data lake -> popular way to store / analyze data (it supports multiple data types from a wide variety of sources)

![스크린샷 2023-09-18 오후 7 35 23](https://github.com/inspirit941/inspirit941/assets/26548454/556211f5-45c1-4d33-a3ee-a6db9eb27689)
<br>

data lake에 data ingestion
- kinesis data firehose, SnowFamily, Glue, AWS Data Sync, Transfer Family, Storage gateway, Direct Connect, AWS DMS

예시: transfer data from on-prem to Cloud?
- snowFamily, Transfer family, Direct Connect, DMS... -> 어떤 경우에 써야 하는가?


### Wrap up

![스크린샷 2023-09-18 오후 7 38 04](https://github.com/inspirit941/inspirit941/assets/26548454/7c6b44b2-0574-4f89-9b62-929c5ca7a394)
<br>

High Performing / scalability in
- storage
  - object / block / file storage 차이점
  - S3, EFS, FSx, EBS 등의 services
- compute
  - 서비스 간 scalable 차이; EC2, Batch, EMR, Fargate, Lambda
  - SQS, SNS 특징.
  - 기타 serverless 서비스들; api gateway, step functions, eventbridge, AWS AppSync
    - api gw: throttling / quota 설정해서 too many request 방지, improve performance.
    - appSync: provides robust, scalable GraphQL interface.
      - combine data from multiple sources (DynamoDB, Lambda, HTTP API)
- network data ingestion
- data transformation


![스크린샷 2023-09-18 오후 8 53 28](https://github.com/inspirit941/inspirit941/assets/26548454/2b9f5130-a4c9-4585-a332-cea2cfd0c233)
<br>

RDS, Aurora, DynamoDB, ElastiCache, DynamoDB Accelerator / RedShift
- read replica 지원하는 서비스들은? read replica 효과는?
- cross region support 지원하는 서비스는?
- global service의 implementation? autoscaling의 Implementation?
- cache strategies; Lazy Loading / Write through
- capacity planning
  - optimize network traffic with services - CloudFront, Global Accelerator, VPC endpoints
  - vpc 세팅할 때 subnets, routings, internet gateways, peering connections, transit gateway
- hybrid environment - site-to-site VPN, Direct Connect
- data transfer services: Data Sync, Storage Gateway

