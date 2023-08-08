## Introduction to Data lakes

Data Lake가 필요한 대표적인 시나리오는 아래와 같다.<Br>

예컨대 startup의 System Administrator라고 가정해보자. 목표는 Everything runs with no issues.
- Workloads는 Backend, Data ingestion, DB, and extra layers of Data processing.
- 규모가 작기 때문에, 소수 인원이 여러 작업을 관리하고 있음.
  - Data Modeling, Project Manager (developing code), DevOps managing DB
- Customer에게서 '요즘 속도가 느리다'는 제보를 받고 확인해보니 DB가 limit 도달... bottleneck.
  - DB 하나가 너무 많은 작업을 전부 감당하고 있음. store streaming Data / System Logs / Customers' Data, running Analytics...
  - broken down into separate component -> Mature Data Administration strategy.

AWS Cloud의 Managed Service를 사용해서 Component 분리.
- Storage
- Data Ingestion
- Analytics
- Real-time Analysis
- Machine Learning

### Why Data Lakes

각자 처한 상황에 따라 하나의 DB를 쓰거나, 각 상황에 맞는 여러 DB를 운영하고 있을 수 있다. 어떤 경우에건, 운영하다 보면 두 가지 문제를 마주한다.
- Load Issues
- Data Cataloging / Security becomes Challenging

Data Lakes는 Powerful DB같은 개념이 아님. 
- DB는 보통 storage와 processing이 결합된 형태. 따라서 scale storage without processing이 어려운 구조. vice versa.
- Data lake: Centralized repository to securely store structured / unstructured data with no scaling restriction.
  - 보통 Encompass multiple functions in the data spectrum
    - data ingestion, processing, ML, data visualization, etc...
- Reasons for a data lake
  - increase operational efficiency
  - make data available from departmental silos
  - lower transactional cost
  - offload capacity from DB / Data warehouse

일반적으로 Data에서 insight 도출을 위해 쓰이는 종류는 아래와 같음.
- Transaction
- WebLogs
- ClickStreaming
- Social Media
- IoT device

핵심 특징은 '데이터 생성량이 매우 많다'이므로, 이런 데이터는 Dedicated Storage가 필요하다.<bR>
Data Storage와 Data Processing을 분리하게 되므로, 필요에 따라 다양한 방식의 Data Processing / Visualization을 사용할 수 있음.

### Characteristics of Data Lakes

**Data-agnostic**
- 특정 데이터 형식이나 포맷에 국한되어서는 안 된다. pictures, text (compressed / encrypted...), audio, video, binary...

**Dive anywhere into the vast data collected, to generate insights**
- 예컨대 이커머스의 fullfillment 관련 데이터가 Data lake에 있다면, 어떤 팀의 어떤 요구사항에도 데이터를 제공할 수 있어야 함.
  - 비즈니스 팀의 연휴시즌의 sales report
  - 데이터팀의 fullfillment logistics / operation 효율화를 위한 ML
  - ...

**Mature Data Lakes are Future Proof**
- 어떤 business 관련한 요구사항이나 질문이 현재 혹은 미래에 있고, 관련된 데이터가 Data Lake에 있다면 Answer can potentially be right there.
  - with Right Data Processing & visualization.

### Data Lake Components

크게 네 가지로 구성됨.
- Ingest and Store
- Catalog and Search
- Process and Serve
- Protect and Secure


#### Ingest and Store

Data agnostic해야 하므로, 어떤 종류의 데이터라도 Data lake에 저장할 수 있게끔 되어야 한다. <br>

