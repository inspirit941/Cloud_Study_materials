# Storage
Storage, Sql, spanner, firestore, Bigtable.

<img width="909" alt="스크린샷 2020-01-23 오후 8 47 49" src="https://user-images.githubusercontent.com/26548454/72992091-80e70000-3e36-11ea-9097-d380666c5cf3.png">

BigQuery도 storage 범주에 있긴 하지만, 본래 목적은 data analysis and interactive querying.

Decision Chart.

<img width="908" alt="스크린샷 2020-01-23 오후 8 50 09" src="https://user-images.githubusercontent.com/26548454/72992115-8e03ef00-3e36-11ea-9120-0f054fdeab76.png">


* If data is not structured -> Storage.
* Structured + Focus on Data analysis -> Bigtable / BigQuery (depends on your latency / update needs)
Whether your data is relational.
* If not relational -> Cloud Firestore.
* Relational -> Cloud SQL , Spanner.

Scope

이 강의 자체는 infrastructure level에서 서술. 즉 어느 상황에서는 어떤 서비스를 써야 하는지, 각 서비스는 어떤 특징이 있는지, 어떻게 세팅하는지 정도를 다룬다.

만약 deeper dive into the design / organization -> Data engineering Track. (DB 엔진 자체에 관심있는 경우)

---
## Cloud Storage
GCP’s objects storage Service.

웹사이트 값 저장 / 유사시를 위한 백업 / large data objects를 사용자에게 direct download 제공할 때 등등 여러 용도로 사용이 가능함.
<img width="907" alt="스크린샷 2020-01-23 오후 8 56 15" src="https://user-images.githubusercontent.com/26548454/72992137-98be8400-3e36-11ea-8eae-0364f53c3cd3.png">


Exabyte 단위의 높은 scalability, ms 단위의 접근속도, High availability across all storage classes, Single API across storage classes.

File system처럼 이해할 수 있지만, 엄밀히 말하면 File system이 아니다. Collections of buckets. Directory에 대응되는 기능을 구현할 수 있지만, 이 directory는 다른 url로 넘어갈 수 있는 창구 역할을 할 뿐, 상하관계를 이루는 게 아니다.

Specific URL to access Objects.

4개의 Storage Class가 존재한다. 

<img width="905" alt="스크린샷 2020-01-23 오후 8 59 34" src="https://user-images.githubusercontent.com/26548454/72992149-a2e08280-3e36-11ea-95c7-aa90af69929d.png">


* Regional : Store data at lower cost, 대신 data is stored in a specific regional location. (Multi-regional redundancy 없음).
Frequently accessed data in a same region일 경우 사용권장.
Data-intensive computation에 유용하다.
 
* Multi-regional : Geo-redundant. 최소 2개의 location에 데이터를 저장하는 것. US, EU, Asia 단위로 설정 가능. Website data serving이나 interactive workloads, data supporting mobile / gaming application에 유용함.

* Nearline Storage : Low cost, high durable storage for infrequently accessed data. 한 달에 한 번 미만으로 데이터 접근 및 변경작업을 할 경우 유용하다. 대신 retrieval cost가 따로 존재함.
Backup storage나 longtail multimedia content serving에도 유용한 편

* Coldline Storage : online backup, disaster recovery 등에 유용함. 그래도 ms 단위의 접근속도는 보장한다. 1년에 한 번 정도 접근할 경우 유용하며, retrieval cost 존재.

Durability는 네 개 다 매우 높음. 단 이게 ‘어느 때나 접근 가능하다’는 의미는 아니고 “lose data가 존재하지 않는다”고 받아들이면 된다. 접근 가능성을 말하는 Availability가 다른 것.

Storage Overviews

- Buckets : Globally unique, cannot be nested.
- Objects : 버켓에 데이터 넣은 것. Storage class of bucket을 그대로 상속받으며, 다양한 파일 종류를 지원 (텍스트, 비디오, docs 등)
크기 하한선은 없고, 상한선은 크기제한 quota 내에서 가능.
- Access : gsutil이나 API 사용.

데이터를 storage에 저장하면서 딱히 클래스 설정을 하지 않으면, bucket storage class로 디폴트 설정된다. 이 디폴트 설정 자체는 어떻게 바꿔도 무방하지만, Regional / Multi-regional 간 변경은 불가능하다. 즉 regional bucket을 multi-regional bucket으로 변경하는 건 불가능하다.

