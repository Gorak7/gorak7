package com.gorak.qa.bookstore;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class BookstoreApiTest {
 @BeforeAll static void setup(){RestAssured.baseURI=System.getenv().getOrDefault("BASE_URL","http://localhost:8081");}
 @Test void healthIsUp(){given().when().get("/api/health").then().statusCode(200).body("status",equalTo("UP"));}
 @Test void listBooksReturnsArray(){given().when().get("/api/books").then().statusCode(200).contentType(ContentType.JSON).body("$",notNullValue());}
 @Test void searchFindsSeedBook(){given().queryParam("q","Clean").when().get("/api/books").then().statusCode(200).body("title",hasItem("Clean Code"));}
 @Test void missingBookReturns404(){given().when().get("/api/books/99999999").then().statusCode(404);}
 @Test void invalidBookIsRejected(){given().contentType(ContentType.JSON).body("{\"title\":\"\",\"author\":\"\",\"price\":-1,\"stock\":-2}").when().post("/api/books").then().statusCode(anyOf(is(400),is(422)));}
 @Test void createReadUpdateDeleteBook(){
  String payload="{\"title\":\"Temporary Test Book\",\"author\":\"QA Test\",\"price\":250.00,\"stock\":3}";
  int id=given().contentType(ContentType.JSON).body(payload).when().post("/api/books").then().statusCode(201).body("title",equalTo("Temporary Test Book")).extract().path("id");
  given().when().get("/api/books/"+id).then().statusCode(200).body("author",equalTo("QA Test"));
  given().contentType(ContentType.JSON).body("{\"title\":\"Updated Test Book\",\"author\":\"QA Test\",\"price\":275.00,\"stock\":2}").when().put("/api/books/"+id).then().statusCode(200).body("title",equalTo("Updated Test Book"));
  given().when().delete("/api/books/"+id).then().statusCode(204);
  given().when().get("/api/books/"+id).then().statusCode(404);
 }
}
