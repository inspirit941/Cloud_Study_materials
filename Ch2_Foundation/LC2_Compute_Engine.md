# VM
VM이 꼭 하드웨어 컴퓨터와 같은 건 아니다. Virtual CPU, Disk Storage, IP address를 부여받은 가상 머신.

설정할 수 있는 기본 옵션도 CPU, Memory, discs, networking.

---
## Compute Engine

Utmost flexiblity를 제공하는 VM. IaaS model의 대표격. Autoscaling도 지원한다.

cpu개수, 메모리 량, persistent disks의 종류, 운영체제 등… 여러 가지 선택이 가능.

1. Compute
Network throughputs -> cpu 1개당 scales at 2GB
이론적으로는 최대 8 CPU로 16GB까지 가능.
vCPU -> 기본적으로 1 hardware hyper-thread.

2. Storage
3개 option : standard, SSD, Local SSD
디스크 사이즈 형태로 선택하기 때문에, 디스크 크기는 동일하다.
standard는 HDD라고 생각하면 됨.
	- SSD : higher number of IOPS / $
	- Local SSD : higher throughput / lower latency -> physical HW와 attached된 상태이기 때문.
	단, instance가 살아 있는 동안에만 데이터가 저장된다. Stop / delete될 경우 데이터가 삭제됨. 최대 3TB까지 할당받을 수 있다.
Standard / non-local SSD의 경우 64TB까지 지원. 

3. Network 방식
VPC에서 설명한 default / custom networks. Inbound / outbound firewall rules의 영향을 받는다.

Regional HTTPS load balancing / Networ load balancing -> no pre-warming. 구글의 load balancer는 a set of traffic engineering rules that are coming into the Google network. VPC는 이 rule을 IP address subnet range에 적용하는 것.

---
### VM Access and lifecycle

4 root privileges.

1. 리눅스: ssh 사용 가능. GCP console로 ssh 접근 권한을 다른 사용자에게 제공할 수 있다.
Requires firewall rule to allow tcp:22
2. 윈도우: GCP console로 사용자 이름 / 비밀번호 설정이 가능. 사용자 이름 + 비밀번호를 아는 누구나 접근할 수 있고, 로그인을 위해 Remote Desktop protocol (RDP client)를 사용한다.
Requires firewall rule to allow tcp:3389
-> firewall rule로 ssh나 RDP 접근을 허용해야 하지만, default network일 경우 굳이 지정해줄 필요가 없다. 자동으로 됨

Lifecycle
모든 인스턴스 속성을 지정하고 생성버튼을 누르면
1. Provisioning. vCPU + Memory -> root disk & persistent disk -> additional disk
2. Staging. resources를 지급받고 instance가 launch 준비를 완료하기까지의 과정. IP address 받고 system image booting up -> boot까지의 과정이다.
3. Running. Pre-configured startup script를 실행하고, enables ssh / RDP access. 여기서 할 수 있는 작업들을 한다
Ex) live migrate your VM to another host ini the same zone (instance reboot 대신 하는 일). Keep infra protected / reliable without interrupting any of your VMs.
Ex) set / get metadata,  export system image, snapshot persistent disk, Move VM to different Zone
4. Stop VM. Adding more cpu를 해야 하는 경우라던가. Pre-configured shutdown script를 실행하고, terminated state에 도달한다.

Available Policy : Automatic changes
(Called Scheduling options in SDK/API)

Maintenance Event - to prevent application from disruption.
* Live Migrate : default. VM을  다른 HW로 migrate without interruption. 이거 대신 ‘해당 인스턴스 terminate’ 등으로도 변경할 수 있다.
* Crash 발생 시 -> automatically restarts by default. (변경 가능)

Instance creation 시 / running일 경우 configuring automatic restart & host maintenance option을 지정할 수 있다.

Terminated instance의 경우 attached disk + reserved IP address의 비용만 나간다.
cf. Terminated state에서도 image는 변경할 수 없다.

---
### Lab

You can’t convert a non-preemptible instance into a preemptible one. This choice must be made at VM creation. A preemptible instance can be interrupted at any time and is available at a lower cost.

---
## Working with virtual machines

GCP console, cmd (cloud shell 포함), REST API 세 가지 방법으로 VM 생성이 가능함.

Machine Type : 두 가지 방식이 있다. 
Predefined / Custom. machine type. 

Predefined :  
1. Standard : balanced CPU / Memory 방식. 1 ~ 96까지의 vCPU, persistent disk 최대 128개, 총 용량 64TB.
2. High-memory machine type : cpu보다 ram 많이 쓰는 경우. Cpu 개당 6.5GB memory.
3. High-CPU : 0.9 memory per CPU
4. Memory-optimized : high-memory보다 메모리 더 쓰는 경우. 14GB per 1 vCPU. in-Memory DB나 in-Memory Analytics에 적합하다. (SAP HANA, business warehouse workloads 등)
5. Compute optimized : vCPU (3.8Ghz sustained), high-cpu보다 robust
6. Shared-core machine type : 1개 cpu의 portion of time on a single hardware hyper-thread on the host cpu running your instance. (일부 쓰레드만 활용하는 방식인 듯). Small + non-resource intensive application에 유용함.
할당된 부분으로 처리하기 어려우면, allow instances to use additional physical CPU (short period of time). 자동으로 실행됨. 


