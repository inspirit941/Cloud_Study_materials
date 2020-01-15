# Module 설명-storage
## GCP Storage Options

Different application / workloads -> different storage DB 필요.
VM의 persistent disk로도 데이터 저장이 가능하지만, GCP의 storage Sys를 활용할 수도 있다. (Structured, unstructured, transactional, relational) 

소개할 서비스는 Cloud Storage / SQL / Spanner / Data Store / Bigtable.

## Cloud Storage
Object Storage는 file storage, block storage와 다르다.

File storage : 폴더의 계층구조 형태로 data를 관리하는 것
Block storage : OS에서 데이터를 chunks of disk로 관리하는 것.

Object storage : keep this arbitrary bunch of bytes -> storage lets you address it with a unique key. 이 unique key가 url로 존재하는 경우, Web tech와 호환성이 아주 좋다.

Cloud Storage가 이런 식으로 동작한다. Fully Managed Scalable Service. provision도 필요없이, 그냥 저장하면 알아서 durability, availability를 확보해준다.

여기 저장된 모든 Objects는 각각의 url을 가지고 있으므로, 단순한 File system이라고 볼 수 없다. 단지 like-a-file처럼 느껴질 뿐. 파일처럼 이해해도 문제는 없다. Linux file system처럼 사용하면 안된다는 의미.
* Comprised of Buckets. Create / configure / use to hold your storage objects.
* cannot edit inplace. Create new version 형태로 진행된다.

디스크에 쓰일 때 (서버에 저장될 때) Server Side에서 항상 Encrypted된다. 마찬가지로, data in-transit (전송 중) 일 때에는 HTTPS를 사용함 (encrypt)

Cloud Storage에서 other GCP Storage service로 데이터 전송도 가능.
Storage를 생성할 때, choose geographic location where buckets and its contents are stored / default storage class.

사용자와의 latency를 최소화할 수 있는 location 권장.

Object / buckets Access Control -> 보통 IAM으로 충분함. Roles are inherited from project -> buckets -> objects. Finer control을 위해서는 Access control List (ACL) 사용할 수 있다.

ACL에 필요한 정보는 두 가지. 
1. A scope which defines who can perform the specified actions.
2. Permission. What actions can be performed.

Object Versioning -> immutable object이기 때문에, 수정 이력은 전부 남길 수 있다. 이 옵션을 선택하지 않을 경우, new always overrides old.
혹시 junk accumulation?? -> lifecycle management policy 있음.

###  Cloud Storage interactions

4 different types of storage classes
Multi-regional, Regional, Nearline, Coldline. 일반적으로 multi-regional & regional은 high performance 용도, nearline & coldline은 backup and archival storage 용도로 쓴다.

네 가지 전부 Cloud storage API 형태로 접근 및 사용이 가능하며, ms 단위의 access time.

1. Regional: store data in specific GCP Region; US central 1 / Europe West / Asia East 1 같은 식. Multi-regional보다 가격이 싼 대신 less redundancy. (Redundancy : 불필요한 중복, 정리해고)

일반적으로 Compute Engine이 운영되는 지역에서 사용. (Store data close to their Compute Engine or kubernetes Engine) data-intensive computation에서 better performance를 내기 때문.

2. Multi-regional : Geo-redundant. 즉, more broad geographical location. (US, European Union, Asia 등) 또한 최소한 두 개의 geographical location (160km 이상 떨어진)에 데이터를 저장한다.

일반적으로 Frequently accessed data에 적용한다. Website content, interactive workloads, mobile or gaming part of data가 보통 해당.

3. Nearline : Low cost, highly durable service for storing infrequently accessed data. 매달 한 번 정도 데이터에 접근하고 수정해야 할 경우에 효율적이다. 예컨대 한 달에 한 번 정도 데이터를 클라우드에 분석용으로 업로드하는 등에 사용함.

4. Coldline : low cost, highly durable for data storage, online backup, disaster recovery. 일 년에 한 번 정도 접근할 경우 용이함. avaliability가 나머지에 비해 높지 않고, 최소 90일의 storage duration이 필요하며, data access cost와 operation cost가 비싼 편이기 때문.

Incurring Cost 기준은 GB/month. Multi가 제일 비싸고, coldline이 제일 싸다. egress(나감, 출구) & data transfer charge도 별도.

Nearline / Coldline의 경우 data access에도 비용이 든다. Coldline이 좀 더 비쌈.

넷 중 뭘 쓰던 상관없이, 어쨌든 데이터를 Cloud Storage로 보내는 방식은 다 똑같다. 대부분은 gsutil이라는, cloud storage command from cloud SDK를 사용함. 크롬을 쓰면 드래그 앤 드롭으로 GCP console 써도 됨.
-> 만약 페타바이트 급으로 큰 데이터라면? Online storage transfer service와 offline transfer appliance 사용. 
it manages Batch transfers to Cloud storage from (another cloud provider, different cloud storage region, from HTTPS endpoints.)

Transfer appliance = rackable / high capacity storage server lease from Google cloud. 여기에 데이터 업로드하는 식으로. Single appliance로 안전하게 데이터 옮길 수 있다는 게 특징.

다른 GCP Service와의 호환성이 매우 좋다.

