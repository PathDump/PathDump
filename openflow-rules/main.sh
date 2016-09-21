#!/bin/bash
suffix=".inf.ed.ac.uk"
node_list=(nsl100 nsl101 nsl102 nsl103 nsl104 nsl105)
add_flows(){
    for var in ${node_list[*]}
    do
       echo "serving "$var
       ssh admin@$var < ./script/del-flows_$var.sh
       ssh admin@$var < ./script/add-flows_$var.sh
   done
}

add_bridges(){
    for var in ${node_list[*]}
    do
       echo "serving "$var
       ssh admin@$var < ./script/del-br_$var.sh
       ssh admin@$var < ./script/add-br_$var.sh
   done
}

del_bridges() {
   for var in ${node_list[*]}
   do
       echo "serving "$var
       ssh admin@$var < ./script/del-br_$var.sh
   done
}

del_flows(){
   for var in ${node_list[*]}
   do
       echo "serving "$var
       ssh admin@$var < ./script/del-flows_$var.sh
   done
}


reset(){
   for var in ${node_list[*]}
   do
       echo "serving "$var
       ssh admin@$var < ./script/del-flows_$var.sh
       ssh admin@$var < ./script/del-br_$var.sh
       ssh admin@$var < ./script/add-br_$var.sh
       ssh admin@$var < ./script/add-flows_$var.sh
   done
}

# Usage info
   show_help() {
   cat << EOF
       -d          delete bridges
       -o          delete flows
       -b          add bridges,ports
       -f          add flows
       -r          reset (del-br,add-br,add-flows on nsl100,nsl101,nsl102,nsl103,nsl104)
EOF
  }




# Initialize our own variables:
  while getopts "s:hrdobfam" opt; do
       case "$opt" in
           h)  show_help
               exit 0
               ;;
           d)  del_bridges
               exit 0
               ;;
           o)  del_flows
               exit 0
               ;;
           b)  add_bridges
               exit 0
               ;;
           f)  add_flows
               exit 0
               ;;
           r) reset
               exit 0
               ;;
       esac
   done
