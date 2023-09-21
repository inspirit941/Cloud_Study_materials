### 1.

> A company will host a static website within an Amazon S3 bucket. The website will serve millions of users globally, and the company wants to minimize data transfer costs. What should a solutions architect do to ensure costs are kept to a minimum?

Create an Amazon CloudFront distribution, with the S3 bucket as the origin server.
- The use of CloudFront can be more cost-effective if your users access your objects frequently. At higher usage, the cost for CloudFront data transfer to the internet is lower than the cost for Amazon S3 data transfer to the internet. In addition, downloads are faster with CloudFront than with Amazon S3 alone because your objects are stored closer to your users.

### 2.

> A solutions architect needs to design a secure environment for AWS resources that are being deployed to Amazon EC2 instances in a VPC. The solution should support a three-tier architecture that consists of web servers, application servers, and a database cluster. The VPC needs to allow resources in the web tier to be accessible from the internet with only the HTTPS protocol. Which combination of actions would meet these requirements? (Select TWO.)

Attach an internet gateway to the VPC. Create public subnets for the web tier. Create private subnets for the application and database tiers.
- Only the web tier needs to be in public subnets. The application and database tiers should be in private subnets.For more information about public and private subnets, see

Create a web server security group that allows HTTPS requests from the internet. Create an application server security group that allows requests from the web security group only. Create a database cluster security group that allows TCP connections from the application security group on the database port only.
- Making the web tier public subnets allows for greater access to the resource while protecting it from traffic on unrequired ports. Restricting traffic to the application and database tiers protects it from accidental and malicious access and ensures that each tier is accessed only through secure communication with the previous tier.


### 3.

> A solutions architect notices an abnormal amount of network traffic coming from an Amazon EC2 instance. The traffic is determined to be malicious, and the destination needs to be determined. What tool can the solutions architect use to identify the destination of the malicious network traffic?

Turn on VPC Flow Logs and filter the logs
- VPC Flow Logs is a feature that gives you the ability to capture information about the IP traffic that goes to and from network interfaces in a VPC.


내가 고른 오답
- Turn on AWS CloudTrail and filter the logs
  - CloudTrail monitors action taken by an IAM user, an IAM role, or an AWS service through API calls. However, CloudTrail does not provide the monitoring of the destination of network communication.


### 4.

> A SysOps administrator wants to automate the deployment of new SSL/TLS certificates to web servers. The administrator wants a centralized way to keep track and manage the deployed certificates. Which AWS service can the administrator use to meet these requirements?

AWS Certificate Manager (ACM)
- ACM is a service that gives you the ability to provision, manage, and deploy public and private SSL/TLS certificates for use with AWS services and your internal connected resources. SSL/TLS certificates are used to secure network communications and establish the identity of websites over the internet and resources on private networks. ACM removes the time-consuming manual process of purchasing, uploading, and renewing SSL/TLS certificates.


### 5.

> A solution architect must create a data store location that will be able to handle different file formats of unknown sizes. The data must be highly available and protected from being accidentally deleted. What solution meets the requirements and is the MOST cost-effective?

Deploy an Amazon S3 bucket and enable object versioning.
- Versioning-enabled buckets can help you recover objects from accidental deletion or overwrite. For example, if you delete an object, Amazon S3 inserts a delete marker instead ofremoving the object permanently. The delete marker becomes the current object version. If you overwrite an object, you get a new object version in the bucket. You can restore the previous version. 


### 6.

> A company is migrating its on-premises application to AWS and refactoring the application's design. The design will consist of frontend Amazon EC2 instances that receive requests, backend EC2 instances that process the requests, and a message-queuing service that addresses decoupling the application. A solutions architect has been informed that a key aspect of the application is that requests are processed in the order in which they are received. Which AWS service should the solutions architect use to decouple the application?


Amazon Simple Queue Service (Amazon SQS) FIFO queue
- Amazon SQS FIFO queues process messages in the order they are received.

### 7. 