요약: Cloud Storage = ingestion point for data being moved into the cloud & Long Term storage Location.

---
## Google Cloud Bigtable
Google’s NoSQL, Big data DB Service를 말함.
Fully managed NoSQL, wide-column database service for terabyte application. 굳이 Configure / tune 할 필요 없다.

(Cloud Bigtable을 Persistent hashtable로 보는 개발자들도 있다. 즉, Each item in DB can be sparsely populated, and looked up with a single Key). 간단히 말해 그냥 큰 해시테이블처럼 본다는 의미니까 해시테이블 특징을 나열한 거임

* ideal for data that has a single lookup key.

Storing Large amount of data with very Low Latency. Operational / Analytical application 둘 다 유용하다. IoT 데이터라던가, 사용자 행동분석 또는 금융데이터 분석 등등.

오픈소스인 Hbase API로도 제공됨. (== native database for Apache Hadoop project)
-> 따라서 Hbase 기반 application과 호환됨.

Hbase manage가 가능한 상태에서도 Bigtable을 써야 하는 이유가 있다면
1. Scalability. Hbase Manage에서 scaling past a certain rate of queries per second = tough. Bigtable에서는 Machine Count만 늘려 주면 된다. 또한 Admin Task(upgrade, restart 등) transparently.
2. Data Encryption in-flight & at rest. IAM permission으로 접근권한 제어도 가능하다.
3. 실제로 구글이 사용하는 핵심 서비스 - 검색, 애널리틱스, 지도, 지메일 등 - 의 데이터베이스 기능을 한다.

마찬가지로 다른 GCP Service와 3rd party client와 interact 가능.
Application API 형태로 read from, written to Cloud BigTable에 사용 가능하며, Stream processing framework에도 적용 가능. 스트리밍이 아니어도, batch process 형태로 사용 가능.

---
## Cloud SQL & Cloud Spanner


RDB의 특징인 keeping Consistent & Correct Data 특성을 갖고 있다.
또 하나의 특징 - transaction. (All or nth)

Cloud SQL : RDB 형태. MySQL / PostgreSQLBeta DB as a Service (fully managed service). 테라바이트 단위의 storage 지원. (후술할 Cloud Spanner가 저장용량이 더 크다. 처음에 DB instance를 설정할 때 한계 용량을 설정할 수 있는 형태라고.)

물론 Compute Engine에서 DB 시스템을 설치하고 관리하는 사람들도 많다. 그럼에도 Cloud SQL이 갖는 이점이 있다면
1. Automatic replication 서비스 제공. Replica service like read, failover, external replica. 즉, outage (정전)  발생시 Cloud SQL은 multiple zones에 자동으로 데이터를 복사한 뒤 failover를 작동시킬 수 있다.
2. Backup data either on-demand / scheduled backups. 
3. Scale both vertically (by changing the machine Type) and horizontally (by read replicas.)
(Scale horizontally = scale by adding more machines, vertically = by adding more power)
4. Security; it includes network firewalls, Encryption when on Google’s internal networks, DB tables, temp files, backups.

마찬가지로 다른 GCP 서비스 / external service와 호환성 제공.

Cloud Spanner : Cloud SQL에서 horizontal scaleability가 부족하다고 느낄 경우 사용할 수 있음. ANSI SQL 2011 with extension을 사용한다.
* Transactional consistency at a global scale
* Schemas, SQL, Auto synchronous replication for high availability.
페타바이트 단위.

Outgrown RDB를 가지고 있거나, sharding DB for throughput high performance가 필요한 경우.

---
## Cloud DataStore

NoSQL : BigTable 소개를 이미 했지만, 또다른 high scalable NoSQL DB = Cloud DataStore.

* Store (semi) structured data from App Engine apps. (Designed for application backends)
* App Engine과 Compute Engine 사이의 integration point로도 사용 가능하다. (?)

Automatic handling sharding and replication. BigTable과 달리 offer translations that affect multiple DB rows, lets you do SQL-like Queries.

Free daily quota that provides storage, read, write, delete and small operations at no charge.

---
## Comparing Storage Options.

- DataStore : need to store unstructured objects / require support for transactions and SQL-like queries. 테라바이트 capacity. (단, Complex Queries는 지원하지 않는다)
Good for Semi-Structured Application Data used in app engines’ application.

- BigTable : store large amount of structured objects. Not Support queries & multi-row transactions. 페타바이트 capacity.
Best for Analytical data with heavy read/write events like AdTech, Financial, IoT.

- Cloud Storage : need to store immutable blobs larger than 10MB (large image / movies) 페타바이트 capacity. 5TB per objects.
For unstructured, binary or object data like images, movies, backups.

- Cloud SQL / Spanner : need full SQL support for an online transaction processing system. SQL은 테라바이트, Spanner는 페타바이트. SQL의 horizontal scalability가 부족하다면 Spanner 사용을 권장함.
SQL은 web frameworks / existing applications like storing user credentials and customer orders.
Spanner는 for large scale DB applications that are larger than 2TB (financial tradings or E-commerce)


- BigQuery: 아직 여기서 다루지는 않았음. Data storage & data processing 어딘가에 있는 기능으로, ML쪽에서 자세히 다룸. 단순한 storage로는 부적합함.

