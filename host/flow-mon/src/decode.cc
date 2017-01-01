#include "decode.h"
decode::decode(int kary) {
    k = kary;
    int num_nodes = std::pow(k,2) + (std::pow(k/2,2)) + 1;
    G.init(num_nodes);
    
    for(int pod=1;pod<=k;pod++){
	// 1 to 8 for 4-ary fat tree
	int start = (pod-1)*(k/2)+1;
	int end = (pod-1)*(k/2)+(k/2);
    	vector<int> tor_list;
	for(int tor_id=start;tor_id<=end;tor_id++){
		tor_list.push_back(tor_id);
	}
	std::pair<int, std::vector<int> > pod_tor_entry(pod,tor_list);
	pod_tor_tbl.insert(pod_tor_entry);
    }
    
    for(int pod=1;pod<=k;pod++){
	// 9 to 16 for 4-ary fat tree
	int start = (k*(k/2)) + ((pod-1)*(k/2)) + 1;
	int end = (k*(k/2)) + ((pod-1)*(k/2)) + (k/2);
    	vector<int> agg_list;
	for(int agg_id=start;agg_id<=end;agg_id++)
		agg_list.push_back(agg_id);
	std::pair<int, std::vector<int> > pod_agg_entry(pod,agg_list);
	pod_agg_tbl.insert(pod_agg_entry);
    }

    for(int seg=1;seg<=(k/2);seg++){
	// 17 to 20 for 4-ary fat tree
	int start = (k*k) + ((seg-1)*(k/2)) + 1;
	int end = (k*k) + ((seg-1)*(k/2)) + (k/2);
    	vector<int> core_list;
	for(int core_id=start;core_id<=end;core_id++)
		core_list.push_back(core_id);
	std::pair<int, std::vector<int> > seg_core_entry(seg,core_list);
	seg_core_tbl.insert(seg_core_entry);
    }
    
    for(int pod=1;pod<=k;pod++){
    	for(std::vector<int>::iterator tor_it=pod_tor_tbl[pod].begin();tor_it != pod_tor_tbl[pod].end();tor_it++){
    		for(std::vector<int>::iterator agg_it=pod_agg_tbl[pod].begin();agg_it != pod_agg_tbl[pod].end();agg_it++){
		    G.addEdge(*tor_it,*agg_it);
	    }
	}
    }
    
    for(int seg=1;seg<=k/2;seg++){
	  for(int pod=1;pod<=k;pod++){
		int agg = pod_agg_tbl[pod][seg-1];
		for(std::vector<int>::iterator core_it=seg_core_tbl[seg].begin();core_it != seg_core_tbl[seg].end();core_it++){
			G.addEdge(agg,*core_it);
		}
	}
     }

    int intrapod_count = std::pow((k/2),2);
    int pod_core_count = k*(k/2);
    int total_ids = intrapod_count + k + pod_core_count;
    for(int i=1;i<=total_ids;i++){
        if (i<=intrapod_count)
            intrapod.push_back(i);
        else if (i<=intrapod_count+k)
            podids.push_back(i);
        else if (i<=total_ids)
            podcore.push_back(i);
    }
    
    for(int seg=1;seg<=k/2;seg++){
	  int link_id_idx = (seg-1)*(k/2);
	  for(int pod=1;pod<=k;pod++){
		int agg = pod_agg_tbl[pod][seg-1];
		for(std::vector<int>::iterator core_it=seg_core_tbl[seg].begin();core_it != seg_core_tbl[seg].end();core_it++){
			int link_id = podcore[link_id_idx % podcore.size()];
			std::string key = to_string(seg)+"-"+to_string(link_id);
			stbl.insert(make_pair(key,make_pair(agg,*core_it)));
			link_id_idx++;
		}
	}
     }
    for(int pod=1;pod<=k;pod++){
	int link_id_idx = 0;
    	for(std::vector<int>::iterator tor_it=pod_tor_tbl[pod].begin();tor_it != pod_tor_tbl[pod].end();tor_it++){
    		for(std::vector<int>::iterator agg_it=pod_agg_tbl[pod].begin();agg_it != pod_agg_tbl[pod].end();agg_it++){
		    int link_id = intrapod[link_id_idx];
		    std::string key = to_string(pod)+"-intra-"+to_string(link_id);
		    ptbl.insert(make_pair(key,make_pair(*tor_it,*agg_it)));
	    	    link_id_idx++;
		}
	}
    }

    for(int pod=1;pod<=k;pod++){
	int link_id_start = (pod-1)*(k/2);
	int link_id_end = link_id_start + pow(k/2,2);
	int num_segs = k/2;
	int seg_idx_counter = 0;
    	for(int link_id_idx=link_id_start; link_id_idx < link_id_end; link_id_idx++){
		std::string key = to_string(pod)+"-pod-core-"+to_string(podcore[link_id_idx % podcore.size()]);
		ptbl.insert(make_pair(key,make_pair((seg_idx_counter/num_segs)+1,0)));
		seg_idx_counter +=1;
		}
	}
}