> A gaming company is experiencing exponential growth. On multiple occasions, customers have been unable to access resources. To keep up with the increased demand, management is considering deploying a cloud-based solution. The company wants a solution that can match on-premises resilience of multiple data centers and robust enough to withstand the increased growth activity. Which configuration should a solutions architect implement to meet these requirements?

A VPC that is configured with an Elastic Load Balancing (ELB) Network Load Balancer that targets an Amazon EC2 Auto Scaling group consisting of Amazon EC2 instances that span two Availability Zones.
- The ELB Network Load Balancer is capable of handling millions of requests per second while maintaining ultra-low latency. Combined with an Auto Scaling group, the network ELB can handle volatile traffic patterns. Setting the Auto Scaling group targets across multiple AZs will make this solution highly available.

내가 고른 오답
- A VPC that is configured with an Elastic Load Balancing (ELB) Application Load Balancer that targets an Amazon EC2 Auto Scaling group consisting of Amazon EC2 instances that span two AWS Regions.
  - The targets for Application Load Balancers must be within a single Region.


### 8.

> A company is deploying a production portal application on AWS. The database tier runs on a MySQL database. The company requires a highly available database solution that maximizes ease of management. How can the company meet these requirements?

Use Amazon RDS with a Multi-AZ deployment. Schedule periodic database snapshots
- Amazon RDS with a Multi-AZ deployment provides automatic failover with minimum manual intervention and is highly available.


### 9.

> A company requires operating system permission on a relational database server. What should a solutions architect suggest as a configuration for a highly available database architecture?

Multiple Amazon EC2 instances in a database replication configuration that uses two Availability Zones


### 10.

> A solutions architect must create a disaster recovery (DR) solution for a company's business-critical applications. The DR site must reside in a different AWS Region than the primary site. The solution requires a recovery point objective (RPO) in seconds and a recovery time objective (RTO) in minutes. The solution also requires the deployment of a completely functional but scaled-down version of the applications. Which DR strategy will meet these requirements?


Warm Standby
- With warm standby fully working at low capacity, all components run at a low capacity. The RPO is in seconds, and the RTO is in minutes. For more information about the various DR strategies, see Plan for Disaster Recovery (DR).

### 11. 

> A financial services company is migrating its multi-tier web application to AWS. The application architecture consists of a fleet of web servers, application servers, and an Oracle database. The company must have full control over the database's underlying operating system. The database must be highly available. Which approach should a solutions architect use for the database tier to meet these requirements?

Migrate to Amazon EC2 instances in two Availability Zones. Install Oracle and configure the instances to operate as a cluster.
- This solution provides the company with full control of the database operating system. The solution also provides high availability.


### 12.

> A company used Amazon EC2 Spot Instances for a demonstration that is now complete. A solutions architect must remove the Spot Instances to stop them from incurring cost. What should the solutions architect do to meet this requirement?

Cancel the Spot request. Terminate the Spot Instances. (서순이 중요)
- To remove the Spot Instances, the appropriate steps are to cancel the Spot request and then to terminate the Spot Instances.

### 13.

> A company is deploying an environment for a new data processing application. The application will be frequently accessed by 20 different departments across the globe seeking to run analytics. The company plans to charge each department for the cost of that department's access. Which solution will meet these requirements with the LEAST effort?

Amazon Athena with workgroups set up for each department. Each department will query through the workgroup tagged for their department in the billing console.
- Athena gives you the ability to make data queries in Amazon S3. Workgroups are purpose-built for cost allocation.


### 14. 

> After reviewing the cost optimization checks in AWS Trusted Advisor, a team finds that it has 10,000 Amazon Elastic Block Store (Amazon EBS) snapshots in its account that are more than 30 days old. The team has determined that it needs to implement better governance for the lifecycle of its resources. Which actions should the team take to automate the lifecycle management of the EBS snapshots with the LEAST effort? (Select TWO.)


Create and schedule a backup plan with AWS Backup.
- Correct. The team wants to automate the lifecycle management of EBS snapshots. AWS Backup is a centralized backup service that automates backup processes for application data across AWS services in the AWS Cloud, helping you meet business and regulatory backup compliance requirements. AWS Backup provides a central place where you can configure and audit the AWS resources you want to back up, automate backup scheduling, set retention policies, and monitor all recent backup and restore activity.

