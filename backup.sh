LOCAL_PDIR="/home/blazer/Pictures/Camera/"
NET_PDIR="/mnt/media/Pictures/Camera/"
SD_DEV="/dev/mmcblk0p1"
SD_MOUNT="/mnt/camera/"

find_sd_dirs () {
    BASE_DIR="$1"
    PDIRS="${BASE_DIR}DCIM/*CANON"
    for pdir in $PDIRS
    do
        if [ -d "$pdir" ]
        then
            echo $pdir
        else
            echo "There were no picture directories found using: $pdir"
            exit 1
        fi
    done
}

backup_sd () {

    DEV="$1"
    MOUNT="$2"
    BASE_DIR="$3"
    DATE=`date +%m-%d-%Y`

    sudo mount $DEV $MOUNT

    mkdir -p $BASE_DIR
    PDIRS="$(find_sd_dirs $MOUNT)"
    for pdir in $PDIRS
    do
        CP_DIR="$BASE_DIR""$DATE"
        echo $CP_DIR
        if [ -d $CP_DIR ]
        then
            OFFSET=0
            printf -v OFFSET_PAD "%03d" $OFFSET
            while [ -d "$BASE_DIR""$DATE""_$OFFSET_PAD" ]
            do
                OFFSET=$(( OFFSET + 1 ))
                printf -v OFFSET_PAD "%03d" $OFFSET
            done
            CP_DIR="$BASE_DIR""$DATE""_$OFFSET_PAD"
        fi
        echo Copying $pdir to $CP_DIR
        rsync -PrltDv "$pdir" "$CP_DIR"
    done

    sudo umount $DEV
}

backup_sd "$SD_DEV" "$SD_MOUNT" "$LOCAL_PDIR"

