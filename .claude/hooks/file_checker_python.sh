#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Change to workspace root if not already there
if [[ -d "/workspaces/claude-codepro" ]]; then
	cd /workspaces/claude-codepro || exit 1
fi

# Find THE most recently modified file (excluding cache/build dirs)
files=$(find . -type f -not -path '*/.ruff_cache/*' -not -path '*/__pycache__/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/.git/*' -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

# Exit if no files found, not Python, or test files
[[ -z $files ]] && exit 0
[[ $files != *.py ]] && exit 0
[[ $files == *test* || $files == *spec* ]] && exit 0

# Get absolute path and find nearest .venv
file_abs_path=$(realpath "$files")
PROJECT_ROOT=""
current_dir=$(dirname "$file_abs_path")
while [[ $current_dir != "/" ]]; do
	if [[ -d "$current_dir/.venv" ]]; then
		PROJECT_ROOT="$current_dir"
		break
	fi
	current_dir=$(dirname "$current_dir")
done

# Exit if no venv found
[[ -z $PROJECT_ROOT ]] && exit 0

# Define tools with their venv paths
declare -A TOOLS=(
	[ruff]="$PROJECT_ROOT/.venv/bin/ruff"
	[basedpyright]="$PROJECT_ROOT/.venv/bin/basedpyright"
	[mypy]="$PROJECT_ROOT/.venv/bin/mypy"
)

# Auto-format before checks
if [[ -x ${TOOLS[ruff]} ]]; then
	${TOOLS[ruff]} check --select I,RUF022 --fix "$files" >/dev/null 2>&1 || true
	${TOOLS[ruff]} format "$files" >/dev/null 2>&1 || true
fi

# Run tool check and store results
run_check() {
	local tool=$1
	local bin=${TOOLS[$tool]}
	[[ ! -x $bin ]] && return 1

	case $tool in
	ruff)
		output=$($bin check "$files" 2>&1 || true)
		[[ -n $output && $output != *"All checks passed"* ]]
		;;
	basedpyright)
		output=$(cd "$PROJECT_ROOT" && $bin --pythonpath "$PROJECT_ROOT/.venv/bin/python" --outputjson "$file_abs_path" 2>&1 || true)
		echo "$output" | grep -qE '"errorCount":\s*[1-9]|" error"'
		;;
	mypy)
		output=$(cd "$PROJECT_ROOT" && $bin "$file_abs_path" 2>&1 || true)
		echo "$output" | grep -qE 'error:' && [[ $output != *"Success:"* ]]
		;;
	esac
}

# Display tool results
display_result() {
	local tool=$1
	local emoji icon error_count

	case $tool in
	ruff)
		emoji="🔧"
		icon="Ruff"
		error_count=$(echo "$output" | grep -c "^F[0-9]\|^E[0-9]\|^W[0-9]" 2>/dev/null || echo "0")
		[[ $error_count -eq 1 ]] && plural="issue" || plural="issues"
		echo "" >&2
		echo "$emoji $icon: $error_count $plural" >&2
		echo "───────────────────────────────────────" >&2
		echo "$output" | grep -E "^(F[0-9]|E[0-9]|W[0-9])" | while IFS= read -r line; do
			code=$(echo "$line" | grep -oP "^[FEW][0-9]+")
			msg=$(echo "$line" | sed -E "s/^[FEW][0-9]+\s+(\[\*\]\s+)?//")
			echo "  $code: $msg" >&2
		done
		;;
	basedpyright)
		emoji="🐍"
		icon="BasedPyright"
		error_count=$(echo "$output" | grep -oP '"errorCount":\s*\K\d+' | head -1)
		[[ -z $error_count ]] && error_count=0
		[[ $error_count -eq 1 ]] && plural="issue" || plural="issues"
		echo "" >&2
		echo "$emoji $icon: $error_count $plural" >&2
		echo "───────────────────────────────────────" >&2
		echo "$output" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for diag in data.get('generalDiagnostics', []):
    file = diag.get('file', '').split('/')[-1]
    line = diag.get('range', {}).get('start', {}).get('line', 0)
    msg = diag.get('message', '').split('\n')[0]
    print(f'  {file}:{line} - {msg}')
" >&2
		;;
	mypy)
		emoji="🔍"
		icon="Mypy"
		error_count=$(echo "$output" | grep -c "error:" 2>/dev/null || echo "0")
		[[ $error_count -eq 1 ]] && plural="issue" || plural="issues"
		echo "" >&2
		echo "$emoji $icon: $error_count $plural" >&2
		echo "───────────────────────────────────────" >&2
		echo "$output" | grep "error:" >&2
		;;
	esac

	echo "" >&2
}

# Run all checks
has_issues=false
declare -A results
for tool in ruff basedpyright mypy; do
	if run_check "$tool"; then
		has_issues=true
		results[$tool]="$output"
	fi
done

# Display results
if [[ $has_issues == true ]]; then
	echo "" >&2
	echo -e "${RED}🛑 Python Issues found in: $files${NC}" >&2
	echo "" >&2

	for tool in ruff basedpyright mypy; do
		if [[ -n ${results[$tool]} ]]; then
			output="${results[$tool]}"
			display_result "$tool"
		fi
	done

	echo -e "${RED}Fix Python issues above before continuing${NC}" >&2
	exit 2
else
	echo "" >&2
	echo -e "${GREEN}✅ Python: All checks passed${NC}" >&2
	exit 2
fi
