import random

mac_addr = "d4:ae:52:d2:5f:c0"
mask_addr = "ff:ff:ff:00:00:00"
dl_src=mac_addr+"/"+mask_addr
dl_dst1="d4:ae:52:12:34:56"
dl_dst2="d4:ae:52:11:22:33"



class Forwarding():
    def __init__(self,file):
        self.file = file

    def add4HopAggFlows(self,br):
        priority =100
        add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst=10."+str(br.pod)+".1.1/0.255.255.0,"+"actions=output:"+str(br.downports[0])
        self.file.write(add_flow_cmd+"\n")
        add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst=10."+str(br.pod)+".2.1/0.255.255.0,"+"actions=output:"+str(br.downports[1])
        self.file.write(add_flow_cmd+"\n")

    def add4HopTorFlows(self,br):
        priority=100

        for port in br.downports:
            if port%len(br.downports):   #only 2 downports
                destip = "10."+str(br.pod)+"."+str(br.pos)+".2/32"
            else:
                destip = "10."+str(br.pod)+"."+str(br.pos)+".3/32"
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table="+str(br.frwdtable)+",priority="+str(priority)+",ip,nw_dst="+destip+",actions=output:"+str(port)
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

