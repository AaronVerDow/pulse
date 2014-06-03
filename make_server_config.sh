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
NUMBER=0
STRIP_NO=10
PIXEL_NO=0
for s in $SERIALS
do
    cat << EOF
        {
            "type": "fadecandy",
            "serial": "$s",
            "map": [
EOF
    for i in {0..7}
    do
        let $((PIXEL_LOCAL=i*64))
        cat << EOF
                [ 0, $PIXEL_NO, $PIXEL_LOCAL, 64 ], //$STRIP_NO
EOF
        let $((STRIP_NO=STRIP_NO+1))
        let $((PIXEL_NO=PIXEL_NO+64))
    done
    cat << EOF
            ]
        },
EOF
done
cat << EOF
        {}
    ]
}
EOF