<img width="908" alt="스크린샷 2020-01-23 오후 9 14 04" src="https://user-images.githubusercontent.com/26548454/72992253-d1f6f400-3e36-11ea-8588-a6b93f678ed5.png">


Regional / Multi-regional에서 Coldline, Nearline으로 변경하는 건 상호 가능하다.
이미 존재하는 Storage class of an object도 자유롭게 변경 가능하다. 다른 bucket에 옮겨담거나 url 재설정하는 등의 수고 없이도 가능.

Setting “Per object” storage class도 유용하다. 만약 특정 형식의 파일은 자주 접근할 필요가 없는 것들이라면, 해당 class의 파일만 Nearline / Coldline Storage를 사용하도록 지정할 수 있음.

To help manage the classes of objects in your bucket, Cloud storage offers “object life cycle management”.


Access Control Part

<img width="902" alt="스크린샷 2020-01-23 오후 9 48 09" src="https://user-images.githubusercontent.com/26548454/72992289-dcb18900-3e36-11ea-88b8-564a01ea5503.png">


* IAM으로 which individual user or service account can see the bucket / list the objects in the bucket / view the names of the objects in the bucket / create new buckets.
* 보통은, IAM으로도 충분하다. Role은 Project -> bucket -> object 순으로 inheritance.
* Access Control List (ACL) -> finer control 지원. Detail control을 위해 signed URL provides cryptographic key. (Time limited access to a bucket / object)
* 여기에 Assigned Policy document -> defines the control by determining (what kind of file can be uploaded by someone) with assigned URL.

<img width="901" alt="스크린샷 2020-01-23 오후 10 33 36" src="https://user-images.githubusercontent.com/26548454/72993488-d1f7f380-3e38-11ea-9785-85239eae0a8f.png">


- ACLs (Access Control lists)
= Mechanism  you can use, to define ‘who has access to your buckets and objects + what level of access they have’. 
ACL entries (create for a bucket or object)는 최대 100개. 
각 Entries는 2개의 information을 담고 있다.
	- scope = who can perform the specific action (ex) user / group of users)
	- permission = what actions can be performed (Owner / writer / reader)
allUsers = anyone who was in internet (regardless of Google Account)
allAuthenticatedUsers = who is authenticated with Google Account.

<img width="910" alt="스크린샷 2020-01-23 오후 10 34 16" src="https://user-images.githubusercontent.com/26548454/72993501-d9b79800-3e38-11ea-8d7c-42ad586ef37a.png">


- Signed URL
Account-based authentication for controlling보다 Limited time access token이 유용할 때가 있다.  이 때 사용 가능한 방법. URL에 특정 cloud storage resource의 reader right을 제공하고, 언제 권한이 만료될지 정하는 것.

request가 들어오면, 해당 access granting URL이 만료시한 안에 들어온 요청인지 체크한다. (Trusted security principle)

---
### Cloud Storage Features

* Customer-supplied encryption Key를 지원한다. (Attaching persistent disks to VM)
* Object LifeCycle Management -> automatically delete or archive objects 지원.
* Object Versioning -> Maintain multiple versions of buckets.
* Directory synchronization -> VM directory with a bucket.
* Object change notification, Data import, Strong consistency


Cloud Storage -> objects are immutable. 즉 uploaded object 자체는 절대 바뀌지 않는다. Object Versioning 기능으로 delete / overwrite 작업을 수행함.

#### Object Versioning

<img width="923" alt="스크린샷 2020-01-24 오후 1 24 14" src="https://user-images.githubusercontent.com/26548454/73051024-0913e680-3ec5-11ea-8043-54c0720ea164.png">

Bucket 단위로 enable이 가능하며, object의 delete나 overwrite가 발생할 때마다 직전의 archived version of an object을 만드는 것. 이름은 그대로고, generation number를 추가로 부여받는다. 기능의 On-off 는 언제든 이루어질 수 있다.

#### Object Lifecycle Management

<img width="921" alt="스크린샷 2020-01-24 오후 1 26 18" src="https://user-images.githubusercontent.com/26548454/73051047-17fa9900-3ec5-11ea-9e33-03ec0502fbcb.png">


setting a time to live for objects. 
Configuration은 일종의 set of rules that apply to all of the objects in the bucket. Storage object 중 rule에 걸리는 게 있으면, 그 rule에 해당하는 specified action을 취한다.

