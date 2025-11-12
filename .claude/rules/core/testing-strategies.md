## Testing Strategies and Coverage

**Standards:** Unit tests | Integration tests | E2E tests | Coverage ≥ 80%

### Test Organization

```
tests/
├── unit/              # Fast, isolated tests
├── integration/       # Component interaction tests
└── e2e/              # End-to-end tests
    └── postman/      # API collections
```

### Unit Testing

**Purpose:** Test individual functions/methods in isolation

**Characteristics:**
- Fast (< 1ms per test)
- No external dependencies
- Mock/stub external services
- Test one thing per test

**When to use:** Pure functions, business logic, data transformations, validation rules

**Mark tests:** Use test markers/decorators to distinguish unit from integration

### Integration Testing

**Purpose:** Test component interactions and integrations

**Characteristics:**
- Slower than unit tests
- Use real dependencies (databases, APIs)
- Test data flow between components
- Setup/teardown fixtures

**When to use:** Database operations, API integrations, message queues, file system operations

### E2E Testing for APIs (Newman/Postman)

**Purpose:** Test complete user workflows and API interactions

**Create Postman collections** with:
- Health check endpoints
- Authentication flows
- CRUD operations
- Error scenarios
- Chained requests (save ID from response, use in next request)

**Environment configuration:**
- base_url, api_key, and other variables
- Separate environments: dev, staging, production

**Run with Newman:**
```bash
newman run postman/collections/api-tests.json \
  -e postman/environments/dev.json \
  --reporters cli,json
```

**Test assertions:**
- Status codes
- Response times
- JSON structure
- Field values
- Save variables between requests

**When to use:** REST APIs, authentication flows, complete workflows, load testing, CI/CD pipelines

### E2E Testing for Data Pipelines

**Purpose:** Verify end-to-end data flow and transformations

**Verification:**
- Data extracted from source
- Transformations applied correctly
- Data loaded to destination
- Data quality checks pass
- Logs show expected behavior

### Coverage Requirements

**Minimum coverage: 80%**

Run tests with coverage reporting to identify untested code.

**What to cover:**
- All business logic
- All API endpoints
- All data transformations
- All validation rules
- Error handling paths

**What to skip:** Main blocks, generated code, configuration files, simple getters/setters

### Test Fixtures and Setup

Use fixtures for reusable test setup:
- Database sessions
- Sample data
- Mock objects
- Temporary files

### Test Naming Conventions

Follow pattern: `test_<function>_<scenario>_<expected_result>`

Be descriptive - test name should explain what's being tested.

### Running Tests

**Run all tests:** Standard test runner command
**Run by type:** Unit only, integration only, E2E only (using markers/tags)
**Run specific file:** Target individual test file
**Run specific test:** Target individual test function
**Show output:** Enable print statements for debugging

### CI/CD Integration

Run tests in order:
1. Fast unit tests
2. Integration tests
3. Coverage check (fail if < 80%)
4. E2E tests (if API exists)

### Best Practices

**DO:**
- Write tests before implementation (TDD)
- Keep tests fast and focused
- Use descriptive test names
- Test edge cases and errors
- Mock external dependencies in unit tests
- Use real dependencies in integration tests

**DON'T:**
- Write tests that depend on each other
- Test implementation details
- Ignore failing tests
- Skip error paths
- Write flaky tests
- Leave commented-out tests
