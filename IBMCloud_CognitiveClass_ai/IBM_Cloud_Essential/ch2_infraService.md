# infraStructure

## VSIs, Bare Metal and Hyper Project

Virtual Servers.
- Available globally
- 64 vCPUs, 512GB RAM
- 1GBps on public / private network Performance.
- 5 SAN Volumns (or 5 local disks on Dedicated VS)
Private network에서 데이터 move에는 비용이 들지 않음.


* Public Virtual Server: 기본적으로 Virtual Server that resides on shared (Multi-tenant) HW. Scalable하며, hourly / monthly billing.

* Dedicated Server : Single tenant HW인 Virtual Server. compliance, Security, performance를 위해 사용함. 특정 host에 provision -> VMs on that host. host는 IBM에서 제공하는 pod.

* Transient Virtual Server : Fraction of the Cost of standard Public VS (preemptible VM in GCP)

* Reserved Virtual Server : shared HW제공. Reserving Capacity for 1 ~ 3 year. long lasting workload에 적합하다.
    - Reserve capacity block - chunk of cpu / ram.
    - VM을 해당 capacity 한도 내에서 생성 가능.

-> GCP의 경우 1~3년 기간동안 사용량을 보장할 수 있는 경우 할인해주는데, 얘네는 애초에 별도상품으로 판매하는 느낌임.