교안 예시를 보면, objects older than a year인 storage class를 coldline으로 변경하거, 특정 날짜 기준으로 이전 값을 삭제하는 등의 행동, 생성날짜 기준으로 몇 개월 지난 값은 삭제하는 등

단, rule이 적용되기까지는 시간이 좀 걸릴 수 있다. New configuration을 적용해도, old configuration이 최대 24시간까지는 지속될 수 있다는 소리.

#### Object change notification

<img width="923" alt="스크린샷 2020-01-24 오후 1 34 02" src="https://user-images.githubusercontent.com/26548454/73051061-2052d400-3ec5-11ea-9a2b-f718d4be9f1a.png">

특정 object가 updated / added to a bucket through a watch request일 때 알림을 주는 것. Watch request가 완료되면 notification channel이 만들어진다. 이 채널은 notification message를 해당 bucket을 주시하고 있을 application에 보내는 역할임. (현재는 WebHook이라는 Notification channel만 지원하고 있다)

한 번 채널이 만들어지면, 이후 발생하는 object add / update / remove는 전부 notification channel을 거쳐 알림이 간다.

*단, 이왕이면 Cloud pub/sub으로 notification 알림을 받는 걸 더 추천한다고 함. 더 빠르고, flexible, easy to set up and cost effective*

#### Data import service

GCP console로 individual File을 bucket에 업로드할 때, 테라 / 페타바이트 단위의 데이터를 처리하기 위한 것.

* transfer appliance : Hardware appliance to securely migrate large volumes of data (수백 테라 ~ 1페타바이트) with out disrupting business operation.
* storage transfer service : high performance imports of online data. (AWS S3나 다른 Storage buckets, HTTP / HTTPS location 등)
* offline media import : 3rd party service where physical media (storage array, hard-disk drive, tapes, USB) is sent to a provider who uploads the data.


일단 storage에 데이터를 올리면, download 기능 + metadata operation from any location where Google offers services. 엥간하면 read / write 과정에서 절대 404 에러 안 띄울 자신 있다고 (Global Consistency)

Choosing Storage Class


<img width="925" alt="스크린샷 2020-01-24 오후 1 44 49" src="https://user-images.githubusercontent.com/26548454/73051077-2f398680-3ec5-11ea-9c67-47b0dc6a21fd.png">

---
### Lab

빈 bucket 만들고, 편의상 구글에서 제공하는 특정 파일 (setup.html) 복사한 다음, 해당 파일에 제공되는 acl 파일을 확인한다. (acl.txt) 형태로 되어 있음

cmd에서 Set private 명령어로 acl파일을 private 설정으로 변경하는 등의 일도 가능.


Customer supplied encryption key 작업도 진행.
홈 디렉토리에서 .boto파일의 encryption_key , decryption_key 항목을 수정한다.

LifeCycle은 lifecycle get gs://파일이름 형태로 확인할 수 있다. life.json 형태.

간단한 life.json 예시
```json
{
  "rule":
  [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 31}
    }
  ]
}
```

31일 지나면 expire된다는 설정.

이 파일을 lifecycle set life.json gs://파일
형태로 setting할 수 있다.

Versioning의 경우 versioning get 형태로 확인할 수 있다. Suspended는 설정이 없다는 뜻.
Versioning set 명렁어로 version 설정을 enable로 변경한 뒤 해당 파일을 수정하고, 
cp -v 변경한파일이름 gs://storage이름
형태로 과거 버전을 저장할 수 있다.

파일이름 뒤에 `#숫자` 형태로 저장된 과거 값을 확인할 수 있는데, 가장 숫자가 작은 게 original. 이 숫자값으로 과거 버전을 되돌리거나 확인하는 게 가능하다
`gsutil cp $VERSION_NAME recovered.txt`
형태.

Synchronize directory & bucket

```
mkdir firstlevel
mkdir ./firstlevel/secondlevel
cp setup.html firstlevel
cp setup.html firstlevel/secondlevel
```
로 디렉토리를 만든 후
```
gsutil rsync -r ./firstlevel gs://$BUCKET_NAME_1/firstlevel
```

로 firstlevel 하단의 모든 디렉토리를 동기화한다.

