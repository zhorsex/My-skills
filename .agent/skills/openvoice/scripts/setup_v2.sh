#!/bin/bash
set -e

echo "🚀 开始设置 OpenVoice V2 环境..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda 未找到，请先安装 Conda。"
    exit 1
fi

# Create conda environment
echo "📦 创建 Conda 环境 'openvoice'..."
conda create -n openvoice python=3.9 -y

echo "⚠️  注意: 请手动激活环境: 'conda activate openvoice'"

# Clone repository
if [ -d "OpenVoice" ]; then
    echo "📂 OpenVoice 目录已存在，跳过克隆。"
else
    echo "⬇️  克隆 OpenVoice 仓库..."
    git clone git@github.com:myshell-ai/OpenVoice.git
fi

echo "📦 安装 MeloTTS (V2 依赖)..."
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download

echo "✅设置完成！"
echo ""
echo "接下来的步骤："
echo "1. 运行 'conda activate openvoice'"
echo "2. 进入目录 'cd OpenVoice'"
echo "3. 安装 OpenVoice 依赖 'pip install -e .'"
echo "4. 下载 V2 检查点并解压到 checkpoints_v2/ 目录"
