#!/bin/bash
#
# Tech Earnings Deep Dive - 科技股财报深度分析
# v3.0 - 完全复刻 Day1Global 功能、逻辑和方法论
#
# 用法：./run.sh <股票代码> [选项]
# 示例：./run.sh NVDA
#       ./run.sh TSLA --full
#       ./run.sh MSFT --perspective buffett
#

set -e

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"
LOG_DIR="${SCRIPT_DIR}/log"
CACHE_DIR="${SCRIPT_DIR}/cache"
MODULES_DIR="${SCRIPT_DIR}/modules"
TEMPLATES_DIR="${SCRIPT_DIR}/templates"
CONFIG_FILE="${SCRIPT_DIR}/config.json"

# 激活虚拟环境
if [[ -d "$VENV_DIR" ]]; then
    source "$VENV_DIR/bin/activate"
else
    echo "⚠️ 虚拟环境不存在，使用系统 Python"
fi

# 日志文件
LOG_FILE="${LOG_DIR}/$(date +%Y-%m-%d).log"

# 创建目录
mkdir -p "$LOG_DIR" "$CACHE_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# 读取配置
get_config() {
    local key=$1
    local default=$2
    local value=$(jq -r ".$key // \"$default\"" "$CONFIG_FILE" 2>/dev/null)
    echo "${value:-$default}"
}

# 检查依赖
check_dependencies() {
    local deps=("jq" "python3" "curl")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log "❌ 错误：缺少依赖 $dep"
            exit 1
        fi
    done
    log "✅ 依赖检查通过"
}

# 获取股票数据
fetch_stock_data() {
    local stock=$1
    log "📊 获取 $stock 数据..."
    
    # 调用 Python 脚本获取数据
    python3 "${SCRIPT_DIR}/modules/fetch_data.py" "$stock"
}

# 执行 16 模块分析
run_modules_analysis() {
    local stock=$1
    local data=$2
    log "🔍 执行 16 模块分析..."
    
    python3 "${SCRIPT_DIR}/modules/analyze.py" "$stock" "$data"
}

# 执行 6 大视角分析
run_perspectives_analysis() {
    local stock=$1
    local data=$2
    log "👁️ 执行 6 大投资哲学视角分析..."
    
    python3 "${SCRIPT_DIR}/modules/perspectives.py" "$stock" "$data"
}

# 执行估值分析
run_valuation() {
    local stock=$1
    local data=$2
    log "💰 执行多方法估值分析..."
    
    python3 "${SCRIPT_DIR}/modules/valuation.py" "$stock" "$data"
}

# 生成最终报告
generate_report() {
    local stock=$1
    local output_file="${SCRIPT_DIR}/output/${stock}_$(date +%Y%m%d_%H%M%S).md"
    
    log "📝 生成最终报告..."
    
    python3 "${SCRIPT_DIR}/modules/report.py" "$stock" "$output_file"
    
    echo ""
    echo "✅ 报告已生成：$output_file"
    echo ""
}

# 主函数
main() {
    local stock="${1:-$(get_config 'default_stock' 'NVDA')}"
    local full_report=false
    local perspective=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --full)
                full_report=true
                shift
                ;;
            --perspective)
                perspective="$2"
                shift 2
                ;;
            -h|--help)
                echo "用法：$0 <股票代码> [选项]"
                echo ""
                echo "选项:"
                echo "  --full           生成完整报告（默认）"
                echo "  --perspective    指定投资视角 (buffett/growth/value/etc)"
                echo "  -h, --help       显示帮助"
                echo ""
                echo "示例:"
                echo "  $0 NVDA"
                echo "  $0 TSLA --full"
                echo "  $0 MSFT --perspective buffett"
                exit 0
                ;;
            *)
                stock="$1"
                shift
                ;;
        esac
    done
    
    log "========================================"
    log "🚀 Tech Earnings Deep Dive v3.0"
    log "========================================"
    log "股票代码：$stock"
    log "完整报告：$full_report"
    log "投资视角：${perspective:-all}"
    log ""
    
    # 检查依赖
    check_dependencies
    
    # 获取数据
    fetch_stock_data "$stock"
    
    # 执行分析
    run_modules_analysis "$stock" "$data"
    run_perspectives_analysis "$stock" "$data"
    run_valuation "$stock" "$data"
    
    # 生成报告
    generate_report "$stock"
    
    log "========================================"
    log "✅ 分析完成"
    log "========================================"
}

# 执行主函数
main "$@"
