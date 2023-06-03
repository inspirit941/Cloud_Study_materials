## Designing a serverless data analytics solution on AWS

### Customer #2 - SW House

#### Customer Requirement

현재 S3 Static Website 쓰고 있으며, admin 전용 사이트도 있음. 메뉴 수정하고 싶을 때 사용함. 데이터는 S3 bucket에 저장됨.
- QR Code pointing to the bucket -> 레스토랑 테이블에 QR Code를 부착함
- payment 솔루션으로 써드파티 서비스 사용중 - static html 웹사이트에 이 기능은 연동하고 싶음.
  - 단, 이 기능은 지금 AWS 사용하려는 게 아니므로 out of scope.
- 데이터 분석을 하고 싶다.
  - what dishes in the menu people are viewing
  - 그냥 scrolling만 하는지 / 애피타이저 같은 특정 메뉴에 멈춰있는지
  - 이런 정보들 토대로 menu design optimize하고 싶다. (Clickstream data anaylsis, based on session data)
- 데이터 ingestion은 JS library. http posts 보낼 수 있으며 rest standard에 부합하는 endpoint가 필요하다. 
- 중요 기준: Cost. per time이 아니라 refined usage별로 가격 지불하는 방식을 선호함
  - managed service 선호. maintaining system 관련 작업은 하고 싶지 않다
  - 수집한 데이터는 Another AWS Region에 백업 + 암호화 (encryption in transit, encryption at rest)

### Requirement Breakdown

