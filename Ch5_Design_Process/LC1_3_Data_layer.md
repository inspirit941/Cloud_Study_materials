# Data Layer
## Overview

<img width="925" alt="스크린샷 2020-02-08 오후 9 27 38" src="https://user-images.githubusercontent.com/26548454/74087790-00c9c700-4ad3-11ea-9b78-ab84ee2a8f92.png">


Storage / retrieval of data를 다루는 영역. Storage / retrieval 영역인 database / file system뿐만 아니라 access method; SQL and API 등등을 포함한다.
하지만 transport of data는 다루지 않음. (Into, around, out of the system) transportation 부분은 presentation layer module에서 다룬다.

## Data Layer Design : Classifying and Characterizing Data

<img width="924" alt="스크린샷 2020-02-08 오후 9 36 06" src="https://user-images.githubusercontent.com/26548454/74087767-c3fdd000-4ad2-11ea-8a90-88c648948c89.png">


사용자 입장에서 중요한 건 Data integrity. Underlying tech에는 관심 없고, data loss / data corruption / extended unavailability 구분하지도 않는다. 데이터가 없으면, 사라진 것과 마찬가지로 본다.

하지만 엔지니어 입장에서는 Persistence와 Access는 완전히 다르다. Access가 불가능하다고 해서 데이터가 없는 게 아니듯.

엔지니어 입장에서의 Goal은 세 가지다. 
* Persistence
* proactive detection
* rapid recovery

어떤 연유에서건 데이터가 사라졌으면, 복구해야 한다. Version control이나 backup, 아니면 failover recovery 등으로.


<img width="928" alt="스크린샷 2020-02-08 오후 10 30 11" src="https://user-images.githubusercontent.com/26548454/74087771-c6602a00-4ad2-11ea-92e4-ef17a3d3f666.png">

데이터의 특성상, 세 가지 특성을 전부 가질 수는 없다. 셋 중 두 가지만 충족 가능. 이걸 CAP Theorem이라 한다.

* Consistency
* Availabilty
* Partition tolerance.

만약 availabilty와 partition tolerance가 필요하다면, BASE를 선택하면 된다. 

This is basically “available” storage. Soft state, Eventual Consistency 를 보장한다. 뭔 소리냐면, update나 specific change may not necessarily be available. 대신 write / expand data quickly 가 가능하며, 결과적으로는 consistency 를 보장하는 형태.

반대로, Pure Consistency가 필요하다면 ACID transaction 형태를 사용해야 한다. 어떤 데이터를 storage system에 썼다면, 그건 반드시 그 안에 존재하는 것을 보장하는 형태. 쓰기 전까지는 not get an acknowledgement이므로, completely fault-tolerant, replicated 등등의 특성을 가지고 있음. Failover Capability가 보장된 형태.


<img width="920" alt="스크린샷 2020-02-08 오후 10 37 28" src="https://user-images.githubusercontent.com/26548454/74087772-c7915700-4ad2-11ea-9d50-100aaec92dc4.png">

GCS를 보면, Global strong consistency에서 강조하는 항목은 결국 하나다. “If you list the actual items in the bucket, those are guaranteed”.

Eventual Consistent는 versioning과 관련돼 있다. 새로 write 작업을 한 뒤 save하는 순간, 새로운 version을 하나 만드는 식. Access decline 작업도 가능하다. 대신 all security table update을 위해서는 약간의 시간이 필요함

Caching an object는 consistency를 보장하지 않는다. Older version을 cache하고 있을 가능성이 높음. Cache의 효율성과 trade-off인 셈이다.


<img width="922" alt="스크린샷 2020-02-08 오후 10 52 50" src="https://user-images.githubusercontent.com/26548454/74087801-10491000-4ad3-11ea-99b9-c27405004758.png">

결국, 어떤 특징을 원하느냐에 따라 달라질 거다.

