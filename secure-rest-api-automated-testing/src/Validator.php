<?php
declare(strict_types=1);
namespace App;
final class Validator {
 public const RULES=[
  'startups'=>['name'=>'string','description'=>'string','website'=>'url','industry'=>'string','location'=>'string','contact_email'=>'email'],
  'mentors'=>['name'=>'string','email'=>'email','expertise'=>'string','bio'=>'string','company'=>'string'],
  'programmes'=>['name'=>'string','description'=>'string','start_date'=>'date','end_date'=>'date','status'=>'status']
 ];
 public static function validate(string $resource,array $data,bool $partial=false): array {
  $errors=[];
  foreach(self::RULES[$resource] as $field=>$type){
   if(!array_key_exists($field,$data)){if(!$partial&&in_array($field,['name','email'],true))$errors[$field]='This field is required.';continue;}
   $v=$data[$field];if($v===null||$v===''){$errors[$field]='This field cannot be empty.';continue;}
   $valid=match($type){
    'string'=>is_string($v)&&strlen($v)<=2000,
    'email'=>is_string($v)&&filter_var($v,FILTER_VALIDATE_EMAIL)!==false,
    'url'=>is_string($v)&&filter_var($v,FILTER_VALIDATE_URL)!==false&&in_array(parse_url($v,PHP_URL_SCHEME),['http','https'],true),
    'date'=>is_string($v)&&self::isDate($v),
    'status'=>is_string($v)&&in_array($v,['planned','active','completed','cancelled'],true),
    default=>false
   };if(!$valid)$errors[$field]='Invalid value for '.$field.'.';
  }return $errors;
 }
 private static function isDate(string $v): bool {$d=\DateTimeImmutable::createFromFormat('!Y-m-d',$v);return $d!==false&&$d->format('Y-m-d')===$v;}
}