![스크린샷 2023-08-06 오후 7 03 31](https://github.com/inspirit941/inspirit941/assets/26548454/0ea5f273-4994-473f-9fa2-e3da7e389915)
<br>

예컨대 위 예시와 같은 IoT 디바이스의 데이터를 minimal latency on a large scale로 지원해야 함.
- 보통 이 정도 데이터의 ingestion을 위해서는 data streaming 기술이 필요하다.
  - AWS Kinesis / AWS Managed Streaming (Kafka)

#### Catalog and Search

Efficient indexing / Searching mechanism to quickly discover What & Where data is stored.
- cf. Data Swamp: disorganized, in terms of data catalog and searching.

#### Process and Serve

Hadoop을 신봉하는 경우가 있음. Data Storage / Data processing 둘다 제공하기 때문.
- Hadoop은 storage / processing이 tightly coupled되기 때문에, hadoop cluster를 발급받을 경우 두 가지 서비스(storage / processing) 비용을 내게 됨
- 하지만 cloud computing의 최대 장점 중 하나는 'only pay for what you use'. hadoop cluster는 processing 기능을 쓰지 않을 때에도 비용을 내게 됨.
- hadoop은 중요한 컴포넌트가 맞다. 하지만 cloud native 방식으로 접근한다면 '필요할 때만' 쓰는 방식을 고려해볼 수 있다.
  - 그래서 dedicated storage service를 쓰는 것. 사용한 만큼만 비용을 낼 수 있게.
  - 예시: 필요할 때 transient Hadoop cluster로 processing 수행한 뒤, storage로는 AWS S3를 쓰는 방식
  - AWS Glue는 hadoop job을 on-demand 방식으로, job이 실행할 때만 비용을 청구하는 방식으로 설계된 서비스.

#### Protect and Secure

prevent unauthorized users from accessing data. AWS의 managed service를 활용해서 아래와 같은 기능을 충족할 수 있다.
- Data Retention
- Encryption
- Access Control Lists
- Refined governance standards

### Comparison of a Data Lake to a Data Warehouse

![It5HCGkWSfqeRwhpFnn6WQ_b75153889ebf412e91cd07b1bddc9309_image-1-](https://github.com/inspirit941/inspirit941/assets/26548454/7b7bb5da-7c6a-457e-95ea-d7d39aa6afab)


**Data warehouse**: DB optimized to perform analytical queries that leads to insights.
- 보통 analytics 용도로 쓰기 때문에, structured table 방식으로 schema 정의하는 과정이 데이터 수집/저장보다 선행되어야 한다. (schema-on-write architecture)
  - 데이터 정규화의 장점은 있으나 flexibility가 약함. 반대로 Data lake의 장점이 flexibility.
- Query로 SQL을 사용. SQL의 기능과 확장성을 넘어서지는 못함
- Structured Data 특화

**Data Lake**: schema-on-read architecture.
- unstructured 데이터를 받아서, 해당 데이터의 구조에 맞는 processing을 수행할 수 있음.
- 즉 Data ingestion 단계에서는 schema 고민을 할 필요가 없다. read data / processing 할 때 필요함.
  - AWS Athena: allows you to match the table schema to your dataset.
  - Athena는 ingested된 데이터의 메타데이터를 저장하는 용도. 실제 데이터는 S3에 저장되는 편. 따라서 S3에 저장된 데이터 구조가 바뀌면 Athena도 바꿔줄 수 있다.
- Use the right compute layer for the job. Custom compute framework (Spark / Python) 등을 사용할 수 있다.
- Structured / Unstructured 구애받지 않고 사용 가능.

그렇다고 두 가지의 우열을 가릴 수는 없다. 보통은 둘 다 씀. Data ingestion은 Data Lake를 활용하고, processing을 거친 뒤 Data Warehouse에 저장하는 방식도 많이 쓰인다.
- Data Warehouse의 Visualization 기능이나 Structured Data 최적화된 기능을 활용하려는 취지

참고: https://www.snowflake.com/trending/data-lake-vs-data-warehouse


cf. Data Warehouse vs Database

![gpJapWkaSAmSWqVpGugJDw_a5509ea0cbe74a62b687d04d9fe3ef1e_image-2-](https://github.com/inspirit941/inspirit941/assets/26548454/459a1429-d526-4538-847b-5642821b97cb)
<br>


### Data Lake Architecture

예컨대 AWS에서 Web Server를 운영중이고, Access Log에서 insight를 얻고 싶은 상황이라고 하자. 

![스크린샷 2023-08-07 오후 10 22 29](https://github.com/inspirit941/inspirit941/assets/26548454/99e0e829-c61d-4cd6-b7ce-ac22c1124dd1)
<br>

Data ingestion
- AWS의 오픈소스인 Amazon Kinesis Agent를 web server에 설치한다.
- Agent continuously sends data to Amazon Kinesis Firehose.

![스크린샷 2023-08-07 오후 10 25 25](https://github.com/inspirit941/inspirit941/assets/26548454/54567a5e-3a43-45f2-bdbb-6ad16d5c4e62)
<br>

Data Storage / Query
- Kinesis Firehose는 AWS S3에 데이터를 저장한다.
- S3에 저장된 데이터는 Amazon Athena로 SQL Query 가능하다.

![스크린샷 2023-08-07 오후 10 25 37](https://github.com/inspirit941/inspirit941/assets/26548454/4c4e18c0-b83f-434e-b9d3-185e539084c4)
<br>

Insights
- Detecting Http Errors after deployments...

위 예시는 '특정 목표 (getting insights from our web servers) 를 달성하기 위한 minimalistic Data Lake' 중 하나. made-to-order라고도 부른다.
- 사용자가 "total control on how you are producing the content" 상태일 때 유용함. 
  - 위 예시의 경우, 데이터를 만들어내는 Web Server가 사용자 관리 하에 있음.
- total control 방식이 유용한 이유는, insight 확보하는 수단인 AWS Athena에 맞게 Data format을 가져갈 수 있기 때문.
  - 미리 정의한 형식과 타입에 맞춰서 데이터를 전달하므로 processing 시간이 짧고, 따라서 low latency가 가능함.

<Br>

데이터 규모가 커지면 해야 할 요구사항이 증가한다.
- Cataloging to query data efficiently.
- ACL. who can do Athena Query / who can reach S3 Bucket.

![스크린샷 2023-08-07 오후 11 08 10](https://github.com/inspirit941/inspirit941/assets/26548454/78d7cf70-172b-4779-bc1e-a4f7b6cdde45)
<br>

요게 잘 되어서, '내가 관리할 수 없는' 다른 팀에서도 서버의 web log를 ingestion으로 넣고 싶어한다고 해 보자. 그러면 좀 더 Generic한 Data Lake architecture 고민을 하게 된다.
- 가장 쉬운 workaround는 Firehose -> AWS S3로 데이터가 업로드될 때마다 Lambda 함수를 실행하는 것.
  - 데이터 형식을 lambda 로직으로 맞추는 것.
- 새로 들어오는 dataset마다 pointing different Athena Table 하게 만들 수도 있지만, original table에서 쓰던 Same Query를 그대로 적용하고 싶다면
  - Lambda를 써서 data Transformation을 도입할 수 있음.
  - remove unnecessary field / convert data from one format to another.

Lambda는 보통 intensive compute power를 필요로 하지 않는 작업에 적합함.
- file renaming, text parsing, field normalization, etc

이렇게 data transformation을 담당하는 모듈을 추가하면서 Data Lake의 Modularization이 진행됨.
<br>

![스크린샷 2023-08-07 오후 11 16 59](https://github.com/inspirit941/inspirit941/assets/26548454/f9fcd604-7566-421f-9db9-0e4de34ab96c)
<br>

요구사항이 많아지면, 요구사항에 대응하기 위한 컴포넌트를 속속 추가할 수 있음.
- kinesis를 쓸 수 없는 환경이라면 API gateway로 http post요청을 받아서 lambda로 transformation + Kinesis Firehose로 전달해주는 컴포넌트.
- AWS ES (full text-search DB)로 text 검색편의성 강화 + Kibana로 visualize.

구성이 복잡해지고 컴포넌트가 많아진다고 해서, 모든 컴포넌트가 활발하게 쓰일 필요는 없다. onyl pay for what you use.