* Uptime : banking을 생각해 보면 됨. 특정 시간대에는 전산망 점검 등의 이유로 사용이 불가능하지만, 그렇다고 데이터가 사라지거나 하는 건 아니듯. 
* latency : 얼마나 빨리 데이터를 받아볼 수 있는지. 이미지나 비디오처럼 용량이 큰 데이터일 경우
* Velocity의 경우 -> how fast will it potentially grow. scale하기 용이한 구조인지, 아니면 threshold 돌파하면 re-architecting을 해줘야 하는지
* privacy : 특정 시간이 지나면 데이터를 의무적으로 삭제하거나, 다시 복구할 수 없다는 걸 보증할 수 있어야 하는지

---

## Data ingest and migration

* Migration : data already exists somewhere, that will be transposed into the cloud. 일단 migration되고 나면, updated & new data will be added to the cloud version. 이전 버전은 필요없게 된다
* Ingestion : data will continue to the originate outside the cloud, and periodically loaded Into the cloud.

클라우드에서 data migration, ingestion 하는 방법을 다룸


<img width="853" alt="스크린샷 2020-02-08 오후 11 02 45" src="https://user-images.githubusercontent.com/26548454/74087804-150dc400-4ad3-11ea-8ed5-4a675dcf63fc.png">

방법은 크게 세 가지.

Gsutil의 경 built-in Amazon S3 SDK 지원. 아마존 bucket에서 데이터 옮겨올 수 있음. Cmd로 IAM, signed url, ACL 등 다양한 기능을 지원한다.

json API 사용 가능.



<img width="852" alt="스크린샷 2020-02-08 오후 11 06 13" src="https://user-images.githubusercontent.com/26548454/74087806-15a65a80-4ad3-11ea-9974-23541334256b.png">

Very Large Data의 transfer에 제공되는 기능들. Web based interface이고, 백엔드에서 다양한 API를 사용해 transferring data를 지원한다. 보통 테라바이트 단위 이상일 경우 사용을 권장하며, 왼쪽의 Synchronize 기능도 제공한다.
(Override any change, delete the source data, optimize the number of streams도 지원함. Optimized number of streams 지원 = ensure we can get this moved over as fast as possible)

<img width="854" alt="스크린샷 2020-02-08 오후 11 10 07" src="https://user-images.githubusercontent.com/26548454/74087807-16d78780-4ad3-11ea-888c-7b8972573520.png">

Size matters. 수백 테라바이트 단위의 데이터 이상이 되면 network 전송은 그다지 선호하지 않게 된다. Ingress가 공짜라고 해도 시간 면에서 비효율적임. 

그래서 transfer appliance를 제공한다. 
Amazon’s Snowball capacity와 유사함.


<img width="854" alt="스크린샷 2020-02-08 오후 11 13 01" src="https://user-images.githubusercontent.com/26548454/74087810-1808b480-4ad3-11ea-9a38-77072ccf337c.png">

대충 얼마나 걸리는지 보여주는 샷. 데이터 크기가 커지면, bandwith 할당량도 늘어나기 마련이다. 100테라가 넘어가면 bandwidths 10GB로도 30시간 정도 걸리게 됨. 데이터 전송에만 혼자 10GB bandwidths 가져가는 것도 현실적으로 쉽지 않다는 점에서, 이 정도 데이터 규모가 되면 Google Transfer appliance 사용하는 게 현실적이다.


<img width="852" alt="스크린샷 2020-02-08 오후 11 14 59" src="https://user-images.githubusercontent.com/26548454/74087811-1939e180-4ad3-11ea-9133-0debde919baa.png">

Data ingestion. 
1. Network를 통한 방법. Globally available, bandwidth 최대 100기가까지. Peering location 활용해서 low latency 확보
2. Post directly to cloud storage by HTTP, RESTful APIs
3. Frontend Application (App Engine) 활용하는 것도 가능하다. Ingest data into your application just with simple API. 

각각의 장단점도 곧 다룰 예정

---

## Identification of Storage Needs & Mapping to Storage System

그래서 구글이 제공하는 수많은 storage 서비스 중에 뭘 쓰는 게 효율적일지?

<img width="853" alt="스크린샷 2020-02-08 오후 11 19 13" src="https://user-images.githubusercontent.com/26548454/74087829-41c1db80-4ad3-11ea-8919-7b32d877a1ce.png">


크게 세 가지로 나눠 볼 수 있다. DISK는 VM에 할당하는 식.

