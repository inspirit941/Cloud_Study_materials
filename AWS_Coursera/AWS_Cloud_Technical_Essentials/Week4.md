## Monitoring & Optimization

<img width="1059" alt="스크린샷 2023-04-30 오후 3 35 36" src="https://user-images.githubusercontent.com/26548454/235339378-1d478891-08e3-4cef-a9ea-ee0e1cf0bb8b.png">
<br>

애플리케이션은 실행 과정에서 "Metric" 이라고 부르는 data point를 생성한다. CPU utilization, network flows...
- Statistics: Metrics that are monitored over time.

이렇게 수집한 데이터는 일종의 baseline이 되어, application이 정상적으로 동작하는지 여부를 체크할 수 있는 기준점이 된다. 애플리케이션의 staticstics가 baseline을 벗어날 경우 자동으로 alert하는 것.
<br>

AWS CloudWatch: Monitoring solution all-in-one place.
- AWS에서 동작하는 cloud-based infrastructures / solutions의 metrics 수집.
- AWS service는 리소스 생성 시 자동으로 cloudwatch에 metric을 전송하도록 되어 있음.

Dashboard: customizable page in the console that you can use to monitor your different types of resources in a single view.
- different region이어도 조회 가능.
- application의 health 여부를 종합적으로 체크하려면 custom metric 정의해서 쓰는 것을 권장한다.


<img width="1071" alt="스크린샷 2023-04-30 오후 4 21 27" src="https://user-images.githubusercontent.com/26548454/235340983-e0f19c48-89eb-4f07-9c1d-8a8931c22aa3.png">
<br>

Alarms: create threshold for the metrics you're monitoring, and send alarm if a metric crosses a boundary for a period of time.
- alarm 발생 시 automated actions 수행하도록 설정 가능

아래 예시는 cpu utilization이 70% 이상인 상태가 5분 이상 지속될 경우 알림을 보내도록 설정한 것.

<img width="1062" alt="스크린샷 2023-04-30 오후 4 22 23" src="https://user-images.githubusercontent.com/26548454/235341010-30aafb6b-1eed-4884-afc0-ae57c93e1f69.png">
<img width="1073" alt="스크린샷 2023-04-30 오후 4 24 10" src="https://user-images.githubusercontent.com/26548454/235341074-ed9ada70-b55a-46d0-bd92-a714dee70d71.png">

alarm 발생 시 어떤 동작을 수행할 것인지 결정할 수 있다.
- alarm 자체는 3개의 state를 가지고 있음. in-alarm, OK, insufficient data. action은 state가 변경될 때 발생한다.
- 예시의 경우 OK -> in-alarm으로 변경될 경우 action을 수행하도록 설정함.
  - AWS SNS를 사용해서 topic 생성 -> topic subscriber에게 메시지를 보낼 수 있도록 설정할 수 있다.
  - action 종류는 다양함.

<br>

Many AWS services send metrics automatically for **free to CloudWatch at a rate of one data point per metric per 5-minute interval**, without you needing to do anything to turn on that data collection. 
- This by itself gives you visibility into your systems without you needing to spend any extra money to do so. This is known as basic monitoring. For many applications, basic monitoring does the job.   

For applications running on EC2 instances, you can get more granularity by posting metrics every minute instead of every 5 minutes using a feature like **detailed monitoring.**
- Detailed monitoring has an extra fee associated. You can read about pricing on the CloudWatch Pricing Page linked in the resources section of this unit.

<br>

**Break Down Metrics**
<br>

Each metric in CloudWatch has a timestamp and is organized into containers called **namespaces**. 
- Metrics in different namespaces are isolated from each other—you can think of them as belonging to different categories.  

AWS services that send data to CloudWatch attach **dimensions** to each metric. 
- A dimension is a name/value pair that is part of the metric’s identity. 
- You can use dimensions to filter the results that CloudWatch returns. 
- For example, you can get statistics for a specific EC2 instance by specifying the InstanceId dimension when you search.

### Cloudwatch Logs