Custom machine Type
동일한 predefined setting보다 비용이 좀 더 나가는 특징. 
Total memory는 256MB의 배수여야 한다.
1 CPU당 6.5GB limit이 걸려 있지만, 추가비용 내면 이 리미트도 해제할 수 있다. (Extende Memory)

Region / Zone 선택 시…
어느 지역에 resource를 실행시킬 건지 보고 정하면 된다.
인스턴스는 Default processes supported in that zone을 따른다. (Us-central 1일 경우 sandy bridge processor를 따라간다고)

---
### Compute Pricing

* Per-second billing, with min of 1 minute. (1분 미만 = 1분 처리, 1분 이상부터는 초 단위로)
* Resource-based pricing. CPU와 메모리 사용량에 따라 각각 billing.
* discounts (Type are not combined)
	- sustained usage인 경우 discount 적용.  (Region collectively rather than to individual machine types)
	-> 1년 ~ 3년 단위 구매조건으로 할인해준다. 최대 57%. (Custom machine type에도 적용) memory optimized type의 경우 최대 70%

Preemptible VM은 가격이 저렴하다는 장점이 있지만, Compute Engine might terminate or preempt these instance if it requires access to those resources for other tasks. (다른 일 때문에 인스턴스 동작 멈출 수 있다는 소리)

Customizing == pricing도 마찬가지로 customized.
일단 VM size 추천도 해 준다. (VM instance resource usage에 따라) 생성 후 24시간 이후부터.

Free usage Limit도 있다. 첨부 링크 참고하라고 하고 넘어감


Significant portion of billing month에 따라 sustained use discount가 자동 적용된다.
Ex) 한 달 기준 25% 이상 사용할 경우 추가되는 매 분마다 할인 적용. 최대 30% net discount까지 가능하다.

discount는 매달 1일에 reset되므로, 만약 full discount를 받으려면 1일에 생성해야 한다.
50% of month use -> 10%, 75% -> 20%, 100% -> 30% 까지 할인.
자세한 건 calculator 활용

Calculator는 해당 vCPU usage, Memory usage across each region, and separately for each of the following categoreies (predefined, custom)

예컨대 month begins에 4 cpu 할당 -> 2주차에 12 cpu 추가할당일 경우 처음 4개는 1일 ~ 말일까지 꾸준히 사용하면 30% 할인, 2주차에 추가된 12개의 cpu는 4주차까지 약 2주 사용했으므로 10% 할인이 적용된다. (메모리도 마찬가지)

---
### Special compute configuration

* Preemptible
Lower price (up to 80%)
	- VM might be terminated at any time
	No charge if terminated in the first 10 min
	24hours max (최대 24시간동안 live)
	30초 전에 preempt 예정임을 공지함
	- No live migrate, no auto start. 대신 load balancer와 monitoring으로 can startup new preemptible VMs in case of failure. 즉, keep preemptible VM하는 external way는 존재한다.
	- 대표적인 사용사례 = batch processing job. 설령 terminated되더라도 slows down, not completely stop이기 때문.
* Sole-tenant
Physical isolation from other workloads or VM in order to meet compliance requirement일 때 사용. VM dedicated to hosting VM instances only for your specific project. 

즉 일반적으로 VM을 할당받을 때에는 하나의 host - hardware - hypervisor 에 여러 명의 customer가 각자 VM을 할당받아 host에 사용하는데, 아예 host 통째로 혼자 쓰려는 경우. 한 host의 모든 프로젝트가 belongs to the same project.
Ex) payment processing workload that needs to be isolated to meet the compliance requirements 

이미 사용하고 있는 OS 라이센스가 있으면, sole-tenant Node에 통째로 들고 와서 사용하는 것도 가능하다.

* Shielded VM -> offer verifiable integrity.
Your instances haven’t been compromised by boot or kernel level of malware or rootkits을 보장한다. 
Secure boot / Virtual Trusted Platform Module (VPTM) / integrity monitoring 등의 방법을 사용

---
### Image

VM을 만들 때, boot disk image를 선택할 수 있다. 
Boot loader / OS / file sys structure / any pre-configured SW and other customizations 등을 총칭한다.

Linux / Window Image를 선택할 수 있다. 최소 1분 charge, 1분 이후부터는 초 단위로 billing. (SQL 서버는 예외. 최소 10분 charge / 분 단위 billing)
프리미엄 image도 있지만, global pricing이며 does not vary by region or zones.

Create / Use custom image로 필요한 SW를 따로 설치하거나, on-premises & other cloud의 image를 importing하는 것도 가능.

---
### Disk Options

Base image를 load할 공간이 필요하기에 기본적으로 persistent disk가 필요함.  VM이 삭제된 이후에도 boot disk를 남기려면, instance 삭제할 때 delete boot disk 옵션을 결정해야 한다.

