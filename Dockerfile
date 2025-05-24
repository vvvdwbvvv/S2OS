# 使用一個包含基本建置工具的 Ubuntu 映像
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    make \
    gcc \
    g++ \
    perl \
    libncurses-dev \
    cpio \
    python3 \
    rsync \
    bc \
    unzip \
    git \
    file \
    coreutils \
    findutils \
    patch \
    xz-utils \
    tar \
    && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /opt/gnu-bin
ENV PATH="/opt/gnu-bin:${PATH}"
RUN ln -sf /usr/bin/true /opt/gnu-bin/true
RUN ln -sf /usr/bin/install /opt/gnu-bin/install
RUN ln -sf /usr/bin/find /opt/gnu-bin/find

ENV TRUE=/usr/bin/true

WORKDIR /app

COPY . .

RUN chmod +x ./build-vm.sh

CMD ["./build-vm.sh"]