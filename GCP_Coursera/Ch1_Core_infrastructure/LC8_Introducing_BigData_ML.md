# Introduction to Big Data / ML
Google은 Build, Maintain data and analytics system을 자동화했다.
Real time analytics / ML과 같은 몇 가지 Tool을 소개할 예정. 
It is intended to be simple + practical for you to embed in your applications.

---
## Google Cloud BigData platform

Google Cloud Big Data Solutions = Integrated Serverless Platforms. 즉, no need to worry about provisioning Compute instance to run this jobs. It is fully managed, and You just pay only for the resources you consume. 또한 Integrated이므로, GCP data services work together to help you create custom solutions.

가장 유명한 건 Apache Hadoop - 빅데이터 오픈소스 프레임워크. This is based on the MapReduce programming which google invented and published.
MapReduce model은 간단히 말해 one function (= map function) runs in parallel with a massive dataset to produce intermediate results. + another function (= reduce function) builds a final result set based on all intermediate results. Apache Hadoop / Spark / Hive / Pig 등등이 있다.

- Cloud Dataproc : fast, easy, managed way to run Apache stuff (하둡, 스파크, 하이브 등등). Hadoop Cluster만 요청하면, 90초 이내에 Compute Engine VM이 준비된다. Scale up / down도 용이하며, default config 말고도 customized 가능. Stackdriver로 monitoring할 수 있도록 지원한다.

하둡을 on-premise로 비싸게 설치하는 대신, Dataproc을 활용하면 only pay for HW resources used during the life of the cluster you create. Rate for pricing is based on the hours. It bills in one-second clock-time increments, subject to a one minute minimum billing.

앞에서 설명한 preemptive Engine을 활용하면 batch processing + 비용 절감도 가능하다.

데이터가 클러스터에 있으면, spark나 spark SQL로 데이터 마이닝을 수행하거나 MLib (Spark의 머신러닝 라이브러리) 사용도 가능함.

---
### Cloud Dataflow

Dataproc : when you have a data set of known size, or when you want to manage your cluster size yourself.
데이터가 실시간으로 쌓이거나 예측 불가능한 경우 DataFlow를 사용하면 좋다.

Unified programming model + managed service, it lets you develop and execute a big range of data processing patterns. (Extract, transforms, load batch computations and continuous computations)
데이터 pipeline build에도 사용할 수 있으며, batch / stream 상관없이 적용 가능

No need to spin up cluster / to size instances. It automates the management of whatever processing resources are required. 즉 resource management / performance optimization에 신경쓸 필요가 없어진다. 

Ex) Bigquery 형태로 데이터 source를 받고, transform을 거쳐 sink로 데이터를 만들어 cloud storage에 저장하는 pipeline을 생성했다고 할 때, Each step in the pipeline is elastically scaled. Launch / manage Cluster 작업이 필요없다. 

Use case는 상당히 많다. General purpose ETL tools (extract / transforms / load) 로도 사용될 수 있고, Fraud detection / financial service 등의 data analysis에도 유용하다.
Orchestrate other (external services 포함) services. Ex) personalizing gaming user experiences.

---
### BigQuery

만약 pipeline building같은 과정이 아니라, your data needs to run more in the way of exploring a vast sea of data라고 해 보자. 이 경우 ad-hoc SQL Queries on a massive data set같은 수요가 생긴다.
-> BigQuery 사용.
= Fully managed, 페타바이트 scale, low-cost analytics data warehouse.

No infrastructure to manage. So just focusing on analyzing data to find meaningful insights using familiar SQL and take advantage of our pay-as-you-go model.

BigQuery에 데이터를 넣는 건 간단하다. Cloud Storage / Cloud datastore 또는 stream it into BigQuery at up to 100,000 rows per second. 넣기만 하면, 테라바이트 단위의 SQL 연산도 가능하게 하는 processing power를 사용할 수 있다. Cloud Dataflow, Hadoop, Spark 등으로 read / write도 가능함.

