cat << EOF
{
    "listen": [null, 7890],
    "verbose": true,

    "color": {
        "gamma": 2.5,
        "whitepoint": [1.0, 1.0, 1.0]
    },

    "devices": [
EOF
SERIALS=`cat serial_nos | awk '{print $2}'`
for s in $SERIALS
do
cat << EOF
        {
            "type": "fadecandy",
            "serial": "$s",
            "map": [
                [ 0, 0, 0, 512 ]
            ]
        },
EOF
done
cat << EOF
        {}
    ]
}
EOF
