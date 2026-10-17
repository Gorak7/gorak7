package com.gorak.qa.bookstore;

/**
 * Evidence workflow notes:
 * - Import postman/Online-Bookstore.postman_collection.json into Postman and run it
 *   against http://localhost:8081.
 * - Save actual response/assertion screenshots in ../evidence/.
 * - Run the SQL statements in ../database/validation.sql and capture the query output.
 * - GitHub Actions uploads the Maven Surefire report as a workflow artifact.
 *
 * This class intentionally contains no fake screenshots or pre-filled test outcomes.
 */
final class BookstoreEvidenceNote { private BookstoreEvidenceNote() {} }
