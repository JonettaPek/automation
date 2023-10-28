#! /bin/bash

# Functions

function displayError() {
        echo "Error: ${1}" 1>&2
        displayHelp 1>&2
        return 1
}

function displayHelp() {
cat<<eof
NAME
         Recycle (move) file(s) in current directory and/or subdirectories to recycle bin in your home directory
SYNOPSIS
        bash recycle [OPTION]... FILE...
OPTIONS
        -i, interactive
                prompt before every transfer
        -v, verbose
                explain what is being done
        -r, recursive
                remove (empty) directories and transfer their files to the recycle bin
        -h
                display this help and exit
eof
return 0
}

function filecheck() {

        local locAbsPath=$(find ~ -name ${1})

        local locNum=$(echo $locAbsPath|tr " " "\n"|wc -l)

        if [ $locNum -eq 1 ]
        then
                if [ ! -e ${1} ]
                then
                        displayError "File supplied, ${1}, does not exist"
                        return 1
                elif [ ! -w ${1} ]
                then
                        displayError "No permission to recycle ${1}"
                        return 1
                elif [ ${locAbsPath} = $HOME/project/recycle ]
                then
                        displayError "Attempting to delete recycle script - operation aborted"
                        return 1
                elif [ ${locAbsPath} = $HOME/project/restore ]
                then
                        displayError "Attempting to delete restore script - operation aborted"
                        return 1
                fi
        else
                displayError "multiple files with the same name exist - please specify absolute path"
                return 1
        fi
}

function setVariable() {

        absPath=$(find ~ -name ${1})

        fileName=$(basename ${absPath})

        inodeNum=$(ls -i ${absPath}|cut -d" " -f1)

        newFileName=${fileName}"_"${inodeNum}

        newFilePath=${HOME}"/recyclebin/"${newFileName}

        return 0
}

function processOption() {

        if $setInteractive && $setVerbose # -vi or -iv
        then
                if interactive ${1}
                then
                        moveAndUpdate ${2} ${3} ${4}
                        verbose ${1}
                        return 0
                else
                        echo "${1} not recycled"
                        return 1
                fi
        elif $setInteractive # -i
        then
                if interactive ${1}
                then
                        moveAndUpdate ${2} ${3} ${4}
                        return 0
                else
                        return 1
                fi
        elif $setVerbose # -v
        then
                moveAndUpdate ${2} ${3} ${4}
                verbose ${1}
                return 0
        else # if no options were passed
                moveAndUpdate ${2} ${3} ${4}
                return 0
        fi
}

function interactive() {
        read -p "recycle: recycle regular file '${1}'?" ans
        case $ans in
                [Yy]*)
                        return 0 ;;

                *)
                        return 1 ;;
        esac
}

function verbose() {
        echo "recycled '${1}'"
        echo "$HOME/.restore.info updated"
        return 0
}

function moveAndUpdate() {

        # Move file to $HOME/recyclebin and rename to filename_inodenumber

        mv ${1} ${2}

        # Collate file's original absolute path in .restore.info

        touch $HOME/.restore.info 2> /dev/null

        echo ${3}":"${1} >> $HOME/.restore.info
}

function displayExitStatus() {
        displayHelp
        echo "Help: $?"
        #displayError
        #echo "Error: $?"
}

# ==== MAIN ====

# Parse and set options

setInteractive=false
setVerbose=false
setRecursive=false
setHelp=false
setInvalid=false
setNone=true

while getopts :ivrh opt
do
        case $opt in
                i)
                        setInteractive=true ;;
                v)
                        setVerbose=true ;;
                r)
                        setRecursive=true ;;
                h)
                        setHelp=true ;;
                \?)
                        setInvalid=true
                        invalidOption=$OPTARG ;;
        esac
done

if $setHelp
then
        displayHelp
        exit 0
elif $setInvalid
then
        displayError "Invalid option -- '$invalidOption'"
        exit 1
elif $setInteractive || $setVerbose || $setRecursive || $setNone
then
        # Shift to remove options

        shift $(($OPTIND - 1))

        # Make recycle bin

        mkdir ${HOME}/recyclebin 2> /dev/null

        # Check if there are any files supplied

        if [ $# -eq 0 ]
        then
               displayError "No files supplied"
        fi

        # Loop through every file if multiple filenames provided

        for file in $@
        do
                if [ -f ${file} ]
                then
                        # Check each file for certain criteria

                        filecheck ${file}

                        if [ $? -eq 1 ]
                        then
                                continue 2 # File 1 failed filecheck, move on to file 2
                        else
                                setVariable ${file}

                                processOption ${file} ${absPath} ${newFilePath} ${newFileName}

                                continue 2
                        fi
                elif [ -d ${file} ] && $setRecursive
                then
                        dirAbsPath=$(find ~ -name ${file})

                        find ${dirAbsPath} -depth -empty -type d -delete

                        list=$(ls -R ${dirAbsPath}|grep -v ":$"|tr -s "\n")

                        # Loop through every file in the directory and subdirectories

                        for f in ${list}
                        do

                                x=$(find ~ -name ${f})

                                if [ -f ${x} ]
                                then
                                        setVariable ${f}

                                        processOption ${f} ${absPath} ${newFilePath} ${newFileName}

                                        continue 1
                                elif [ -d ${x} ]
                                then
                                        continue 1
                                fi
                        done

                        rm -Rd ${dirAbsPath}

                        continue 1

                elif [ -d ${file} ] && [ $setRecursive = false ]
                then
                        displayError "${file} is a directory - try using options"

                        continue 1
                fi

        done

fi

#displayExitStatus
