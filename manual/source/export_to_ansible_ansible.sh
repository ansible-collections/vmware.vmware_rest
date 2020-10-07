#!/usr/bin/env bash

set -eux

target_dir=$1
dest_dir="${target_dir}/docs/docsite/rst/scenario_guides"
mkdir -p ${dest_dir}/vmware_rest_scenarios/task_outputs

cp -v *.rst ${dest_dir} 
cp -v vmware_rest_scenarios/*.rst ${dest_dir}/vmware_rest_scenarios 
for i in $(grep 'literalinclude:' vmware_rest_scenarios/*.rst|awk '{print $3}'); do
    cp -v vmware_rest_scenarios/${i} ${dest_dir}/vmware_rest_scenarios/${i}
done
rm ${dest_dir}/index.rst
