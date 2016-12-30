import random

class Forwarding():
    def __init__(self,file):
        self.file = file

    def add4HopAggFlows(self,br):
        priority =100
        start = 1
        for port in br.downports:
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst=10."+str(br.pod)+"."+str(start)+".1/0.255.255.0,"+"actions=output:"+str(port)
            start += 1
            self.file.write(add_flow_cmd+"\n")
        
        priority -= 1
        start = 2 
        if br.imbalance:
            dstip = "10.1.1.2/0.0.255.255"
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst="+dstip+",actions=output:"+str(br.upports[0])
            self.file.write(add_flow_cmd+"\n")
            dstip = "10.1.2.2/0.0.255.255"
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst="+dstip+",actions=output:"+str(br.upports[0])
            self.file.write(add_flow_cmd+"\n")
            dstip = "10.1.2.3/0.0.255.255"
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst="+dstip+",actions=output:"+str(br.upports[0])
            self.file.write(add_flow_cmd+"\n")
            dstip = "10.1.1.3/0.0.255.255"
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst="+dstip+",actions=output:"+str(br.upports[1])
            self.file.write(add_flow_cmd+"\n")
        else:
            for port in br.upports:
                dstip = "10."+str(br.pod)+"."+str(br.pos)+"."+str(start)+"/0.0.0.255"
                start +=1
                add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst="+dstip+",actions=output:"+str(port)
                self.file.write(add_flow_cmd+"\n")
    
    def add4HopTorFlows(self,br):
        priority=100
        start = 2
        for port in br.downports:
            destip = "10."+str(br.pod)+"."+str(br.pos)+"."+str(start)+"/32"
            start += 1
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst="+destip+",actions=output:"+str(port)
            self.file.write(add_flow_cmd+"\n")
    
        priority -= 1
        start = 2
        for port in br.upports:
            srcip=  "10."+str(br.pod)+"."+str(br.pos)+"."+str(start)+"/32"
            start += 1
            if br.imbalance:
                add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_src="+srcip+",actions=output:"+str(br.upports[0])
            else:
                add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_src="+srcip+",actions=output:"+str(port)
            self.file.write(add_flow_cmd+"\n")


    def add4HopCoreFlows(self,br):
        priority=100
        for pod in range(1,br.pod):
            if pod==len(br.downports):
                inports=br.downports[:pod-1]
            else:
                inports=br.downports[:pod-1]+br.downports[pod:]
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst=10."+str(pod)+".0.0/16,"+"actions=output:"+str(br.downports[pod-1])

            self.file.write(add_flow_cmd+"\n")

    def addTorFlows(self,br):
         self.add4HopTorFlows(br)

    def addAggFlows(self,br):
         self.add4HopAggFlows(br)

    def addCoreFlows(self,br):
         self.add4HopCoreFlows(br)

