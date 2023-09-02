## Ingesting the River

### Use the right tool for the job

Data categorizing: 필요할 때 원하는 데이터를 정확히 찾아내기 위해 필요함.
- 사용자의 access pattern에 따라 다름.
- Consider classifying data, according to the access pattern needed by the processing layer.

for auto-generated data (server log, IoT Device streaming)
- 일반적으로 unstructured data, comes in streaming.
- **Ingest** with AWS Kinesis
- **Store** in AWS S3
- **Catalog** with AWS Gloue
- **Process** with Lambda
- **Query** with AWS Athena

for operational data (inventory, sales, expense reports...)
- 일반적으로 comes in batches. visualize / statictics 수요가 많은 편.
- **Ingest** with API Gateway
- **Stores** in AWS S3
- **Catalog** with AWS Glue
- **Transport** to AWS ES, **Visualize** with Kibana

for human-generated data (소셜 미디어 피드, contact forms, call center audio...)
- accees pattern 분석에 많이 사용
- **Ingest** with AWS S3 SFTP or AppFlow
- **Store** in AWS S3
- **Catalog** with AWS Glue
- **Use** a service like AWS Comprehend.
  - NLP Processing Service


### Understanding Data Structure / When to Process Data

Structured Data: data that is eassy for a computer system to consume in its format, without further modification.
- RDBMS with schema, PK, FK, relations.

Real-time Data source가 많아지면서, transforming real-world data into insights as quick as possible 요구가 증가함.
- 예컨대 같은 IoT 디바이스라 해도
  - 온도 수집 -> 숫자 전송일 경우 (Semi) Structured Data.
  - video, audio 형태일 경우 unstructured.

Structured / Unstructured 여부는 Data Content에 따라 다르다. Data Format 문제가 아님.
- Format은 단순히 represent data 목적으로 선택된 것일 뿐임. 
  - 예컨대 csv는 plain text that contains a list of data. structured data와 잘 어울리지만, csv파일이 전부 structured data라고 단언할 수는 없다.

unstructured data handling에 사용할 수 있는 AWS 서비스는 **AWS EMR** / **AWS Glue**
- Data lake architecture에서 processing layer 가장 앞단에 위치, transform unstructured data into structured data.

일반적으로 데이터를 다룰 때 많이 쓰는 용어로 ETL이 있다. Extract, Transform, Load. <br>

Data Lake의 경우 ELT - Extract, Load, Transform - 라는 용어를 쓴다.
- 예컨대 수집하는 모든 형태의 데이터가 매우 귀중한 경우 (i.e. 우주 탐사선으로부터 받는 데이터) Classic ELT 개념이 적용됨. 일단 Extract & Load. 필요시 나중에 Transform한다

**EtLT라는 개념도 있음. Extract, minor transformation, Load, major Transformation**
- MRI나 X-ray 같은 형태의 의료정보일 경우, 데이터 수집 / 저장의 최초 단계에서는 PII (Personally identifiable information) 관련 규약을 해제한 채 먼저 저장한다.
- 일단 store. minor transformation (PII removal) 수행한 이후에 Load하는 식.
  - 필요시 개인정보 비식별화를 거쳐 Friendly Format (이미지 등) 으로 수정.
  - PII 관련 절차와 Friendly format 변환이 같은 Processing layer에서 수행되기 어려운 이유?
    - process에 필요한 서비스 종류가 다르고
    - process할 때, 굳이 불필요한 정보까지 추가할 이유는 없음. 일단 store / 필요한 정보만 processing input으로 쓴다.


### Data Streaming ingestion with Kinesis Services