![스크린샷 2023-05-29 오후 6 53 03](https://github.com/inspirit941/inspirit941/assets/26548454/bdaec253-6bac-4fa7-99aa-d4a00edf3adc)
<br>

- S3 기반 Static Web hosting 방식을 사용중. bucket과 object가 public access 가능하면 HTTPS 통신도 지원한다.
- Admin 페이지에서 레스토랑 운영자가 메뉴를 업로드하면 S3 bucket에 저장되는 방식.
- 이외에도 S3 Bucket을 pointing하는 QR Code 생성 로직이 있고, admin페이지에서 생성된 QR Code를 사용할 수 있도록 지원하고 있다.
- client-side에서 clickstream information 수집하는 JS Library를 쓰고 있다. 이 데이터를 Push할 RESTful HTTPS endpoint가 필요한 상황

즉 Requirement를 정리하면
1. Provide HTTPS endpoint for data collection
2. Prefer using AWS managed Service
3. Prefer service with per-usage billing, not per-time billing
4. Have cross-region data replication and encryption
5. Use different storage classes to save on cost & encryption

### Architecting the Solution

How to use collected data to produce information that would be useful for business needs.
- Data transformation이 필요. 
  - AWS는 data injest 단계 / after it has arrived 단계에서 Data transformation service를 제공한다.
- customer requirement에 따르면 JS library로 데이터 수집은 하고 있다. 따라서 injest & store만 하면 된다.

**How data comes into the architecture you were designing.**
- 여러 타입의 데이터를 / 여러 디바이스에서 수집해야 하는 Generic solution일 경우 위 특성이 굉장히 중요해진다.

**Use the right tool for the job.**
- perform better, saving money.
- '어떤 서비스를 써야 하는가'를 잘 이해해야 함.

https://aws.amazon.com/ko/big-data/datalakes-and-analytics/

AWS는 데이터 관련 서비스를 크게 네 가지 카테고리로 분류함. '목적에 맞는 정확한 service를 사용하는 것을 권장한다'
- Analytics
  - AWS Athena: interactive query, analyze data in S3 using Standard SQL. Serverless
  - AWS EMR / AWS Glue: Big Data Analysis that can run managed Hadoop clusters or jobs.
    - Glue는 real-time movement에 보다 적합한 솔루션, EMR의 경우 data transformation 쪽 고급기능을 제공함.
    - massive parallel processing of distributed data.
    - Apache Spark, Hive, Presto 등 다양한 종류의 오픈소스 지원
- Data movement
- Data lake
- Predictive analytics and Machine learning

서비스를 선택할 때 고려해야 할 기준점 몇 가지를 제시하자면
- What latency is acceptable between ingesting the data / making it available?
- Can customer afford to wait some time to get the data?
- Where is the data coming from?
- Purpose: DB migration? clickstream data ingestion? batch file uploads?

#### AWS Data Service 개요

##### Data lakes & storage

###### S3

object storage service that offers scalability, data availability, security, and performance.
<br>

![xpDo1_CATs6a3dnaA9cVzA_4b9ae8b78cb3407baf58440f97a67cf1_Reading2 1A](https://github.com/inspirit941/inspirit941/assets/26548454/e0c6b1fd-e04e-40e7-9e82-3777e80330ae)
<br>

- **Archive data at the lowest cost**: Move data archives to the AWS S3 Glacier classes to lower costs, reduce operational complexities, and gain new insights.
- **Run cloud-native applications**: Build fast, powerful, mobile and web-based cloud-native applications that scale automatically in a highly available configuration, such as **static websites** that use the client side for coding.
- **Build a data lake**: Run big data analytics, artificial intelligence (AI), machine learning (ML), and high performance computing (HPC) applications to unlock data insights.
- **Back up and restore critical data**: Meet Recovery Time Objectives (RTO), Recovery Point Objectives (RPO), and compliance requirements with the robust replication features of Amazon S3.

###### AWS Lake Formation

> service that you can use to set up a secure data lake in days. 
> A data lake is a centralized, curated, and secured repository that stores all your data, both in its original form and prepared for analysis. 
> You can use a data lake to break down data silos and combine different types of analytics to gain insights and guide better business decisions.

##### Data Analytics

###### AWS Athena

> Amazon Athena is an interactive query service that you can use to analyze data in Amazon S3 by using standard Structured Query Language (SQL). 
> Athena is serverless, so you don’t need to manage infrastructure, and you pay only for the queries that you run.

> Using Athena is straightforward. You point to your data in Amazon S3, define the schema, and start querying by using standard SQL. 
> Most results are delivered within seconds. With Athena, you don’t need complex extract, transform, and load (ETL) jobs to prepare your data for analysis. 
> Anyone with SQL skills can use Athena to quickly analyze large-scale datasets.

###### AWS EMR

Amazon EMR is a big data solution for petabyte-scale data processing, interactive analytics, and machine learning that use open-source frameworks, such as Apache Spark, Apache Hive, and Presto.
<br>


- Run large-scale data processing and what-if analysis 
  - by using statistical algorithms and predictive models to uncover hidden patterns, correlations, market trends, and customer preferences.
- Extract data from various sources, process it at scale, and make the data available for applications and users.
- Analyze events from streaming data sources in real time to create long-running, highly available, and fault-tolerant streaming data pipelines.
- Analyze data using open-source ML frameworks, such as Apache Spark MLlib, TensorFlow, and Apache MXNet.
- Connect to Amazon SageMaker Studio for large-scale model training, analysis, and reporting.

###### AWS OpenSearch Service

> to perform interactive log analytics, real-time application monitoring, website search, and more. 

> OpenSearch is an open source, distributed search and analytics suite that is derived from Elasticsearch. Amazon OpenSearch Service is the successor to Amazon Elasticsearch Service. 
> It offers the latest versions of OpenSearch, support for 19 versions of Elasticsearch, and visualization capabilities that are powered by OpenSearch Dashboards and Kibana. 
> Amazon OpenSearch Service currently has tens of thousands of active customers, with hundreds of thousands of clusters under management, processing hundreds of trillions of requests per month.

##### Data Movement

###### AWS Kinesis

> Amazon Kinesis, you can collect, process, and analyze real-time, streaming data so that you can get timely insights and react quickly to new information. 
> Amazon Kinesis offers key capabilities to cost-effectively process streaming data at virtually any scale, along with the flexibility to choose the tools that best suit the requirements of your application. 

> With Amazon Kinesis, you can ingest real-time data such as video, audio, application logs, website clickstreams, and Internet of Things (IoT) telemetry data for machine learning, analytics, and other applications. 
> You can use Amazon Kinesis to process and analyze data as it arrives, which means that you can respond quickly—you don’t need to wait for all your data to be collected before processing can begin.

###### AWS Glue

> serverless data integration service that you can use to discover, prepare, and combine data for analytics, machine learning, and application development. 
> AWS Glue provides capabilities that are needed for data integration so that you can start analyzing your data and using your data in minutes instead of months. 
> Data integration is the process of preparing and combining data for analytics, machine learning, and application development. It involves multiple tasks, such as discovering and extracting data from various sources; enriching, cleaning, normalizing, and combining data; and loading and organizing data in databases, data warehouses, and data lakes. These tasks are often handled by different types of users who each use different products.

###### AWS DMS (Data Migration Service)

> AWS Database Migration Service (AWS DMS) helps you migrate databases to AWS quickly and securely. 
> The source database remains fully operational during the migration, which minimizes downtime to applications that rely on the database. 
> AWS DMS can migrate your data to and from the most widely used commercial and open-source databases.

##### Predictive analytics and machine learning

###### AWS SageMaker

> SageMaker can be used for any generic ML solution. You can use it to build, train, and deploy ML models for virtually any use case with fully managed infrastructure, tools, and workflows. 
> SageMaker requires a learning curve to use, but it’s a managed serverless service that many people can use to innovate with ML through a choice of tools—such as integrated development environments (IDEs) for data scientists and no-code interfaces for business analysts.

###### Amazon Rekognition

With Amazon Rekognition, you can automate image and video analysis by adding pretrained or customizable computer vision API operations to your applications without building ML models and infrastructure from scratch.

###### Amazon Comprehend

natural-language processing (NLP) service that uses ML to uncover valuable insights and connections in text, which is instrumental for a data analytics solution. For example, you could mine business and call center analytics or process financial documents. For medical use cases, you can use Amazon Comprehend Medical, which focuses on extracting information accurately and quickly from unstructured medical text.For more information, see [Amazon Comprehend](https://aws.amazon.com/comprehend/) and [Amazon Comprehend Medical](https://aws.amazon.com/comprehend/medical/).

#### AWS S3 for Storage

EBS, EFS, S3 등 여러 서비스 중 S3가 이 requirement에 제일 부합하는 이유
- EBS: block level access when you need a file system. EC2에 Attach된 형태여야 하고, S3처럼 granular한 billing management 기능이 없으므로 배제. S3의 Durability가 EBS보다 높은 것도 있다.
- EFS: Replicate data across AWS Region이나, EC2 / Container / Server와 같은 리소스에 Attach해야만 동작함. storage 그 자체로 존재해야 하는 Data analytics 서비스 구조에 부합하지는 않는 편.
- S3: API call로 서비스 접근이 가능하므로, data processing과 storage를 분리할 때 가장 이상적임.
  - 분리해야 하는 이유: ingestion과 data processing을 분리할 수 있기 때문. 하나의 데이터 source에 다양한 processing을 병렬 실행하는 등 독립적인 수행이 가능하다.
  - Data Lake로도 사용됨
  - high durability (99.999999999%) - object 단위로 AWS region 내 여러 개의 physical facilities에 복제되어 보관하기 때문.
  - refined usage 단위로 비용이 청구되며, Access pattern 토대로 intelligent-Tiering을 지원함.
  - encrypt data in transit / at rest for free.

![스크린샷 2023-06-01 오후 5 04 39](https://github.com/inspirit941/inspirit941/assets/26548454/0371485c-87a3-42fa-b033-befded25a8dc)
<br>

Bucket을 생성할 때 Block Public Access 해제 버튼을 클릭할 수 있지만, 이것만 해제한다고 bucket이 public access가 되는 게 아니다.
- Bucket이 public 공개될 수 있도록 Configuration을 활성화하는 것.

![스크린샷 2023-06-01 오후 5 07 04](https://github.com/inspirit941/inspirit941/assets/26548454/64df9a80-bf72-4187-bde7-b87c0aef9a2c)
<br>

**Block Public Access Setting for this Account** 에서 public access 활성화를 해줘야 한다.
- 특정 bucket에서 public access를 활성화해도, account level에서 disable이면 public access가 적용되지 않는다고 함

![스크린샷 2023-06-01 오후 5 11 37](https://github.com/inspirit941/inspirit941/assets/26548454/c98e7128-ede5-4179-b1ed-5089a65d10f3)
<br>

해당 bucket의 property 탭에서 static website hosting 옵션을 Enabled로 변경한다.
- index document와 error document에 html 파일을 지정해준다.

![스크린샷 2023-06-01 오후 5 12 49](https://github.com/inspirit941/inspirit941/assets/26548454/3da3938e-1460-4ef3-91d4-69718fcf6391)
![스크린샷 2023-06-01 오후 5 13 48](https://github.com/inspirit941/inspirit941/assets/26548454/e9408fb0-d989-457e-b3e3-72481467e587)
![스크린샷 2023-06-01 오후 5 14 48](https://github.com/inspirit941/inspirit941/assets/26548454/5570f8e0-123d-46b8-802a-316dd9bfbe52)
<br>

bucket의 permission 탭에서 bucket policy를 'allow to be public'으로 수정해줘야 한다.
- policy가 정상적으로 적용되면, S3 bucket에 'publicly accessible'이라는 문구가 보인다.
- Static website hosting을 들어가보면 URL이 주어진다.

##### S3 Cross-Region Replication

Replicate Object with Tag & Metadata into other AWS Regions
- for reduced latency, compliance, security, disaster recovery, etc.
  - Compliance: compliance requirements might require you to store data at even greater distances. You can use CRR to replicate data between distant AWS Regions to satisfy these requirements.
  - Latency performance: If your customers or end users are distributed across one or more geographic locations, you can minimize latency for data access by maintaining multiple object copies in AWS Regions that are geographically closer to your customers.
  - Regional efficiency: If you have compute clusters in two or more AWS Regions that analyze the same set of objects, you might choose to maintain object copies in all of those AWS Regions.
- Bucket / shared prefix / object 단위로 설정 가능. object의 경우 tag을 붙여야 활성화 가능하다

##### Lifecycle of S3

저장한 object를 다른 S3 storage class로 저장하도록 rule을 설정할 수 있다.
- infrequently access
- do not need to access in real time

###### AWS S3 Intelligent-Tiering storage class

명확한 rule을 설정하기 어려운 상황이라면 **AWS S3 Intelligent-Tiering storage class** 를 사용할 수 있다.

![amazon-s3-intelligent-tiering-how-it-works-diagram 936ae9768ad84227feab5023c86432ce1aab4798](https://github.com/inspirit941/inspirit941/assets/26548454/c35bdc97-87e5-4bb0-8b6a-c5214d8784d5)
<br>

자동으로 해 준다.
- unknown / changing / unpredictable access-pattern인 경우에 적용 가능함. 목적이 optimize storage costs by automatically moving data to the most cost-effective access tier.
  - monthly object monitoring and automation charge가 부과됨
  - 128KB 이하의 작은 파일은 intelligent-tiering 대상이 아님. 항상 Frequent Access tier rate로 비용이 부과되며, monitoring / automation charge는 없다.
- default storage class로 사용 가능 - data lakes / data analytics / applications / user-generated content.

###### AWS S3 Glacier storage class

![s3-glacier-overview 0d570958d5161d19059c7dee00865500c1470256](https://github.com/inspirit941/inspirit941/assets/26548454/1dec6d54-cebb-4eb5-aabc-9b42435275e1)
<br>

데이터 아카이브 용도로 설계된 storage class. 일반 클래스보다 저장 비용이 저렴하고, 99.999999999% duarbility 보장 

#### Service for Data ingestion

예시에 따르면, S3에 저정할 데이터는 clickstream data.
- Small events containing piece of data, that are generated continuously, high speed and volume.
- 일반적으로 user action을 토대로 생성된다.
  - 예시의 경우 navigating restaurant menu using html code
- 일반적으로, 데이터 로깅해서 사용자 행동 분석을 하는 것이 목적.
  - 사용자가 특정 페이지에 얼마나 있었는가
  - 사용자가 어디서부터 navigate 시작하고 어디서 끝나는가 등등
- real time 단위로 확인함으로써 추천 시스템, 고도화된 A/B testing, push notification based on session length 등등.. 이 가능하다.

**Data ingestion 서비스 후보군**
- Amazon EMR -> Managed Hadoop cluster with installing a streaming framework.
  - Managed Cluster이므로 charges per time, 사용자가 Operate knowledge가 있어야 사용 가능.
- AWS DMS -> Migrate Database to a Cloud 목적으로 사용 가능한 서비스. source DB는 up and running 유지한 채로 Migration이 가능하다.
- AWS Data Exchange -> Data analytics service that provides data catalogs, useful for integrating 3rd part data into a data lake for further analysis.

Kinesis 계열 서비스가 큰 틀에서 목적에는 부합하는 편. Designed to ingest large amounts of small bits of data.
- Kinesis Data Analytics: real-time processing에 적합. data transformation, aggregation, filtering, cleaning... 등등 manipulation 관련한 모든 정보.
  - Designed to transform / analyze streaming data in real time with Apache Flink.
  - reduces the complexity of building / managing / integrating Apache Flink applications with other AWS service.
  - Managed Service: scales automatically to match the volume and throughput.
- Kinesis Data Firehose
  - Designed for reliably load streaming data into data lakes, data stores, and analytics services.
  - capture, transform, deliver streaming data to AWS S3, Redshift, ES, generic HTTP endpoints, service providers (datadog, new Relic, MongoDB, Splunk...)
  - Fully managed service - automate scaling to match the throughput of your data
    - batch, compress, transform, encrypt your data streams before loading -> minimize amount of storage & increase security
  - Stream과 비교했을 때 convenience over control. latency는 Data stream 대비 확연히 길다.
    - send batch internval to 60 sec if you want to receive new data within 60 sec of sending it to your delivery stream.
- Kinesis Data Streams
  - Designed for continuously capture GB of data per second from hundreds of thousands of sources. (clickstream, DB event stream, financial transaction, social media feeds, IT logs, location-tracking events.)
  - collect 후 ms 단위로 available 가능 - real time anayltics에 사용할 수 있다. firehose보다 lower latency 지원.
  - requires writing additional code, both producer and consumer.
  - 

추가로 customer에게 확인한 결과, clickstream 데이터는 async processing이므로 latency가 중요 요건이 아님. 따라서 이 경우 Firehose가 더 나은 선택지.
<br>

Kinesis 앞단에 서비스를 하나 더 추가하는 게 필요하다.
- 사용자 요구사항에서 JS Library를 사용해 data ingest를 한다고 했는데, kinesis API는 HTTP Post 방식을 직접 지원하지 않음. 따라서 request proxy가 필요함
  - API gateway: Sends data out to Kinesis Stream 으로 service integration이 가능함.
  - API gateway 자체가 data ingestion 기능을 하는 건 아니지만, 사용자 요구사항을 맞추기 위한 HTTP proxy 역할.


##### Exploring AWS Kinesis service

<img width="945" alt="스크린샷 2023-06-03 오후 1 54 48" src="https://github.com/inspirit941/inspirit941/assets/26548454/226fa3e3-059f-4609-ab38-56c86914ca3f">
<img width="952" alt="스크린샷 2023-06-03 오후 1 55 38" src="https://github.com/inspirit941/inspirit941/assets/26548454/4a5e2d9b-abf9-4292-9d09-217cd72767e7">

Firehose 생성 화면을 보면 Source / Destination을 선택할 수 있게 되어 있음.
- Source를 보면 AWS Kinesis Data Stream을 선택할 수 있다. 즉 하나의 data stream을 다른 data stream으로 전달하는 것이 가능함

<img width="957" alt="스크린샷 2023-06-03 오후 1 57 19" src="https://github.com/inspirit941/inspirit941/assets/26548454/d23800a8-8c9d-4ba3-9f57-de1f2477289a">
<img width="950" alt="스크린샷 2023-06-03 오후 1 59 13" src="https://github.com/inspirit941/inspirit941/assets/26548454/001f66b8-fe96-422c-b992-d0ff07dccc3b">
<br>

API Gateway로 들어오는 데이터이므로 Source로는 Direct Put을 선택하고, Destination으로 S3를 선택한다.
- Destination Setting에서 S3 bucket을 선택하고, 여러 configuration을 진행하면 된다. prefix 같은.
- 생성하고 나면 Cloudwatch monitoring / Data transformation by Lambda 등을 세팅할 수 있음.

#### Accessing the Ingested Data

S3에 저장된 데이터에 접근하고, 필요한 작업을 수행하기 위한 서비스 후보군은 아래와 같다.
- AWS S3 Select: S3의 기능 중 하나. SQL로 filter contents of S3 Objects.
  - only query one file per query (one file at a time.)
- AWS Glue / AWS EMR: for processing unstructured Data using big data frameworks. 서비스 사용을 위한 learning curve가 있음
  - converting data format, performing data aggresgation, using AI / ML when processing data.
- AWS Athena: interactive query service that makes it easy to analyze data in S3 using SQL.
  - managed, serverless.

<br>
<img width="943" alt="스크린샷 2023-06-03 오후 2 59 51" src="https://github.com/inspirit941/inspirit941/assets/26548454/162b0b4d-29e5-4469-8c53-d6f18eeff365">
<img width="949" alt="스크린샷 2023-06-03 오후 3 01 59" src="https://github.com/inspirit941/inspirit941/assets/26548454/a8ef49ac-ad8d-4d38-9ed0-fba172d11fb1">
<Br>

AWS Athena 추가설명
- it Does not make a copy of your data. Athena 테이블을 만드려면, 조죄할 S3 bucket prefix를 지정해야 한다.
  - SQL에서 create table할 때 EXTERNAL 키워드를 쓰는 이유. Location으로 s3 domain 주소를 확인할 수 있다.
  - S3에 저장된 테이블 형식과 일치해야 함. 예컨대 S3에 csv 파일이 있고 column name이 지정돼 있다면, Athena의 create table 명령어에도 해당 structure가 있어야 한다.

<img width="953" alt="스크린샷 2023-06-03 오후 3 03 31" src="https://github.com/inspirit941/inspirit941/assets/26548454/460ca4b7-b016-4f43-a35e-f8dc1436ceb2">
<br>

여러 개의 Athena 테이블을 만들어두고 join해서 쓸 수도 있다. 각각의 테이블은 서로 다른 S3 bucket을 보고 있어도 됨.
- S3에 데이터가 있고, Table Schema와 실제 데이터가 일치하기만 하면 된다
  - 예컨대 S3 데이터가 csv라면 Query도 csv처럼, json 형태라면 json 쿼리하는 식으로 만들면 됨.

사용자에 따르면 JS library로 수집하는 데이터 포맷은 Json. Athena 사용할 때 특수한 serializer / Deserializer 쓸 필요 없는 상황.

<img width="937" alt="스크린샷 2023-06-03 오후 3 10 14" src="https://github.com/inspirit941/inspirit941/assets/26548454/9bf84b0f-bf04-44ad-8f7f-b32a81bf5b73">
<br>

Athena Web brower 예시. S3에 저장된 CSV 파일을 확인하고, SQL 쿼리로 조회할 수 있다.


#### Visualizing Data

For BI / Data Analytics.
- AWS CloudWatch: 대시보드 지원. real-time resource monitoring을 지원하지만, **Operational metric 수집 목적**임. 이상치 탐지 정도에 쓸 수는 있지만, Not intended to be used for BI.
- AWS OpenSearch Service: 대시보드 지원. Apache 오픈소스 기반 search / analytics.
  - 단, 서비스 사용을 위해 클러스터를 발급받으면 processing power / storage가 부여됨.
  - 예시의 경우 storage와 processing을 분리하기 위해 S3와 Athena를 도입한 상황. 굳이 BI 목적만을 위해 중복되는 리소스를 발급받아 쓸 이유는 없음
- AWS Managed Grafana: time-series data 시각화에 매우 유용함. 
  - Grafana의 사용예시가 대부분 Operational Metric monitoring이지만, clickstream도 timestamp 기반 데이터.
- AWS QuickSight: Data visualization service with Other AWS Service.
  - serverless + pay-per-use pricing model.
  - native AWS Service Integrations with built-in Security

목적 달성할 수 있는 서비스가 2개 이상이니까, 비슷한 서비스를 이미 customer가 쓰고 있는지 확인해보자. 쓰고 있는 게 있다면 그걸 도입하는 편이 나음
- 강의 예시에서는 QuickSight를 선택.

##### AWS QuickSight Features

![2G2G_jcsQyCkvCkUtyScGQ_d7c3c30b82bd4adea527841a67022ff1_Reading2 4A](https://github.com/inspirit941/inspirit941/assets/26548454/13f0b8c5-6eea-4b25-bed5-c08c1dfe71f0)
<br>

대략 이런 형태의 대시보드를 지원하는 서비스.
- Connect & Scale all your data
  - support all data in AWS / 3rd party cloud service provider / on premise as Well
  - use SPICE in-memory storage to scale data exploration to thousands of users
  - combine data from multiple sources / create complex data models for governed data sharing.
- Build customizable dashboards
  - deliver customized email reports and alerts to end users
  - access information from virtually anywhere, by using QuickSight access for iOS, Andriod, mobile Web
- ML integrations for insight
  - Anomaly Detection 지원
  - Forecast business metrics / perform interactive what-if analysis
  - Customize auto-narratives and weave them into dashboards to provide deeper context for users.
- Enable self-service BI for everyone.
  - web 기반 authoring interface로 시각화 가능
  - Embed quicksight capabilities in applications for data-driven UX
- Native Integration with AWS
  - VPC connectivity for secure AWS access to AWS Redshift, Snowflake, Exasol, AWS RDS...
  - AWS IAM permission for S3, Athena
  - SageMaker integration to incorporate ML models without complex data pipelines.
- Managed, Serverless Service. Pay-by-Usage
  - autoscale 지원 by SPICE in-memory DB
  - consistent, fast-response times for end users
  - pay-per-session으로 actual usage에만 과금. large-scale BI나 Embedded analytics의 라이센스 비용 낼 필요 없음
- Built-in Security / Governance / Compliance
  - end-to-end data encryption, encryption at rest for data in SPICE
  - row-level, column-level security with API suport for control at the user or group level.


### Solution Overview

Final Architecture

<img width="938" alt="스크린샷 2023-06-03 오후 3 21 51" src="https://github.com/inspirit941/inspirit941/assets/26548454/237b79a6-2a09-4092-906f-41eb08a2181e">
<br>

- HTTPS Endpoint: API Gateway + Kinesis Data Firehose.
  - kinesis endpoint 자체는 외부로 노출시키지 않음
  - Custom domain name, own SSL Certificate.
- Data Storage: S3
  - Detach from any processing / computing / visualization layer.
- Data Anaylize: Athena
  - regular SQL Query on the table.
- Data Visualization: QuickSight

Q. What if data format is misconfigured? (wrong format?)
- Kinesis Firehose에서 data manipulation 적용 가능 / Bucket Action (S3에 putObject될 때마다 Lambda 실행)
  - kinesis firehose 작업 결과 S3에 file 형태로 데이터를 저장할 때만 lambda가 실행된다.
  - 데이터 원본에 lambda 붙여서 직접 수정하는 대신, 수정된 데이터는 other bucket으로 저장하는 방식을 많이 사용함


#### Architecture Optimization

<img width="954" alt="스크린샷 2023-06-03 오후 3 44 18" src="https://github.com/inspirit941/inspirit941/assets/26548454/7b62ee72-6c9d-4957-9e5b-3fe0b44a8d9b">
<br>

Out-ot-scope까지 포함한 서비스 전체 흐름도는 위 사진과 같음. out of scope에서의 보완점이라면
- Admin에서 QR Code 생성하는 로직 - Serverless로 전환.
- Bucket이 두 개 (데이터 분석용, 레스토랑 메뉴 serving용)
  - CloudFront로 CDN 수행 - deliver cost 감소, faster
- API Gateway 걷어내고 AWS Cognito 도입.
  - Authorization을 위한 identity pool 제공. Authorization workflows with Cognito.
  - workflow integration이 가능하지만, 이 경우 JS Library 소스코드 변경이 필요
  - Authenticate 완료되면, JS에서 AWS SDK 사용해서 직접 Kinesis API를 쏘는 식으로 변경할 수 있다. API gateway 유지비용 절감
- Entire Solution을 CloudFormation으로 만든다. 다른 AWS account로도 동일한 세팅을 할 수 있도록
  - for governance.
    - separate billing per account
    - reduce manual mistakes
- 현재 구조는 client code에서 retry 로직을 넣어야 함.
  - JS library -> API gateway로 요청을 보낼 때 gateway 쪽 이슈가 있다면, retry 로직 시행 주기를 점차 줄여야 함. (retry - retry less. Exponential Backoff)
  - AWS Javascript SDK에서 built-in.
- S3에 데이터 저장할 때 보다 Athena-friendly하게 format.
  - csv, json -> Apache Parquet. faster / cheaper query가 가능함



