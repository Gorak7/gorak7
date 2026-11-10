<?php
declare(strict_types=1);
require dirname(__DIR__).'/vendor/autoload.php';
use App\Api;use App\Database;use App\Http\Request;use App\Http\Response;
try{$config=require dirname(__DIR__).'/src/config.php';$db=Database::connect($config['database']);(new Api($db,$config))->handle(Request::fromGlobals())->send();}
catch(Throwable $e){error_log((string)$e);Response::json(['error'=>['code'=>'INTERNAL_SERVER_ERROR','message'=>'An unexpected server error occurred.']],500)->send();}
