#!/usr/bin/python
'''
Created on 30 Mar 2015

@author: praveen
'''
import os
import sys
import time
from forwarding import Forwarding
from cherrypickflows import CherryPickFlows
import random
import math
import yaml

forwarding_only = False

class phy_switch():
    def __init__(self, name, virt_nodes, edgeInfo, file):
        self.name=name
        self.virt_nodes = virt_nodes
        self.file=file
        self.bridges=[]
        self.br_list=[]
        self.forw_inst=Forwarding(file)
        self.cherry_inst=CherryPickFlows(file, edgeInfo)
        for br_id in self.virt_nodes.keys():
            self.br_list.append(br_id)

    def del_bridges(self):
        for br_id in self.br_list:
            del_br_cmd ="ovs-vsctl del-br br"+str(br_id)
            self.file.write(del_br_cmd+"\n")

    def add_flows(self):
        if len(self.bridges)==0:
            self.update_bridges()
        for br in self.bridges:
            if forwarding_only:
                table = br.frwdtable
            else:
                table = br.cherrytable
            self.addstubFlows(br,table)
            if br.type == "ToR":
                if not forwarding_only:
                    self.cherry_inst.addTorCherryFlows(br)
                self.forw_inst.addTorFlows(br)
            elif br.type=="Agg":
                if not forwarding_only:
                    self.cherry_inst.addAggCherryFlows(br)
                self.forw_inst.addAggFlows(br)
            elif br.type=="Core":
                if not forwarding_only:
                    self.cherry_inst.addCoreCherryFlows(br)
                self.forw_inst.addCoreFlows(br)

    def update_bridges(self):
        self.add_bridges()

    def addstubFlows(self,br,table):
        for port in br.upports:
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table=0,priority=100,in_port="+str(port)+",ip,actions=goto_table:"+str(table)
            self.file.write(add_flow_cmd+"\n")

        for port in br.downports:
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" table=0,priority=100,in_port="+str(port)+",ip,actions=goto_table:"+str(table)
            self.file.write(add_flow_cmd+"\n")
    
    def add_bridges(self,write=False):
        for br_id,br_info in self.virt_nodes.items():
            br_inst=bridge(br_id,br_info,self.name)
            self.bridges.append(br_inst)
            if write:
                self.add_bridge(br_inst)
                self.add_ports(br_inst)

    def del_flows(self):
        for br_id in self.br_list:
            del_br_cmd ="ovs-ofctl del-flows br"+str(br_id)
            self.file.write(del_br_cmd+"\n")

    def del_groups(self):
        for br_id in self.br_list:
            del_group_cmd ="ovs-ofctl del-groups br"+str(br_id)
            self.file.write(del_group_cmd+"\n")

    def add_bridge(self,br):
        add_br_cmd="ovs-vsctl add-br "+br.name+" -- set bridge "+br.name+" datapath_type=pica8 other-config=datapath-id="+br.datapathID
        set_cntrl_cmd="ovs-vsctl set-controller "+br.name+" tcp:"+br.controller
        set_proto_cmd="ovs-vsctl -- set bridge "+br.name+" protocols="+br.ofproto

        self.file.write(add_br_cmd+"\n")
        self.file.write(set_cntrl_cmd+"\n")
        self.file.write(set_proto_cmd+"\n")

    def add_ports(self,br):
        for port in br.downports:
            add_port_cmd = "ovs-vsctl add-port "+br.name+" ge-1/1/"+str(port)+" vlan_mode=trunk -- set interface ge-1/1/"+str(port)+" type=pica8"
            self.file.write(add_port_cmd+"\n")

        for port in br.upports:
            add_port_cmd = "ovs-vsctl add-port "+br.name+" ge-1/1/"+str(port)+" vlan_mode=trunk -- set interface ge-1/1/"+str(port)+" type=pica8"
            self.file.write(add_port_cmd+"\n")

controller_ip="129.215.164.111:6633"

class bridge():
    def __init__(self, id, br_info, switchName):
        self.type=br_info['level']
        self.switch=switchName
        self.num_ports=len(br_info['up'])+len(br_info['down'])
        self.upports=br_info['up']
        self.downports=br_info['down']
        self.id=id
        self.name="br"+str(id)
        self.pod=br_info['pod']
        self.pos=br_info['pos']
        self.ipaddr=br_info['ipaddr']
        self.datapathID=br_info['datapathID']
        self.controller=controller_ip
        self.ofproto="OpenFlow13"
        self.groups=(id*5)
        self.table=((id-1)*5)+1
        self.groupid=((id-1)*10)+1
        self.frwdtable = self.table+1
        self.cherrytable = self.table

class labSetup():
    def __init__(self):
        self.switch_insts=[]

    def add_bridges(self,switch,file):
        phy_switch_inst = phy_switch(switch,file)
        phy_switch_inst.add_bridges(True)

    def del_bridges(self,switch,file):
        phy_switch_inst = phy_switch(switch,file)
        phy_switch_inst.del_bridges()

    def add_flows(self,switch,file,parm,faulty_links=[]):
        phy_switch_inst = phy_switch(switch,file,parm)
        phy_switch_inst.add_flows(faulty_links)

    def del_flows(self,switch,file):
        phy_switch_inst = phy_switch(switch,file)
        phy_switch_inst.del_flows()

    def del_groups(self,switch,file):
        phy_switch_inst = phy_switch(switch,file)
        phy_switch_inst.del_groups()

if __name__ == "__main__":
    if len (sys.argv) < 2:
        print "Please specify the topology file"
        exit (1)

    yml_file=sys.argv[1]
    if len (sys.argv) == 3 and sys.argv[2] == '-f':
        forwarding_only = True

    topo=yaml.load(open(yml_file,'r'))
    edgeInfo = topo['edges']
    dst_path = "./script/"
    if not os.path.exists (dst_path):
        os.makedirs (dst_path)
    for nodes in topo['nodes']:
        for phy_node, virt_nodes in nodes.items():
            fh=open(dst_path+"add-flows_"+phy_node+".sh",'w')
            phy_switch_inst = phy_switch(phy_node, virt_nodes, edgeInfo, fh)
            phy_switch_inst.add_flows()
            fh=open(dst_path+"del-flows_"+phy_node+".sh",'w')
            phy_switch_inst = phy_switch(phy_node, virt_nodes, edgeInfo, fh)
            phy_switch_inst.del_flows()
            fh=open(dst_path+"add-br_"+phy_node+".sh",'w')
            phy_switch_inst = phy_switch(phy_node, virt_nodes, edgeInfo, fh)
            phy_switch_inst.add_bridges(True)
            fh=open(dst_path+"del-br_"+phy_node+".sh",'w')
            phy_switch_inst = phy_switch(phy_node, virt_nodes, edgeInfo, fh)
            phy_switch_inst.del_bridges()
