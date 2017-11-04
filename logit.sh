#!/bin/bash
echo "$(date) >>> $*" >> /tmp/logit
output=$($*)
ret=$?
echo $output | tee -a /tmp/logit
exit $ret
