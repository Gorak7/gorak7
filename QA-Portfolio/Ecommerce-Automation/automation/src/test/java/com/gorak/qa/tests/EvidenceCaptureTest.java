package com.gorak.qa.tests;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.Assert;
import org.testng.annotations.*;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;

public class EvidenceCaptureTest {
    private WebDriver driver;
    private final String baseUrl = System.getenv().getOrDefault("BASE_URL", "http://localhost:8080");
    private final Path evidence = Path.of("evidence", "screenshots");

    @BeforeClass public void makeEvidenceFolder() throws Exception { Files.createDirectories(evidence); }
    @BeforeMethod public void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1440,1100");
        driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(4));
    }
    private void capture(String name) throws Exception {
        File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
        Files.copy(src.toPath(), evidence.resolve(name), java.nio.file.StandardCopyOption.REPLACE_EXISTING);
    }
    @Test public void captureHomepageAndSearchEvidence() throws Exception {
        driver.get(baseUrl);
        Assert.assertTrue(driver.getTitle().contains("Northstar Market"), "Store did not load");
        Assert.assertTrue(driver.findElements(By.cssSelector("#products .card")).size() > 0, "Products did not render");
        capture("01-ecommerce-homepage.png");
        driver.findElement(By.id("search")).sendKeys("Mouse");
        driver.findElement(By.id("searchBtn")).click();
        Assert.assertTrue(driver.findElements(By.cssSelector("#products .card")).size() > 0, "Search returned no matching products");
        capture("02-ecommerce-product-search.png");
    }
    @Test public void captureCartAndCheckoutValidationEvidence() throws Exception {
        driver.get(baseUrl);
        driver.findElement(By.cssSelector("#products .card button")).click();
        Assert.assertTrue(Integer.parseInt(driver.findElement(By.id("cartCount")).getText()) > 0);
        capture("03-ecommerce-cart.png");
        driver.findElement(By.id("checkout")).click();
        Assert.assertTrue(driver.findElement(By.id("orderResult")).getText().contains("Enter a valid email"));
        capture("04-ecommerce-checkout-validation.png");
    }
    @AfterMethod(alwaysRun = true) public void tearDown() { if(driver != null) driver.quit(); }
}
