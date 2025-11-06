# CLAUDE.local.md

## Core Rules

**Git:** READ-ONLY - `git status/diff/log/show/branch` ✅ | `git add/commit/push` ❌
**Python:** `uv` not pip | One-line docstrings | No inline comments | Edit > Create
**Standards:** TDD mandatory | DRY/YAGNI | Clean imports | Check diagnostics before/after
**Evidence:** Show actual output, never claim "should work" | Tests must pass AND code must execute

## MCP Servers Available

### Memory & Search
- **Cipher** (`mcp__cipher__ask_cipher`) - Query patterns, store learnings, project memory
- **Claude Context** (`mcp__claude-context__`) - Index & search codebase semantically
  - `index_codebase(path)` - Index for searching
  - `search_code(path, query)` - Semantic search
  - `get_indexing_status(path)` - Check index status

### Development Tools
- **IDE** (`mcp__ide__`) - VS Code integration
  - `getDiagnostics()` - Check errors/warnings
  - `executeCode(code)` - Run Python in Jupyter kernel (notebooks only)
- **Database** (`mcp__dbhub-postgres__execute_sql`) - PostgreSQL queries

### Documentation & Research
- **Ref** (`mcp__Ref__`) - Search web/GitHub docs
  - `ref_search_documentation(query)` - Find docs
  - `ref_read_url(url)` - Read content from URL
- **Context7** (`mcp__context7__`) - Library documentation
  - `resolve-library-id(libraryName)` - Get library ID
  - `get-library-docs(context7CompatibleLibraryID)` - Get docs

### Web Scraping & Search
- **Firecrawl** (`mcp__firecrawl__`) - Web scraping/search
  - `mcp__firecrawl-mcp__firecrawl_scrape(url, formats)` - Scrape single URL
  - `mcp__firecrawl-mcp__firecrawl_search(query, sources)` - Search web
  - `mcp__firecrawl-mcp__firecrawl_extract(urls, schema)` - Extract structured data
  - `mcp__firecrawl-mcp__firecrawl_map(url)` - Map website URLs
  - `mcp__firecrawl-mcp__firecrawl_crawl(url)` - Crawl website

### Tool Discovery
- **MCP Funnel** (`mcp__mcp-funnel__`) - Discover/bridge tools
  - `discover_tools_by_words(words, enable)` - Find tools
  - `get_tool_schema(tool)` - Get tool parameters
  - `bridge_tool_request(tool, arguments)` - Execute discovered tools

## Available Skills

**Testing:** @testing-test-driven-development | @testing-debugging | @testing-final-verification
**Global:** @global-coding-style | @global-error-handling | @global-validation
**Backend:** @backend-api | @backend-models | @backend-queries | @backend-migrations
**Frontend:** @frontend-accessibility | @frontend-components | @frontend-css | @frontend-responsive
