---
title: "Windows Clash使用教程：从客户端安装到系统代理与TUN虚拟网卡配置"
description: "Windows 平台使用 Clash 的完整实战：Clash Verge Rev 客户端安装、系统代理、TUN模式接管与常见报错排查。"
pubDate: 2026-09-28
category: "tutorial"
recommendationContext: "clash"
tags: ["Windows Clash", "Clash Verge Rev", "TUN模式", "PC代理教程", "系统代理"]
faq:
  - q: "开启系统代理后，浏览器可以打开外网，但终端（CMD/PowerShell）和游戏无法代理怎么办？"
    a: "系统代理仅对遵循系统 HTTP 代理设置的应用（如浏览器）生效。要代理命令行、Git、Steam 或游戏，请在客户端中开启‘TUN 模式’，利用虚拟网卡接管系统全部网络流量。"
  - q: "Windows 11 提示 WebView2 运行时缺失导致客户端无法打开怎么办？"
    a: "微软官方提供 Evergreen WebView2 运行时安装包，前往微软官方网站下载并安装对应体系架构的安装包后重启客户端即可。"
  - q: "Clash 开启后系统提示 7890 端口冲突如何解决？"
    a: "在客户端‘设置’中找到‘混合端口’（Mixed Port），将默认的 7890 更改为 7895、7899 等未被占用的端口并保存。"
---

# Windows Clash使用教程：从客户端安装到系统代理与TUN虚拟网卡配置

Windows 是日常办公、学术检索以及游戏娱乐的主流平台。在原版 Clash for Windows 停更之后，新一代基于开源 Mihomo 内核的 **Clash Verge Rev** 已成为 Windows 平台上的首选客户端。本文将从零开始演示 Windows 端的完整配置步骤、系统代理与 TUN 模式的区别及应用。

---

## 一、环境要求与客户端选型

在安装前，请确认你的电脑满足以下条件：

1. **操作系统**：Windows 10 64-bit (1809 及以上) 或 Windows 11。
2. **核心依赖**：Windows 10 早期版本需安装 **Microsoft Edge WebView2 Runtime**；Windows 11 系统通常已内置。
3. **软件选型**：推荐下载 **Clash Verge Rev**（支持 Windows x64 与 ARM64 安装包或便携版）。该客户端拥有现代化的界面设计，并原生集成了 Mihomo 内核。
4. **订阅准备**：准备好一条有效的订阅链接。如果你尚未选择机场，可以参考[Clash机场推荐与评估指南](/posts/clash-airport-recommendation-guide/)或前往[机场大全数据库](/airports/)查阅参数明细。

---

## 二、客户端安装与界面设置

1. 前往开源代码托管平台 Release 页面下载 `Clash.Verge_x.x.x_x64-setup.exe` 安装文件。
2. 运行安装向导，按提示完成安装。如果 Windows Defender 弹出智能屏幕阻止提示，点击“更多信息”并选择“仍要运行”。
3. 启动 Clash Verge Rev，点击左侧菜单栏齿轮图标（设置）：
   - 将 **Clash 内核** 切换为 **Mihomo (Meta)** 内核。
   - 在语言设置中将界面切换为 **简体中文**。

---

## 三、导入并激活订阅配置

1. 打开服务商后台，复制 Clash 订阅链接。
2. 在 Clash Verge Rev 界面点击左侧 **“订阅” (Profiles)**。
3. 在顶部的输入框中粘贴订阅 URL，点击右侧的 **“导入” (Import)** 按钮。
4. 客户端将自动发起 HTTP 请求下载配置文件。下载完成后，列表中会出现该机场的配置卡片。
5. **右键点击该卡片**，选择 **“使用” (Use)**，卡片周围出现高亮边框即表示当前已激活该配置。
6. 右键还可以设置 **自动更新周期**，建议设置为 24 小时，以便自动同步服务商最新的节点变动。

若遇到导入卡在 0% 或提示报错，请参考[Clash订阅下载失败排查指南](/posts/clash-subscription-download-failed/)。

---

## 四、启用系统代理与模式选择

1. 点击左侧 **“代理” (Proxy)** 菜单，选择工作模式：
   - **规则 (Rule)**：最常用模式。依据规则分流，访问国内百度、B站等直连，访问 GitHub、Google 等走代理。
   - **全局 (Global)**：强制所有通过代理的软件统一走选定的单一节点。
   - **直连 (Direct)**：不进行任何代理转发。
2. 在策略组展开列表中，找到合适的分流组并手动选定一个低延迟节点（如香港或日本节点）。
3. 点击主界面或系统托盘图标，开启 **“系统代理” (System Proxy)** 开关。
4. 打开 Edge 或 Chrome 浏览器，尝试访问海外网站，若能迅速加载，说明系统代理配置成功。

---

## 五、进阶功能：TUN 虚拟网卡模式实战

许多开发者和游戏玩家会发现，CMD/PowerShell 命令行、Git clone、以及部分网游客户端并不遵循 Windows 系统的 HTTP 代理，导致无法连接外网。此时需要开启 **TUN 模式**：

1. **安装核心服务**：在 Clash Verge Rev 的“设置”页面，找到 **“服务模式” (Service Mode)**，点击右侧的“安装/配置”，授权 Windows 管理员权限。安装成功后状态会显示为绿色的“已激活”。
2. **开启 TUN 模式**：在设置页面中打开 **“TUN 模式”** 开关。
3. **工作原理**：TUN 模式会在 Windows 网络连接中创建一个名为 `wintun` 的虚拟网络适配器，并在底层通过路由表将整台电脑的网络数据包捕获并送入 Mihomo 内核进行透明分流，无需对第三方软件单独配置代理端口。
4. **验证方式**：打开 PowerShell 窗口，无需执行任何 `set http_proxy` 变量，直接执行 `curl https://api.ipify.org`，返回的 IP 即为节点 IP。

---

## 六、常见故障与维护排查

- **系统代理无法开启**：如果点击系统代理开关后立刻弹回关闭，通常是杀毒软件锁定了注册表 `Internet Settings` 项。可阅读[Clash系统代理打不开排查指南](/posts/clash-system-proxy-cannot-open/)排查修复。
- **浏览器提示代理拒绝连接**：先检查 Clash 进程是否意外崩溃，再确认本地端口是否被修改。
- **想要了解更多客户端**：Windows 用户也可以体验专为现代 UI 打造的[Mihomo Party客户端新手指南](/posts/mihomo-party-tutorial/)。更多突发断网问题可查阅[常见故障排查](/problems/)。
