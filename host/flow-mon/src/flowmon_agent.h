#include <map>

struct flowkey_path_t{
    int32_t sip;
    int32_t sport;
    int32_t dip;
    int32_t dport;
    int32_t pkts;
    int64_t bytes;
    int8_t  proto;
    string  linkids; //"id1-id2-..."
    list<int> path;
    struct timeval start;
    struct timeval end;
    bool del_flag;
};

struct path_t{
    int32_t sip;
    string  linkids; //"id1-id2-..."
    list<int> path;
};

typedef struct {
    int32_t saddr;
    int32_t daddr;
    int32_t sport;
    int32_t dport;
     int8_t proto;
    int16_t vlan_buff[2];
}fkey_tags_t;

typedef struct{
    int32_t pkts;
    int64_t bytes;
     int8_t vlan_len;
    struct timeval stime;
    struct timeval etime;
}fkey_data_t;

typedef struct {
    fkey_tags_t fkey_tags;
    fkey_data_t fkey_data;
}flow_stats_t;

struct ans_t {
    struct nlmsghdr n;
    flow_stats_t  data;
};

typedef std::map<std::string,struct flowkey_path_t> connTbl;
typedef std::map<std::string,struct flowkey_path_t>::iterator conn_it;
typedef std::map<std::string,std::list<int> > pathCacheTbl;
typedef std::map<std::string,std::list<int> >::iterator pathCache_it;