Use Amazon Data Lifecycle Manager.
- Correct. With Amazon Data Lifecycle Manager, you can manage the lifecycle of your AWS resources through lifecycle policies. Lifecycle policies automate operations on specified resources. The team requires lifecycle management for EBS snapshots. Amazon Data Lifecycle Manager supports EBS volumes and snapshots

### 15.

> A company is using an Amazon S3 bucket to store archived data for audits. The company needs long-term storage for the data. The data is rarely accessed and must be available for retrieval the next business day. After a quarterly review, the company wants to reduce the storage cost for the S3 bucket. A solutions architect must recommend the most cost-effective solution to store the archived data. Which solution will meet these requirements?

Store the data in S3 Glacier Flexible Retrieval.
- Of these options, S3 Glacier Flexible Retrieval is the most cost-effective solution. S3 Glacier Flexible Retrieval is an ideal fit for archival data that does not need to be frequently accessed or modified.


### 16. 

> A prediction process requires access to a trained model that is stored in an Amazon S3 bucket. The process takes a few seconds to process an image and make a prediction. The process is not overly resource-intensive, does not require any specialized hardware, and takes less than 512 MB of memory to run. What is the MOST cost-effective compute solution for this use case?

AWS Lambda functions

### 17.

> A hospital is migrating from another cloud provider to AWS and wants to modernize as they migrate. The hospital has containerized applications that run on tablets. During spikes caused by increases in patient visits, the communications from the applications to the central database occasionally fail. As a result, the hospital currently has the applications try to write to the central database once. If that write fails, the application writes to a dedicated application PostgreSQL database run by the hospital IT team on premises. Each of the PostgreSQL databases then sends batch information to the central database. The hospital is asking for recommendations on migrating or refactoring the database write process to lower operational overhead. What should the solutions architect recommend? (Select TWO.)


Migrate the local databases to Amazon Aurora Serverless PostgreSQL-Compatible Edition.
- Correct. You can use PostgreSQL as a kind of messaging service (holding all of the data until the batch job runs), even though you can handle that task better with a queuing service. Moving to Aurora Serverless will lower overhead for running the database and is a valid solution.

Refactor the applications to use Amazon Simple Queue Service (Amazon SQS) and eliminate the local PostgreSQL databases.
- Correct. The hospital can decouple the messaging aspect of the application and eliminate the databases (which are effectively a workaround messaging service).

내가 선택한 오답
- Migrate the containerized applications to AWS Fargate.
  - Incorrect. The container system behind the application is not the issue. Instead, communication with the central database is the issue. This solution does not address the write process.


### 18.

> A company uses Amazon EC2 instances in a test environment. The company has optimized the instances for their current workload. The company uses the instances only during business hours. The company uses Compute Savings Plans and Spot Instances. The company must retain control over the compute resources. A solutions architect must recommend a solution to reduce costs associated with the EC2 instances in the test environment. Which solution will meet these requirements?

Create a time-based Amazon CloudWatch alarm action to start and stop the instances.
- A CloudWatch alarm action would give the company the ability to reduce the costs by turning off the instances during evenings and weekends.

내가 선택한 오답
- Use Reserved Instances in addition to the Compute Savings Plan and Spot Instances.
  - The company uses the instances only during business hours. Reserved Instances would add unnecessary cost to the solution.


### 19.

> A company is running its application in a single Region on Amazon EC2 with Amazon Elastic Block Store (Amazon EBS) and Amazon S3 as part of the storage design. What should be done to reduce data transfer costs?

Create an Amazon CloudFront distribution with Amazon S3 as the origin.
- The charges for data transfer from CloudFront to the internet are lower than charges for data transfer from Amazon S3 to the internet. Additionally, there is no charge for data transfer from an AWS origin such as Amazon S3 to any CloudFront edge location. Therefore, this solution would reduce data transfer costs.