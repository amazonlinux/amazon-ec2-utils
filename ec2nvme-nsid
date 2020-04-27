#!/bin/bash

# Copyright 2016 Amazon.com, Inc. and its affiliates. All Rights Reserved.
#
# Licensed under the MIT License. See the LICENSE accompanying this file
# for the specific language governing permissions and limitations under
# the License.

#Expected input if partition's kernel name like nvme0n1p2
if [ $# -eq 0 ] ; then
  exit 1
else
  # extract ns id from partition's kernel name and export it
  NSID=$(echo -n "$@" | cut -f 3 -d 'n' | cut -f 1 -d 'p')
  echo "_NS_ID=${NSID}"
fi
