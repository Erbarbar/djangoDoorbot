#!/bin/sh

cd doorBot
#./updatejeKers.sh && ./refreshInternet.sh && fg

./refreshInternet.sh &
P1=$!
./updatejeKers.sh &
P2=$!
wait $P1 $P2
