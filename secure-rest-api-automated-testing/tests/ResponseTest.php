<?php
declare(strict_types=1);
namespace Tests;
use App\Http\Response;use PHPUnit\Framework\TestCase;
final class ResponseTest extends TestCase {
 public function testJsonResponseKeepsStatusAndPayload():void{$r=Response::json(['message'=>'ok'],201,['Location'=>'/api/v1/startups/1']);self::assertSame(201,$r->status);self::assertSame(['message'=>'ok'],$r->payload);self::assertSame('/api/v1/startups/1',$r->headers['Location']);}
}