![스크린샷 2023-08-30 오후 10 22 47](https://github.com/inspirit941/inspirit941/assets/26548454/da1fe50c-76f3-4949-9f99-46346f91ec2c)
<br>

Data producer와 Data consumer를 연결하는 Kinesis Data Stream 예시
- producer: IoT device, web server logs, clickstream logs
- consumer: EC2 Instance / Lambda Function
  - EC2: processing. Lambda: store in S3

Kinesis의 세 가지 특징
- Data Agnostic. 
  - XML, text, JSON, 기타 unstructured data 등 어떤 종류의 데이터라도 Kinesis SDK 사용하면 kinesis 내부에 저장됨
- Data Retention period / data consumption replay
  - kinesis에 저장된 데이터는 consumed or not 상관없이 kinesis에 Data Retention Period 기간 동안에는 저장되어 있다. default 값은 24시간.
  - multiple consumers can consume the same data at the same time. / consumer에서 fail 발생해도 동일한 데이터를 다시 input할 수 있음.
- Pull-based Mechanism
  - kinesis는 push-based 방식이 아니다. consumer가 kinesis와 통신하려면 Kinesis Client Library를 사용해서 Connection을 맺어야 함.
    - 일반적으로 kinesis에서 데이터를 가져오는 이유는 두 가지. 
      - place(store) to somewhere like S3.
        - 이 경우, kinesis Firehose를 사용하면 multiple destination으로 데이터 전달을 쉽게 할 수 있다.
      - performing real-time analysis.
        - 이 경우 AWS Lambda Functions을 권장. can invoke functions when new data is in the stream.
        - managed service 간 통신이므로 push-based처럼 동작할 수 있다.

real-time analytics로 lambda를 사용한다면 코드 작성이 필요하다.<br>

만약 코드 작성을 아예 안 하고 싶다면 Managed service인 **Kinesis Analytics**를 이용할 수 있다.
- SQL Query를 사용한 real-time process data가 가능.
- Apache Flink 사용해서 더 복잡한 analytics 가능.
- Two main Concepts: In-Application Streams, Data Pumps
  - streaming data handling을 위한 abstraction.

<img width="941" alt="스크린샷 2023-09-02 오후 12 08 35" src="https://github.com/inspirit941/inspirit941/assets/26548454/004a2c49-cef7-425a-bae8-23ab6e152326">
<br>


### Batch Data Ingestion With AWS Transfer Family / AWS Snow Family


On-Prem처럼 이미 어딘가에 저장되어 있는 데이터로 작업하거나, 데이터 생산량은 많지만 time-sensitive analysis가 필요하지 않은 경우에는 보통 Batch를 사용한다.
<br>

AWS Transfer Family
- serverless AWS Service that gives a file transfer endpoint.

만약 internet으로 batch 데이터를 전송하기 어려운 상황일 경우, AWS Snow Family를 사용할 수 있다.
- Snowcon Device (hardware) 
  - 8TB, 신청 후 next business day에 지급됨.
  - ruggedized, tamper-proof, dustproof, water-resistent device.
  - 10GB ethernet port 지원
  - OpsHub 라는 AWS 프로그램 활용해서 Snowcon device를 서버에 연결하고, 데이터 전송이 가능함
- Snowball device
  - Snowcon보다 more capacity가 필요할 경우 사용가능. 50TB per device.
  - capacity가 더 필요하면 여러 개의 snwoball device를 클러스터로 구성해서 쓰면 된다.
- AWS SnowMobile.
  - PB 단위 데이터 전송이 필요하면 AWS Sales Representative에 문의했을 때 제공됨. 일종의 data center on wheels.
  - 100PB per device. 규모에서 알 수 있듯, 이 정도가 되면 일반적인 data tranfer mechanism과 다름..

### Data Cataloging

Data Lake에 데이터가 적재되는 순간부터 Data transformation, processing, analytics 등 많은 작업의 history tracking이 가능해야 함. 
- Data Storage 용도로는 S3가 보편적으로 쓰이고 있으므로, Single Source of Truth 보장을 위한 Cataloging Service가 필요.

Data Cataloging 종류는 크게 두 가지.
- Comprehensive Data Catalog
  - contains information about All Ingested Data
  - 모든 데이터가 전부 저장된 General Database 느낌
- HCatalog (Hive Store catalog)
  - contains information about data assets that has been transformed / ready to be used with data processing services (Athena, EMR, others...)
  - processing service tool to get insights 느낌

보통 Data lake에는 둘 다 쓰인다. data asset 검색에는 Comprehensive Data Catalog을 쓰고, 검색에서 찾은 데이터를 추가로 query / discover할 때 HCatalog을 사용하는 식.

<img width="942" alt="스크린샷 2023-09-02 오후 1 11 27" src="https://github.com/inspirit941/inspirit941/assets/26548454/e89d78a3-b6a0-48b7-9e98-a3c7225daaab">
<br>

Comprehensive Data Catalog의 예시
- S3에 object가 저장되면 Lambda trigger가 실행된다.
- lambda
  - DynamoDB table에 object name / actual information을 저장한다.
  - index information in AWS Elasticsearch Services. used to search for specific assets.


HCatalog
- 일반적으로 AWS Glue databases / tables을 Glue Crawler 사용해서 구축한다.
- 이렇게 만든 table은 AWS Athena 또는 Standard Hive metastore catalog (Hadoop)을 사용하는 서비스에서 사용할 수 있다.
- Glue에서 만든 Table은 Athena에서 Query할 수 있다.

S3에 저장된 csv 파일을 Glue Crawler를 사용하면 자동으로 Table 생성해준다. Serialize / Deserialize (SerDe) 지원해주고, 생성된 Table은 Athena 사용해서 query가 가능함.