CloudWatch can also be the centralized place for logs to be stored and analyzed, using CloudWatch Logs. CloudWatch Logs can monitor, store, and access your log files from applications running on Amazon EC2 instances, AWS Lambda functions, and other sources.  

- allows you to query and filter your log data. 
  - 에러 발생 시 stacktrace id 기반으로 로그 조회 가능.
  - You also set up metric filters on logs, which turn log data into numerical CloudWatch metrics that you graph and use on your dashboards.  
- Lambda처럼 IAM 권한관리만 잘 설정하면 별다른 설정 없이도 CloudWatch Logs가 적용되는 서비스도 있는 반면, 설정이 필요한 서비스도 있다.
  - EC2에 cloudwatch Logs를 설치하려면, 해당 인스턴스에 Cloudwatch Logs Agent의 install / configure 작업이 선행되어야 한다.

The CloudWatch Logs agent enables Amazon EC2 instances to automatically send log data to CloudWatch Logs. The agent includes the following components.
- A plug-in to the AWS Command Line Interface (CLI) that pushes log data to CloudWatch Logs.
- A script that initiates the process to push data to CloudWatch Logs.
- A cron job that ensures the daemon is always running.

After the agent is installed and configured, you can then view your application logs in CloudWatch Logs. 

#### Learn the CloudWatch Logs Terminology
Log data sent to CloudWatch Logs can come from different sources, so it’s important you understand how they’re organized and the terminology used to describe your logs.  
- Log event: A log event is a **record of activity** recorded by the application or resource being monitored, and it has a **timestamp and an event message.**  
- Log stream: Log events are then grouped into log streams, which are sequences of log events that all belong to the same resource being monitored. 
  - For example, logs for an EC2 instance are grouped together into a log stream that you can then filter or query for insights.  
- Log groups: Log streams are then organized into log groups. A log group is composed of log streams that all share the same retention and permissions settings. 
  - For example, if you have multiple EC2 instances hosting your application and you are sending application log data to CloudWatch Logs, you can group the log streams from each instance into one log group. This helps keep your logs organized.

### Optimizing solutions on AWS


capacity, performance, availability 등에서 문제가 발생할 경우 alarm 보내는 건 가능.
- 문제가 발생하지 않도록 prevent / respond automatically 할 수 있으면 더 좋다.

<br>
<img width="1060" alt="스크린샷 2023-04-30 오후 4 54 30" src="https://user-images.githubusercontent.com/26548454/235342230-4ec49063-4641-4dd5-b2f4-ae1806c30abd.png">
<br>

예컨대 위와 같은 서비스 구조라면
- S3와 DynamoDB는 이미 HA 보장하는 구조이므로 고려 X
- single EC2가 다운되면 서비스 접근 불가능. 
  - redundancy + Multi AZ로 해결
  - scalability - EC2 autoscaling으로 해결 가능. (horizontal)

<br>
<img width="1057" alt="스크린샷 2023-04-30 오후 5 00 40" src="https://user-images.githubusercontent.com/26548454/235342432-11927013-262d-43aa-a24f-e535b1433ae6.png">
<br>

horizontal scale 적용 시 발생하는 또다른 이슈: how to access those servers?
- Load balancer 사용해서 endpoint는 하나로 통일하고, 여러 인스턴스에 트래픽을 전달하는 식의 구조가 필요함.
- instance 하나에 public IP 붙여서 외부 접근을 허용할 필요가 없어짐



#### Availability?

typically expressed as a percentage of uptime in a given year or as a number of nines. 
- 일반적으로, availability를 높이는 방법은 redundancy 적용.
- more infrastructure needed; more server / infrastructure / datacenter. == higher cost


| Availability (%) | Downtime (per year) |
| --- | --- |
| 90% ("one nine") | 36.53 days |
| 99% ("two nines") | 3.65 days |
| 99.9% ("three nines") | 8.77 hours |
| 99.95% ("three and a half nines") | 4.38 hours |
| 99.99% ("four nines") | 52.60 minutes |
| 99.995% ("four and a half nines") | 26.30 minutes |
| 99.999% ("five nines") | 5.26 minutes |

