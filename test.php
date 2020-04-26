<?php

$obj = new SplMinHeap();
$x = 100;
$obj->insert($x);
$i= 0;
while((($x-1)/2) > 0){
    $x = intval(($x-1)/2);
    $obj->insert($x);
}

while(!$obj->isEmpty()) {
 if($obj->extract()%2){
    echo "2";
 }else{
    echo "3";
 }
}
