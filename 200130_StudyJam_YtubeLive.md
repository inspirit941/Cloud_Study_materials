# Study Jam Lecture

<img width="849" alt="스크린샷 2020-01-30 오후 9 12 42" src="https://user-images.githubusercontent.com/26548454/73454410-63bfad80-43b1-11ea-8c25-7c8831794b62.png">

자격증 로드맵. 파란색이 코세라, 노란색이 퀵랩.

ACE와 PCA의 가장 큰 차이 = Business Requirement의 존재여부.

## 개념설명

1. Storage

<img width="844" alt="스크린샷 2020-01-30 오후 9 17 12" src="https://user-images.githubusercontent.com/26548454/73454411-64584400-43b1-11ea-9530-3454866bda87.png">

데이터 유형에 맞게 적절한 제품을 선택하면 된다.

* Unstructured Data일 경우 (비정형 데이터) -> Cloud Storage 사용. (Data Lake용도)
	- 자주 쓰진 않는데 저장해야 하는 경우… Nearline, ColdLine, Archive (1년에 한 번 정도 access할 경우)

* OLTP, OLAP에 해당하는 것들 = structured.
Transactional Data 저장하기 + 데이터에서 의미 찾기 (분석)
But 바로 분석하기는 원래 어렵다.
	1. Raw 데이터 자체의 불완전성. 값이 비었거나 형식상 불완
전
	2. 원본데이터 그 자체를 분석으로 쓰지는 않음.

따라서 보통 ETL(Extract, Transform, Load) 과정을 거쳐 데이터를 복사하고 정제하기 마련이다. 그 후 DB에 저장함.

Transactional DB를 SQL / NoSQL 형태로 다시 나눌 수 있음. (Relational인지 아닌지)

- 만약 RDB로 MySQL, PostgreSQL 썼으면 cloud SQL에 그대로 옮길 수 있다.
단, RDB는 Scale up 방식을 사용한다. 대충 수백 기가 정도를 넘어가게 되면 그다지 추천하지 않음. 저장할 데이터의 양이 테라바이트를 넘어갈 것 같으면 Scale up보다는 out을 사용함.
- Cloud Spanner. 현재 경쟁자 없음. Scale out을 제공하는 최신 기술. 구글에서도 이거 쓰고 있음.

- NoSQL은 Cloud Datastore / Firestore 사용 가능.


* 분석용 DB는 크게 Bigtable / BigQuery.
가진 데이터가 Table 형태면 BigQuery. Key-value Form이면 Bigtable에 적용 가능.
또는, 고도의 분석을 하고 싶으면 BigQuery, 단순연산 위주라면 BigTable. BigQuery보다 데이터 저장량이 많을 경우 BigTable (IoT나 Time Series 데이터 등)

---

## Data Pipeline

<img width="840" alt="스크린샷 2020-01-30 오후 10 16 08" src="https://user-images.githubusercontent.com/26548454/73454412-64584400-43b1-11ea-8bec-e67b274bde27.png">


데이터 파이프라인을 클라우드에서 만들 경우의 아키텍처.
1. 실시간 데이터 (센서에서 수집하는 데이터, 또는 공장에서 매순간 생산되는 Stream 데이터) -> GCP에서는 Pub/Sub을 사용한다. 
	- *실시간으로 오는 데이터 수집은 Pub/Sub라고 보면 된다* 무지막지한 크기의 데이터도 다 받아낼 수 있음. Kafka 같은 제품군.
	- File형태 같은 유형은 Storage에 저장하면 됨. 얘네는 보통 Batch data라고 부른다.

2. 데이터 분석하기. 단 stream / batch 데이터를 동시에 분석하는  on-premise에서는 거의 불가능함. GCP에서는 Cloud DataFlow를 지원한다.

Apache Beam. (Batch + Stream) 을 사용해 ETL 진행. 이런 식의 전처리 작업을 도와주는 다른 프로그램으로는 Dataprep (데이터프랩)이 있다. UI가 잘 되어 있는 게 특징.

그 외에도 data Fusion이 있음. 다양한 소스에서 오는 데이터 integration + 전처리에 장점.

3. 전처리 마친 데이터는 BigQuery / BigTable에 넣고 분석. 보다 심도있는 분석을 원한다면 AI platform 서비스를 사용할 수 있다. Jupyter notebook에 Python 지원. 알아서 코드짜는 게 가능. 

4. 시각화 - data studio. G suite에 포함된 제품. 태블로 등도 사용 가능하다.


그 외에도, dataproc은 on-premises에서 하둡과 같은 대용량 분산처리 시스템을 사용하고 있을 경우 GCP에 적용할 수 있게 해주는 서비스라고 보면 된다. (Map-reduce 작업 등)

---
## VPC

물리적으로 네트워크를 연결하는 게 LAN이었음. 구글 네트워크는 SDN이라는 프로그램을 써서 네트워크를 추상화해 구현해뒀음. 정확히는 프로그램으로 routing을 만들어둠.

따라서 router 하나에 전세계의 네트워크를 하나로 묶을 수 있게 됨. LAN의 물리적 한계를 깸. 하나의 라우터로 전세계 어디서든 Compute Engine 생성 및 internal IP로 소통이 가능하다.

### 로드밸런싱

수많은 클라이언트에게 서비스를 제공하려면, 여러 대의 서버가 필요 + 각 서버에 클라이언트 트래픽을 할당해주는 게 로드 밸런서. GCP의 장점이라면, 로드밸런서 한 개로 충분함. 전세계 커버 가능. PoP라는 걸로 구현했기 때문.

### AutoScaling

시간대별로 클라이언트 서비스 양이 다름. 고객 수요에 맞게 VM 생성 및 shutdown 작업.

### Container

<img width="841" alt="스크린샷 2020-01-30 오후 10 31 47" src="https://user-images.githubusercontent.com/26548454/73454413-64584400-43b1-11ea-9b9b-6f1aaef61ee7.png">


이전까지는 컴퓨터 한 대 + 운영체제 + 여러 개의 소프트웨어 설치해 사용. (각 컴퓨터당 운영체제 하나.) 서버의 경우 컴퓨터 한 대에 서비스 하나. -> 이건 비효율적이다. 컴퓨터 한 대에 어플리케이션 하나..
-> 그래서 등장한 게 Virtualization. 하드웨어 하나에 여러 커널 (운영체제)를 설치하고, 그 위에 애플리케이션을 올림. 이 방식으로 많이들 운영하고 있음

-> 문제점? = 운영체제 자체가 무겁다. 구글에서는 아예 하드웨어 하나 + 운영체제 하나 + “어플리케이션 독립”을 구현함. 이 구현방식이 Container. 컨테이너 단위로 서비스를 제공하게 됨.


<img width="840" alt="스크린샷 2020-01-30 오후 10 34 02" src="https://user-images.githubusercontent.com/26548454/73454494-8c47a780-43b1-11ea-9cc7-0dd0a0fc10b3.png">

어플리케이션을 Container 형태로 변환해 주는 서비스가 Cloud Build. 이제 Container를 Registry에 등록. (깃허브같은). 컨테이너가 필요하면 다운받아서 사용할 수 있도록.

이 때, 컨테이너 최소 두 개 정도를 하나의 Pod라는 개념으로 담는다. 이 Pod를 각 VM에 deploy하는 방식.

이렇게 만들어지는 수많은 container의 생성과 배치 작업… 쉽게 하는 Tool이 쿠버네티스. Managed Kubernetes 서비스가 GKE.

---




Linkedin: Keetaek Park
Email : keetaekpark@google.com

multiregion과 region의 차이 : Availability. 
