import {
  Workflow,
  FileCode2,
  Plug2,
  ShieldCheck,
  Container,
  Infinity as InfinityIcon,
  Users,
  GitBranch,
} from "lucide-react";
import { useInView } from "@/hooks/use-in-view";
import ImageModal from "@/components/ImageModal";

interface InsideItem {
  icon: React.ElementType;
  title: string;
  description: string;
  items: string[];
}

const insideItems: InsideItem[] = [
  {
    icon: InfinityIcon,
    title: "Endless Mode",
    description: "Never lose context mid-task",
    items: [
      "Context monitor with 80% / 90% / 95% thresholds",
      "Automatic session handoff with state preservation",
      "Crash recovery with exponential backoff (max 3 retries)",
      "Multiple Pilot sessions in parallel, zero interference",
      "Persistent memory bridges observations across all sessions",
    ],
  },
  {
    icon: Workflow,
    title: "Spec-Driven Development",
    description: "Structured planning with verification",
    items: [
      "Plan: semantic search, clarifying questions, markdown spec",
      "Approve: human review gate before any code is written",
      "Implement: mandatory TDD — RED, GREEN, REFACTOR cycle",
      "Verify: sub-agent code review + full test suite",
      "Automatic loop-back if verification finds issues",
    ],
  },
  {
    icon: ShieldCheck,
    title: "Quality Automation",
    description: "7 hooks enforce standards on every edit",
    items: [
      "TDD enforcer — warns if no failing test before code change",
      "Python: ruff format + lint + basedpyright type checking",
      "TypeScript: Prettier + ESLint + vtsls type checking",
      "Go: gofmt + golangci-lint + gopls type checking",
      "Status line — live context, memory, plan, and license info",
    ],
  },
  {
    icon: FileCode2,
    title: "Rules, Commands & Skills",
    description: "21 rules, 6 commands, 14 skills",
    items: [
      "21 rules (2,800+ lines) loaded into every session",
      "/spec, /sync, /learn — structured workflows",
      "14 coding standard skills activated on demand",
      "Custom rules, commands, skills survive updates",
      "/sync: 11-phase codebase analysis and documentation",
    ],
  },
  {
    icon: Plug2,
    title: "Enhanced Context",
    description: "5 MCP servers + 3 language servers",
    items: [
      "Pilot Console at localhost:41777 — visual dashboard",
      "Persistent memory with semantic search (Vexor)",
      "Context7 library docs + grep-mcp GitHub search",
      "LSP: basedpyright, vtsls, gopls — real-time diagnostics",
      "Agent browser for E2E UI testing",
    ],
  },
  {
    icon: Container,
    title: "One-Command Installer",
    description: "Ready in minutes, auto-updates",
    items: [
      "8-step installer with progress, rollback, and idempotent re-runs",
      "Dev Container auto-setup with all tools pre-configured",
      "Auto-updater with release notes and one-key upgrade",
      "Shell integration: bash, fish, zsh with pilot alias",
      "macOS, Linux, Windows (WSL2) support",
    ],
  },
  {
    icon: Users,
    title: "Team Vault",
    description: "Share knowledge across your team",
    items: [
      "Private Git repo for shared rules, commands, skills",
      "Pull shared assets from your team's vault",
      "Push custom rules and skills to teammates",
      "Automatic versioning (v1, v2, v3...)",
      "Works with GitHub, GitLab, Bitbucket",
    ],
  },
  {
    icon: GitBranch,
    title: "Online Learning",
    description: "Captures discoveries as reusable skills",
    items: [
      "Extracts non-obvious debugging patterns automatically",
      "Captures workarounds and tool integration knowledge",
      "Creates .claude/skills/ with proper frontmatter",
      "Triggered by 10+ minute investigation sessions",
      "Quality gates verify content is reusable",
    ],
  },
];

const WhatsInside = () => {
  const [headerRef, headerInView] = useInView<HTMLDivElement>();
  const [gridRef, gridInView] = useInView<HTMLDivElement>();

  const animationDelays = [
    "animation-delay-0",
    "animation-delay-100",
    "animation-delay-200",
    "animation-delay-300",
    "animation-delay-400",
    "animation-delay-500",
    "animation-delay-0",
    "animation-delay-100",
  ];

  return (
    <section id="features" className="py-16 lg:py-24 px-4 sm:px-6 relative">
      <div className="max-w-6xl mx-auto">
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-border to-transparent" />

        {/* Header */}
        <div
          ref={headerRef}
          className={`text-center mb-16 ${headerInView ? "animate-fade-in-up" : "opacity-0"}`}
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-foreground mb-4">
            What's Inside
          </h2>
          <p className="text-muted-foreground text-lg sm:text-xl max-w-3xl mx-auto">
            A production-grade system — not a prompt template. Every component is designed to enforce
            quality, preserve context, and automate verification across your entire development workflow.
          </p>
        </div>

        {/* Feature Grid */}
        <div
          ref={gridRef}
          className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5"
        >
          {insideItems.map((item, index) => {
            const Icon = item.icon;
            return (
              <div
                key={item.title}
                className={`group relative rounded-2xl p-5 border border-border/50 bg-card/30 backdrop-blur-sm
                  hover:border-primary/50 hover:bg-card/50 hover:shadow-lg hover:shadow-primary/5
                  hover:-translate-y-1 transition-all duration-300
                  ${gridInView ? `animate-fade-in-up ${animationDelays[index]}` : "opacity-0"}`}
              >
                {/* Icon and Title */}
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center
                    group-hover:bg-primary/20 group-hover:scale-110 transition-all duration-300">
                    <Icon className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-base font-semibold text-foreground">
                      {item.title}
                    </h3>
                    <p className="text-[11px] text-muted-foreground">
                      {item.description}
                    </p>
                  </div>
                </div>

                {/* Feature List */}
                <ul className="space-y-1.5 mt-3">
                  {item.items.map((listItem, i) => (
                    <li
                      key={i}
                      className="text-muted-foreground text-xs flex items-start gap-1.5"
                    >
                      <span className="text-primary mt-0.5 text-[10px]">&#x25B8;</span>
                      <span className="group-hover:text-foreground/80 transition-colors duration-200">
                        {listItem}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* Subtle gradient overlay on hover */}
                <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
              </div>
            );
          })}
        </div>

        {/* Console Screenshot */}
        <div className={`mt-16 ${gridInView ? "animate-fade-in-up animation-delay-500" : "opacity-0"}`}>
          <div className="text-center mb-6">
            <h3 className="text-xl sm:text-2xl font-semibold text-foreground mb-2">
              Pilot Console
            </h3>
            <p className="text-muted-foreground text-sm sm:text-base">
              Visual dashboard at localhost:41777 — real-time observations, session management, and semantic search
            </p>
          </div>
          <div className="relative rounded-xl overflow-hidden border border-border/50 shadow-2xl shadow-primary/10 max-w-4xl mx-auto">
            <ImageModal
              src="/console.png"
              alt="Claude Pilot Console Dashboard"
              className="w-full rounded-xl"
            />
            <p className="text-xs text-muted-foreground text-center mt-2 mb-1">Click to enlarge</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default WhatsInside;
