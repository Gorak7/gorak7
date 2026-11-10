<?php
declare(strict_types=1);
namespace App;
use PDO;
final class Database {
 public static function connect(array $c): PDO {
  $dsn=sprintf('mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',$c['host'],$c['port'],$c['name']);
  return new PDO($dsn,$c['user'],$c['pass'],[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC,PDO::ATTR_EMULATE_PREPARES=>false]);
 }
}