<img width="853" alt="스크린샷 2020-02-08 오후 11 21 16" src="https://user-images.githubusercontent.com/26548454/74087834-46868f80-4ad3-11ea-8c33-a34c154744ec.png">

* data not structured -> Storage. Persistent disk도 가능하지만 scale에 약점. 모바일 SDK가 필요하다면 Firebase 기반 solution.
* 데이터 분석 쪽이라면 (log ingest, big data 등) -> Bigtable if you need low latency & frequent update. BigQuery for large data warehouses; storing petabytes (stream or batch) + query가 필요할 경우
* Relational data? Need to draw insight from data? -> 물론 bigquery로도 가능하지만, 
	- frequent update / very tight schema
	- lot of data coming in, update often일 경우
Cloud SQL (MySQL & Postgre) / (horizontal scalable Structured) Spanner 사용 가능. Spanner는 relational DB에서 일종의 panacea.
* 다 안맞을 경우, 모바일 SDK가 필요한지? 또는 plugging into sth like App Engine | Kubernetes?
	- Firebase for mobile, Cloud Datastore for high transaction. 포켓몬고는 datastore 쓰고 있다고 함. Horizontal scalability 때문.


<img width="853" alt="스크린샷 2020-02-08 오후 11 30 11" src="https://user-images.githubusercontent.com/26548454/74087835-49818000-4ad3-11ea-84fc-dc19d53872da.png">

Static Cloud Storage 선택지. 지겹도록 봤지만 복습차원에서 또 보자

Multi-regional = 2.6 cent per GB. Regional이 2 cent per GB인 걸 감안하면, 두 개 region 쓰면서 가격 저렴한 선택지가 multi-regional이다.


<img width="854" alt="스크린샷 2020-02-08 오후 11 50 23" src="https://user-images.githubusercontent.com/26548454/74087836-4b4b4380-4ad3-11ea-96f7-d4b4d54856ba.png">

BigQuery -> 데이터 분석 at scale. 테라바이트 단위까지도 okay. 2 cent per GB. 1 penny per GB after 90 days. 따라서 굳이 여기 올려놓은 걸 다른 데로 offload 할 필요는 없다.

Data you access에만 비용이 나감. 따라서 데이터 분석을 위해 query로 데이터에 접근할 때, 5$ per TB 정도. SQL이나 기타 데이터분석도 지원함. 따라서 단지 데이터분석에만 사용할 용도라면, 굳이 Hadoop cluster를 생성하는 식의 작업을 할 필요가 없다. 이거 쓰면 됨

<img width="856" alt="스크린샷 2020-02-08 오후 11 54 15" src="https://user-images.githubusercontent.com/26548454/74087837-4d150700-4ad3-11ea-89d4-d62d2d353edf.png">

* outgrown RDB -> spanner. 선택의 여지 없음
* 변동 가능한 Schema가 있고, 바뀔 수 있으며, horizontal scale이 어느 정도 필요하다면 -> NoSQL.
그거 아니면, RDB를 언제 써야 하는지는 대부분 잘 알고 있으니 패스


<img width="857" alt="스크린샷 2020-02-08 오후 11 58 28" src="https://user-images.githubusercontent.com/26548454/74087839-4edeca80-4ad3-11ea-88d5-9d446e75b447.png">

Horizontal Scale with RDB.

<img width="855" alt="스크린샷 2020-02-08 오후 11 59 53" src="https://user-images.githubusercontent.com/26548454/74087841-51412480-4ad3-11ea-95b4-84f88f5898cd.png">

* schema going to be changing인 경우, horizontal scale 필요한 경우
SQL-like  transaction 제공 (Not SQL). Datastore로 migration을 진행하면, 완전히 다른 API를 사용하는 등. 많이 다르다.

만약 strong transcations이 필요하면 bigTable을 쓰는 게 맞다. Datastore는 Eventual conssistency를 지원하기 때문.

<img width="855" alt="스크린샷 2020-02-09 오전 12 18 55" src="https://user-images.githubusercontent.com/26548454/74087842-52725180-4ad3-11ea-8162-acc5b05f0855.png">

* Datastore : more complex query capability
* BigTable : key-value.

---
