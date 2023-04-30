## Storage on AWS

### Storage types on AWS

<img width="1039" alt="스크린샷 2023-04-28 오후 1 45 59" src="https://user-images.githubusercontent.com/26548454/235056445-7c5e9737-0747-41cd-b64b-f6ad49ff04f6.png">
<bR>

storage 저장 방식은 크게 두 가지. Block storage / Object storage.
- Block Storage: 파일을 고정된 크기의 chunk로 구분해서 저장.
- Object Storage: 파일 자체를 하나의 고유 unit으로 저장.

만약 1GB 파일의 글자 하나를 수정한다면?
- block storage의 경우, 수정할 대상이 되는 chunk 하나만 업데이트. 데이터 업데이트 빈도가 잦거나 high transaction rate인 데이터를 저장할 때 적합
- object storage의 경우, 파일 전체를 업데이트. 따라서 보통 WORM (write once, read many) 데이터에 적합


### AWS EC2 instance storage / AWS Elastic Block Store

EC2 생성 시 os boot volume / data volume 용도로 사용할 block storage가 필요함. 노트북으로 예를 들면, 노트북에 내장된 storage와 외장하드와 같은 외부 storage가 EC2에도 적용되는 셈

<br>
<img width="1063" alt="스크린샷 2023-04-28 오후 2 16 19" src="https://user-images.githubusercontent.com/26548454/235060233-b2e61d4c-9d68-4225-af9e-3ef5dc94e987.png">
<br>

- Instance Store : EC2 내장 storage. Directly Attached to EC2.
  - EC2에 내장된 개념이므로 접근 속도가 매우 빠름
  - Lifecycle이 EC2에 종속되므로, ec2 다운되면 데이터 유실. 그래서 ephemeral storage라고도 부름.
- AWS EBS : External Storage. 하나의 ec2에 여러 대 연결할 수도 있고, ec2와 연결되면 서로만 통신할 수 있는 secure Direct Communication Line이 형성됨. 일종의 persistent storage
  - 다른 Ec2에 연결하려면 Detach -> attach 수행하면 됨.
  - 여러 ec2에 동시에 attach 가능한 "AWS EBS Multi-Attach"를 사용할 수도 있다.
  - Data Encryption, on-the-fly change (실시간으로 IOPs, volume type/size 등을 변경할 수 있음) 지원.
  

백업: snapshot.
- incremental backups that are stored redundantly.
- 데이터에 문제가 생기면 snapshot 토대로 volume을 다시 생성하는 식으로 대응할 수 있음.

EBS Type은 아래 표를 참고.

<br>

| Attribute                  | EBS Provisioned IOPS SSD | EBS General Purpose SSD | Throughput Optimized HDD | Cold HDD                 |
|----------------------------|-------------------------|-------------------------|--------------------------|-------------------------|
| Description                | Highest performance SSD designed for latency-sensitive transactional workloads | General purpose SSD that balances price and performance for a wide variety of transactional workloads | Low-cost HDD designed for frequently accessed, throughput intensive workloads | Lowest cost HDD designed for less frequently accessed workloads |
| Use Cases                  | I/O-intensive NoSQL and relational databases | Boot volumes, low-latency interactive apps, development, and test | Big data, data warehouses, log processing | Colder data requiring fewer scans per day |
| Volume Size                | 4 GB-16 TB               | 1 GB-16 TB               | 500 GB-16 TB              | 500 GB-16 TB             |
| Max IOPS/Volume            | 64,000                   | 16,000                   | 500                       | 250                      |
| Max Throughput/Volume      | 1,000 MB/s               | 250 MB/s                 | 500 MB/s                  | 250 MB/s                 |

<br>


### Object Storage: S3

EBS가 있음에도 Object storage가 필요할 수 있는 이유
- 일반적으로 EBS는 하나의 EC2에 매핑됨. 모든 종류의 volume과 instance가 multi-attach 기능을 지원하는 게 아님. 애플리케이션이 scale될수록 여러 인스턴스가 EBS에 접근하기는 쉽지 않다.
- EBS의 size limitation.

