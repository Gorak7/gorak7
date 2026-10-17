package com.gorak.qa.tests;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.Assert;
import org.testng.annotations.*;
import java.time.Duration;

public class StoreSmokeTest {
    private WebDriver driver;
    private final String baseUrl = System.getenv().getOrDefault("BASE_URL", "http://localhost:8080");

    @BeforeMethod
    public void setUp() {
        ChromeOptions options = new ChromeOptions();
        if (Boolean.parseBoolean(System.getenv().getOrDefault("HEADLESS", "false"))) {
            options.addArguments("--headless=new");
        }
        options.addArguments("--window-size=1440,1000");
        driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(3));
    }

    @Test
    public void homepageLoadsAndProductsRender() {
        driver.get(baseUrl);
        Assert.assertTrue(driver.getTitle().contains("Northstar Market"), "Store page title should be visible");
        Assert.assertTrue(driver.findElements(By.cssSelector("#products .card")).size() > 0,
                "At least one product card should render; confirm API and database are running");
    }

    @Test
    public void searchFiltersProducts() {
        driver.get(baseUrl);
        driver.findElement(By.id("search")).sendKeys("Mouse");
        driver.findElement(By.id("searchBtn")).click();
        Assert.assertTrue(driver.findElements(By.cssSelector("#products .card")).size() >= 1,
                "Search should show matching product(s)");
    }

    @Test
    public void emptyCheckoutShowsValidation() {
        driver.get(baseUrl);
        driver.findElement(By.id("email")).sendKeys("qa@example.com");
        driver.findElement(By.id("checkout")).click();
        Assert.assertTrue(driver.findElement(By.id("orderResult")).getText().contains("Add at least one product"),
                "Checkout should reject an empty cart");
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown() { if (driver != null) driver.quit(); }
}
