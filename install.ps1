<#
.SYNOPSIS
  CareerExpert — 全能型 AI 原生求职与学术 CV 工作流系统
  Multi-Skills 矩阵跨 Harness 一键安装器 (Windows PowerShell)

.DESCRIPTION
  一键将全套 CareerExpert 技能矩阵部署至当前用户或指定项目的全局 Agent 环境：
  - /career-ops        -> 全流程求职与学术工作流总指挥
  - /career-style      -> UI 视觉排版、HTML/CSS 调色与单页高度契合 (内容锁定)
  - /career-polish     -> Google XYZ / HBS PAR 经历战果量化改写 (样式锁定)
  - /career-cv         -> 出国留学与海外硕博学术 CV (Harvard/MIT 规范)
  - /career-interview  -> 四级提示交互式模拟面试攻防与复盘
  - /career-coach      -> 简历通盘掌握、经历软肋排雷与精美答辩复习手册生成

.PARAMETER Target
  目标环境: All (默认), Claude, Agents, Antigravity, Codex, Local
#>

[CmdletBinding()]
param(
    [ValidateSet("All", "Claude", "Agents", "Antigravity", "Codex", "Local")]
    [string]$Target = "All",
    [string]$CustomPath = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  CareerExpert — Multi-Skills 技能矩阵与 Slash 命令" -ForegroundColor Cyan
Write-Host "  跨 Harness 一键安装器 (Windows)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$SkillsBase = Join-Path $ScriptDir "skills"

function Install-Skills([string]$DestSkillsDir, [string]$PlatformName) {
    Write-Host "`n[*] 正在部署技能矩阵至 $PlatformName : $DestSkillsDir ..." -ForegroundColor Yellow
    if (-not (Test-Path $DestSkillsDir)) {
        New-Item -ItemType Directory -Path $DestSkillsDir -Force | Out-Null
    }

    # 清理旧命名空间残留以避免命令重复
    $legacySkills = @("job-finding", "resume-style", "resume-polish", "academic-cv", "mock-interview")
    foreach ($leg in $legacySkills) {
        $legPath = Join-Path $DestSkillsDir $leg
        if (Test-Path $legPath) {
            Remove-Item -Path $legPath -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    Get-ChildItem -Directory $SkillsBase | ForEach-Object {
        $skillName = $_.Name
        $targetSkillPath = Join-Path $DestSkillsDir $skillName
        if (-not (Test-Path $targetSkillPath)) {
            New-Item -ItemType Directory -Path $targetSkillPath -Force | Out-Null
        }
        Copy-Item -Path (Join-Path $_.FullName "*") -Destination $targetSkillPath -Recurse -Force
        Write-Host "  [+] 成功安装技能: $skillName" -ForegroundColor DarkGreen
    }
    Write-Host "[✓] 成功部署技能矩阵至 $PlatformName" -ForegroundColor Green
}

function Cleanup-Legacy-Commands([string]$DestCommandsDir) {
    if (Test-Path $DestCommandsDir) {
        # 清理旧的裸命令，避免在 Claude 中与 skill 重复
        $legacyCommands = @("resume.md", "style.md", "polish.md", "cv.md", "interview.md")
        foreach ($cmd in $legacyCommands) {
            $cmdPath = Join-Path $DestCommandsDir $cmd
            if (Test-Path $cmdPath) {
                Remove-Item -Path $cmdPath -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

if ($CustomPath -ne "") {
    Install-Skills -DestSkillsDir $CustomPath -PlatformName "自定义目录"
    exit 0
}

$HomeDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)

if ($Target -eq "Claude" -or $Target -eq "All") {
    $ClaudeSkills = Join-Path $HomeDir ".claude\skills"
    $ClaudeCommands = Join-Path $HomeDir ".claude\commands"
    Install-Skills -DestSkillsDir $ClaudeSkills -PlatformName "Claude Code 全局"
    Cleanup-Legacy-Commands -DestCommandsDir $ClaudeCommands
}

if ($Target -eq "Agents" -or $Target -eq "All") {
    $AgentsSkills = Join-Path $HomeDir ".agents\skills"
    Install-Skills -DestSkillsDir $AgentsSkills -PlatformName "Agents 全局"
}

if ($Target -eq "Antigravity" -or $Target -eq "All") {
    $AntigravitySkills = Join-Path $HomeDir ".gemini\config\skills"
    Install-Skills -DestSkillsDir $AntigravitySkills -PlatformName "Antigravity 全局"
}

if ($Target -eq "Codex" -or $Target -eq "All") {
    $CodexSkills = Join-Path $HomeDir ".codex\skills"
    Install-Skills -DestSkillsDir $CodexSkills -PlatformName "Codex 全局"
}

if ($Target -eq "Local") {
    $LocalPath = Join-Path (Get-Location) ".agents\skills"
    Install-Skills -DestSkillsDir $LocalPath -PlatformName "当前本地工程"
}

Write-Host "`n====================================================" -ForegroundColor Cyan
Write-Host "  ✨ CareerExpert 技能矩阵部署完成 (唯一命名空间)！" -ForegroundColor Cyan
Write-Host "  可用原生 Slash 快捷指令：" -ForegroundColor Cyan
Write-Host "    - /career-ops        -> 全流程求职与学术规划总指挥" -ForegroundColor White
Write-Host "    - /career-style      -> 简历 UI 视觉排版调优 (文字绝对锁定)" -ForegroundColor White
Write-Host "    - /career-polish     -> Google XYZ 战果量化改写 (排版绝对锁定)" -ForegroundColor White
Write-Host "    - /career-cv         -> 出国留学海外硕博学术 CV (Harvard 规范)" -ForegroundColor White
Write-Host "    - /career-interview  -> 四级渐进式模拟面试攻防与复盘" -ForegroundColor White
Write-Host "    - /career-coach      -> 简历通盘掌握、经历软肋排雷与答辩复习手册生成" -ForegroundColor White
Write-Host "====================================================" -ForegroundColor Cyan
