### AWS Data Related Services

![스크린샷 2023-08-08 오후 8 03 29](https://github.com/inspirit941/inspirit941/assets/26548454/991c8e3b-7eeb-456e-a933-3ecfecd942ff)
<br>


다양한 AWS Service를 일종의 모듈 개념으로 조합해서 Data Lake를 구성할 수 있다.
- 핵심 컴포넌트 위주로 먼저 보고, 해당 컴포넌트의 기능을 추가하거나 보완해주는 서비스를 점차 추가하는 식으로 만드는 것을 권장함.

Data lake를 구성하는 핵심 컴포넌트는 크게 세 가지.
- Data Storage / Cataloging
- Data Movement (data ingestion)
- Analytics / Processing
  - SQL Query
  - Visualization
  - Business Report
  - etc...

세 가지 컴포넌트는 Decoupled Layer로 이해하는 편이 좋다. 각 layer별로 Managed / Secure / Scale을 관리할 수 있기 때문.
- 특히 Compute과 Storage는 구분하는 것을 권장한다.


### Storage / Cataloging

#### AWS S3

Data lake는 
- 저장해야 할 데이터 규모가 terabytes
- dataset 규모가 커질수록 scale up할 수 있어야 함
- structured / unstructured data 가리지 않고 저장할 수 있어야 함.
- RDBMS는 indexing / query 가능하다는 점은 있으나, schema-on-read 방식을 쓰기 어렵다는 점에서 Not feasible.

schema-on-read 방식과 built-in scalable 방식을 지원하는 AWS Service로는 **AWS S3와 S3 Glacier** 가 있다.
- store any type of data you want, in a centralized place
- managed service에서 제공하는 기능
  - scaling
  - durability
- offers integrations for analysis

<img width="945" alt="스크린샷 2023-08-11 오후 3 01 44" src="https://github.com/inspirit941/inspirit941/assets/26548454/81d9157e-d2e4-404e-95a8-157fab0b941e">
<BR>

소개할만한 특징으로는 cost optimization이 있음.
- S3는 data access frequency에 기반한 cost tier가 있다.
  - 데이터 접근이 자주 있을 경우.. Access cost는 낮은 대신 storage cost가 높은 tier
  - 데이터 접근이 별로 없는 경우.. Access cost가 높은 대신 storage cost가 낮은 tier 
- tier를 사용자가 생각할 필요는 없다. Intelligent Tiering 기능으로 S3가 알아서 구별해준다.
- S3 Glacier / S3 Deep Archive의 경우 '데이터 보존' 용도로서의 tier. 가장 낮은 storage cost

#### AWS Glue Data Catalog

Data lake를 구성하고 운영할 때 겪는 이슈들 몇 가지를 소개하면
- 쌓여있는 데이터는 많은데, user 입장에서는 내가 원하는 데이터가 lake에 있는지 / 어떻게 analyze, processing하는지 파악하기 쉽지 않다
- 시간에 따라 변경되는 데이터 format / versions 이력을 tracking할 수 있는 기능이 필요함.

위와 같은 구성이 잘 안 되어 있다면, Data lake의 기능을 제대로 활용할 수 없다. Data Swamp가 됨.
<br>

첫 번째로 해야 하는 작업이 Proper Metadata Setting이고, 이를 담당하는 서비스로 **AWS Glue**가 있다.
- Fully Managed, Serverless data processing & cataloging service (ETL)
- Central Metadata Repository인 **AWS Glue Data Catalog**
- Drop-in Replacement for Apache Hive Metastore.

<img width="737" alt="스크린샷 2023-08-11 오후 6 22 27" src="https://github.com/inspirit941/inspirit941/assets/26548454/9daa6550-af72-4901-bfd1-ca3805ca7b76">
<br>

AWS Glue Data Catalog의 구성
- table: 데이터의 metadata definition 정보를 담고 있음.
  - consists of Schemas
- databases: table들을 logical 단위로 묶은 Group

<img width="932" alt="스크린샷 2023-08-11 오후 6 26 06" src="https://github.com/inspirit941/inspirit941/assets/26548454/0d713091-2a54-4f7c-87d8-9573b7d15d29">
<br>

Glue crawler
- populate the AWS Glue Data Catalog with tables
- triggered to sort data in S3 & calls classifier logic to infer the schema, format, and data types.
  - Existing classifier (i.e. json)를 사용하거나, customized classifier를 등록해서 쓸 수 있다.
  - schema가 생성 / 변경 / 삭제되었을 때 data catalog에도 변경사항이 반영되도록 할 수 있다.
- Eliminates the need to manually create / define schemas.

crawler와 classifier를 통해 만들어진 metadata로 
- authoring processing of ETL jobs 
- readily available for querying in other AWS processing services

### Data Movement

Data source / data type에 따라 'data lake에 어떤 방식으로 데이터가 쌓이는지'가 결정됨. <br>

#### Amazon Kinesis Service

**real-time data streaming** <br>

**Amazon Kinesis service**를 쓰면 된다. Kinesis Service에는 몇 가지 종류가 있음.
- kinesis Data streams.
  - various source에서 데이터 받고, kinesis application에서 continuously process data / generate metrics, power live dashboards, send aggregated data into stores (like S3)
  - AWS SDK 사용해야 함. data processing 단위는 shards
  - scaling shards in / out, processed by one or multiple consumers
- kinesis firehose.
  - SDK 같은 코드 기반 Management를 원치 않는 경우 사용 가능.
  - storage에 데이터 저장할 때, 별다른 aggregation / processing 필요 없는 데이터일 때 유용하다.

#### AWS API Gateway

**ingest data in RESTful Manner.** <Br>

예컨대 하드웨어 스펙이 제한적인 IoT라면 streaming보다 Standard HTTP call 방식이 보다 적합할 수 있다. <br>

**AWS API Gateway**를 쓰면 된다. it acts as a front door / interface to a backend. 
- 단, kinesis처럼 data ingestion 관련해서 다양한 기능을 제공하는 수준까지는 아님. 

#### AWS Data Exchange

<img width="941" alt="스크린샷 2023-08-11 오후 8 07 05" src="https://github.com/inspirit941/inspirit941/assets/26548454/f5425392-8477-4814-905f-219893a4a09b">
<br>

**Third Party Generated Data** <br>

해당 서드파티와 호환되는 통신 프로토콜이나 서버 구축하는 것도 좋지만, **AWS Data Exchange**를 사용할 수 있다.
- offers interface to 100+ commercial products from data providers.
  - Data exchange API 사용해서 S3에 바로 저장할 수 있다.

#### Amazon AppFlow

<img width="951" alt="스크린샷 2023-08-11 오후 8 11 00" src="https://github.com/inspirit941/inspirit941/assets/26548454/7f79f7e1-33e4-4cd9-b437-8263801eb77a">
<Br>

SaaS Provider (Google Analytics, Salesfore 등)일 경우 **Amazon AppFlow**를 사용할 수 있다.
- data collection / secure transfer to your data lake, without custom code to connect services.
- invoke on-demand / on a schedule / after an event 
- S3에 저장된 데이터는 Athena 등을 활용해 analyze 가능.

#### Registry of Open Data on AWS

- pre-curated Dataset 활용 가능. discover / analyze public datasets
- register datasets to be shared.

### AWS Service for Data Processing

수집한 데이터를 분석 가능한 형태로 만들기 위한 Transform 작업.

#### Batch Processing

일반적으로 Apache Hadoop cluster로 massive data / parallel processing을 수행함. on-prem으로 클러스터가 구동중인 상태에서 minimal change로 AWS에 옮기고 싶다면 **AWS EMR**을 사용할 수 있다.
- managed cluster platform that allows to process / analyze the data from your Data lake.
- decouples compute / storage -> scale independently by using S3 as the storage layer.
- Long-running (persistent cluster) or transient cluster 형태로 운영 가능. 
  - transient cluster의 경우, process 작업이 끝나면 turns off the cluster. (only pay for what you use)


![스크린샷 2023-08-13 오후 3 00 53](https://github.com/inspirit941/inspirit941/assets/26548454/05aa0e43-23c7-499d-9045-be3e0ddb5e33)
![스크린샷 2023-08-15 오후 5 31 48](https://github.com/inspirit941/inspirit941/assets/26548454/f027b047-74dc-4e45-924b-902e804f9a4f)
<br>

Cluster Configuration 설정과 같은 작업 없이, run processing job에만 집중하고 싶다면 **AWS Glue** 를 사용할 수 있다.
- Glue는 Managed ETL tool to categorize, transform, enrich, and move data. 
  - categorize 담당하는 게 Glue Data catalog
  - classifier
  - crawler
  - **job**

Glue에서는 EMR처럼 직접 cluster를 구축하는 대신, Job 단위로 작업을 수행할 수 있다.
- job은 'data processing이 필요한 business logic'으로 정의된다.
  - Glue Data Catalog에서 구성한 table 정보를 기반으로 Source / Target Configuration을 job에 등록한다.
  - 추가로 필요한 customized logic을 등록할 수 있고, Transformation Script를 실행할 수 있다.
- 등록한 Glue Job은 일정한 시간대에 scheduled 또는 Triggered by Event.\
  - Move / Transform / run 등의 작업이 실행될 때, underlying infrastructure는 Glue에서 관리한다.

일종의 serverless Hadoop처럼 이해하면 됨.

#### Real time Data

kinesis stream이나 firehose로 받게 되는 real time data는 보통 raw data.
- 특성상, 데이터가 들어오는 즉시 processing을 바로 처리하는 편이 효율적이다.

적용 가능한 서비스들
- AWS Lambda: Serverless compute service runs on-demand, based on triggers.
  - kinesis와 호환되며, 보통 S3에 데이터 저장하기 전 preprocessing 용도로 사용한다.

### AWS Services for Analytics

데이터 자체 특성 / desired outcome 종류에 따라 여러 가지 Analytics tool 사용 가능.
- S3에 저장된 데이터 사용하기: Athena, Redshift
- real time으로 들어오는 데이터 사용하기 (detecting anomaly 같은 용도): Kinesis Data Analytics

#### AWS Athena

![스크린샷 2023-08-15 오후 6 56 31](https://github.com/inspirit941/inspirit941/assets/26548454/ca90a57c-762f-4ec1-9293-d1d79eb1893e)
<br>

Serverless service works with Data Lake.
- S3에 저장된 데이터에 RDBMS에서 쓰는 것과 비슷하게 SQL Query를 사용할 수 있다.
- ad-hoc Query against your datasets 가능
- cluster나 data warehouse 같은 resource management 필요 없음 (serverless)
- Integrates with AWS Glue
  - natively supports Querying datasets / datasource from AWS Glue Data Catalog.

#### AWS Redshift

이외에도 S3와의 direct integration을 지원하는 Solution으로는 **AWS Redshift**가 있다. Data Warehouse Service.
- spin up cluster to run Complex SQL queries for analytics against your data.
- S3 외에도 다양한 종류의 datasource를 지원하므로, join across datasets도 가능하다


#### AWS Kinesis Data Analytics

real-time으로 들어온 데이터를 real-time으로 분석하기 위한 service
- run SQL code against streaming data.
  - time-series analytics / feed realtime dashboards & create realtime metrics.
- 예컨대 IoT 디바이스를 사용한 지진 감지 시스템이라고 하면
  - kinesis data streams로 real time data transfer to S3
  - kinesis data analytics로 real time dashboard 생성, normal threshold 초과할 경우 SNS 로 alert 가능.
- analytics 수행 결과를 어디로 전송할 것인지 쉽게 설정할 수 있음.
  - S3에 분석결과를 저장한다거나
  - 검색 용도로 AWS ElasticSearch (AWS ES)에 전달한다거나.

**AWS ElasticSerach Service?**

- 데이터 종류 무관하게 search / analytics에 사용 가능한 오픈소스 service
- kinesis에 적용 가능한 예시로는 보통 Log analytics.
  - full-text log from various sources, to make it queryable / discoverable.
- ELK Stack에서 ElasticSearch 컴포넌트로 사용할 수 있음.
  - data ingest, store, visualize data.
  - ELK의 Kibana로 시각화할 수도 있지만, AWS에서는 visualization service로 **QuickSight** 지원한다.


### AWS Services for Predictive Analytics & Machine Learning


ML로 할 수 있는 대표적인 기능 중 하나가 Predictive Analytics. 예컨대 Forecasting - 과거 데이터를 기반으로 미래의 결과를 예측하는 것.
- ML로 classification, recommendation, prediction 등의 기능을 수행하기 위해서는 데이터 학습이 필요함.
- 학습에 필요한 데이터의 collect, store, prepare, categorize data 작업을 Data Lake에서 처리할 수 있다.
  - Schema-on-read 특징은 flexibility를 확보하기 용이함.


![스크린샷 2023-08-15 오후 8 58 50](https://github.com/inspirit941/inspirit941/assets/26548454/f16c633a-55c4-48c3-9ecd-b79e93096798)
<br>

ML을 사용하려는 사용자 상황에 따라 총 세 가지 선택지가 있음.
- Managed ML service. hard work의 어느 정도 범주는 AWS에서 지원하지만, 사용자 본인도 어느 정도 지식이 있어야 사용할 수 있다.
  - Amazon SageMaker 사용 가능. Building / Training / Deploying ML models 지원.
  - connect to training data, select & optimize the best algorithm and framework, deploy model on autoscaling clusters on EC2 instances.
- DIY. ML 하나부터 열까지 사용자가 직접 세팅한다.
  - Data lake인 S3의 데이터를 own model / own algorithm을 사용한 학습 가능.
  - Compute Power로는 EC2 + DeepLearning AMI or Amazon Machine Images 사용 가능.
- Solution-Oriented, pre-built AI model을 API 형태로 사용할 수 있음. NLP와 Computer Vision 쪽.
  - Amazon Recognition (image / video classification)
  - Amazon Comprehend (NLP)

### intro to AWS Lakeformation

![스크린샷 2023-08-15 오후 9 07 02](https://github.com/inspirit941/inspirit941/assets/26548454/41b3859f-0c5d-4b2b-9e15-bdab469532c5)
<BR>

Daka Lake 구축을 위해 지금까지 설명한 components를 직접 조합할 수 있다. 하지만 이걸 전부 provisioning / configuring 직접 하는 대신 Lakeformation을 사용할 수도 있다.
- automates some manual steps required to create Data Lakes;
  - collecting, cleansing, moving, cataloging data.
  - securely making the data available for deriving insights.

사용 시 대략적인 특징은 아래와 같다.
- data source를 lake formation 서비스와 연결한다.
- lake formation에서 crawler / ETL / cataloging 등의 작업을 자동으로 수행하고, Data lake인 S3 Storage에 저장한다
  - predefined Datasource (RDBMS, Cloudtrail logs 등)로 구성된 supported blueprints를 사용할 수 있다.
    - data source, data target, schedule을 입력으로 받는다.
    - blueprint 선택 후, workflow를 생성한다. workflow에서는 AWS Glue crawlers, jobs, triggers 정보가 자동으로 생성된다.
  - 또는 필요로 하는 customized crawlers / classifiers를 지정해서 적용할 수 있다.
- analytical services를 lake formation과 연결할 수 있다.