* Persistent Disk
Attached to the VM through network interface. 단, physically attached된 게 아니라서 VM을 삭제할 때 disk는 삭제하지 않고 내버려둘 수 있다.
Snapshot으로 incremental backup 기능 수행 가능.
HDD / SSD 선택 가능.
실행 중에도 Dynamically resize 가능. Read only 모드로 여러 VM에서 접근 가능하도록 만들 수도 있는데, 여러 instance 간 static 데이터 공유하는 용도로 유용하다.
구글은 알아서 encrypt all data at rest. 구글이 알아서 하는 일이라 따로 action 취할 필요도 없고 돈낼 필요도 없다. 만약 encryption management가 필요하면 Cloud key management service를 이용할 수 있다. 또는 own key encryption keys를 생성하고 사용하는 customer supplied encryption key 기능을 지원함.

(Persistent SSD -> very random IOPS)

* Local SSD
Physically attached to VM. 따라서 ephemeral이지만 high IOPS를 제공함. 여기 올라간 데이터는 reset일 때는 살아남지만, VM의 stop이나 terminate 상태에서는 삭제된다. (다른 VM에 re-attached되는 게 불가능하기 때문)

* RAM disk
tepfs 사용 가능. 메모리에 데이터 저장하는 방식.
데이터구조가 크지 않을 경우 가장 빠른 속도 제공. 이거 할 거면 high-memory machine을 사용하는 걸 권장한다. 마찬가지로 ephemeral.

컴퓨터 하드디스크와의 차이점
- 하드디스크는 (re)partitioning 가능. Encryption할 경우 디스크에 저장하기 전에 수행해야 한다는 특징
- cloud에서는 전부 백엔드 작업으로 빠져 있다. Snapshot / resize 등등을 지원하고, single file system을 권장하며 (파티셔닝보다는), automate encryption을 지원한다. 

---
### Common Compute Engine Actions

모든 VM instance는 메타데이터를 metadata server에 저장하고 있다. 이 기능은 startup / shutdown script를 사용할 때 유용한데, 별다른 인증절차 없이 원하는 instance의 데이터에 접근할 수 있기 때문.

Default metadata keys == same on every instance. 코드 작업이 한결 쉽다. Startup / shutdown script는 일반적으로 cloud storage에 저장하는 게 편리함.

*Move an instance to New Zone*
-> Same region일 경우 `gcloud compute instance move` 명령어로 쉽게 처리랄 수 있다.
-> 다른 region일 경우 Manually do so
1. Source VM의 모든 persistent disk의 snapshot을 만든다
2. Create new persistent zones restored from snapshots.
3. Create new VM -> attach new persistent disks.
4. Assign static IP to new VM
5. Update reference to VM
6. Delete original VM, disks, snapshots.

Snapshot을 좀 더 들여다보자. 유용함
* use to backup critical data into a durable storage solution to meet applications, availability, recovery requirement. 보통 cloud storage에 저장됨.
* migrate data btwn zones. 
* transferring data to a different disk type (improve performance). HDD persistent disk 내용을 SSD에 그대로 옮기는 식.

위/아래의 특징들 = Persistent disk snapshot에 해당하는 내용들
따라서 local SSD는 해당사항 없음. Periodic backup을 주로 수행한다는 점에서도 images와 다르다. Incremental / automatically compressed이므로, 생성하는 데 부담도 적고 비용효율적이다.

*resize persistent disk.*
-> I/O performance를 증가시키기 위해서 하는 작업으로, 이건 snapshot 만들 필요도 없음. Running VM에 attach하면 됨. 단, 한 번 올린 사이즈는 내릴 수 없다.

---
### Lab

마인크래프트 서버를 만들고, 게임 데이터를 저장할 disk를 추가로 붙여 VM을 만듬.
서버 들어가서 디렉토리 만들어주고, 디스크 포맷해준 다음 마운트한다.

서버를 그냥 돌리면, ssh 세션 끝나면 서버도 죽어버린다. 그걸 막기 위해 screen을 사용. Virtual terminal that can be detached.

`sudo screen -S mcs java -Xmx1024M -Xms1024M -jar server.jar nogui` 로 마인크래프트 서버를 screen에 실행하고
Ctrl A, ctrl D로 detached한다. 다시 foreground 작업하려면 `sudo screen -r mcs`

마크 클라이언트는 기본 25565로 접속. 따라서 firewall rule에 mc-server에 지정해놓은 tag에 맞게 새로 생성해서 적용해준다.

Regular backup을 위해 storage bucket을 사용한다. 서버 내용을 storage에 저장하는 Backup script를 만들고,  755 모드로 변경해준 다음 실행해서 저장되었는지를 console로 확인.

Sudo crontab -e 명령어로 nano editor를 연 다음
`0 */4 * * * /home/minecraft/backup.sh`를 입력한다. 4시간마다 실행되는 스크립트라고 함.

Startup / shutdown script를 지정하려면
“Custom metadata”란을 VM edit창에서 확인하고
Key - value에 startup-script-url - 구글api의 url 
넣으면 된다. (구글에서 스크립트를 api로 만들어뒀음)

---