S3는 individual object 크기가 5TB 이하인 데이터를 저장할 수 있는 storage.
- Object Storage의 특징을 전부 가지고 있다. 
  - flat structure
  - unique identifier...
- distributed storage -> 하나의 region 내 여러 facilities에 저장함
  - 99.99% availability / 11 nines of durability (99.999999999%) 지원


1. Bucket을 생성한다.
2. object를 Bucket 하위에 업로드할 수 있따.
3. bucket 내에 folder를 생성해서 object를 관리할 수 있다.

S3에 저장된 데이터는 기본적으로 Private. 따라서 default 설정으로는 해당 bucket이나 object를 생성한 사람만 데이터를 볼 수 있다. Public으로 s3 object를 공개하려면 몇 가지 절차를 거쳐야 함.

<br>
<img width="1069" alt="스크린샷 2023-04-28 오후 2 40 47" src="https://user-images.githubusercontent.com/26548454/235063824-3e44c671-649f-4aa6-a71d-8ae87639c353.png">
<br>

Bucket의 Permission - Block Public access 옵션을 비활성화한다.

<br>
<img width="1067" alt="스크린샷 2023-04-28 오후 2 41 27" src="https://user-images.githubusercontent.com/26548454/235063913-141ae459-8cef-4b36-aa13-312cbb9531d9.png">
<br>

Bucket의 Object OwnerShip 옵션 - ACL Enabled 설정
<br>

<img width="1063" alt="스크린샷 2023-04-28 오후 2 44 15" src="https://user-images.githubusercontent.com/26548454/235064314-ee2a8035-819e-4a54-80cb-e6a5bec88778.png">
<br>

공개하고 싶은 Object의 Options - Make public using ACL 활성화

---

Granular Access Control을 적용하고 싶다면 IAM / S3 Bucket Policy를 사용할 수 있다.
- IAM은 AWS user, groups, roles 기반 ACL
- S3 bucket policy는 **특정 bucket 단위로만** 적용하는 ACL. json format으로 사용한다.
  - What Actions you allowed / denied

--- 

Encryption으로 두 가지 방식 지원
- Server side Encryption -> 암호화한 채로 s3에 저장, 다운로드할 때 decrypt
- Client side Encryption -> 데이터를 사용자가 암호화해서 S3에 저장.

---

Versioning
- versioning 비활성화한 상태에서 동일한 파일명으로 업로드하면, s3는 파일을 덮어쓴다.
- versioning을 활성화하면
  - 저장할 때 S3에서 unique version ID를 object에 추가로 부여함.
  - accidental delete 방지 - 삭제요청 시 soft delete적용함 (mark붙임). 복구하고 싶으면 mark 해제요청하면 된다

S3가 지원하는 Versioning 상태는 세 가지
- Unversioning (default): 버전 없음
- Versioning Enabled: 모든 object에 버전 추가
- Versioning Suspended: 버전을 활성화했던 시기에 업로드된 object는 버전 유지, 이후에 업로드된 object는 버전 없음

---

Storage class 구분

- Amazon S3 Standard: This is considered general purpose storage for cloud applications, dynamic websites, content distribution, mobile and gaming applications, and big data analytics.

- Amazon S3 Intelligent-Tiering: This tier is useful if your data has unknown or changing access patterns. S3 Intelligent-Tiering stores objects in two tiers, a frequent access tier and an infrequent access tier. Amazon S3 monitors access patterns of your data, and automatically moves your data to the most cost-effective storage tier based on frequency of access.

- Amazon S3 Standard-Infrequent Access (S3 Standard-IA): S3 Standard-IA is for data that is accessed less frequently, but requires rapid access when needed. S3 Standard-IA offers the high durability, high throughput, and low latency of S3 Standard, with a low per-GB storage price and per-GB retrieval fee. This storage tier is ideal if you want to store long-term backups, disaster recovery files, and so on.

