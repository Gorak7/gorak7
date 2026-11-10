<?php
declare(strict_types=1);
namespace Tests;
use App\Validator;use PHPUnit\Framework\TestCase;
final class ValidatorTest extends TestCase {
 public function testValidStartupPayloadPasses():void{self::assertSame([],Validator::validate('startups',['name'=>'Northstar Labs','website'=>'https://example.com','contact_email'=>'hello@example.com']));}
 public function testMissingRequiredStartupNameIsRejected():void{self::assertArrayHasKey('name',Validator::validate('startups',['industry'=>'Technology']));}
 public function testInvalidEmailIsRejected():void{self::assertArrayHasKey('email',Validator::validate('mentors',['name'=>'A Mentor','email'=>'not-an-email']));}
 public function testInvalidProgrammeStatusIsRejected():void{self::assertArrayHasKey('status',Validator::validate('programmes',['name'=>'Launchpad','status'=>'unknown']));}
 public function testPartialUpdateDoesNotRequireName():void{self::assertSame([],Validator::validate('startups',['industry'=>'HealthTech'],true));}
 public function testUnsafeUrlSchemeIsRejected():void{self::assertArrayHasKey('website',Validator::validate('startups',['name'=>'Example','website'=>'javascript:alert(1)']));}
}