#### Manage Replication, Redirection, and High Availability

Create a Process for Replication
- The first challenge is that you need to create a process to replicate the configuration files, software patches, and application itself across instances. The best method is to automate where you can.

Address Customer Redirection
- The second challenge is how to let the clients, the computers sending requests to your server, know about the different servers. 
- There are different tools that can be used here. 
  - Domain Name System (DNS) where the client uses one record which points to the IP address of all available servers. 
    - However, the time it takes to update that list of IP addresses and for the clients to become aware of such change, sometimes called propagation, is typically the reason why this method isn’t always used. 
  - Another option is to use a load balancer which takes care of health checks and distributing the load across each server. Being between the client and the server, the load balancer avoids propagation time issues. 

Understand the Types of High Availability
- The last challenge to address when having more than one server is the type of availability you need; either be an active-passive or an active-active system. 

- **Active-Passive**: With an active-passive system, only one of the two instances is available at a time. 
  - One advantage of this method is that for stateful applications where data about the client’s session is stored on the server, there won’t be any issues as the customers are always sent to the same server where their session is stored.
- **Active-Active**: A disadvantage of active-passive and where an active-active system shines is **scalability**. By having both servers available, the second server can take some load for the application, thus allowing the entire system to take more load. 
  - However, if the application is stateful, there would be an issue if the customer’s session isn’t available on both servers. **Stateless applications work better for active-active systems.**

### Route traffic with AWS ELB (Elastic Load Balancing)

<img width="1062" alt="스크린샷 2023-04-30 오후 5 08 32" src="https://user-images.githubusercontent.com/26548454/235342752-f463231e-be97-47c1-9f1c-9bd8a8be96b8.png">
<br>

- client browser에서 ELB로 요청 전달
- ELB가 어떤 Instance로 트래픽을 전달할 것인지 결정
- instance의 응답을 받아서 browser로 응답.

구조만 보면 ELB가 SPOF 같지만, ELB 서비스는 구조적으로 High availability / Scalability를 보장하는 Regional Service.
- AZ별로 ELB 구축할 필요 없음.
- throughput 감당할 수 있도록 알아서 autoscale.

<br>
<img width="1053" alt="스크린샷 2023-04-30 오후 5 10 49" src="https://user-images.githubusercontent.com/26548454/235342816-739d7b10-3482-4c88-a226-62e03573e940.png">
<br>

ELB에서 지원하는 로드밸런서는 세 가지
- Application LB - Layer7 (http / https)
  - url path / http method / sourceIP 등 http protocol 기반 routing 가능
  - send response directly to client. 특정 요청의 경우 백엔드 서버로 보내지 않고 바로 응답 줄 수 있음.
  - TLS offloading / sticky session 지원
  - Authenticate user 가능
  - secure traffic
  - round-robin routing / least-outstanding request routing 알고리즘 적용 가능
- Network LB - Layer4 (tcp / udp / tls)
  - flow hash routing 방식 사용 - protocol / sourceIP & port / destinationIP & port / tcp sequential number 전부 동일할 경우 동일한 Target으로 전달.
  - sticky session / tls offloading 지원
  - ALB보다 안정적으로 수백만 request/sec 지원 가능. ALB는 scaling 시차가 일부 있다.
  - static / elastic ip주소 지원. (LB를 dns로 호출하는 대신 IP로 호출)
  - preserves sourceIP. ALB를 통과한 request의 sourceIP는 load balancer의 ip이지만 NLB에서 조회한 sourceIP는 real client ip주소.
- Gateway LB - Layer3+4 (ip) mainly used to load balance requests to third party application

Here is the table in markdown format:

| Feature | Application Load Balancer | Network Load Balancer |
| --- | --- | --- |
| Protocols | HTTP, HTTPS | TCP, UDP, TLS |
| Connection draining (deregistration delay) | ✔ |  |
| IP addresses as targets | ✔ | ✔ |
| Static IP and Elastic IP address |  | ✔ |
| Preserve Source IP address |  | ✔ |
| Routing based on Source IP address, path, host, HTTP headers, HTTP method, and query string | ✔ |  |
| Redirects | ✔ |  |
| Fixed response | ✔ |  |
| User authentication | ✔ |  |

