<#
.SYNOPSIS
  CareerOps — 全能型 AI 原生求职与学术 CV 工作流系统
  Multi-Skills 矩阵与 Slash 快捷命令跨平台一键安装器 (Windows PowerShell)

.DESCRIPTION
  一键将全套 CareerOps 技能矩阵与 Slash 命令部署至当前用户或指定项目的全局 Agent 环境：
  - /resume    -> 唤起 career-ops (全流程定制与追踪)
  - /style     -> 唤起 resume-style (UI/CSS 换色与排版调优)
  - /polish    -> 唤起 resume-polish (Google XYZ 战果量化改写)
  - /cv        -> 唤起 academic-cv (海外高校硕博学术 CV)
  - /interview -> 唤起 mock-interview (四级提示模拟面试攻防)
  - .claude/commands/* (/resume, /style, /polish, /cv, /interview)

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
Write-Host "  CareerOps — Multi-Skills 技能矩阵与 Slash 命令" -ForegroundColor Cyan
Write-Host "  跨 Harness 一键安装器 (Windows)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$SkillsBase = Join-Path $ScriptDir "skills"
$CommandsBase = Join-Path $ScriptDir ".claude\commands"

function Install-Skills([string]$DestSkillsDir, [string]$PlatformName) {
    Write-Host "`n[*] 正在部署技能矩阵至 $PlatformName : $DestSkillsDir ..." -ForegroundColor Yellow
    if (-not (Test-Path $DestSkillsDir)) {
        New-Item -ItemType Directory -Path $DestSkillsDir -Force | Out-Null
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

function Install-Commands([string]$DestCommandsDir) {
    if (Test-Path $CommandsBase) {
        Write-Host "`n[*] 正在部署 Slash 快捷指令至 : $DestCommandsDir ..." -ForegroundColor Yellow
        if (-not (Test-Path $DestCommandsDir)) {
            New-Item -ItemType Directory -Path $DestCommandsDir -Force | Out-Null
        }
        Copy-Item -Path (Join-Path $CommandsBase "*") -Destination $DestCommandsDir -Recurse -Force
        Write-Host "[✓] 成功安装快捷指令: /resume, /style, /polish, /cv, /interview" -ForegroundColor Green
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
    Install-Commands -DestCommandsDir $ClaudeCommands
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
Write-Host "  ✨ 技能矩阵与 Slash 命令部署完成！" -ForegroundColor Cyan
Write-Host "  可用快捷指令与技能：" -ForegroundColor Cyan
Write-Host "    - /resume    -> 唤起 career-ops (全流程定制与追踪)" -ForegroundColor White
Write-Host "    - /style     -> 唤起 resume-style (UI/CSS 换色与排版调优)" -ForegroundColor White
Write-Host "    - /polish    -> 唤起 resume-polish (Google XYZ 战果量化改写)" -ForegroundColor White
Write-Host "    - /cv        -> 唤起 academic-cv (海外高校硕博学术 CV)" -ForegroundColor White
Write-Host "    - /interview -> 唤起 mock-interview (四级提示模拟面试攻防)" -ForegroundColor White
Write-Host "====================================================" -ForegroundColor Cyan
