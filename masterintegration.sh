#!/bin/bash

#==============================================================================
# Globals
#==============================================================================

whatstep="$1"
whatmonth="$2"
whatyear="$3"
airline="$4"
demo="$6"
content_id_date="content-$airline-$whatmonth$whatyear"
old_content_id_date=`ls /content/integrator/content-sets/$airline/ | grep "content-$airline"`
serverdestonation="172.16.40.$5"
#serverdestonation_dir=`ssh $serverdestonation; ls /content-xfer-dis/ | grep "content-$airline"; exit`
consus="172.16.40.92:/root/QA"
#==============================================================================
# Functions
#==============================================================================


function help_usage() {
        echo "$0 <qa1/qa2> <month> <year> <customer> <build server IP> <demo name only for digecordemo content>"
        echo "REQUIRES the first five, the sixth is REQUIRED when using digecordemo customer for demo/rental content"
        echo
        echo "Example:"
        echo "$0 qa1 10 2014 alaskal7 241"
	echo "OR"
	echo "$0 qa1 10 2014 digecordemo 241 charter"
        exit 0
} # help_usage

function updating__dir() {
	cd /content/integrator/content-sets/$airline/
	if [[ ! -z "${old_content_id_date}" ]] ; then
		if [ "$content_id_date" != "$old_content_id_date" ]  ;then 
			mv $old_content_id_date content-$airline-$whatmonth$whatyear
			if [ -d content-$airline-$whatmonth$whatyear/audio/ ] ;then
				rm -r content-$airline-$whatmonth$whatyear/audio/* 
			fi
			if [ -d content-$airline-$whatmonth$whatyear/musicvideos/ ] ;then
				rm content-$airline-$whatmonth$whatyear/musicvideos/*
			fi
			rm content-$airline-$whatmonth$whatyear/videos/*
			rm -r content-$airline-$whatmonth$whatyear/menu/*
		fi
	else
			mkdir content-$airline-$whatmonth$whatyear
			rsync -avh --progress /content/integrator/content-sets/content-starter/ content-$airline-$whatmonth$whatyear/
	fi
} #updating__dir

function syncing__content() {
	if [[ "${airline}" == "digecordemo" ]] ;then
		rsync -avh --progress --delete content-$airline-$demo$whatmonth$whatyear/ $serverdestonation:/content-xfer-dis/content-$airline-$demo$whatmonth$whatyear/
	elif [[ ! -z "${serverdestonation_dir}" ]] ;then
		if [ "$serverdestonation_dir" != "content-$airline-$whatmonth$whatyear" ] ;then
			worked=`ssh $serverdestonation 'mv /content-xfer-dis/'$serverdestonation_dir'/ /content-xfer-dis/content-'$airline'-'$whatmonth$whatyear'/'`
			rsync -avh --progress --delete content-$airline-$whatmonth$whatyear/ $serverdestonation:/content-xfer-dis/content-$airline-$whatmonth$whatyear/
		else
        	        rsync -avh --progress --delete content-$airline-$whatmonth$whatyear/ $serverdestonation:/content-xfer-dis/content-$airline-$whatmonth$whatyear
		fi
	else
		rsync -avh --progress --delete content-$airline-$whatmonth$whatyear/ $serverdestonation:/content-xfer-dis/content-$airline-$whatmonth$whatyear/
	fi
} #syncing__content

function clean__up() {
	cd /content/integrator/ctrs/
	current_ctrs=`ls /content/integrator/ctrs/ | grep "$airline"`
	blank=""
	for i in $(seq 1 12); 
	do
		last_ctr_year="0"
		last_ctr_month="0"
        	try_last_ctr_month=`expr $whatmonth - "$i"`
		try_last_ctr_year=$whatyear
		if [[ $try_last_ctr_month -lt 1 ]] ;then
			try_last_ctr_month=`expr $try_last_ctr_month + 12`
			try_last_ctr_year=`expr $whatyear - 1`
		fi
	        if [[ $try_last_ctr_month -lt 10 ]] ;then
        		try_last_ctr_month="0$try_last_ctr_month"
        	fi
		last_ctr_array_bait=`ls /content/integrator/ctrs/ | grep "$airline"_"$try_last_ctr_year-$try_last_ctr_month"`
		if [[ ! -z "${last_ctr_array_bait}" ]] ;then
			for i in ${last_ctr_array_bait// / } ;
        		do
                		current_ctrs=${current_ctrs//"$i"/$blank}
        		done
			last_ctr_month=$try_last_ctr_month
			last_ctr_year=$try_last_ctr_year
			break
		fi
	done
	array_bait=`ls /content/integrator/ctrs/ | grep "$airline"_"$whatyear-$whatmonth"`
	for i in ${array_bait// / } ;
	do
		current_ctrs=${current_ctrs//"$i"/$blank}
	done
	if [[ ! -z "${current_ctrs}" ]] ;then
		while true; do
			echo -e "\nDelete the following CTR's:\n"
			for i in ${current_ctrs// / } ;
			do
				echo -e $i"\n"
			done
			read -p "[Y]es or [N]o:" yn
			case $yn in
				[Yy]* ) rm $current_ctrs; break;;
				[Nn]* ) break;;
				* ) echo "Please answer Y or N.";;
			esac
		done
	fi
} #clean__up

function sync_ctrs() {
	scp $consus/*.xls /content/integrator/ctrs/

	if [[ "${airline}" != "digecordemo" ]] ;then
	        ctr_exist=`ls /content/integrator/ctrs/ | grep "$airline"_"$whatyear-$whatmonth"`
	        if [[ -z "${ctr_exist}" ]] ;then
	                echo "No CTR's exist for $airline"_"$whatyear-$whatmonth"
	                exit
	        fi
	        clean__up
	elif [[ ! -z "${demo}" ]] ;then
	        ctr_exist=`ls /content/integrator/ctrs/ | grep "$demo"_"$whatyear-$whatmonth"`
	
	        if [[ -z "${ctr_exist}" ]] ;then
	                echo "No CTR's exist for $demo"_"$whatyear-$whatmonth"
	                exit
	        fi
	else
	        help_usage
	fi
} #sync_ctrs

function create__contentkeys() {
	cd /content/integrator/content-sets/$airline/content-$airline-$whatmonth$whatyear/
	createkeyfiles.py videos/ /mnt/allmkvkeys.txt > /mnt/$airline-keys.txt
	createkeyfiles.py ads/ /mnt/allmkvkeys.txt >> /mnt/$airline-keys.txt
	$a=$(ls ./ | grep extkey.txt)
		if [ ! -z "${a}" ];then
			cat extkey.txt >> /mnt/$airline-keys.txt
		fi
	digkey -e /mnt/$airline-keys.txt -k /usr/customerkeys/$airline-group-key.txt > /keys/keys.bin
	cd /content/integrator/content-sets/$airline/
} #create__contentkeys
		
		
#===============================================================================
# Main
#===============================================================================

if [[ $whatstep == "--help" ]]
 then 
	help_usage
elif [[ $whatstep == "qa1" ]]
 then 
	sync_ctrs
	if [[ "${airline}" != "digecordemo" ]] ;then
		updating__dir
	elif [ ! -d "/content/integrator/content-sets/$airline/content-$airline-$demo$whatmonth$whatyear/" ]; then
		mkdir /content/integrator/content-sets/$airline/content-$airline-$demo$whatmonth$whatyear/
		rsync -avh --progress /content/integrator/content-sets/content-starter/ /content/integrator/content-sets/$airline/content-$airline-$demo$whatmonth$whatyear/
	fi
	MasterMenuGenKronos.py $airline $whatmonth $whatyear $whatstep $last_ctr_month $last_ctr_year $demo
	ret=$?
	if [ $ret -ne 0 ]; then
		echo "Menu Generation Failed!!"
		exit
	fi
	sync
#	rsync -avh --progress /content/integrator/ctrs/CTR_$airline"_"$whatyear-$whatmonth* $consus/
	serverdestonation_dir=`ssh $serverdestonation 'ls /content-xfer-dis/ | grep content-'$airline`
	sync
	syncing__content 
	if [ ! -z "$(cat /content/integrator/content-sets/$airline/config$demo/errors.txt)" ]; then
                echo "Warnings found:"
                cat /content/integrator/content-sets/$airline/config$demo/errors.txt
        else
                echo "Good news, no issues! Have a victory cup of coffee!"
        fi
elif [[ $whatstep == "qa2" ]]
 then
	sync_ctrs
	updating__dir
if [[ "${airline}" != "digecordemo" ]] ;then
                updating__dir
        elif [ ! -d "/content/integrator/content-sets/$airline/content-$airline-$demo$whatmonth$whatyear/" ]; then
                mkdir /content/integrator/content-sets/$airline/content-$airline-$demo$whatmonth$whatyear/
                rsync -avh --progress /content/integrator/content-sets/content-starter/ /content/integrator/content-sets/$airline/content-$airline$
        fi
        MasterMenuGenKronos.py $airline $whatmonth $whatyear $whatstep $last_ctr_month $last_ctr_year $demo
        ret=$?
        if [ $ret -ne 0 ]; then
                echo "Menu Generation Failed!!"
                exit
        fi
        sync
        rsync -avh --progress /content/integrator/ctrs/CTR_$airline"_"$whatyear-$whatmonth* $consus/
	serverdestonation_dir=`ssh $serverdestonation 'ls /content-xfer-dis/ | grep content-'$airline`
	sync
#	syncing_content
	if [ ! -z "$(cat /content/integrator/content-sets/$airline/config$demo/video-list.txt)" ]; then
		echo "Missing videos for:"
		cat /content/integrator/content-sets/$airline/config$demo/video-list.txt
	else
		echo "Menu Generation Complete!"
	fi
	if [ ! -z "$(cat /content/integrator/content-sets/$airline/config$demo/errors.txt)" ]; then
		echo "Warnings found:"
		cat /content/integrator/content-sets/$airline/config$demo/errors.txt
	else
		echo "Good news, no issues! Have a victory cup of coffee!"
	fi
else 
	echo "You did something wrong, check yourself!"
	help_usage
fi
