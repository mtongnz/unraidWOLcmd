#!/bin/bash

vm=$1;
action=$2;

if [ $action == "stop" ] ; then
    echo "Stopping VM: $vm";
    # if domain is running, shut down
    if virsh list | grep "$vm .*running" ; then
      virsh shutdown "$vm"
    fi

elif [ $action == "start" ] ; then
    echo "Starting VM: $vm";
    # resume domain if it's paused
    if virsh list | grep "$vm .*paused" ; then
      virsh resume "$vm"
    elif virsh list | grep "$vm .*pmsuspended" ; then
      virsh dompmwakeup "$vm"
    
    # otherwise start domain
    else
      virsh start "$vm"
    fi
fi
