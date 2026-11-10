<?php
declare(strict_types=1);
namespace App;
use PDO;
final class RateLimiter {
 public function __construct(private PDO $db,private int $limit,private int $windowSeconds){}
 public function allow(string $key): bool {
  $now=time();$window=intdiv($now,$this->windowSeconds)*$this->windowSeconds;
  $s=$this->db->prepare('INSERT INTO rate_limits (rate_key, window_start, request_count) VALUES (?, ?, 1) ON DUPLICATE KEY UPDATE request_count = IF(window_start = VALUES(window_start), request_count + 1, 1), window_start = VALUES(window_start)');$s->execute([$key,$window]);
  $q=$this->db->prepare('SELECT request_count FROM rate_limits WHERE rate_key = ? AND window_start = ?');$q->execute([$key,$window]);return (int)$q->fetchColumn()<=$this->limit;
 }
}
