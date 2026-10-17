package com.gorak.qa.bookstore;

import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import java.nio.file.*;
import java.time.Duration;

class BookstoreUiEvidenceTest {
 static WebDriver driver;
 static final String baseUrl=System.getenv().getOrDefault("UI_BASE_URL","http://localhost:8081");
 static final Path evidence=Path.of("evidence","screenshots");
 @BeforeAll static void start() throws Exception {
  Files.createDirectories(evidence);
  ChromeOptions options=new ChromeOptions();
  options.addArguments("--headless=new","--no-sandbox","--disable-dev-shm-usage","--window-size=1440,1100");
  driver=new ChromeDriver(options); driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(4));
 }
 static void capture(String name) throws Exception {
  byte[] png=((TakesScreenshot)driver).getScreenshotAs(OutputType.BYTES);
  Files.write(evidence.resolve(name),png);
 }
 @Test void homepageAndSearchScreenshots() throws Exception {
  driver.get(baseUrl);
  Assertions.assertTrue(driver.getTitle().contains("Chapter & Co."),"Bookstore UI failed to load");
  Assertions.assertTrue(driver.findElements(By.cssSelector("#books .book")).size()>0,"Books did not render");
  capture("01-bookstore-homepage.png");
  driver.findElement(By.id("q")).sendKeys("Clean");
  driver.findElement(By.id("search")).click();
  Assertions.assertTrue(driver.findElements(By.cssSelector("#books .book")).size()>0,"Search did not return a book");
  capture("02-bookstore-search.png");
 }
 @AfterAll static void stop(){if(driver!=null)driver.quit();}
}
