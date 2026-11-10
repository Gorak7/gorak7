<?php
declare(strict_types=1);
require dirname(__DIR__).'/vendor/autoload.php';
$config=require dirname(__DIR__).'/src/config.php';$db=App\Database::connect($config['database']);
$username=getenv('SEED_USERNAME')?:'demo-admin';$password=getenv('SEED_PASSWORD')?:'ChangeThisDemoPassword!2026';
$s=$db->prepare('INSERT INTO users (username,password_hash) VALUES (?,?) ON DUPLICATE KEY UPDATE username=VALUES(username)');$s->execute([$username,password_hash($password,PASSWORD_DEFAULT)]);
echo "Seeded user: {$username}\nSet SEED_PASSWORD before using outside a local demo.\n";