스타트업에서 포츈지 선정기업까지 다양한 곳에서 BigQuery를 사용한다. 작은 곳은 free monthly quotas 한도 내에서 사용할 수 있고, 큰 곳에서는 seamless scale + 99.9 service level agreement 보장.

BigQuery에서는 데이터가 저장될 Region을 선택할 수 있다. 대신, 클러스터를 생성하거나 할 거 없이 그냥 해당 Region location에서 데이터셋을 만들면 된다.

BigQuery는 storage / computation을 구분한다. 따라서 query와 별도로, storage 비용도 내야 한다. 다른 서비스와 마찬가지로 BigQuery에서 사용자의 full control 조정이 가능하다. Sharing 권한을 누군가에게 줬다고 할 때, 그 사람의 performance가 내 cost에 영향을 미치진 않음. query를 만들고 사용한 사람이 돈 내는 시스템이다.

Long-time storage pricing = automatic discount for data residing in BigQuery for extended period of time. 90일 넘어가면 자동으로 drop the price.

---
### Cloud Pub/Sub, Cloud Datalab

(끊임없이 앃이는 데이터를 처리하는 느낌? 백준 문제 제출하는 queue를 생각하면 됨)

Pub/Sub = Messaging Service. Reliable / scalable foundation for stream analytics. Independent application에서 send / receive message 기능을 부여할 수 있다. Decoupled되어 있으므로, scale independently.

Pub = Publisher, Sub = Subscriber. 즉 Application은 Pub/sub으로 메세지를 publish할 수 있고, Subscriber는 그 메세지를 받을 수 있는 식이다. Receiving msg does not have to be synchronous. -> decoupling system이 가능한 이유.

It’s designed to provide ‘at least once’ delivery at low latency. ‘At least once’ means, small chances are some messages might be delivered more than once.

On-demand scalability to 1M msg per second and beyond. quota만 선택하면 된다.

구글 내부적으로 사용하는 시스템이기도 하다. It’s an important building block for applications where data arrives at high & unpredictable rates (IoT같은 경우). 
* Streaming Data를 사용할 경우, Cloud DataFlow + Pub/Sub is natural pairing.
* Pub/Sub는 GCP compute Platform과도 궁합이 좋다.
* can configure your subscribers to receive messages on a push or pull base. 즉 msg 도착 시 notification을 제공하거나, check for new msg at intervals

Cloud Datalab 

데이터 사이언스에서 많이 사용하는 lab project인 Jupyter -> web-based notebooks containing python code, can run interactively + view results.

Compute Engine VM에서 실행되며, 처음에 Region + VM type을 선택할 수 있다. Jupiter Python 환경을 세팅해주며, GCP service를 지원한다. 얘도 마찬가지로 Resource 사용비용만 내면 된다.
BigQuery, Compute Engine, Cloud Storage와 통합된 환경이기 때문에, authentication hassles.

Google Chart / Matplotlib 시각화가 가능함. 통계나 머신러닝 라이브러리 지원.

---
### Google Cloud ML platform


ML도 Cloud Service 형태로 제공. Pretained model + platform to generate your own tailored models. 텐서플로우.

Cloud TPU 제공. Upfront investment 대신 on-demand 형태.

GC ML Engine -> any type of data / any size ML model 생성을 돕는다. API 형태로도 제공.

- 데이터가 Structured data일 경우 
classification / regression, Recommendation, Anomaly Detection 등
- 데이터가 Unstrcutured data일 경우
Image / video analysis (identify damage shipment, identifying style, flagging content), text analysis (language identification, topic classification, sentiment analysis)

---
### ML APIs

1. Cloud Vision API -> understand the content of an image. (Classify image by category.), OCR 등
2. Speech API -> Audio to Text. 80여 개의 언어 지원.
3. NLP API -> syntax analysis, break down sentences of users into tokens, 형태소분석, relationships among the words. 감정분석도 가능.
4. Translation API -> 언어 자동인식 지원
5. Cloud Video Intelligence API -> annotate videos. (Identify key entities (usually nouns) within video, when it occurs… 즉, video content의 searchable, discoverable을 담당)




