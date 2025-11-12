## Input Validation Standards

**Standards:** Server-side validation | Fail early | Specific errors | Sanitize input

### Server-Side Validation is Mandatory

Always validate on the server. Never trust client-side validation alone.

**Why:** Users can bypass client validation, malicious actors can send requests directly, APIs must be secure by default

### Client-Side for User Experience

Use client-side validation for immediate feedback, but duplicate all checks server-side.

### Fail Early

Validate input as early as possible and reject invalid data before processing.

Avoid wasting resources on invalid requests - check first, process later.

### Specific Error Messages

Provide clear, field-specific error messages that help users correct their input.

Return structured errors with field names and specific reasons, not generic "Invalid data" messages.

### Allowlists Over Blocklists

Define what is allowed rather than trying to block everything that's not.

Use patterns to specify valid formats instead of listing forbidden characters.

### Type and Format Validation

Check systematically:
- Required fields present
- Data types correct
- Formats valid (email, phone, date, etc.)
- Ranges appropriate (age 18-120, amount > 0)
- Lengths within limits

### Sanitize Input

Prevent injection attacks:

**SQL Injection:** Use parameterized queries, never string concatenation
**XSS:** Escape HTML special characters in output
**Command Injection:** Use list arguments, never shell=True with user input

### Business Rule Validation

Validate at appropriate layer:
- Format/type validation: Input layer
- Business rules: Service layer (sufficient balance, valid dates, authorization)
- Data integrity: Database constraints

### Consistent Validation Across Entry Points

Apply same validation everywhere:
- Web forms
- API endpoints
- Background jobs
- Batch imports
- Internal APIs

Share validation logic - don't duplicate rules.

### Validation Libraries

Use validation libraries for complex schemas:
- Pydantic for Python
- Joi for Node.js
- Class-validator for TypeScript
- ActiveModel for Rails

### Testing Validation

Test all validation rules:
- Valid input accepted
- Invalid input rejected
- Error messages correct
- Edge cases covered
- Business rules enforced

### Best Practices

**DO:**
- Always validate server-side
- Use client-side for UX
- Fail early
- Provide specific errors
- Use allowlists
- Sanitize input
- Apply consistently

**DON'T:**
- Trust client-side validation
- Use generic error messages
- Process before validating
- Use blocklists for security
- Skip validation in batch jobs
- Allow SQL injection through string concatenation
