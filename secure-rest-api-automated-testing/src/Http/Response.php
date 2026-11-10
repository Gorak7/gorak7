<?php
declare(strict_types=1);
namespace App\Http;
final class Response {
 public function __construct(public readonly array $payload,public readonly int $status=200,public readonly array $headers=[]) {}
 public static function json(array $p,int $s=200,array $h=[]): self{return new self($p,$s,$h);}
 public function send(): void {http_response_code($this->status);header('Content-Type: application/json; charset=utf-8');header('X-Content-Type-Options: nosniff');header('Cache-Control: no-store');foreach($this->headers as $k=>$v)header($k.': '.$v);echo json_encode($this->payload,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);}
}
