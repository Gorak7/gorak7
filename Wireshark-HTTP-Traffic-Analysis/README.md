# Wireshark HTTP Traffic Analysis

## Overview

This project demonstrates how to capture, filter, and analyze HTTP network traffic using **Wireshark**. The lab focuses on understanding web communication at the packet level, inspecting HTTP requests and responses, and examining application-layer payloads.

HTTP traffic analysis is an important networking and cybersecurity skill used for troubleshooting, traffic investigation, security monitoring, and identifying potentially suspicious network activity.

## Objectives

- Capture HTTP traffic using Wireshark.
- Apply Wireshark display filters to isolate HTTP packets.
- Analyze HTTP GET requests and request headers.
- Analyze HTTP responses, status codes, and content types.
- Inspect TCP streams and transferred payload data.
- Understand the relationship between HTTP requests and responses.

## Prerequisites

- Basic understanding of networking concepts.
- Wireshark installed on the system.
- A web browser for generating test traffic.

## Tools & Technologies

- **Wireshark** – Network protocol analyzer
- **HTTP** – Application-layer web communication protocol
- **TCP/IP** – Network communication stack
- **Web Browser** – Used to generate HTTP traffic

## Lab Setup

1. Install Wireshark from the official website: https://www.wireshark.org/download.html
2. Open Wireshark and identify the network interface currently connected to the network.
3. Use a controlled HTTP test environment or a site that intentionally provides HTTP traffic for educational analysis.

> **Note:** Most modern websites use HTTPS rather than plain HTTP. For this reason, an HTTP-specific lab should use an intentionally available HTTP test target or a local lab environment. Do not attempt to intercept traffic that you are not authorized to inspect.

## Visual Walkthrough

The following screenshots provide visual context for the Wireshark interface and HTTP traffic analysis workflow.

### Wireshark Packet Capture Interface

![Wireshark Packet Capture Interface](https://www.wireshark.org/docs/wsug_html_chunked/images/ws-main.png)

*Official Wireshark User's Guide screenshot showing the packet list, display-filter area, packet details, and packet bytes panes.*

### HTTP Request Sequence Analysis

![Wireshark HTTP Request Sequence Analysis](https://www.wireshark.org/docs/wsug_html_chunked/images/ws-stats-http-requestsequences.png)

*Official Wireshark documentation screenshot demonstrating HTTP request sequence analysis.*

> **Portfolio note:** These are reference screenshots from the official Wireshark documentation. Project-specific screenshots from an actual lab capture can be added to demonstrate the author's own hands-on analysis.

## Exercises

### Exercise 1: Capture HTTP Traffic

**Steps:**

1. Open Wireshark.
2. Select the active network interface.
3. Start the packet capture.
4. Generate HTTP traffic from the browser using an authorized test target.
5. Allow the traffic to complete.
6. Stop the capture.
7. Save the capture as a `.pcapng` file if required.

**Expected Result:**

A packet capture containing network traffic that can be inspected for HTTP communication.

### Exercise 2: Filter HTTP Traffic

Use the following Wireshark display filter:

```text
http
```

**Steps:**

1. Enter `http` in the Wireshark display-filter bar.
2. Apply the filter.
3. Review the packets identified as HTTP traffic.

**Expected Result:**

The packet list is limited to traffic identified by Wireshark as HTTP.

### Exercise 3: Analyze HTTP GET Requests

**Steps:**

1. Locate an HTTP GET request in the filtered capture.
2. Select the packet.
3. Expand the **Hypertext Transfer Protocol** section in the packet details pane.
4. Examine fields such as the request method, request URI, host, HTTP version, and headers.

**Key Observations:**

- HTTP request method
- Requested resource/URI
- Host header
- HTTP version
- User-Agent and other request headers

### Exercise 4: Analyze HTTP Responses

**Steps:**

1. Identify the HTTP response associated with the GET request.
2. Select the response packet.
3. Expand the **Hypertext Transfer Protocol** section.
4. Examine the response status code, headers, and content type.

**Key Observations:**

- HTTP status code
- Response headers
- Content type
- Content length
- Server-related information when exposed by the response

### Exercise 5: Follow the TCP Stream

**Steps:**

1. Select an HTTP packet that belongs to the conversation you want to inspect.
2. Right-click the packet.
3. Select **Follow → TCP Stream**.
4. Review the reconstructed TCP conversation.
5. Examine the HTTP request and response data exchanged within the stream.

**Expected Result:**

The TCP stream provides a consolidated view of the communication between the client and server, making it easier to understand the sequence of exchanged data.

## Security Considerations

Plain HTTP does not provide encryption for application-layer content. Depending on the application and traffic, sensitive information may therefore be exposed to someone who can observe the network traffic.

This project is intended for **authorized laboratory and educational environments only**. Capture and inspect traffic only when you have permission to do so.

## Skills Demonstrated

- Network packet capture
- Wireshark traffic analysis
- HTTP protocol analysis
- TCP stream analysis
- Network troubleshooting fundamentals
- Basic security traffic investigation

## Learning Outcomes

After completing this project, you should be able to use Wireshark to identify HTTP traffic, inspect HTTP requests and responses, understand packet-level web communication, and use TCP stream analysis to investigate network conversations.

## Project Structure

```text
Wireshark-HTTP-Traffic-Analysis/
└── README.md
```

## Conclusion

This hands-on lab provides a practical introduction to HTTP traffic analysis with Wireshark. The techniques demonstrated here form a foundation for network troubleshooting, SOC monitoring, incident investigation, and broader cybersecurity analysis.
