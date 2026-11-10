<?php
declare(strict_types=1);
namespace App;
use App\Http\Request;use App\Http\Response;use PDO;use Throwable;
final class Api {
 private array $resources=['startups'=>['name','description','website','industry','location','contact_email'],'mentors'=>['name','email','expertise','bio','company'],'programmes'=>['name','description','start_date','end_date','status']];
 private RateLimiter $limiter;
 public function __construct(private PDO $db,private array $config){$this->limiter=new RateLimiter($db,$config['rate_limit'],$config['rate_window']);}
 public function handle(Request $r): Response {
  if($r->invalidJson)return $this->error('INVALID_JSON','Request body must be valid JSON.',400);
  if(!$this->limiter->allow('ip:'.$r->ip))return $this->error('RATE_LIMIT_EXCEEDED','Too many requests. Try again later.',429,['Retry-After'=>(string)$this->config['rate_window']]);
  $path=rtrim($r->path,'/')?:'/';
  if($path==='/api/v1/health'&&$r->method==='GET')return Response::json(['status'=>'ok','service'=>'secure-rest-api','version'=>'1.0.0']);
  if($path==='/api/v1/auth/token'&&$r->method==='POST')return $this->issueToken($r);
  if(!preg_match('#^/api/v1/(startups|mentors|programmes)(?:/(\d+))?$#',$path,$m))return $this->error('NOT_FOUND','Endpoint not found.',404);
  $resource=$m[1];$id=isset($m[2])?(int)$m[2]:null;$user=$this->authenticate($r);
  if($user===null)return $this->error('UNAUTHORIZED','A valid bearer token is required.',401);
  if(!$this->limiter->allow('user:'.$user['id']))return $this->error('RATE_LIMIT_EXCEEDED','Too many requests. Try again later.',429,['Retry-After'=>(string)$this->config['rate_window']]);
  try{return match($r->method){
   'GET'=>$id===null?$this->index($resource,$r):$this->show($resource,$id),
   'POST'=>$id===null?$this->create($resource,$r,$user):$this->error('METHOD_NOT_ALLOWED','Use the collection endpoint to create records.',405),
   'PUT','PATCH'=>$id===null?$this->error('METHOD_NOT_ALLOWED','A record ID is required.',405):$this->update($resource,$id,$r,$user,$r->method==='PATCH'),
   'DELETE'=>$id===null?$this->error('METHOD_NOT_ALLOWED','A record ID is required.',405):$this->delete($resource,$id,$user),
   default=>$this->error('METHOD_NOT_ALLOWED','HTTP method not supported.',405)
  };}catch(Throwable $e){error_log((string)$e);return $this->error('INTERNAL_SERVER_ERROR','The request could not be completed.',500);}
 }
 private function issueToken(Request $r): Response {
  $u=$r->body['username']??'';$p=$r->body['password']??'';if(!is_string($u)||!is_string($p)||$u===''||$p==='')return $this->error('VALIDATION_ERROR','Username and password are required.',422);
  $s=$this->db->prepare('SELECT id, username, password_hash FROM users WHERE username = ? AND is_active = 1');$s->execute([$u]);$user=$s->fetch();
  if(!$user||!password_verify($p,$user['password_hash']))return $this->error('INVALID_CREDENTIALS','Username or password is incorrect.',401);
  $token=bin2hex(random_bytes(32));$hash=hash('sha256',$token);$i=$this->db->prepare('INSERT INTO api_tokens (user_id, token_hash, expires_at) VALUES (?, ?, DATE_ADD(UTC_TIMESTAMP(), INTERVAL 8 HOUR))');$i->execute([$user['id'],$hash]);
  return Response::json(['data'=>['token_type'=>'Bearer','access_token'=>$token,'expires_in'=>28800]],201);
 }
 private function authenticate(Request $r): ?array {
  $token=$r->bearerToken();if(!$token||strlen($token)!==64)return null;
  $s=$this->db->prepare('SELECT u.id, u.username FROM api_tokens t JOIN users u ON u.id=t.user_id WHERE t.token_hash=? AND t.revoked_at IS NULL AND t.expires_at>UTC_TIMESTAMP() AND u.is_active=1');$s->execute([hash('sha256',$token)]);$u=$s->fetch();return $u?:null;
 }
 private function index(string $res,Request $r): Response {
  $limit=filter_var($r->query['limit']??20,FILTER_VALIDATE_INT,['options'=>['min_range'=>1,'max_range'=>100]]);$page=filter_var($r->query['page']??1,FILTER_VALIDATE_INT,['options'=>['min_range'=>1]]);
  if($limit===false||$page===false)return $this->error('VALIDATION_ERROR','Page must be positive and limit must be between 1 and 100.',422);
  $offset=($page-1)*$limit;$s=$this->db->prepare('SELECT * FROM '.$res.' ORDER BY id DESC LIMIT :lim OFFSET :off');$s->bindValue(':lim',$limit,PDO::PARAM_INT);$s->bindValue(':off',$offset,PDO::PARAM_INT);$s->execute();
  $count=(int)$this->db->query('SELECT COUNT(*) FROM '.$res)->fetchColumn();return Response::json(['data'=>$s->fetchAll(),'meta'=>['page'=>$page,'limit'=>$limit,'total'=>$count]]);
 }
 private function show(string $res,int $id): Response {$s=$this->db->prepare('SELECT * FROM '.$res.' WHERE id=?');$s->execute([$id]);$row=$s->fetch();return $row?Response::json(['data'=>$row]):$this->error('RESOURCE_NOT_FOUND','Record not found.',404);}
 private function create(string $res,Request $r,array $u): Response {
  $errors=Validator::validate($res,$r->body);if($errors)return $this->error('VALIDATION_ERROR','The supplied data is invalid.',422,[],['fields'=>$errors]);
  $data=array_intersect_key($r->body,array_flip($this->resources[$res]));$cols=array_keys($data);$sql='INSERT INTO '.$res.' ('.implode(',',$cols).') VALUES ('.implode(',',array_fill(0,count($cols),'?')).')';$s=$this->db->prepare($sql);$s->execute(array_values($data));$id=(int)$this->db->lastInsertId();$this->audit($u['id'],'create',$res,$id,$data);
  return Response::json(['data'=>$this->findRow($res,$id),'message'=>'Record created.'],201,['Location'=>'/api/v1/'.$res.'/'.$id]);
 }
 private function update(string $res,int $id,Request $r,array $u,bool $partial): Response {
  if(!$this->findRow($res,$id))return $this->error('RESOURCE_NOT_FOUND','Record not found.',404);
  $data=array_intersect_key($r->body,array_flip($this->resources[$res]));if(!$data)return $this->error('VALIDATION_ERROR','At least one valid field is required.',422);
  $errors=Validator::validate($res,$data,$partial);if($errors)return $this->error('VALIDATION_ERROR','The supplied data is invalid.',422,[],['fields'=>$errors]);
  $sets=array_map(static fn($c)=>$c.' = ?',array_keys($data));$s=$this->db->prepare('UPDATE '.$res.' SET '.implode(', ',$sets).' WHERE id=?');$s->execute([...array_values($data),$id]);$this->audit($u['id'],$partial?'update_partial':'update',$res,$id,$data);
  return Response::json(['data'=>$this->findRow($res,$id),'message'=>'Record updated.']);
 }
 private function delete(string $res,int $id,array $u): Response {$row=$this->findRow($res,$id);if(!$row)return $this->error('RESOURCE_NOT_FOUND','Record not found.',404);$s=$this->db->prepare('DELETE FROM '.$res.' WHERE id=?');$s->execute([$id]);$this->audit($u['id'],'delete',$res,$id,['deleted'=>true]);return Response::json(['message'=>'Record deleted.']);}
 private function findRow(string $res,int $id): ?array {$s=$this->db->prepare('SELECT * FROM '.$res.' WHERE id=?');$s->execute([$id]);return $s->fetch()?:null;}
 private function audit(int $uid,string $action,string $res,int $id,array $data): void {$s=$this->db->prepare('INSERT INTO audit_logs (user_id,action,resource,resource_id,payload) VALUES (?,?,?,?,?)');$s->execute([$uid,$action,$res,$id,json_encode($data,JSON_UNESCAPED_SLASHES)]);}
 private function error(string $code,string $message,int $status,array $headers=[],array $extra=[]): Response{return Response::json(['error'=>array_merge(['code'=>$code,'message'=>$message],$extra)],$status,$headers);}
}