![i9pCEqt4SsCB_h-15irXaw_a37c73d64d7e4da1ab2055a798c5cef1_image](https://user-images.githubusercontent.com/26548454/235343917-4ec917cc-1e6d-412c-9546-4e3e4d7ff6d4.png)
<br>

예시의 경우 http 트래픽이므로 ALB (application LB)를 사용하는 게 낫다. ALB 적용 시, 세 가지 컴포넌트를 생성해야 함
- Listener: check for request. 사용할 port + protocol 지정이 필수
  - 예컨대 애플리케이션이 80포트로 트래픽을 받으면, LB도 port 80을 Listen하고 있어야 함. https라면 443
- Target Group: 트래픽을 전달할 Target backend의 group. EC2 group / Lambda functions / IP address 등등
  - LB가 트래픽 routing할 때 필요한 정보인 health check가 있어야 한다.
- Rule: L7이라서 지원되는 기능 중 하나. Defines how your requests are routed to your targets.
  - Listener 자체에 default rule이 있고, 필요시 additional rule이 추가되는 형태

<img width="1051" alt="스크린샷 2023-04-30 오후 5 22 34" src="https://user-images.githubusercontent.com/26548454/235343243-b636e125-69ce-421e-99e6-fb75203a2ae0.png">
<br>

예컨대 위의 그림처럼, path가 /info 일 경우 특정 target group (B)로만 트래픽을 Routing 하는 것이 가능함

<br>

LB의 scheme는 두 가지가 있다.

<img width="1053" alt="스크린샷 2023-04-30 오후 5 31 49" src="https://user-images.githubusercontent.com/26548454/235343577-63ac0217-961c-41fc-9bb7-7ee814242315.png">
<br>

- Internet-facing: internet 트래픽을 backend server / targets로 routing
- Internal: client가 private IP로 보낸 요청을 받아서 backend / target으로 routing
  - 예컨대 3 tier (web / app / DB) 구조로 된 애플리케이션이라면, web tier에서 app tier로 요청을 전달하기 위해 internal LB을 사용할 수 있음

<br>
<img width="1022" alt="스크린샷 2023-04-30 오후 5 36 24" src="https://user-images.githubusercontent.com/26548454/235343772-08b1bece-6ceb-433b-b7d9-37f5775e7411.png">
<br>

Traffic Allow Policy로 Security Group을 적용할 수 있다.
- 80번 포트의 Incoming traffic을 Security Group에서 allow해야 트래픽을 받을 수 있고, LB를 수행할 수 있음.

Listeners and Routing에서 LB 설정이 가능.
- Target Group을 생성할 때 종류를 선택할 수 있다. EC2 / IP addressses / lambda functions...
- 이후, target Group에 포함될 리소스를 선택하면 됨.

<img width="1075" alt="스크린샷 2023-04-30 오후 5 38 48" src="https://user-images.githubusercontent.com/26548454/235343883-8975661f-28e8-40c9-afa0-2656dcc1e8bc.png">
<Br>

### EC2 Autoscaling

provision more capacity on demand, depending on different thresholds that we set. (threshold는 cloudwatch에서 정의할 수 있다)

![스크린샷 2023-04-30 오후 9 08 41](https://user-images.githubusercontent.com/26548454/235352129-158d378b-e1ae-440e-8d19-3138fc3c0abd.png)
![스크린샷 2023-04-30 오후 9 11 22](https://user-images.githubusercontent.com/26548454/235352260-b3cc675a-14a2-453d-9db7-967c5f5ccd78.png)
<br>

- EC2 instance는 autoscaling group으로 정의되어 있다. 각 인스턴스는 동일한 configuration.
- instance에 부하가 들어가면 cloudwatch에 metrics 전달
- 부하가 기준치를 초과하면, cloudwatch에서 new instance create 요청 전달
- ec2 인스턴스가 올라오면, ELB에서 healthCheck 후 트래픽 routing

<br>

![스크린샷 2023-04-30 오후 9 14 10](https://user-images.githubusercontent.com/26548454/235352370-5333c00a-a087-4bf6-8fcf-25a682f12a10.png)
![스크린샷 2023-04-30 오후 9 26 58](https://user-images.githubusercontent.com/26548454/235352955-312f5823-25f6-440d-b453-611c9d16d698.png)
<br>

autoscaling group을 생성하려면, EC2에서 launch template을 생성해야 함.
- Existing ec2 instance 옵션을 선택할 수 있다.
- instance type, Security group 설정

![스크린샷 2023-04-30 오후 9 29 02](https://user-images.githubusercontent.com/26548454/235353033-1cf5b87e-aae8-4817-a87c-40e25a0391f7.png)
![스크린샷 2023-04-30 오후 9 29 02](https://user-images.githubusercontent.com/26548454/235353035-2516cd8c-d083-4ca3-94b1-2a29398e829b.png)
<br>

advanced details에서 IAM policy를 선택하면, user data에 붙여넣을 수 있는 startup script를 제공해준다.
- ec2 Instance에 애플리케이션 코드 + dependency를 설치하고 실행할 수 있음.

<br>

![스크린샷 2023-04-30 오후 9 31 11](https://user-images.githubusercontent.com/26548454/235353124-cd01fa71-f948-4f0c-94bf-91512bcba55d.png)
<img width="1071" alt="스크린샷 2023-05-01 오전 10 33 11" src="https://user-images.githubusercontent.com/26548454/235388302-e3aeb73e-5971-4ac6-8670-1ecd7726923a.png">
<br>

autoscaling template 설정 시
- autoscale에 사용할 launch template 선택
- Security Group 설정 - vpc 선택, AZ 선택

<img width="1047" alt="스크린샷 2023-05-01 오전 10 41 00" src="https://user-images.githubusercontent.com/26548454/235388892-6238133f-6c9c-43d3-a468-f2decf252780.png">
<img width="1072" alt="스크린샷 2023-05-01 오전 10 44 17" src="https://user-images.githubusercontent.com/26548454/235389035-eb5e8bf6-5183-4034-9cc1-a41322e6350a.png">

- load balancer 선택 - attach 가능. target group 선택, health check 체크박스 선택
- cloudwatch alarm와 유사한 방식으로 policy 설정 가능
  - cloudwatch 예시에서는 cpu 사용량 %가 일정시간 이상 유지될 경우 알림이 메일로 오도록 했음
  - 여기서도 metric type별로, 특정 값이 일정시간 이상 지속될 경우 autoscale event 발생하도록 설정할 수 있다.
    - warm up time: until the instance's specified warm-up time has expired, the instance is not counted toward the aggregated metrics of the AutoScaling group.


![pVmtoRo0R2KIdGTo68hnWQ_d8a3718739a7477398aaff28f86847f1_image](https://user-images.githubusercontent.com/26548454/235389689-6f87d6eb-0fec-461d-8920-fa774afda087.png)
![Mw0CKJAzTg6PC8FtpAAlfw_aa974712ced74ca092f793c0e94a38f1_image](https://user-images.githubusercontent.com/26548454/235389751-a2f296b8-4eef-4640-8001-a7fc5bd9e99f.png)

- min / max scale capacity 설정이 가능함. max를 따로 설정하지 않았을 경우, min값과 동일하게 설정된다.
  - desired capacity: group 생성 시 최초에 구성할 instance 개수. min / max 사이값으로만 지정 가능. 이 값을 줄이면, oldest instance부터 삭제한다.
- HA를 위해서는 min, max, default 값을 셋 다 동일하게 맞추는 것도 좋다. 해당 인스턴스 개수를 보장하는 조합임.


Scaling policy 종류

Simple Scaling Policy: 기계적이고 단순한 방식. drastical change에 대응하기는 쉽지 않다.
> A simple scaling policy allows you to do exactly what’s described above. You use a CloudWatch alarm and specify what to do when it is triggered. 
> - This can be a number of EC2 instances to add or remove, or a specific number to set the desired capacity to. 
> - You can specify a percentage of the group instead of using an amount of EC2 instances, which makes the group grow or shrink more quickly. 
> Once this scaling policy is triggered, it waits a cooldown period before taking any other action. This is important as **it takes time for the EC2 instances to start and the CloudWatch alarm may still be triggered while the EC2 instance is booting**. 
> - For example, you could decide to add an EC2 instance if the CPU utilization across all instances is above 65%. You don’t want to add more instances until that new EC2 instance is accepting traffic. 
> However, what if the CPU utilization was now above 85% across the ASG? Only adding one instance may not be the right move here. Instead, you may want to add another step in your scaling policy. Unfortunately, a simple scaling policy can’t help with that.

Step Scaling Policy: additional step을 추가할 수 있음.
> This is where a step scaling policy helps. Step scaling policies respond to additional alarms even while a scaling activity or health check replacement is in progress. Similar to the example above, **you decide to add two more instances in case the CPU utilization is at 85%, and four more instances when it’s at 95%**.

Deciding when to add and remove instances based on CloudWatch alarms may seem like a difficult task. This is why the third type of scaling policy exists: target tracking.

Target Tracking Scaling Policy: 아예 특정 metrics을 기준으로 설정
> If your application scales based on average CPU utilization, average network utilization (in or out), or based on request count, then this scaling policy type is the one to use. All you need to provide is the target value to track and it automatically creates the required CloudWatch alarms.


### Going serverless

![스크린샷 2023-05-01 오후 2 27 56](https://user-images.githubusercontent.com/26548454/235411174-206ba323-5a11-45ed-950f-12bf3fbb654a.png)
<br>

예시로 제공한 employee directory service 구조. 훌륭하지만, EC2 instance 위에 애플리케이션을 올리는 방식이므로 EC2 인스턴스 infra 관련 설정을 사용자가 해야 함.
- 위의 아키텍처는 3-tier application 방식.
  - Presentation layer: user interface (static web server - html, css, js)
  - Application layer : business logic
  - Data layer: DB
- cloud-native service 장점을 최대한 활용한 serverless 방식으로 아키텍처 변경이 가능하다.
  - Presentation layer와 Application layer로 EC2를 활용하는 구조.
    - Presentation layer 동작에 EC2 인스턴스 리소스를 직접 쓰지 않고, AWS S3의 static website hosting을 사용할 수 있다.
    - Application layer 동작은 EC2 대신 lambda로 대체할 수 있다.
    - S3와 lambda를 연결하기 위해 apigw를 사용할 수 있다.
    - 로직의 호출은 IAM의 role-based access로 통제할 수 있다.
  - service들의 연결을 위해 몇몇 서비스를 추가로 사용할 수 있다.
    - 도메인을 쉽게 호출하기 위한 Route53
    - S3 콘텐츠를 사용자에게 빠르게 serving하기 위한 CDN으로 CloudFront


![스크린샷 2023-05-01 오후 2 37 32](https://user-images.githubusercontent.com/26548454/235412050-2a2c0db6-6b7a-458d-b638-87169363f34a.png)
<br>

구조를 변경했을 때 service flow는 위와 같다.
- browser가 입력한 도메인이 Route53로 전달되고, Route53은 CDN 주소를 리턴해준다.
- 사용자는 CDN으로 서비스에 접근하고, javascript를 통해 백엔드 Api path를 확인해서 호출한다.
- apigw로 요청이 들어오면, apigw는 대응되는 lambda 함수를 실행한다.

Serverless workload 기반으로 서비스가 동작하므로, EC2를 쓰는 것보다 사용자는 operation 부담을 줄일 수 있다.
- container 기반 서비스를 만들 경우 아키텍처가 또 달라지지만, 어쨌든 AWS는 api call 기반으로 동작하므로 또 다른 아키텍처를 써서 구성할 수 있다.


