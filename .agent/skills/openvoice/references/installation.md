# OpenVoice 安装指南

本指南详细介绍了如何在不同平台上安装 OpenVoice。

## Linux 安装 (推荐)

这是官方推荐的安装方式，适用于熟悉 Linux、Python 和 PyTorch 的开发者和研究人员。

### 前置要求
- Linux 系统
- Python 3.9
- Conda

### 安装步骤

1. **创建 Conda 环境**
   ```bash
   conda create -n openvoice python=3.9
   conda activate openvoice
   ```

2. **克隆仓库**
   ```bash
   git clone git@github.com:myshell-ai/OpenVoice.git
   cd OpenVoice
   ```

3. **安装依赖**
   ```bash
   pip install -e .
   ```

   无论是使用 V1 还是 V2 版本，上述基础安装步骤都是相同的。

## Windows 安装

这是由社区贡献的非官方安装指南。

详细步骤请参考 [@Alienpups 的指南](https://github.com/Alienpups/OpenVoice/blob/main/docs/USAGE_WINDOWS.md)。

## Docker 安装

这是由社区贡献的非官方 Docker 部署指南。

详细步骤请参考 [@StevenJSCF 的指南](https://github.com/StevenJSCF/OpenVoice/blob/update-docs/docs/DF_USAGE.md)。

## 资源下载

### OpenVoice V1
- **检查点**: [下载链接](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip)
- **安装位置**: 解压到项目根目录下的 `checkpoints` 文件夹

### OpenVoice V2
- **检查点**: [下载链接](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip)
- **安装位置**: 解压到项目根目录下的 `checkpoints_v2` 文件夹
- **额外依赖**: 需要安装 MeloTTS
  ```bash
  pip install git+https://github.com/myshell-ai/MeloTTS.git
  python -m unidic download
  ```
