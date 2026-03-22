# 使用 Ubuntu 作为基础镜像
FROM ubuntu:22.04

# 避免交互式安装时的提示
ENV DEBIAN_FRONTEND=noninteractive

# 使用官方 Ubuntu 源
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 安装基础依赖、Python、Node.js 和常用工具
RUN apt-get update && apt-get install -y \
    curl \
    net-tools \
    vim \
    jq \
    tmux \
    htop \
    python3 \
    python3-pip \
    python3-dev \
    software-properties-common \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /src

CMD ["tail", "-f", "/dev/null"]