- Amazon S3 One Zone-Infrequent Access (S3 One Zone-IA): Unlike other S3 storage classes which store data in a minimum of three Availability Zones (AZs), S3 One Zone-IA stores data in a single AZ and costs 20% less than S3 Standard-IA. S3 One Zone-IA is ideal for customers who want a lower-cost option for infrequently accessed data but do not require the availability and resilience of S3 Standard or S3 Standard-IA. It’s a good choice for storing secondary backup copies of on-premises data or easily re-creatable data.

- Amazon S3 Glacier Instant Retrieval: Amazon S3 Glacier Instant Retrieval is an archive storage class that delivers the lowest-cost storage for long-lived data that is rarely accessed and requires retrieval in milliseconds.

- Amazon S3 Glacier Flexible Retrieval:S3 Glacier Flexible Retrieval delivers low-cost storage, up to 10% lower cost (than S3 Glacier Instant Retrieval), for archive data that is accessed 1—2 times per year and is retrieved asynchronously.

- Amazon S3 Glacier Deep Archive: S3 Glacier Deep Archive is Amazon S3’s lowest-cost storage class and supports long-term retention and digital preservation for data that may be accessed once or twice in a year. It is designed for customers—particularly those in highly regulated industries, such as the Financial Services, Healthcare, and Public Sectors—that retain data sets for 7 to 10 years or longer to meet regulatory compliance requirements.

- Amazon S3 Outposts:Amazon S3 on Outposts delivers object storage to your on-premises AWS Outposts environment.

---

Lifecycle policy 적용하기
- Transition action: storage class를 변경할 때
  - i.e. 최초생성 시점부터 30일간은 s3 standard-IA Storage class에 저장, 이후에는 s3 Glacier storage로 이동
  - = 어느 시점까지는 데이터 접근이 활발하지만, 그 이후에는 접근할 필요가 거의 없는 데이터의 경우.
- Expiration action: object 만료기한 설정 + permanent delete
  - i.e. Periodic logs 관리하기

### Choose the Right Storage store

Q. transcode large media file - needs to store both original file / transcoded media file. transcode logic은 Lambda. store duration should be at least a year.
- AWS S3
  - EBS라면 large file 처리를 위해 volume이 커야 함
  - EC2 안씀 (lambda)

Q. 이커머스 회사. mysql on EC2 요구사항. 데이터 추가 / 수정빈도 높으므로 반응속도 빨라야 함. (fast & durable)
- AWS EBS
  - EC2 Instance store도 가능은 한데 권장하지 않음. 비즈니스 핵심로직을 EC2 인스턴스 날아가면 소실되는 instance store에 두는 건 부적합.

Q. 연산을 주로 하는 web app. 연산에 쓰는 데이터는 persistency 필요 없음. 속도 빠르고 비용 낮을수록 좋다.
- EC2 instance store.
  - EBS 필요할 만큼 데이터 크기가 큰 것도 아니고, durability도 중요하지 않음.
  - 문제가 생겼을 경우, 처음부터 다시 연산 시작하면 됨
  - EBS보다 비용이 낮음

Q. wordpress 사이트를 여러 인스턴스에 올릴 건데, wordpress는 local storage에 파일을 저장하는 식으로 되어 있음. 사용자가 업로드하는 파일을 shared storage platform에 저장하고 싶다.
- AWS EFS(Elastic File System) - AWS에서 제공하는 file storage.
  - AWS s3 - flat hierarchy + multiple instance에 mount할 수 없음
  - wordpress가 local file system에 저장하는 로직을 가지고 있으므로, file system path를 AWS EFS로 변경하는 것만으로도 처리 가능


## Database on AWS


<img width="1056" alt="스크린샷 2023-04-29 오전 11 12 04" src="https://user-images.githubusercontent.com/26548454/235278959-74756138-39c6-4047-ae49-a093369c2012.png">
<br>

EC2 instance에 Database를 설치해서 운영하는 경우도 있다. 이 경우 EC2가 인프라 리소스 관련 이슈를 담당하지만, RDBMS 자체의 설정은 사용자의 몫이 됨.
- scaling / availability
- optimization
- backup
- ...

