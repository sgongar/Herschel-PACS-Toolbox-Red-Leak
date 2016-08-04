dir=`pwd`
declare -a arr_1=($(find $dir -type f -name "*.tar"))

for i in "${arr_1[@]}"
do
    j=${i%?}
    j=${j%?}
    j=${j%?}
    j=${j%?}
    mkdir $j
    tar -xf $i -C $j
done

