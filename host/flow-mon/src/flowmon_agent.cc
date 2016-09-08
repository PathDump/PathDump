#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/netlink.h>
#include <string.h>
#include <sys/socket.h>
#include "decode.h"
#include <netinet/in.h>
#include "flowmon_agent.h"
#include <unistd.h>
#include <pthread.h>
#include <queue>
#include <sys/time.h>
#include "mongo/client/dbclient.h" // for the driver
#include "mongo/bson/bson.h"
#include "yaml-cpp/yaml.h"

using namespace std;
#define SERVER_PORT 5555
#define nl_msg_hdrsize 16
#define nl_data(na) ((void *)((char*)na+nl_msg_hdrsize))
#define NL_RBUFF 1000000000

connTbl conn;
pathCacheTbl cacheTbl;
pthread_mutex_t mtx;
std::queue<flow_stats_t> q1;
int done = 0;
int err_cnt=0;
int nl_sd; /*the socket*/
decode *D;

int init_mongodb(mongo::DBClientConnection *c){
    try {
            c->connect("localhost");
            std::cout << "connected ok" << std::endl;
        } catch( const mongo::DBException &e ) {
       std::cout << "caught " << e.what() << std::endl;
        }
    return EXIT_SUCCESS;
}


/*
 * Create a raw netlink socket and bind
 */

/* return an integer greater than, equal to, or less than 0, 
 *    according as the timeval a is greater than, 
 *       equal to, or less than the timeval b. */
int compare_timeval(struct timeval *a, struct timeval *b) {
        if (a->tv_sec > b->tv_sec)
         return 1;
        else if (a->tv_sec < b->tv_sec)
         return -1;
        else if (a->tv_usec > b->tv_usec)
         return 1;
        else if (a->tv_usec < b->tv_usec)
         return -1;
    return 0;
}
static int create_nl_socket(int protocol, int groups)
{
        int fd,size,rv;
        int size_len;
        struct sockaddr_nl local;
        
        size_len=sizeof(size);
        
        fd = socket(AF_NETLINK, SOCK_RAW, protocol);
        
        if (fd < 0){
		perror("socket");
                return -1;
        }
        size=NL_RBUFF;
        
        rv = setsockopt(fd,SOL_SOCKET,SO_RCVBUF,&size,size_len);
        if(rv < 0){
            perror("set to soc error");
            return -1;
        }
        rv = setsockopt(fd,SOL_SOCKET,SO_SNDBUF,&size,size_len);
        if(rv < 0){
            perror("set to soc error");
            return -1;
        }
        
        rv = getsockopt(fd, SOL_SOCKET, SO_RCVBUF, &size, (socklen_t *)&size_len); 
        cout << "netlink soc rcv size = : "<< size << endl;
        rv = getsockopt(fd, SOL_SOCKET, SO_SNDBUF, &size, (socklen_t *)&size_len); 
        cout << "netlink soc rcv size = : "<< size << endl;
        memset(&local, 0, sizeof(local));
        local.nl_family = AF_NETLINK;
        local.nl_groups = groups;
        local.nl_pid=SERVER_PORT;
        if (bind(fd, (struct sockaddr *) &local, sizeof(local)) < 0)
                goto error;
        
        return fd;
 error:
        close(fd);
        return -1;
}


void itoip(int *ip,int8_t *bytes)
{
    bytes[3] = (*ip) & 0xFF;
    bytes[2] = ((*ip) >> 8) & 0xFF;
    bytes[1] = ((*ip) >> 16) & 0xFF;
    bytes[0] = ((*ip) >> 24) & 0xFF;
}

unsigned long long getmillisec(struct timeval *tv){
    unsigned long long millisecondsSinceEpoch = (unsigned long long)(tv->tv_sec) * 1000 + (unsigned long long)(tv->tv_usec) / 1000;
    return millisecondsSinceEpoch;
}

unsigned long long getmicrosec(struct timeval *tv){
    unsigned long long microsecondsSinceEpoch = (unsigned long long)(tv->tv_sec) * 1000000 + (unsigned long long)(tv->tv_usec);
    return microsecondsSinceEpoch;
}


string getIP(int32_t ip){
    int8_t sbytes[4]; 
    char ip_c[20];
    int32_t addr;
    addr=ntohl(ip);
    itoip(&addr,sbytes);
    sprintf(ip_c,"%d.%d.%d.%d",sbytes[0],sbytes[1],sbytes[2],sbytes[3]);
    return string(ip_c);
}

string getPort(int16_t port){
    int32_t p=ntohs(port);
    char port_c[10];
    sprintf(port_c,"%d",p);
    return string(port_c);
}

string getProto(int8_t proto){
    int8_t p=ntohs(proto);
    char proto_c[10];
    memset(proto_c,0,sizeof(proto_c));
    sprintf(proto_c,"%d",p);
    return string(proto_c);
}

template <typename T>
string NumberToString(T Number)
{
	stringstream ss;
	ss << Number;
	return ss.str();
}

