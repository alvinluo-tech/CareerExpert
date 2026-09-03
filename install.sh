#!/usr/bin/env bash
# ==============================================================================
# CareerExpert — 全能型 AI 原生求职与学术 CV 工作流系统
# Multi-Skills 矩阵跨平台一键安装器 (Linux/macOS)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-all}"
CUSTOM_PATH="${2:-}"

echo -e "\033[36m====================================================\033[0m"
echo -e "\033[36m  CareerExpert — Multi-Skills 技能矩阵与 Slash 命令\033[0m"
echo -e "\033[36m  跨 Harness 一键安装器 (Linux/macOS)\033[0m"
echo -e "\033[36m====================================================\033[0m"

SKILLS_BASE="${SCRIPT_DIR}/skills"

install_skills() {
    local dest_skills_dir="$1"
    local platform_name="$2"

    echo -e "\n\033[33m[*] 正在部署技能矩阵至 ${platform_name} : ${dest_skills_dir} ...\033[0m"
    mkdir -p "${dest_skills_dir}"

    # 清理旧命名空间残留以避免命令重复
    local legacy_skills=("job-finding" "resume-style" "resume-polish" "academic-cv" "mock-interview")
    for leg in "${legacy_skills[@]}"; do
        if [ -d "${dest_skills_dir}/${leg}" ]; then
            rm -rf "${dest_skills_dir}/${leg}"
        fi
    done

    for skill_path in "${SKILLS_BASE}"/*; do
        if [ -d "${skill_path}" ]; then
            local skill_name
            skill_name=$(basename "${skill_path}")
            local target_dir="${dest_skills_dir}/${skill_name}"
            mkdir -p "${target_dir}"
            cp -r "${skill_path}/"* "${target_dir}/"
            echo -e "  \033[32m[+] 成功安装技能: ${skill_name}\033[0m"
        fi
    done
    echo -e "\033[32m[✓] 成功部署技能矩阵至 ${platform_name}\033[0m"
}

cleanup_legacy_commands() {
    local dest_commands_dir="$1"
    if [ -d "${dest_commands_dir}" ]; then
        local legacy_cmds=("resume.md" "style.md" "polish.md" "cv.md" "interview.md")
        for cmd in "${legacy_cmds[@]}"; do
            if [ -f "${dest_commands_dir}/${cmd}" ]; then
                rm -f "${dest_commands_dir}/${cmd}"
            fi
        done
    fi
}

if [ -n "${CUSTOM_PATH}" ]; then
    install_skills "${CUSTOM_PATH}" "自定义目录"
    exit 0
fi

USER_HOME="${HOME}"

if [ "$TARGET" = "claude" ] || [ "$TARGET" = "all" ]; then
    install_skills "${USER_HOME}/.claude/skills" "Claude Code 全局"
    cleanup_legacy_commands "${USER_HOME}/.claude/commands"
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
echo -e "\033[36m  ✨ CareerExpert 技能矩阵部署完成 (唯一命名空间)！\033[0m"
echo -e "\033[36m  可用原生 Slash 快捷指令：\033[0m"
echo -e "    - \033[37m/career-ops        -> 全流程求职与学术规划总指挥\033[0m"
echo -e "    - \033[37m/career-style      -> 简历 UI 视觉排版调优 (文字绝对锁定)\033[0m"
echo -e "    - \033[37m/career-polish     -> Google XYZ 战果量化改写 (排版绝对锁定)\033[0m"
echo -e "    - \033[37m/career-cv         -> 出国留学海外硕博学术 CV (Harvard 规范)\033[0m"
echo -e "    - \033[37m/career-interview  -> 四级渐进式模拟面试攻防与复盘\033[0m"
echo -e "\033[36m====================================================\033[0m"
