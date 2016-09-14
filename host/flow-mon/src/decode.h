#include <string>
#include <map>
#include <vector>
#include <utility> 
#include <sstream>
#include <boost/algorithm/string.hpp>
#include "sp.h"
#include <cmath>
using namespace std;

typedef std::map<std::string, std::pair<int,int> > segTable;
typedef std::map<std::string, std::pair<int,int> > podTable;
typedef std::map<std::string, std::pair<int,int> >::iterator segTableIt;
typedef std::map<std::string, std::pair<int,int> >::iterator podTableIt;
typedef std::map<int, std::vector<int> > podSwitchTable;
typedef std::map<int, std::vector<int> >::iterator podSwitchTableIt;
typedef std::pair<int,int> upair;

class decode {
    int k;
    segTable stbl;
    podTable ptbl;
    podSwitchTable pod_tor_tbl;
    podSwitchTable pod_agg_tbl;
    podSwitchTable seg_core_tbl;
    Graph G; 
    vector<int> intrapod;
    vector<int> podcore;
    vector<int> podids;
    vector<int> pod_switches;
    vector<int> core_switches;
    	
public:
    decode(int);
    //int getPodFromIp(std::string addr);
    string to_string(int);
    upair* getSwitchPairInPod(int pod_id,int link_id);
    upair* getSwitchPairInPodCore(int seg_id,int link_id);
    int getSegFromCurPod(int pod_id,int link_id);
    void addToPath(list<int> *path,int x,int y);
    void getLocation(char *sbuff,int size,int* loc);
    void decode_path(int16_t *vlan_ids,int8_t vlan_len,int8_t *sbuff,int8_t *dbuff,list<int> *path);

};
