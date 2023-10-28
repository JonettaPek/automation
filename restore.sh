#! /bin/bash

# Functions

function displayError() {
        echo "Error: ${1}" 1>&2
        return 1
}

function setVariable() {

        rfilepath=$(find ~ -name ${1})

        if [ -z ${rfilepath} ]
        then
                return 1
        else
                rfile=$(basename ${rfilepath})

                restore_info=${HOME}"/.restore.info"

                targetPath=$(grep "${rfile}"  ${restore_info}|cut -d":" -f2)

                return 0
        fi
}

function moveAndUpdate() {

        y=$(dirname ${2})

        if [ ! -e ${y} ]
        then
                mkdir -p ${y}
        fi

        mv ${1} ${2}

        local temp_restore_info=${HOME}"/.temp.restore.info"

        touch ${temp_restore_info} 2> /dev/null

        grep -v "${3}" ${4} > ${temp_restore_info}

        mv ${temp_restore_info} ${4}
}

# ====MAIN====

if [ $# -eq 0 ]
then
        displayError "No file provided"
        exit 1
fi

for file in $@
do
        setVariable ${file}

        if [ -z ${rfilepath} ]
        then
                displayError "File supplied does not exist"

                continue 1

        elif [ ! -e ${targetPath} ] && [ -f ${rfilepath} ]
        then
                moveAndUpdate ${rfilepath} ${targetPath} ${rfile} ${restore_info}

                continue 1

        elif [ -e ${targetPath} ] && [ -f ${rfilepath} ]
        then
                read -p "Do you want to overwrite? " ans

                case ${ans} in
                        [Yy]*)
                                moveAndUpdate ${rfilepath} ${targetPath} ${rfile} ${restore_info}

                                echo "${rfile} is restored: ${targetPath}"

                                continue 2 ;;
                        [Nn]*)
                                echo "${rfile} is not restored - operation aborted"

                                continue 2 ;;
                        *)
                                echo "Invalid option"

                                continue 2 ;;
                esac
        fi

done
