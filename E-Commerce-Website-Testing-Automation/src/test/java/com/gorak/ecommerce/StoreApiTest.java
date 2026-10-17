package com.gorak.ecommerce;

import org.testng.Assert;
import org.testng.annotations.Test;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class StoreApiTest {
    private final HttpClient client = HttpClient.newHttpClient();
    private final String baseUrl = System.getProperty("baseUrl", "http://localhost:8080");

    @Test
    public void healthEndpointReturnsUp() throws Exception {
        HttpResponse<String> response = client.send(HttpRequest.newBuilder(URI.create(baseUrl + "/api/health")).GET().build(), HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(response.statusCode(), 200);
        Assert.assertTrue(response.body().contains("UP"));
    }

    @Test
    public void productsEndpointReturnsCatalogue() throws Exception {
        HttpResponse<String> response = client.send(HttpRequest.newBuilder(URI.create(baseUrl + "/api/products")).GET().build(), HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(response.statusCode(), 200);
        Assert.assertTrue(response.body().contains("Wireless Headphones"));
        Assert.assertTrue(response.body().contains("Mechanical Keyboard"));
    }

    @Test
    public void validOrderIsCreatedAndPersisted() throws Exception {
        String payload = "{\"name\":\"QA API\",\"email\":\"qa.api@example.com\",\"productIds\":[1]}";
        HttpRequest request = HttpRequest.newBuilder(URI.create(baseUrl + "/api/orders"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(payload)).build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(response.statusCode(), 201, response.body());
        Assert.assertTrue(response.body().contains("\"orderId\""));
        Assert.assertTrue(response.body().contains("CONFIRMED"));
    }

    @Test
    public void invalidEmailIsRejected() throws Exception {
        String payload = "{\"name\":\"QA API\",\"email\":\"not-an-email\",\"productIds\":[1]}";
        HttpRequest request = HttpRequest.newBuilder(URI.create(baseUrl + "/api/orders"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(payload)).build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        Assert.assertEquals(response.statusCode(), 400, response.body());
    }
}