Cross project sharing
-> project 2에서 bucket과 service account를 생성한다. IAM에서 storage object viewer 권한을 설정하고, create key에서 json을 선택해 키를 다운받는다. (이 키를 project 1에서 VM이 사용할 예정)

project1에서 VM 생성 후 
`gcloud auth activate-service-account --key-file credentials.json`

형태로, 아까 다운받은 json 파일을 활용해 Google SDK 적용한 Service Account authentication을 수행하자.

---
## Cloud SQL

VM에 SQL 설치해서 쓸 수 있는데도 Cloud SQL을 써야 하는 이유가 있다면?

-> Build own DB system vs use Managed Service? 의 차이라고 보면 된다.

<img width="746" alt="스크린샷 2020-01-24 오후 2 43 27" src="https://user-images.githubusercontent.com/26548454/73051094-3cef0c00-3ec5-11ea-80b4-0f34374feccf.png">


Cloud SQL instance
* Performance
	- 30TB까지 지원
	- 40,000 IOPS
	- 416 GB RAM
	- scale up to 64 processors, out with read replicas
* Choice
MySQL은 5.6 / 5.7
PostgreSQL은 9.6 / 11.1


<img width="754" alt="스크린샷 2020-01-24 오후 2 47 36" src="https://user-images.githubusercontent.com/26548454/73051105-4c6e5500-3ec5-11ea-8c68-260f464b5e36.png">

* Replica Service : replicate data btwn multiple Zones. Outage 발생 시 대처하기 용이하다
* Automated / on-demand Backups. (With point-in-time recovery)
* import export (Mysql Dump or csv)
* scale up을 위해서는 machine restart / scale out using read replicas.

-> 이 특징 때문에 horizontal scability가 필요하면 Spanner 쓰라고 하는 것.


<img width="748" alt="스크린샷 2020-01-24 오후 2 50 29" src="https://user-images.githubusercontent.com/26548454/73051309-cacaf700-3ec5-11ea-872b-b49277374c5b.png">


Connection type choosing = how secure / performance / automated it will be.

- hosted with the same GCP projects & co-located in same region -> private IP connection 추천. 빠르고 안전하다
- hosted in another (region / project) | outside of GCP -> 옵션 3개

1. Cloud proxy -> authentication, encryption, key rotation 제공
2. Manual control over SSL connection을 원할 경우 generate / periodically rotate the certificate yourself.
3. Unencrypted connection by authorizing specific IP address to connect SQL server.

<img width="750" alt="스크린샷 2020-01-24 오후 3 03 18" src="https://user-images.githubusercontent.com/26548454/73051330-d9191300-3ec5-11ea-8d80-2ab34af760e4.png">

---
### Lab

Configure proxy on VM

When your application does not reside in the same VPC connected network and region as your Cloud SQL instance, use a proxy to secure its external connection.

Proxy로 다른 region의 VM이 데이터베이스에 접근하도록 만드는 것, private IP로 같은 region의 VM이 데이터베이스에 접근하는 것 실습

---
## Cloud Spanner

Horizontal Scalability. 즉 relational Data structure + non-relational horizontal scale이 필요할 경우 유용하다. 전통적인 SQL 기술적인 면을 지원하는 형태.

<img width="924" alt="스크린샷 2020-01-24 오후 3 35 04" src="https://user-images.githubusercontent.com/26548454/73051278-bab31780-3ec5-11ea-8049-c3237020d834.png">

Cloud Spanner는 n개의 cloud Zone에 replicates data. (One or several regions). 어느 region을 선택할지는 사용자가 정한다. (Availability 확보를 위한 것)

Synchronized across Zones. Atomic clocks로 data atomicity 보장. 

<img width="924" alt="스크린샷 2020-01-24 오후 3 38 45" src="https://user-images.githubusercontent.com/26548454/73051614-652b3a80-3ec6-11ea-9262-4a724420c78a.png">


DB outgrown 상태 -> high performance 위한 샤딩이 필요할 경우, transaction consistency, global data, consolidate DB 등의 작업이 필요하면 spanner 사용 권장.

---
### Cloud Firestore

Scalable NoSQL DB.

<img width="929" alt="스크린샷 2020-01-24 오후 3 41 38" src="https://user-images.githubusercontent.com/26548454/73051632-72e0c000-3ec6-11ea-97f1-b61964c5f30b.png">


