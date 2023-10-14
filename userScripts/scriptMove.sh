#!/bin/bash

mkdir /scripts
cp /boot/scripts/* /scripts
chown nobody:users /scripts/*
chmod +x /scripts/*.sh