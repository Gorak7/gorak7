<?php
declare(strict_types=1);
$env = static function (string $key, mixed $default = null): mixed { $value = getenv($key); return $value === false ? $default : $value; };
return [
 'database'=>['host'=>$env('DB_HOST','127.0.0.1'),'port'=>(int)$env('DB_PORT',3306),'name'=>$env('DB_NAME','secure_api'),'user'=>$env('DB_USER','root'),'pass'=>$env('DB_PASS','')],
 'rate_limit'=>(int)$env('API_RATE_LIMIT',60),'rate_window'=>(int)$env('API_RATE_WINDOW',60),'debug'=>filter_var($env('APP_DEBUG','false'),FILTER_VALIDATE_BOOL)
];
