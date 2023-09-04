## Processing Data in the Data Lake

### Data Prep and AWS Glue Jobs

Data Ingestion in raw format. 사용하고자 하는 목적에 맞게 data format을 정리하는 건 또 다른 일이다. 그래서 Data Prep이 필요하다.
<br>

Raw Source of Data의 특징
- Raw Data Shuld be immutable.
  - S3 offers 'Object Lock' to ensure data is not modified.
- Lifecycle Policies for cost optimization.
  - S3 offers Lifecycle tier management services.

data prep 과정에서 사용하는 데이터는
- Copy from Raw Source
- Processed data Saved in other S3 Location
- Analytics tools use data in other S3 Location

Dataprep을 위한 process 생성 방식
- Shaping
  - analytics에 필요한 데이터만 select, combining fields or files into one, or otherwise transforming / aggregating data in regards to its shape or schema.
- Blending Data
  - 제각기 다른 schema로 구성된 데이터를 데이터 분석 가능한 형태로 format match.
- Cleaning
  - missing values 채우기 / Conflicting 처리 / Normalizing the data

AWS에서 사용할 수 있는 Dataprep의 핵심은 Automation. 자동화 가능한 Managed AWS Service를 소개할 예정.
- AWS Glue Jobs: run scripts that transforms data based on triggers / on a schedule.
  - batch processing에 유용함.
- AWS Lambda: triggered as data is uploaded to your data lake.
  - triggers as data comes in. real-time data processing에 유용함.

AWS Glue의 세 가지 컴포넌트
- Glue Data Catalog
- Glue Crawler / Classifiers
- Glue Jobs

Glue Job
- Job은 ETL을 수행하는 Business Logic 단위를 의미함.
  - Specify Data Sources / Targets. Provide Job customization.
  - result: Generated Apache Spark API / PySpark Script.
  - Trigger or Schedule the job to run.
    - Extracts the data from the source, transforms data, loads it into the targets.


<img width="944" alt="스크린샷 2023-09-02 오후 2 04 01" src="https://github.com/inspirit941/inspirit941/assets/26548454/08455ab3-8d4d-407b-84f5-5e9f5bc028d4">
<br>

1. Select Source Tables: table must be defined in your data catalog. 일반적으로 Raw data befor transformation.
   1. Athena 등을 사용한다면, table can point to data sources like a DyanmoDB table, S3 bucket, or DB requires a JDBC connection.
2. Choose Data Target: transformed data가 어디로 Load될 것인지 선택. 이미 생성된 Table을 선택하거나 job에서 target table을 생성하도록 만들 수 있다.
3. Customize configuration for your jobs. -> 설정에 맞는 script를 생성하거나, script가 있는 S3 location을 명시할 수 있다.
   1. 예컨대 what type of job environment to run; Apache ETL script, Spark Streaming script, Python Shell script 등.
   2. Transformation type을 선택할 수 있다. source data의 schema 변경해서 new target dataset을 생성하거나, choose to find matching records.
   3. logging / monitoring requirements
4. AWS Glue가 생성한 Script를 추가로 edit할 수 있다.
   1. add things like transforms, or whatever PySpark code that you want to add.
   2. Glue에서는 built-in transforms을 몇 가지 제공함. dropping null fields / filtering records / joining dataset / mapping fields from source to targets...
5. Determine When you want to Run; Set a trigger or Schedule.


### File Optimization

some file optimization technique to to do better extracts performance / costs.  **columnar data formats**
- compression and splitting
- Athena Partitioning
<br>