string decode::to_string(int s){
    string String = static_cast<ostringstream*>( &(ostringstream() << s) )->str();
    return String;
}

upair* decode::getSwitchPairInPod(int pod_id,int link_id) {
    podTableIt it=ptbl.find(to_string(pod_id)+ "-intra-" + to_string(link_id));
    if (it != ptbl.end())
        return &(it->second);
    return NULL;
}
        
upair* decode::getSwitchPairInPodCore(int seg_id,int link_id) { 
    segTableIt it=stbl.find(to_string(seg_id) + "-" + to_string(link_id));
    if(it != stbl.end())
        return &(it->second);
    return NULL;
}

int decode::getSegFromCurPod(int pod_id,int id){
    podTableIt it=ptbl.find(to_string(pod_id) + "-pod-core-" + to_string(id));
    if(it != ptbl.end())
        return (it->second.first);
    return 0;
}

void decode::addToPath(list<int> *path,int x,int y){
    int last_switch=0;
    last_switch = path->back();
    list<int> path_to_x = G.getPath(last_switch,x);
    path_to_x.pop_front();
    for (std::list<int>::iterator it=path_to_x.begin();it != path_to_x.end(); ++it)
        path->push_back(*it);
        if (x != y)
            path->push_back(y);
}

void print( vector <string> & v )
{
      for (size_t n = 0; n < v.size(); n++)
              cout << "\"" << v[ n ] << "\"\n";
        cout << endl;
}

void decode::decode_path(int16_t *vlan_ids,int8_t vlan_len,int8_t *sbuff,int8_t *dbuff,list<int> *path) {
    int src_pod,dst_pod,curr_pod,curr_seg;
    bool saw_pod_core;
    int dest_tor,src_tor;
    int32_t id;
    std::vector<int>::iterator it; 
    upair *spair;
    curr_seg=0;
    saw_pod_core=false;
    src_pod=sbuff[1];
    dst_pod=dbuff[1];
    curr_pod=src_pod;
    src_tor = ((src_pod-1)*(k/2))+sbuff[2];
    dest_tor = ((dst_pod-1)*(k/2))+dbuff[2];
    path->push_back(src_tor);

    for(int i=vlan_len-1;i >= 0;i--) {
        id=vlan_ids[i];
        if(vlan_ids[i]==0)
            return;
        else if(find(podcore.begin(),podcore.end(),id) != podcore.end()){
            if (curr_seg==0)
                {
                curr_seg=getSegFromCurPod(curr_pod,id);
                }

            spair=getSwitchPairInPodCore(curr_seg,id);
            if (spair == NULL)
                cout << "upair is NULL"<< endl;
            
            addToPath(path,(*spair).first,(*spair).second);
	    if (saw_pod_core==false)
                saw_pod_core=true;
            
        }
        else if(find(intrapod.begin(),intrapod.end(),id) != intrapod.end()){
            if (saw_pod_core)
                curr_pod=dst_pod;
            spair=getSwitchPairInPod(curr_pod,id);
            if (spair == NULL)
                cout << "upair is NULL"<< endl;
            addToPath(path,(*spair).first,(*spair).second);
        }
        else if(find(podids.begin(),podids.end(),id) != podids.end()){
            curr_pod=(id)-3;
            curr_seg=0;
            cout << "why 8 hop case is excecuting ? It is TODO job"<< endl;
            continue;
        }
      }
    addToPath(path,dest_tor,dest_tor);
}



