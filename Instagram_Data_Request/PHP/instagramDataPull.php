<?php
require_once('Libraries\Instagram.php');


$instag = new Instagram(array(
    'apiKey'      => 'e19d696c1efa44678542f920b00b765c',
    'apiSecret'   => 'd23b6bab6ffa4972baa1d6b08220aab5',
    'apiCallback' => '	https://54.172.40.48'
));

$code = $_GET['code'];

if(isset($code)){
	
}else{
	
}


?>