for i in {4..10}
do
    python3 twt.py $i > twt_out_$i.txt &
done