string getDateString(struct timeval *tv)
{
	struct tm *nowtm;
	char tmbuf[64];
	time_t nowtime;
	string date_str;

	nowtime=tv->tv_sec;
	nowtm = localtime(&nowtime);
	strftime(tmbuf, sizeof tmbuf, "%Y-%m-%d %H:%M:%S", nowtm);
	date_str=string(tmbuf);
	
	return date_str+"."+NumberToString(tv->tv_usec);

}

int insert_db(conn_it e,mongo::DBClientConnection *cdb){
    
    mongo::BSONObjBuilder b;
    mongo::BSONArrayBuilder a;
    struct timeval c;
    char buff[10];
    string sip,dip,sport,dport,proto,id;
    sip=getIP(e->second.sip);
    dip=getIP(e->second.dip);
    sport=getPort(e->second.sport);
    dport=getPort(e->second.dport);
    proto=getProto(e->second.proto); 
    id = sip+"-"+sport+"-"+dip+"-"+dport+"-"+proto+"-"+e->second.linkids;
    cout << "DB: Inserting flow with key: " << id << "\n";
    b << "sip" << sip << "dip" << dip << "sport" << sport << "dport" << dport << "proto" << proto;
    b << "id" << id << "pkts" << e->second.pkts << "bytes" << (long long) e->second.bytes;
    b << "start" << mongo::Date_t(getmillisec(&(e->second.start)));
    b << "end" << mongo::Date_t(getmillisec(&(e->second.end)));
    gettimeofday(&c,NULL);
    b << "log" << mongo::Date_t(getmillisec(&c));
    mongo::BSONArrayBuilder barr;
    std::list<int>::iterator k;
    barr.append(sip);
    if(e->second.path.size() > 1){
      for(std::list<int>::iterator i=e->second.path.begin(),j=--e->second.path.end();i!=j;++i){
        k=i;
        sprintf(buff,"%d-%d",*i,*(++k));
        barr.append(string(buff));
       }
      }
      else{
       for(std::list<int>::iterator i=e->second.path.begin();i!=e->second.path.end();++i){
        sprintf(buff,"%d",*i);
        barr.append(string(buff));
       }
      }
    barr.append(dip);
    b << "path" << barr.arr();
    mongo::BSONObj p=b.obj();

    cdb->insert("PathDump.TIB",p);
    return 0;
}

void* monflows(void *ptr){
    mongo::DBClientConnection *cdb;
    cdb = (mongo::DBClientConnection *) ptr;
    struct timeval c;
    while (true){
        pthread_mutex_lock(&mtx);
        for (conn_it it=conn.begin();it!=conn.end();){
                gettimeofday(&c,NULL);
                cout<<"deleting key : "<<it->first << " bytes: "<<it->second.bytes << " pkts: " << it->second.pkts << "err_cnt: "<<err_cnt << endl;
                insert_db(it,cdb);
                conn.erase(it++);
         }
        pthread_mutex_unlock(&mtx);
        sleep(2);
    }
    return NULL;
}


int decodepath(flow_stats_t data);

void* read_soc(void *ptr){
    int rep_len;
    struct ans_t ans;
    while (true){
        rep_len = recv(nl_sd, &ans, sizeof(ans), 0);
        decodepath(ans.data);
        if (rep_len < 0) {
            ++err_cnt;
            continue;
        } 
    }
    return NULL;
}

string getLinkIdsString(int8_t len, int16_t *linkids){
    char key_c[30];
    char atoi_buff[15];
    memset(key_c,0,sizeof(key_c)); 
    if(len==1){
	sprintf(atoi_buff,"%d",linkids[0]);
	strcat(key_c,atoi_buff);
    }
    else if(len==2){
	sprintf(atoi_buff,"%d",linkids[0]);
	strcat(key_c,atoi_buff);
	strcat(key_c,"-");
	sprintf(atoi_buff,"%d",linkids[1]);
	strcat(key_c,atoi_buff);
    }
    return string(key_c);
}

string getFlowPathKey(flow_stats_t *data){
    	char key_c[100];
	string key;
    	char atoi_buff[15];
    	memset(key_c,0,sizeof(key_c)); 
    	
	sprintf(atoi_buff,"%d",data->fkey_tags.saddr);
        strcat(key_c,atoi_buff);
        strcat(key_c,"-");
        
        sprintf(atoi_buff,"%d",data->fkey_tags.sport);
        strcat(key_c,atoi_buff);
        strcat(key_c,"-");
        
        sprintf(atoi_buff,"%d",data->fkey_tags.daddr);
        strcat(key_c,atoi_buff);
        strcat(key_c,"-");
        
        sprintf(atoi_buff,"%d",data->fkey_tags.dport);
        strcat(key_c,atoi_buff);
        strcat(key_c,"-");

        sprintf(atoi_buff,"%d",data->fkey_tags.proto);
        strcat(key_c,atoi_buff);
        strcat(key_c,"-");
    return string(key_c)+getLinkIdsString(data->fkey_data.vlan_len,data->fkey_tags.vlan_buff);
}

