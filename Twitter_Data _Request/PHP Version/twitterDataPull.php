<?php

#change to exact location of lib
require_once('Library\TwitterAPIExchange.php');


$settings = array(
    'oauth_access_token' => "788587562-H44SFWDYPH2tAEjKPSLOopjddWHeFlq6Izi2d9Jj",
    'oauth_access_token_secret' => "5Wd7iIJrB2PMS5m4kT9cApljKUtLjUItVHdpZHkQh3i6E",
    'consumer_key' => "IYI98EkHxXsNXivYX7xm19eOi",
    'consumer_secret' => "ByPKtxN0rFKhCGeWhloGHsV5tMnB1mYxgZTiAKDDyAt3aFKC3S"
);



$url = 'https://api.twitter.com/1.1/search/tweets.json';
$requestMethod = 'GET';

$postfields = array(
    'q' => '#oxy',
);

$queryStuff = "q=".urlencode("#oxy OR #weed"); 

$twitter = new TwitterAPIExchange($settings);
$data = json_decode($twitter->setGetfield($queryStuff)
	->buildOauth($url, $requestMethod)
    ->performRequest());
$array = array();	
	foreach($data->statuses as $status){
		$array[] = array(
		 "userID" => $status->id_str,
		 "userTweet" => $status->text,
		);
	}
	#echo print_r($data);
	file_put_contents("keyWordsRequest.json",json_encode($array));

?>