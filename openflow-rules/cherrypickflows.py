class CherryPickFlows():
    def __init__(self,file,edgeInfo):
        self.file=file
        self.edgeInfo=edgeInfo;

    def addTorCherryFlows(self,br):
        priority=100
        table=br.cherrytable
        nxt_table=br.frwdtable
        for port in br.upports:
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" priority="+str(priority)+",table="+str(table)+",in_port="+str(port)+",ip,nw_src=10."+str(br.pod)+".0.0/16,nw_dst=10."+str(br.pod)+".0.0/16,actions=goto_table:"+str(nxt_table)
            self.file.write(add_flow_cmd+"\n")

        priority -= 1



        for port in br.upports:
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" priority="+str(priority)+",table="+str(table)+",in_port="+str(port)+",ip,nw_src=10."+str(br.pod)+".0.0/16,actions=push_vlan:0x8100,set_field:"+self.getLinkId(port,br)+"-\>vlan_vid,goto_table:"+str(nxt_table)
            self.file.write(add_flow_cmd+"\n")


        priority -= 1

        add_flow_cmd="ovs-ofctl add-flow "+br.name+" priority="+str(priority)+",table="+str(table)+",ip,actions=goto_table:"+str(nxt_table)
        self.file.write(add_flow_cmd+"\n")


    def addAggCherryFlows(self,br):
        priority=100
        table=br.cherrytable
        nxt_table=br.frwdtable

        for port in br.downports:
	    add_flow_cmd="ovs-ofctl add-flow "+br.name+" priority="+str(priority)+",table="+str(table)+",in_port="+str(port)+",ip,nw_dst=10."+str(br.pod)+".0.0/16,actions=push_vlan:0x8100,set_field:"+self.getLinkId(port,br)+"-\>vlan_vid,goto_table:"+str(nxt_table)
            self.file.write(add_flow_cmd+"\n")

        priority -= 1

        add_flow_cmd="ovs-ofctl add-flow "+br.name+" priority="+str(priority)+",table="+str(table)+",ip,actions=goto_table:"+str(nxt_table)
        self.file.write(add_flow_cmd+"\n")


    def addCoreCherryFlows(self,br):
        priority=100
        table=br.cherrytable
        nxt_table=br.frwdtable

        for port in br.downports:
            add_flow_cmd="ovs-ofctl add-flow "+br.name+" priority="+str(priority)+",table="+str(table)+",in_port="+str(port)+",ip,actions=push_vlan:0x8100,set_field:"+self.getLinkId(port,br)+"-\>vlan_vid,goto_table:"+str(nxt_table)
            self.file.write(add_flow_cmd+"\n")

    def getLinkId(self,port,br):
	for edge in self.edgeInfo:
	    if edge['x'][0] == br.id and edge['x'][1]==port:
		return str(edge['link_id'])
	    elif edge['y'][0] == br.id and edge['y'][1]==port:
		return str(edge['link_id'])
	  
	print "Port ",port," is not present in bridge ",br.id
	return None


		