string getPathCacheKey(flow_stats_t *data){
    char key_c[30];
    char atoi_buff[15];
    memset(key_c,0,sizeof(key_c)); 

    sprintf(atoi_buff,"%d",data->fkey_tags.saddr);
    strcat(key_c,atoi_buff);
    strcat(key_c,"-");

    return string(key_c)+getLinkIdsString(data->fkey_data.vlan_len,data->fkey_tags.vlan_buff);
}

void printIntList(list<int> *p){
     cout << "printing list " << "\t";
     for(list<int>::iterator it=p->begin();it != p->end(); it++){
     	cout << *it << "\t";
     }
     cout << "\n";
}

void getPath(flow_stats_t *data, int8_t *saddr, int8_t *daddr,list<int> *path){
    string key;
    pathCache_it cache_it;
    key = getPathCacheKey(data);
    cache_it = cacheTbl.find(key);
    if (cache_it == cacheTbl.end()) {
	cout << "Miss !! updating cache with key " << key << "\n";
	D->decode_path(data->fkey_tags.vlan_buff,data->fkey_data.vlan_len,saddr,daddr,path);
 	std::pair<std::string, list<int> > path_entry(key,*path);	
	cacheTbl.insert(path_entry);
    } 
    else {
	cout << "Hit !! Found entry in cache" << key << "\n";
	for (list<int>::iterator it=cache_it->second.begin();it != cache_it->second.end(); it++){
		path->push_back(*it);
	}
    }
}

int decodepath(flow_stats_t data){
        int8_t sbytes[4],dbytes[4];
        int32_t saddr,daddr;
        string linkids_str;
        string key;
        conn_it cit;
        bool insert=false;
        bool update=false;
        
        linkids_str=getLinkIdsString(data.fkey_data.vlan_len,data.fkey_tags.vlan_buff); 
	key=getFlowPathKey(&data);
	cout << "User: Received flow with key  : " << key << "\n";
        
	pthread_mutex_lock(&mtx);
        if(!insert){
            cit = conn.find(key);
            if(cit==conn.end())
                insert=true;
            else
                update=true;
        }
        if (insert){
           struct flowkey_path_t fs; 
           fs.sip=data.fkey_tags.saddr;
           fs.sport=data.fkey_tags.sport;
           fs.dip=data.fkey_tags.daddr;
           fs.dport=data.fkey_tags.dport;
           fs.proto=data.fkey_tags.proto;
	   fs.pkts=data.fkey_data.pkts;
           fs.bytes=data.fkey_data.bytes;
           fs.linkids=linkids_str;
           fs.start.tv_sec=data.fkey_data.stime.tv_sec;
           fs.start.tv_usec=data.fkey_data.stime.tv_usec;
           fs.end.tv_sec=data.fkey_data.etime.tv_sec;
           fs.end.tv_usec=data.fkey_data.etime.tv_usec;
           
	   saddr=ntohl(data.fkey_tags.saddr);
           daddr=ntohl(data.fkey_tags.daddr); 
           itoip(&saddr,sbytes);
           itoip(&daddr,dbytes);
           getPath(&data,sbytes,dbytes,&(fs.path));
	   printIntList(&(fs.path));
	   std::pair<std::string,struct flowkey_path_t> flowkey_path_entry(key,fs);
	   cout << "User: Inserting flow "<< "\n";
	   conn.insert(flowkey_path_entry);
        }
        else if(update) {
            cit->second.pkts +=data.fkey_data.pkts;
            cit->second.bytes += data.fkey_data.bytes;
            cit->second.end.tv_sec=data.fkey_data.etime.tv_sec;
            cit->second.end.tv_usec=data.fkey_data.etime.tv_usec;
            cit->second.start.tv_sec=data.fkey_data.stime.tv_sec;
            cit->second.start.tv_usec=data.fkey_data.stime.tv_usec;
            cout << "User: Updating flow" << "\n";
	}
        pthread_mutex_unlock(&mtx); 
    return 0;
}

int main()
{
    vector<pthread_t *> vt;
    YAML::Node config = YAML::LoadFile("../../../config/config.yaml");
    decode d(config["k"].as<int>());
    D=&d;
    pthread_t thread1,thread2;
    mongo::client::initialize();
    mongo::DBClientConnection c;
    init_mongodb(&c);
    pthread_create(&thread1,NULL, monflows, &c);
    nl_sd = create_nl_socket(NETLINK_UNUSED,0);
    if(nl_sd < 0){
       printf("Socket create failure. Check modified OVS kernel module (openvswitch.ko) is installed (check with lsmod)\n");
       return 0;
    }
    pthread_create(&thread2,NULL, read_soc, NULL);
    pthread_join(thread1,NULL);
    pthread_join(thread2,NULL);
    return 0;
}
