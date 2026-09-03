#!/usr/bin/env bash
# ==============================================================================
# CareerOps — 全能型 AI 原生求职与学术 CV 工作流系统
# Multi-Skills 矩阵与 Slash 快捷命令跨平台一键安装器 (Linux/macOS)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-all}"
CUSTOM_PATH="${2:-}"

echo -e "\033[36m====================================================\033[0m"
echo -e "\033[36m  CareerOps — Multi-Skills 技能矩阵与 Slash 命令\033[0m"
echo -e "\033[36m  跨 Harness 一键安装器 (Linux/macOS)\033[0m"
echo -e "\033[36m====================================================\033[0m"

SKILLS_BASE="${SCRIPT_DIR}/skills"
COMMANDS_BASE="${SCRIPT_DIR}/.claude/commands"

install_skills() {
    local dest_skills_dir="$1"
    local platform_name="$2"

    echo -e "\n\033[33m[*] 正在部署技能矩阵至 ${platform_name} : ${dest_skills_dir} ...\033[0m"
    mkdir -p "${dest_skills_dir}"

    for skill_dir in "${SKILLS_BASE}"/*; do
        if [ -d "${skill_dir}" ]; then
            skill_name="$(basename "${skill_dir}")"
            mkdir -p "${dest_skills_dir}/${skill_name}"
            cp -R "${skill_dir}/"* "${dest_skills_dir}/${skill_name}/"
            echo -e "  \033[32m[+] 成功安装技能: ${skill_name}\033[0m"
        fi
    done
    echo -e "\033[32m[✓] 成功部署技能矩阵至 ${platform_name}\033[0m"
}

install_commands() {
    local dest_commands_dir="$1"
    if [ -d "${COMMANDS_BASE}" ]; then
        echo -e "\n\033[33m[*] 正在部署 Slash 快捷指令至 : ${dest_commands_dir} ...\033[0m"
        mkdir -p "${dest_commands_dir}"
        cp -R "${COMMANDS_BASE}/"* "${dest_commands_dir}/"
        echo -e "\033[32m[✓] 成功安装快捷指令: /resume, /style, /polish, /cv, /interview\033[0m"
    fi
}

if [ -n "$CUSTOM_PATH" ]; then
    install_skills "$CUSTOM_PATH" "自定义目录"
    exit 0
fi

USER_HOME="$HOME"

if [ "$TARGET" = "claude" ] || [ "$TARGET" = "all" ]; then
    install_skills "${USER_HOME}/.claude/skills" "Claude Code 全局"
    install_commands "${USER_HOME}/.claude/commands"
fi

if [ "$TARGET" = "agents" ] || [ "$TARGET" = "all" ]; then
    install_skills "${USER_HOME}/.agents/skills" "Agents 全局"
fi

if [ "$TARGET" = "antigravity" ] || [ "$TARGET" = "all" ]; then
    install_skills "${USER_HOME}/.gemini/config/skills" "Antigravity 全局"
fi

if [ "$TARGET" = "codex" ] || [ "$TARGET" = "all" ]; then
    install_skills "${USER_HOME}/.codex/skills" "Codex 全局"
fi

if [ "$TARGET" = "local" ]; then
    install_skills "$(pwd)/.agents/skills" "当前本地工程"
fi

echo -e "\n\033[36m====================================================\033[0m"
echo -e "\033[36m  ✨ 技能矩阵与 Slash 命令部署完成！\033[0m"
echo -e "\033[36m  可用快捷指令与技能：\033[0m"
echo -e "    - \033[37m/resume    -> 唤起 career-ops (全流程定制与追踪)\033[0m
    - \033[37m/style     -> 唤起 resume-style (UI/CSS 换色与排版调优)\033[0m
    - \033[37m/polish    -> 唤起 resume-polish (Google XYZ 战果量化改写)\033[0m
    - \033[37m/cv        -> 唤起 academic-cv (海外高校硕博学术 CV)\033[0m
    - \033[37m/interview -> 唤起 mock-interview (四级提示模拟面试攻防)\033[0m"
echo -e "\033[36m====================================================\033[0m"
