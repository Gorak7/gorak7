<?php
declare(strict_types=1);
namespace App\Http;
final class Request {
 public function __construct(public readonly string $method,public readonly string $path,public readonly array $headers,public readonly array $query,public readonly array $body,public readonly string $ip,public readonly bool $invalidJson=false) {}
 public static function fromGlobals(): self {
  $headers=function_exists('getallheaders')?getallheaders():[];$normalized=[];
  foreach($headers as $k=>$v)$normalized[strtolower((string)$k)]=$v;
  $raw=file_get_contents('php://input')?:'';$body=[];
  if($raw!==''){$decoded=json_decode($raw,true);if(!is_array($decoded))return new self($_SERVER['REQUEST_METHOD']??'GET',parse_url($_SERVER['REQUEST_URI']??'/',PHP_URL_PATH)?:'/',$normalized,$_GET,[],$_SERVER['REMOTE_ADDR']??'unknown',true);$body=$decoded;}
  return new self($_SERVER['REQUEST_METHOD']??'GET',parse_url($_SERVER['REQUEST_URI']??'/',PHP_URL_PATH)?:'/',$normalized,$_GET,$body,$_SERVER['REMOTE_ADDR']??'unknown');
 }
 public function bearerToken(): ?string {$h=$this->headers['authorization']??'';return preg_match('/^Bearer\s+(.+)$/i',$h,$m)?trim($m[1]):null;}
}
