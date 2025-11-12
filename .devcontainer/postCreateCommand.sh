#!/usr/bin/env bash

# Install zsh fzf
echo -e "\nsource <(fzf --zsh)" >>~/.zshrc

# Enable dotenv plugin for automatic .env loading
# This will auto-load .env files when you cd into directories
if ! grep -q "plugins=.*dotenv" ~/.zshrc; then
    # Add dotenv to plugins array if not already present
    sed -i 's/plugins=(/plugins=(dotenv /' ~/.zshrc

    # Disable prompt for auto-loading .env (trust dev container environment)
    echo -e "\n# Auto-load .env files without prompting" >>~/.zshrc
    echo 'export ZSH_DOTENV_PROMPT=false' >>~/.zshrc
fi

# Install uv venv for Python and sync Commands and Skills
uv sync --frozen
uv run /workspaces/claude-codepro/.claude/rules/builder.py

# Install qlty fresh and initialize
if [ -d "/workspaces/claude-codepro/.qlty" ]; then
    find /workspaces/claude-codepro/.qlty -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
    find /workspaces/claude-codepro/.qlty -mindepth 1 -maxdepth 1 -type l -delete
    find /workspaces/claude-codepro/.qlty -mindepth 1 -maxdepth 1 -type f ! -name 'qlty.toml' ! -name '.gitignore' -delete
fi
curl https://qlty.sh | sh
echo -e "\nexport QLTY_INSTALL=\"$HOME/.qlty\"" >>~/.zshrc
echo -e 'export PATH=$QLTY_INSTALL/bin:$PATH' >>~/.zshrc
/root/.qlty/bin/qlty check --install-only

# Install Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# Install CC Statusline
curl -fsSL https://raw.githubusercontent.com/hagan/claudia-statusline/main/scripts/quick-install.sh | bash

# Install Dotenvx CLI
curl -sfS https://dotenvx.sh | bash

# Install CodeRabbit CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Install Cipher
npm install -g @byterover/cipher

# Install Newman
npm install -g newman

# Start Local Postgres with Docker Compose on Port 5433
docker-compose -f .devcontainer/docker-compose.yml up -d

# Add cc alias for Claude Code with rule builder
# Runs rule_builder.py before starting Claude Code to ensure commands/skills are up-to-date
{
    echo ""
    echo "# Claude Code quick alias"
    echo 'alias cc="cd /workspaces/claude-codepro && uv run .claude/rules/builder.py && clear && dotenvx run claude"'
} | tee -a ~/.bashrc ~/.zshrc >/dev/null

# Print finish message
echo ""
echo "======================================================================"
echo "✅ Dev Container Build Complete!"
echo "======================================================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Configure your environment:"
echo "   cp .env.example .env"
echo "   vim .env  # Add your API keys and credentials"
echo ""
echo "2. Run setup commands:"
echo "   cc  # Setup Claude Code"
echo "   cr  # Setup CodeRabbit CLI"
echo ""
echo "3. Configure Claude Code:"
echo "   - Run /config to set auto-connect to IDE=true, Auto-compact=false"
echo "   - Run /ide to connect to VS Code diagnostics"
echo "   - Run /mcp to verify all MCP servers are online"
echo ""
echo "4. Start coding:"
echo "   - Use /quick to implement small tasks quickly"
echo "   - Use /plan to create a spec with clarifying questions"
echo "   - Use /implement to execute with automatic TDD"
echo "   - Use /verify to run AI code review and quality checks"
echo ""
echo "📚 For more details, see the README.md"
echo "======================================================================"
echo ""
