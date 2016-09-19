add_flows(){
   for var in nsl100 nsl101 nsl102 nsl103 nsl104 nsl105
   do
       echo "serving "$var
       ssh admin@$var < ./script/del-flows_$var.sh
       ssh admin@$var < ./script/add-flows_$var.sh
   done
}

add_bridges(){
   for var in nsl100 nsl101 nsl102 nsl103 nsl104 nsl105
   do
       echo "serving "$var
       ssh admin@$1 < ./script/del-br_$1.sh
       ssh admin@$1 < ./script/add-br_$1.sh
   done
}

del_bridges() {
   for var in nsl100 nsl101 nsl102 nsl103 nsl104 nsl105
   do
       echo "serving "$var
       ssh admin@$1 < ./script/del-br_$1.sh
   done
}

del_flows(){
   for var in nsl100 nsl101 nsl102 nsl103 nsl104 nsl105
   do
       echo "serving "$var
       ssh admin@$var < ./script/del-flows_$var.sh
   done
}


reset(){
   for var in nsl100 nsl101 nsl102 nsl103 nsl104 nsl105
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
