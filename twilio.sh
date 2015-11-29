#!/bin/bash
#
# ${1}=authtoken
# ${2}=phonenumbers
#
echo << EOF > ./message.txt
Dear Coaches and Parents,

Millbrook Elementary School
3200 Millbrook Dr
San Jose

Arrive 30 minutes early.
Each team must provide a club lines person or referee for their game.

Players must wear shin guards.
If players don't have their uniform, wear dark shorts, and a dark shirt.
No jewelry on players.
Each team is responsible for  cleanup after their game. No trash on the field.

This is for the children to have fun, praise them, cheer, be happy.
You are a very lucky person with a wonderful child, appreciate the moment.

Coaches must bring 2 printed Game Cards (see attached).
This form is editable via adobe reader, do it once, and use it the rest of the season.
(Tom will bring blanks if your printer isn't working)

This Weekends Game Schedule:

Sat: 8:00am   B9 x B6
Sat: 9:00am   G1 x G3
Sat: 10:00am  G5 x G6
Sat: 11:00am  B2 x B3
Sat: 12:00am  B4 x B5
Sat: 1:00pm   B1 x B11
Sat: 3:00pm   G4 x G2

Sun: 3:00pm B7 x B8
EOF
MSG=`cat ./message.txt`
while read -u3 -r CALL;do
  echo "CALL:${CALL}"
  curl -X POST 'https://api.twilio.com/2010-04-01/Accounts/AC5efed982ce7ebfe7c4582d51d3ca778c/Messages.json'  \
  --data-urlencode To=${CALL} \
  --data-urlencode 'From=+14083894623' \
  --data-urlencode '${MSG}' \
  -u AC5efed982ce7ebfe7c4582d51d3ca778c:${1}
done 3<${2}
exit 0