Serverless, Cloud Native, NoSQL, document DB를 말한다.

Serverless apps 구현에 도움이 될 법한 서비스. 
ACID 특징 제공.
Automated Multi-region replication.

NoSQL Query로 복잡한 연산을 no degradation in performance 수행 가능. = flexibility.

Cloud Datastore의 진화 버전이라고 보면 된다. Backward compatible with Cloud Datastore 가능. Datastore mode / Native Mode 둘 다 지원하며, Datastore에서 지원하지 못했던 몇 가지 기능 - 예컨대 transaction limitation - 이 없어졌다.

사용 권장은 보통 
- New server project의 경우 Datastore Mode,
- New mobile / Web app의 경우 Native Mode


<img width="925" alt="스크린샷 2020-01-24 오후 3 47 32" src="https://user-images.githubusercontent.com/26548454/73051176-758ee580-3ec5-11ea-8a79-8e60cab4366a.png">

Schema가 유동적이고 adaptable DB가 필요한 경우, low maintenance overhead scaling up to 테라바이트 인 경우 유용하다.

---
### Cloud Bigtable

Do not require transactional consistency일 경우 유용하다. 구글에서 실제 사용하는 서비스의 DB역할을 담당. IoT, analytics, finance analysis에 유용하다. ML App의 storage에도 유용함. 다른 빅데이터 툴 - 하둡 등 - 과 호환됨.

HBase API 지원함.

Storage Model : Massive scalable Table에 데이터를 저장하는 식. (Sorted key - value map 형태) 

row는 single Entity. (Index)이며, 비슷한 특징을 가진 column이 grouped되어 column family라고 통칭한다. Column은 곧 Column family + Column qualifier (unique name in family). 형태로 이루어진 것

Row - column의 접점이 multiple cells인 경우가 있다 (versions at different timestamps) -> how stored data being altered over time.

Sparse Data로,  셀 안에 데이터가 없으면 not take up any space.

<img width="922" alt="스크린샷 2020-01-24 오후 3 52 58" src="https://user-images.githubusercontent.com/26548454/73051178-76277c00-3ec5-11ea-9dff-e5736c2d70f1.png">

사진은 각 대통령이 서로를 Following하는지 여부를 저자한 일종의 가상예시. username을 Row key로 사용한 상태이며 username이 알파벳 순서로 evenly spread 상태라면, 데이터 접근시간은 uniform에 가까울 것.



<img width="926" alt="스크린샷 2020-01-24 오후 3 59 45" src="https://user-images.githubusercontent.com/26548454/73051179-76277c00-3ec5-11ea-904b-4fd5d8f281f9.png">

이런 식으로 운영된다. Storage와 processing이 분리되어 있고,  table 자체도 shared into blocks of contiguous rows called “tablets”. (Balancing the workload of queries) HBase의 Region과 유사한 개념이다.

Tablets는 Colosus라는 SSTable format의 구글 file system에 저장된 상태. SSTable이 일종의 immutable key - value map이라고 보면 된다.

특정 노드에 쿼리가 과도하게 몰릴 경우, 알아서 workload balancing 수행한다고 함. 따라서 scales linearly가 가능함.

bigtable에는 최소 3개의 노드가 필요하며, 각 노드당 30,000 operations per sec. 노드가 실행될 때에만 비용 나간다.

<img width="923" alt="스크린샷 2020-01-24 오후 4 03 56" src="https://user-images.githubusercontent.com/26548454/73051181-76277c00-3ec5-11ea-8718-b94d46e9fb30.png">

---
### Cloud Memorystore

In-memory data store service.

Allows you to spend more time writing code, (application 개발에 집중할 수 있도록 돕는다고 함)
Automates complex tasks (enable high availability, failover, patching, monitoring 등)
- high availiabilty -> 2 zone에 데이터 복제.

300GB까지 지원, 12GB throughput per sec.

Redis 프로토콜과 완벽 호환되므로, 오픈소스인 Redis 그대로 사용 가능함.

---
### Quiz

*What data storage service might you select if you just needed to migrate a standard relational database running on a single machine in a datacenter to the cloud?* -> Cloud SQL

*Which GCP data storage service offers ACID transactions and can scale globally?* -> Cloud Spanner provides ACID (Atomicity, Consistency, Isolation, Durability) properties that enable transactional reads and writes on the database. It can also scale globally.

