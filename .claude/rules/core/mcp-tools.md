## MCP Tools Available

**Standards:** Query first | Store learnings | Search before asking

### Memory & Search

**Cipher** (`mcp__cipher__ask_cipher`)
- Query patterns: "How did we implement X?"
- Store learnings: "Store: Fixed Y using Z pattern"
- Project memory and past decisions

**Claude Context** (`mcp__claude-context__`)
- `index_codebase(path)` - Index for semantic search
- `search_code(path, query)` - Search codebase
- `get_indexing_status(path)` - Check index status

### Development Tools

**IDE** (`mcp__ide__`)
- `getDiagnostics()` - Check errors/warnings
- `executeCode(code)` - Run code in Jupyter kernel (notebooks only)

**Database** (`mcp__dbhub-postgres__execute_sql`)
- Execute PostgreSQL queries

### Documentation & Research

**Ref** (`mcp__Ref__`)
- `ref_search_documentation(query)` - Search web/GitHub docs
- `ref_read_url(url)` - Read content from URL

**Context7** (`mcp__context7__`)
- `resolve-library-id(libraryName)` - Get library ID
- `get-library-docs(context7CompatibleLibraryID)` - Get docs

### Web Scraping & Crawling (FireCrawl via MCP Funnel)

**FireCrawl MCP server provides powerful web scraping tools via MCP Funnel:**

**Discover FireCrawl tools:**
```
mcp__mcp-funnel__discover_tools_by_words(words="firecrawl", enable=true)
```

**Available FireCrawl capabilities:**

1. **firecrawl_scrape** - Scrape single page (fastest, most reliable)
   - Best for: Single page content extraction
   - Returns: Markdown, HTML, or other formats
   - Use `maxAge` parameter for 500% faster cached scrapes

2. **firecrawl_search** - Web search with optional scraping
   - Best for: Finding information across multiple websites
   - Supports search operators: `site:`, `inurl:`, `intitle:`, etc.
   - Returns: Search results with optional scraped content

3. **firecrawl_map** - Discover all URLs on a website
   - Best for: Finding URLs before deciding what to scrape
   - Returns: Array of URLs found on site

4. **firecrawl_crawl** - Crawl entire website
   - Best for: Comprehensive coverage of multiple pages
   - Warning: Can be slow, may exceed token limits
   - Returns: Operation ID for status checking

5. **firecrawl_extract** - Extract structured data using LLM
   - Best for: Extracting specific structured data
   - Supports custom prompts and JSON schemas
   - Returns: Structured data as defined by schema

**Optimal workflow:** Search first with `firecrawl_search`, then scrape specific pages with `firecrawl_scrape`

### Tool Discovery

**MCP Funnel** (`mcp__mcp-funnel__`)
- `discover_tools_by_words(words, enable)` - Find tools by keywords
- `get_tool_schema(tool)` - Get tool parameters
- `bridge_tool_request(tool, arguments)` - Execute discovered tools

**When to use MCP Funnel:**
- Need web scraping/crawling (FireCrawl)
- Looking for specialized tools
- Exploring available capabilities

Use MCP Funnel to discover additional tools when needed - many more MCP servers available.

### Usage Patterns

**Start every task:**
1. `mcp__ide__getDiagnostics()` - Check existing errors
2. `mcp__cipher__ask_cipher("How did we do X?")` - Query knowledge
3. `mcp__claude-context__search_code(path, query)` - Find patterns

**End every task:**
1. `mcp__ide__getDiagnostics()` - Verify no new errors
2. `mcp__cipher__ask_cipher("Store: [learning]")` - Save knowledge

**When stuck:**
- Query Cipher for past solutions
- Search codebase for similar patterns
- Use Ref to find external documentation
- Use Context7 for library-specific docs
- Use MCP Funnel to discover specialized tools (e.g., FireCrawl for web scraping)