<img width="1065" alt="스크린샷 2023-04-29 오전 11 14 28" src="https://user-images.githubusercontent.com/26548454/235279041-f2cf28b7-126e-4e54-aedd-eeef745e0217.png">
<br>

Managed AWS Database를 쓰면, Database 사용을 제외한 모든 항목을 AWS managed service로 돌릴 수 있다.

<br>
<img width="1074" alt="스크린샷 2023-04-29 오전 11 35 21" src="https://user-images.githubusercontent.com/26548454/235279697-74f20067-9103-49af-a12f-dbb2a0be7200.png">
<Br>

Easy create 옵션으로 default 세팅 설정된 RDS 서버를 빠르게 만들 수 있음.
- AWS Aurora: Scalablity / Durability 특화된 AWS-specific DB. 
  - compatible with MySQL / PostgreSQL.
  - standard MySQL보다 5배, standard PostgreSQL보다 3배 빠름.
  - scale up to 128TB per DB instance.

<br>
<img width="1066" alt="스크린샷 2023-04-29 오전 11 43 37" src="https://user-images.githubusercontent.com/26548454/235279960-d6b0bb45-26fc-4363-920a-ffb2693216f9.png">
<Br>

HA 관련
- RDS를 생성하면, EC2와 마찬가지로 VPC 내부의 하위 Subnet에 생성된다.
- HA를 충족하려면 multiple subnet in different AZ.
  - RDS는 다른 AZ + Subnet에 secondary DB 구축이 쉽다. (Multi-AZ Deployment)
  - 두 개의 인스턴스 간 Data Replication + Sync 지원.
  - Primary / Secondary 지정 -> single DMS로 DB 접근하므로 failover 대응.
- Secondary는 일반적으로 active DB 취급받지 않음. primary DB가 주기적으로 동기화되는 용도로, 쿼리를 받지 않는다. primary에 문제가 생겼을 때 secondary가 primary role을 대신 부여받음.

<br>

