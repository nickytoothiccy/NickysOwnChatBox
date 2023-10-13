from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Grouped Workers", show=False):
    elb = ELB("lb")

    with Cluster("Worker Group 1"):
        worker1 = [EC2("worker1.1"),
                   EC2("worker1.2")]

    with Cluster("Worker Group 2"):
        worker2 = [EC2("worker2.1"),
                   EC2("worker2.2")]

    with Cluster("RDS Cluster"):
        db_master = RDS("master")
        db_master - [RDS("slave1"),
                     RDS("slave2")]

    elb >> worker1
    elb >> worker2
    worker1 >> db_master
    worker2 >> db_master