![스크린샷 2023-09-02 오후 4 27 24](https://github.com/inspirit941/inspirit941/assets/26548454/0e875c9e-3b06-4193-bb3e-6d99480be681)
<br>

**예시: columnar data format.** <br>

데이터가 table format이고 id, name, age 정보를 담고 있는 csv 파일이라고 가정하자.
- csv는 row-oriented이므로, stored in disk organized by blocks per row.
- `select avg(age) from table` 을 수행해야 한다면, age라는 column의 모든 값을 확인해야 한다. 데이터는 row-oriented이기 때문에, column값을 확인하기 위해 여러 번의 disk I/O가 발생한다.

![스크린샷 2023-09-02 오후 3 52 00](https://github.com/inspirit941/inspirit941/assets/26548454/dbc4538a-3604-45b5-b287-7d90f8634bf5)
<br>

위 예시를 column-oriented (i.e. parquet) 로 변경할 경우
- 하나의 block에 특정 column 모든 데이터가 저장된다.
- `select avg(age) from table` 을 수행해야 한다면, age라는 column의 모든 값을 확인할 때 block 하나만 조회하면 된다. disk I/O가 감소한다.
  - 따라서 avg 조회 query의 속도가 row-oriented보다 Optimized.
- BigData Analysis / Data Lake Related Query의 경우 Extracting values from Entire Column이 많은 편... 성능 최적화에 유리한 편.

물론 column data format이 항상 더 나은 선택지인 건 아니다.
- row-based 방식은 하나의 entire row 조회에 특화되어 있고
- sorting / adding new entry가 자주 발생하는 구조에서 더 효율적으로 동작한다.

<br>

**Compression**
- 일반적으로 compression은 'data processing system의 메모리 사용량을 최적화할 수 있다' / 'bucket size 줄여서 비용 절약할 수 있다'. 
- 즉 Faster / Cheaper by Compression

**Data Partitioning**
- AWS Athena 사용할 경우 특히 중요한 기능.
- Athena는 TB scan 단위로 과금. 따라서 Query하기 전 appropriate format을 만들어두면 query faster / cheaper.

columnar format으로 데이터 세팅해두고 Athena로 Entire scan을 수행하면
- Athena는 내부적으로 Partial GET operation을 수행해서 특정 column이 있는 S3 Object만 조회한다.
- 이 방식이 scan fewer data / consuming less memory.

이전에 설명한 것처럼, Data Lake는 Schema-on-read 방식. Processing layer can adapt to the datset. cost / performance를 생각한다면 Dataprep 과정에서의 optimization은 꼭 필요하다.


### Introduction to Data Lake Security

Data Lake에 접근하려는 사용자마다 접근할 데이터 / 사용목적이 다르므로 different permission이 필요하다. Data Lake에 데이터를 전송하는 producer에게도 적절한 권한을 부여해야 할 필요가 있다.
- Data lake 접근 주체는 크게 셋. Data producer / Data consumer / Data Analytics tools.
- 이들의 Data Access Pattern을 파악하고, shape your security pattern around these patterns.
- Data Lake 자체에 Sensitive Data가 저장되어 있을 수 있음. 어떤 종류의 Compliance program을 준수해야 하는지.
  - creating / applying data access, protection, compliance policies.
  - 예컨대 PII (Personally Identifiable Information)이라면, 아무나 접근할 수 없도록 restrict access / Encrypt Data / keep audit logs who & when access the data

![스크린샷 2023-09-03 오후 3 11 10](https://github.com/inspirit941/inspirit941/assets/26548454/b09982ff-2d4a-4041-a350-726c72124f7b)
<br>

security 체크할 부분
- storage layer
- cataloging layer
- service layer that process / analyze data

각 AWS 서비스에서 Encryption in transit / Encryption at rest, Access Controls, IAM permissions 과 같은 설정을 확인하고 활성화하면 된다.

![스크린샷 2023-09-03 오후 4 16 24](https://github.com/inspirit941/inspirit941/assets/26548454/8600dd21-66f9-4587-adae-a82f69c65362)
<br>

AWS의 Shared Responsibility Model: Managed Service 사용하되, 사용자가 security 신경써야 할 부분이 분명히 있다.
- AWS Responsibility: Security of the Cloud.
- User Responsibility: Security in the Cloud.

<BR>

Security for AWS S3. Take preemptive measures to protect data before you allow anyone access to data lake.
- Encrpytion
  - Enable **encryption at rest**. (Free feature)
  - Default encryption uses AES-256 keys.
  - S3에서 default로 제공하는 key를 사용하거나, custom key를 사용하거나, AWS KMS keys service를 사용할 수 있다.
- Security
  - S3 Bucket access policy - Restrict who can access your S3 bucket using granular controls.
  - does not set public by default.

Security for AWS Glue.
- AWS 에서 SSL encryption은 기본적으로 제공함. 따라서 다른 서비스와 AWS Glue 간 통신은 기본적으로 encrypted.
  - Enable **Encryption at rest** for the metadata
  - **use IAM Policy** that explicitly allow / deny actions to AWS Glue
    - scoping the permission accordingly in IAM
  - resource-based-policy를 추가로 적용할 수도 있다. 이것까지 추가한다면, IAM permission과 resource-based-policy 조건을 둘다 충족하는 user만 리소스에 접근 가능.

![스크린샷 2023-09-03 오후 4 29 31](https://github.com/inspirit941/inspirit941/assets/26548454/6f864873-8461-414b-9c27-1b3e54577973)

resource-based-policy 예시.

<br>

이외에도 각 AWS Service마다 설정할 수 있는 Security 범위와 방법이 있으므로, 맞춰서 진행하면 됨.
- Data lake related service들 대부분, 예컨대 AWS Athena / AWS Elasticsearch Service 도 resource-based-policy와 IAM based control access 두 가지를 지원함.

권장하는 security 원칙: Principle of Least Privilege.
- each entity only gets the access they need, and nothing more.

Access Auditing으로는
- S3 server access logs
- AWS Cloudtrails

## Data Visualization

### introduction to AWS QuickSight

![스크린샷 2023-09-03 오후 4 41 09](https://github.com/inspirit941/inspirit941/assets/26548454/7b393d55-1477-4e1e-885c-2839f2933140)
<br>

AWS의 Data visualization service.
1. connect to your data you want to analyze
2. (optional) fine-tuning data to optimize it for visualization layer
   1. calculation layer / apply filters to the data / change field names or data types
   2. SQL query 수행하기 위한 data preparation features to join tables 등
3. create data analysis; visual representation of the data (dashboards)
4. make better decisions

bar chart, time series graph, line graphs, scatter plots, heatmaps... 등 다양한 Visual Format 제공
- QuickSight는 data properties 확인해서 적절한 graph format을 찾아주는 autoGraph feature를 제공한다.

QuickSight만의 장점 / 특징
- seamless integration
  - S3 데이터뿐만 아니라 RedShift, AWS RDS 등과 연동
  - import csv / excel file 가능
  - SaaS Product (Salesforce) 또는 on-prem DB도 지원
  - AWS SageMaker (ML service) 연동 
    - Augment with sagemaker
    - select dataset, choose ML model, provide schema & other configuration, Run model
- scaling mechanisms
  - visualization에 사용할 데이터 크기가 얼마건 상관없이 scaling 지원. traditional BI tool 대비 특장점.
- ad-hoc transformation / analysis
  - 사용자가 원하는 형태의 visual representation을 그때그때 지원 가능.
- **SPICE**: feature that allows you to speed up analysis
  - Super-fast, Parallel, In-memory Calculation Engine
  - designed for advance calculation / server data quickly. storage / processing capacity available.

### Registry of Open Data on AWS

public data you can use to try out some of techniques.
- AWS resources에 사용 가능한 데이터셋을 제공함.
- lowers cost of research