![B6tbjrEXSG-Yl4yNpB63OA_4691a670ca6b4d85b712430a9297fff1_image](https://user-images.githubusercontent.com/26548454/235331718-76529474-c078-4b36-90e0-48c917a0fe07.png)
<br>

DB instance 종류
- Standard, which include general-purpose instances
- Memory Optimized, which are optimized for memory-intensive applications
- Burstable Performance, which provides a baseline performance level, with the ability to burst to full CPU usage.
<br>

![fLiYsSwuTjm0rj_g9xWmbg_91eef5ea15bf44c9891166bd697d4df1_image](https://user-images.githubusercontent.com/26548454/235331719-c4b79382-8e5e-482f-a96e-e663ca5c7d48.png)

각각의 종류에 맞게 Instance storage 선택이 가능하다.
- General purpose (SSD)
- Provisioned IOPS (SSD)
- Magnetic storage (not recommended)





Backup strategy
<br>

![D9_ilR_RTgWuODxywRWNyw_198e5735498c4c9ca0182010242846f1_image](https://user-images.githubusercontent.com/26548454/235280014-ad9cfab3-633f-4be4-9bb3-f70b802a8c53.png)
<br>

- Automate Backup: turned on by default.
  - 백업본 저장기간은 0 ~ 35일 중 선택가능. (0 = disable backup. 0 설정 시 existing backup도 전부 제거)
  - 백업 방법: Point-in-time recovery 선택.


![Fxm7W4g-RSGQIqYQYM6y3A_f7bd4f9671c342db90cfec9269e635f1_image](https://user-images.githubusercontent.com/26548454/235300845-a17e8ee6-df2c-408d-9271-1a4216f47e0a.png)

- Manual backup: 백업본을 35일 이상 저장해야 할 경우 사용
  - RDS에서 관리하는 일종의 EBS snapshot.


### purpose built database on AWS


RDS가 모든 비즈니스에서 유효한 DB 수단인 건 아님. 
- AWS는 여러 형태의 usecase에 대응할 수 있도록 다양한 Built DB 서비스를 제공함.
  - 예컨대 Employee management 서비스의 경우 RDB의 복잡한 relation이 필요하지 않은, 일종의 Lookup table 역할만 수행한다.
  - 주말에는 트래픽을 거의 받지 않는다.
  - 따라서 일반적인 RDS의 과금방식인 instance running time은 비용 효율적이지 못함.

<br>
<img width="1055" alt="스크린샷 2023-04-29 오후 9 01 29" src="https://user-images.githubusercontent.com/26548454/235301442-f875a1e3-0c24-429c-8f89-24a2e8d8e82e.png">
<br>

AWS DynamoDB: Managed NoSQL database
- suitable for key-value pairs / document data.
- massive scale / ms latency
- charge based on the usage of table & amount of data you're reading from the table.

AWS DocumentDB (MongoDB compatible)
- content management, catalogs, or user profiles

AWS Neptune: graph Database
- social network connectivity (graph figure) / recommend system engine / fraud detection

AWS QLDB: Ledger Database
- 100% immutable system (은행), audit for regulatory / compliance reason

### AWS DynamoDB

<img width="1060" alt="스크린샷 2023-04-29 오후 9 04 37" src="https://user-images.githubusercontent.com/26548454/235301605-da8c5ce3-41e7-4d76-b3df-ac99f7bff231.png">
<br>

Serverless DB. underlying instance / infrastructure 신경쓸 필요 없음.
- RDB처럼 relation 등록하지 않는다. 각각이 standalone table.
- 데이터는 items 단위, items는 attribute로 구성됨
- rigid schema, complex relationship / constraint를 다루지 않는다.

<br>
<img width="1060" alt="스크린샷 2023-04-29 오후 9 06 33" src="https://user-images.githubusercontent.com/26548454/235301698-2aeeb589-002d-4666-a3ed-3f33f7347b44.png">
<br>

내부적으로는 store data redundantly with Multiple AZs, mirrors the data across multiple drives. -> HA 확보. scalable & highly performant.
- RDB처럼 strict schema가 필요하지 않은 경우, access at a high rate일 경우 유용함. (relation과 Constraint + rigid schema일수록 scalable / performance issue under stress)

<br>
<img width="1056" alt="스크린샷 2023-04-29 오후 9 13 04" src="https://user-images.githubusercontent.com/26548454/235301932-13f8ff4d-ebe8-4342-bc5d-de2591c68260.png">
<Br>

DynamoDB의 경우
- Schema 제약에서 자유롭다. 각 items마다 attribute값이 달라도 됨
- Query 요청 자체가 collection of items from One table의 형태. 여러 테이블을 걸쳐 데이터를 조회하지 않는다.
  - 빠른 response time, 10 trillion request per day가 가능한 이유 중 하나


AWS Database Service 구분표

| Database Type | Use Cases | AWS Service |
| --- | --- | --- |
| Relational | Traditional applications, ERP, CRM, e-commerce | Amazon RDS, Amazon Aurora, Amazon Redshift |
| Key-value | High-traffic web apps, e-commerce systems, gaming applications | Amazon DynamoDB |
| In-memory | Caching, session management, gaming leaderboards, geospatial applications | Amazon ElastiCache for Memcached, Amazon ElastiCache for Redis |
| Document | Content management, catalogs, user profiles | Amazon DocumentDB (with MongoDB compatibility) |
| Wide column | High-scale industrial apps for equipment maintenance, fleet management, and route optimization | Amazon Keyspaces (for Apache Cassandra) |
| Graph | Fraud detection, social networking, recommendation engines | Amazon Neptune |
| Time series | IoT applications, DevOps, industrial telemetry | Amazon Timestream |
| Ledger | Systems of record, supply chain, registrations, banking transactions | Amazon QLDB |



Quiz에서 추가로 확인한 개념
- common use cases for file storage
  - User home directories: example of file storage that uses a hierarchical system to store and organize data
  - Large content repositories: use a hierarchical system to store and organize data
- RDS Supports "general-purpose instances", "memory optimized instance"

