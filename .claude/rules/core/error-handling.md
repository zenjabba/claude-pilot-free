## Error Handling Standards

**Standards:** Fail fast | User-friendly messages | Graceful degradation | Resource cleanup

### Fail Fast and Explicitly

Validate input and check preconditions early. Fail with clear error messages rather than allowing invalid state.

Never return null or undefined to indicate errors - throw exceptions or return error types.

### User-Friendly Error Messages

Provide clear, actionable error messages without exposing technical details or security information.

Log technical details for debugging, show safe messages to users.

### Specific Exception Types

Use specific exception/error types rather than generic ones to enable targeted handling.

Create exception hierarchies for better organization and handling.

### Centralized Error Handling

Handle errors at appropriate boundaries (controllers, API layers) rather than scattering try-catch blocks everywhere.

Let exceptions bubble up to centralized handlers.

### Graceful Degradation

Design systems to degrade gracefully when non-critical services fail.

Distinguish critical failures (must stop) from non-critical (log and continue with reduced functionality).

### Retry Strategies

Implement exponential backoff for transient failures in external service calls.

**When to retry:** Network timeouts, temporary unavailability (503), rate limiting (429)

**When NOT to retry:** Bad requests (400), unauthorized (401), not found (404), business logic errors

### Resource Cleanup

Always clean up resources (file handles, connections, locks) in finally blocks or equivalent mechanisms.

Use context managers, using statements, defer, or try-finally patterns.

### Error Logging

Log errors for debugging while showing safe messages to users.

**What to log:** Error type, message, stack trace, request context, timestamp

**What NOT to log:** Passwords, credit cards, secrets, PII

### Exception Hierarchy

Create exception hierarchies for better error handling:
- Base application exception
- Category exceptions (validation, authentication, resource not found)
- Specific exceptions

Benefits: Catch broad categories or handle specific cases selectively.

### Frontend Error Handling

Use error boundaries or equivalent mechanisms to catch and display errors gracefully.

Log errors to monitoring services, show friendly fallback UI to users.

### Testing Error Handling

Always test error paths:
- Invalid input raises correct errors
- Error messages are clear
- Resources are cleaned up
- Errors are logged appropriately
- User sees safe messages

### Best Practices

**DO:**
- Validate early and fail fast
- Use specific exception types
- Centralize error handling at boundaries
- Log errors with context
- Clean up resources properly
- Implement retries for transient failures
- Provide user-friendly messages

**DON'T:**
- Catch exceptions without handling them
- Expose technical details to users
- Ignore errors or fail silently
- Use bare catch-all clauses
- Log sensitive information
- Retry non-idempotent operations blindly
