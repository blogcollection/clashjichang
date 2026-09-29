import os
from datetime import datetime

articles = [
    # 1. Clash机场类
    {
        "slug": "what-is-clash-airport",
        "title": "Clash机场是什么？从底层原理到订阅与节点完整解析",
        "category": "airport",
        "recommendationContext": "beginner",
        "tags": ["Clash机场", "科学上网原理", "Clash新手入门", "代理机场"],
        "description": "详细解析Clash机场的定义、技术原理、与传统VPN的区别，以及为什么现代网络工具普遍采用Clash订阅节点服务。",
        "faq": [
            {"q": "为什么网络代理服务商被称为‘机场’？", "a": "早期的知名代理客户端 Shadowsocks 其图标是一架小纸飞机，提供 Shadowsocks 节点和订阅服务的平台便被网友形象地戏称为‘飞机场’或‘机场’。"},
            {"q": "Clash本身包含免费节点吗？", "a": "Clash只是一个规则分流代理客户端软件本身不附带任何网络节点，用户需要导入第三方机场提供的订阅链接才能正常使用。"},
            {"q": "新手第一次接触Clash该怎么起步？", "a": "首先选择一家支持全平台客户端导入的优质机场，购买合适的基础月付套餐获取订阅链接，再下载对应的 Clash Verge 或 Mihomo 客户端完成导入即可。"}
        ]
    },
    {
        "slug": "clash-airport-recommendation-guide",
        "title": "Clash机场推荐指南：2026年如何避坑与筛选高性价比优质节点",
        "category": "airport",
        "recommendationContext": "clash",
        "tags": ["Clash机场推荐", "优质机场", "机场避坑", "节点筛选"],
        "description": "汇总Clash机场选择核心考量指标：专线质量、晚高峰稳定性、流媒体/AI解锁支持与客服保障，拒绝盲目跟风踩雷。",
        "faq": [
            {"q": "如何判断一家Clash机场是否值得长期使用？", "a": "建议始终先购买一个月付套餐进行晚高峰（晚上8点-11点）测速与真实流媒体播放体验，确认无卡顿、掉线后再考虑季付或年付。"},
            {"q": "专线机场和普通公网中转有什么区别？", "a": "两者是不同的服务商线路描述。实际路由、延迟、可用性和流量策略会随服务商与本地网络变化，购买前应以当前说明和短周期体验确认。"}
        ]
    },
    {
        "slug": "how-to-choose-clash-airport",
        "title": "Clash机场怎么选？不同使用场景的量身选择决策树",
        "category": "airport",
        "recommendationContext": "beginner",
        "tags": ["机场怎么选", "场景选机场", "大流量机场", "流媒体机场"],
        "description": "日常轻度办公、外贸跨境、4K流媒体追剧、ChatGPT/Claude生产力等不同用户群体的Clash机场精细化选型方案。",
        "faq": [
            {"q": "轻度办公查资料一个月需要多少流量？", "a": "普通网页浏览、查阅文献、收发邮件一般每月 30GB-60GB 足够，可优先考虑百元内年付小包或不限时流量包。"},
            {"q": "看 Netflix 或 YouTube 4K 视频推荐多大流量？", "a": "播放 4K 视频每小时消耗约 7GB-10GB 流量，建议选择月流量在 200GB-500GB 以上的大流量套餐。"}
        ]
    },
    {
        "slug": "how-to-buy-clash-airport",
        "title": "Clash机场怎么买？注册、选套餐、支付到导入完整流程",
        "category": "airport",
        "recommendationContext": "beginner",
        "tags": ["机场怎么买", "购买套餐", "支付宝付款", "订阅导入"],
        "description": "小白保姆级购买教程：从官网注册、套餐周期甄别、支付方式安全注意事项到获取订阅链接全流程讲解。",
        "faq": [
            {"q": "机场购买支持哪些支付方式？", "a": "大多数面向中文用户的机场支持支付宝、微信或 USDT 加密货币支付，建议优先使用常规渠道月付体验。"},
            {"q": "购买后多久能开始使用？", "a": "下单付款后系统通常在数十秒内自动开通服务，在机场后台复制订阅链接即可导入客户端使用。"}
        ]
    },
    {
        "slug": "cheap-clash-airport-selection",
        "title": "便宜Clash机场怎么选？低预算也能兼顾稳定的实用法则",
        "category": "airport",
        "recommendationContext": "cheap",
        "tags": ["便宜机场", "高性价比机场", "低价订阅", "学生党机场"],
        "description": "解析几元到十几元低价机场的优缺点，如何在控制开支的前提下避开跑路风险与严重超售。",
        "faq": [
            {"q": "便宜机场容易跑路吗？", "a": "定价过低（如几元一年）且无稳定运营基础的机场超售和跑路概率较高。建议选择运营时间较长、有明确工单支持的正规老牌平价机场。"},
            {"q": "低预算用户的最佳购买策略是什么？", "a": "始终坚持‘月付’或购买‘不限时按量计费包’，避免一次性充值过长周期以降低资金风险。"}
        ]
    },
    {
        "slug": "clash-airport-vs-vpn",
        "title": "Clash机场和传统VPN的区别：技术架构、速度与安全性全方位对比",
        "category": "airport",
        "recommendationContext": "clash",
        "tags": ["VPN区别", "Clash优势", "规则分流", "网络协议"],
        "description": "深入对比Clash基于分流规则的代理协议架构与传统全局VPN的差异，揭示为什么国内用户普遍更青睐Clash。",
        "faq": [
            {"q": "Clash比传统VPN好在哪里？", "a": "Clash最大的优势是‘规则分流’：国内网站直接直连不耗流量，仅海外受限网址走代理；同时协议经过混淆抗封锁能力远高于易被特征识别的传统VPN。"},
            {"q": "公司或学校网络更适合哪种？", "a": "对于防火墙严格的网络环境，采用 Shadowsocks/VLESS/Trojan 等现代协议的 Clash 节点穿透率显著高于 OpenVPN 或 WireGuard 等传统 VPN。"}
        ]
    },
    {
        "slug": "what-is-clash-subscription",
        "title": "Clash机场订阅是什么？订阅链接工作原理与格式说明",
        "category": "subscription",
        "recommendationContext": "clash",
        "tags": ["Clash订阅", "订阅链接", "YAML配置", "订阅原理"],
        "description": "解析订阅链接如何将远端服务器节点、分流规则集与策略组同步到你的设备，以及订阅安全防泄漏指南。",
        "faq": [
            {"q": "订阅链接泄露会有什么后果？", "a": "他人获取你的订阅链接后可以消耗你的套餐流量，甚至导致你的账户被多地并发挤下线。一旦泄露应立即在机场后台重置订阅链接。"},
            {"q": "订阅链接打开为什么是一堆乱码或英文代码？", "a": "订阅链接返回的通常是 Base64 编码数据或 YAML 配置文件，专供客户端程序解析阅读，在普通浏览器中直接打开即呈现为纯文本代码。"}
        ]
    },
    {
        "slug": "what-is-airport-node",
        "title": "机场节点是什么意思？落地机、中转机与入口节点详解",
        "category": "node",
        "recommendationContext": "clash",
        "tags": ["机场节点", "落地节点", "入口中转", "节点原理"],
        "description": "从网络传输路径解构一个节点的构成：用户设备如何经过国内入口机、专线中转最终抵达海外落地服务器。",
        "faq": [
            {"q": "为什么同一个国家会有多个节点（如香港01、香港02）？", "a": "为了实现负载均衡和防单点故障，机场通常在同一个热门地区部署多台落地服务器分散流量并发。"},
            {"q": "香港节点和美国节点主要区别在哪？", "a": "香港物理距离中国大陆最近，网络延迟极低（通常 15ms-40ms），适合日常主力浏览；美国节点延迟较高（150ms-220ms），但原生 IP 支持覆盖更全。"}
        ]
    },

    # 2. Clash客户端类
    {
        "slug": "clash-verge-usage-tutorial",
        "title": "Clash Verge怎么用？2026年Windows/macOS新手配置教程",
        "category": "client",
        "recommendationContext": "beginner",
        "tags": ["Clash Verge", "使用教程", "配置指南", "客户端下载"],
        "description": "经典 Clash Verge 客户端从安装、设置中文、导入订阅、切换代理模式到开启系统代理全流程步骤演示。",
        "faq": [
            {"q": "Clash Verge 原作者停更后还能继续用吗？", "a": "原版仍可正常运行，但更推荐升级到目前社区积极维护的 Clash Verge Rev 分支，体验更完备的内核功能。"},
            {"q": "为什么开了代理后浏览器还是打不开 Google？", "a": "请检查‘系统代理’开关是否已打开，以及配置文件的节点是否测速正常且延迟有效。"}
        ]
    },
    {
        "slug": "clash-verge-rev-tutorial",
        "title": "Clash Verge Rev使用教程：当代主流Mihomo内核桌面端配置全景",
        "category": "client",
        "recommendationContext": "clash",
        "tags": ["Clash Verge Rev", "Mihomo", "桌面客户端", "进阶配置"],
        "description": "深入讲解当前最活跃的开源客户端 Clash Verge Rev：内核切换、TUN虚拟网卡模式、规则扩展与性能调优。",
        "faq": [
            {"q": "Clash Verge Rev 与原版 Verge 有什么不同？", "a": "Rev 是社区重构分支，全面升级支持最新的 Mihomo (Clash.Meta) 内核，支持更多协议（如 VLESS、Hysteria 2）且修复了大量底层系统代理 bug。"},
            {"q": "什么时候需要开启 TUN 模式？", "a": "当某些软件（如特定电脑游戏、命令行终端或部分不遵循系统代理的海外办公软件）无法走代理时，开启 TUN 虚拟网卡接管系统全局流量。"}
        ]
    },
    {
        "slug": "mihomo-party-tutorial",
        "title": "Mihomo Party使用教程：高颜值、易上手的全新Meta内核客户端",
        "category": "client",
        "recommendationContext": "clash",
        "tags": ["Mihomo Party", "Mihomo", "Clash Meta", "新一代客户端"],
        "description": "全面剖析新一代基于 Mihomo 内核的极简美学客户端 Mihomo Party，包括订阅管理、节点聚合与便捷快捷键。",
        "faq": [
            {"q": "Mihomo Party 适合新手还是老手？", "a": "Mihomo Party 界面开箱即用、交互直观，没有复杂冗余的选项，非常适合追求简约美观的现代桌面用户。"},
            {"q": "支持哪些操作系统？", "a": "支持 Windows、macOS（支持 Intel 及 Apple Silicon）以及 Linux 平台。"}
        ]
    },
    {
        "slug": "what-is-clash-meta",
        "title": "Clash Meta是什么？Mihomo内核技术演进与核心特性解析",
        "category": "client",
        "recommendationContext": "clash",
        "tags": ["Clash Meta", "Mihomo内核", "技术演进", "新协议支持"],
        "description": "介绍从原版 Clash Premium 闭源停更到开源社区接棒的 Clash.Meta（现更名 Mihomo）的发展脉络与先进功能。",
        "faq": [
            {"q": "为什么现在大家都推荐 Meta/Mihomo 内核？", "a": "原版 Clash 内核已不再更新，而 Mihomo 持续维护，支持 VLESS、Trojan、Hysteria 2、TUIC、WireGuard 等新协议，且对现代 DNS 泄漏防御大幅升级。"},
            {"q": "旧版 Clash 订阅可以在 Meta 内核上运行吗？", "a": "完全兼容，Meta 内核向下兼容所有的经典 Clash YAML 规则配置。"}
        ]
    },
    {
        "slug": "windows-clash-tutorial",
        "title": "Windows Clash完整安装使用教程：从零开始配置PC网络代理",
        "category": "client",
        "recommendationContext": "beginner",
        "tags": ["Windows Clash", "PC代理", "Win11配置", "系统代理"],
        "description": "专为 Windows 10/11 用户撰写的全套指南：客户端选择推荐、开机自启、服务模式安装与网络排错技巧。",
        "faq": [
            {"q": "Windows 安装提示杀毒软件拦截怎么办？", "a": "由于代理客户端涉及底层网络端口与虚拟网卡操作，部分杀软可能产生误报，从官方 GitHub Release 页面下载的正版安装包直接添加信任即可。"},
            {"q": "如何让电脑开机自动启动并进入代理状态？", "a": "在客户端设置中勾选‘开机自启’以及‘静默启动’，并在配置中保持‘系统代理’处于开启状态即可。"}
        ]
    },
    {
        "slug": "android-clash-tutorial",
        "title": "Android Clash手机端教程：Clash Meta for Android配置与省电技巧",
        "category": "client",
        "recommendationContext": "beginner",
        "tags": ["Android Clash", "安卓代理", "CMFA", "手机节点配置"],
        "description": "安卓手机安装使用 Clash 的详尽步骤：应用分流排除、电池白名单优化、常驻后台避免断连与节点测速。",
        "faq": [
            {"q": "为什么手机锁屏后 Clash 容易掉线？", "a": "因为安卓系统的电池省电优化会强行杀死后台应用，请在系统设置中将 Clash 应用的后台权限设为‘无限制’或锁定后台任务卡片。"},
            {"q": "可以指定国内微信、淘宝不经过 Clash 吗？", "a": "可以在客户端开启‘分流模式’（Rule），或者在‘应用分流’功能中直接勾选排除微信等国内本土 App。"}
        ]
    },
    {
        "slug": "macos-clash-tutorial",
        "title": "macOS Clash使用教程：Mac用户推荐客户端与权限设置全解",
        "category": "client",
        "recommendationContext": "beginner",
        "tags": ["macOS Clash", "苹果电脑代理", "Mac节点设置", "M芯片兼容"],
        "description": "苹果 Mac 用户专项指南：兼容 M1/M2/M3 芯片架构的 Clash 客户端选型、辅助功能权限授予与终端代理配置。",
        "faq": [
            {"q": "Mac 提示‘无法打开，因为无法验证开发者’怎么办？", "a": "打开‘系统设置’ -> ‘隐私与安全性’，在下方找到拦截提示，点击‘仍要打开’即可。"},
            {"q": "Mac 终端（Terminal / iTerm）如何走 Clash 代理？", "a": "可以在客户端点击复制终端代理命令，或在 ~/.zshrc 中添加 export http_proxy 等端口环境变量指向 7890 端口。"}
        ]
    },

    # 3. Clash订阅类
    {
        "slug": "how-to-import-clash-subscription",
        "title": "Clash怎么导入订阅？一键导入与手动复制链接完整图文步骤",
        "category": "subscription",
        "recommendationContext": "beginner",
        "tags": ["导入订阅", "订阅配置", "一键导入", "订阅更新"],
        "description": "无论是手机还是电脑端，掌握正确的 Clash 订阅导入姿势：从机场用户中心获取链接到客户端成功下载节点列表。",
        "faq": [
            {"q": "什么是‘一键导入’与‘手动导入’？", "a": "‘一键导入’是调用网页协议自动唤起本地 Clash 并填入链接；‘手动导入’则是复制长链接粘贴到客户端的配置界面中点击下载。"},
            {"q": "如果一键导入无法唤醒客户端怎么办？", "a": "直接复制订阅 URL 地址，手动打开客户端，进入 Profiles（配置）页面，粘贴到 URL 输入框后点击 Download（下载）即可。"}
        ]
    },
    {
        "slug": "what-is-clash-subscription-url",
        "title": "Clash订阅地址是什么？格式辨析、更新周期与安全管理",
        "category": "subscription",
        "recommendationContext": "clash",
        "tags": ["订阅地址", "订阅链接格式", "订阅安全", "节点同步"],
        "description": "搞懂订阅链接的本质结构、为什么订阅地址会定期变动，以及如何配置自动定时更新保持节点鲜活。",
        "faq": [
            {"q": "订阅地址通常包含哪些信息？", "a": "包含机场的 API 域名、你的专属加密 Token、客户端类型标识等参数。"},
            {"q": "建议多久更新一次订阅？", "a": "通常建议将客户端配置为‘每日自动更新一次’，如果遇到个别节点不可用时可手动点击一次立即更新。"}
        ]
    },
    {
        "slug": "how-to-update-clash-subscription",
        "title": "Clash订阅怎么更新？自动更新设置与节点列表失效排查",
        "category": "subscription",
        "recommendationContext": "clash",
        "tags": ["更新订阅", "自动更新", "节点失效", "订阅刷新"],
        "description": "详细介绍配置自动更新间隔（小时/天）、处理更新超时以及当节点名称更新时如何平滑切换代理策略。",
        "faq": [
            {"q": "为什么点击更新订阅会提示 Timeout 或失败？", "a": "可能是机场订阅分发域名受到当前网络波动影响，可以先开启已有的可用节点代理，或更换手机热点后再尝试更新。"},
            {"q": "更新后原有的选定节点会变吗？", "a": "若机场节点名称发生变更，客户端可能会回落至默认节点，更新后请重新到代理组中检查并选择延迟最低的节点。"}
        ]
    },
    {
        "slug": "clash-subscription-failed-solutions",
        "title": "Clash订阅失败怎么办？常见错误码分析与高频解决方案速查",
        "category": "subscription",
        "recommendationContext": "clash",
        "tags": ["订阅失败", "排错指南", "证书错误", "订阅报错"],
        "description": "针对 Invalid Config、Network Error、SSL Certificate 报错等典型订阅失败问题的全套针对性诊断和排障手册。",
        "faq": [
            {"q": "提示 SSL/TLS Handshake 错误怎么解决？", "a": "检查系统本地时间是否与北京时间一致，系统时间偏差超过几分钟就会引发 SSL 证书验证失败。"},
            {"q": "提示 Download Fail 怎么办？", "a": "尝试关闭本地其他代理软件，将订阅链接粘贴进浏览器直接访问，若浏览器也打不开则说明机场订阅分发服务正在维护。"}
        ]
    },
    {
        "slug": "what-is-clash-subconverter",
        "title": "Clash订阅转换是什么？在线转换安全隐患与自建转换器指南",
        "category": "subscription",
        "recommendationContext": "clash",
        "tags": ["订阅转换", "Subconverter", "安全隐私", "自建转换"],
        "description": "探讨将 V2Ray、Shadowsocks、Sing-box 等原始链接转换为 Clash 格式的技术机制，警惕免费第三方转换站盗取节点流量。",
        "faq": [
            {"q": "为什么需要订阅转换？", "a": "因为有些老牌服务商只提供原始的 VMess/SS 节点长链接，而没有生成 Clash 专用的 YAML 规则格式，需要转换器进行结构重组。"},
            {"q": "公共在线订阅转换平台安全吗？", "a": "存在节点信息被未加密缓存或恶意记录的风险，建议优先使用机场原生提供的 Clash 订阅，或使用 Docker 自建私有转换后端。"}
        ]
    },

    # 4. Clash节点类
    {
        "slug": "how-to-choose-clash-nodes",
        "title": "Clash怎么选择节点？不同用途（游戏、视频、AI办公）挑选标准",
        "category": "node",
        "recommendationContext": "beginner",
        "tags": ["选择节点", "节点挑选", "低延迟节点", "办公节点"],
        "description": "不要只看节点延迟数值！从物理距离、带宽吞吐量、原生IP纯净度多维度为不同使用目的匹配最佳节点。",
        "faq": [
            {"q": "延迟最低的节点一定网速最快吗？", "a": "不一定。延迟只代表数据包往返时间（适合联机游戏），而下载大文件或看高清视频取决于节点的出口带宽上限。"},
            {"q": "玩外服联机游戏推荐选什么节点？", "a": "优先选择香港或日本的 IPLC/IEPL 专线节点，网络抖动极小、丢包率接近零。"}
        ]
    },
    {
        "slug": "how-to-read-clash-node-latency",
        "title": "Clash节点延迟怎么看？TCP延迟、HTTP真实握手与丢包率辨析",
        "category": "node",
        "recommendationContext": "clash",
        "tags": ["节点延迟", "延迟测试", "TCP握手", "测速说明"],
        "description": "揭秘客户端测速按钮背后测的究竟是什么：为什么测出来的数字和实际网页加载速度有时不匹配？",
        "faq": [
            {"q": "Clash 界面的毫秒数（ms）是怎么计算出来的？", "a": "客户端通常向预设的测速网址（如 Google 或 Cloudflare）发送一次 HTTP GET 请求，记录完成握手与返回响应的时间差。"},
            {"q": "为什么测速显示 20ms，但打开网页却很慢？", "a": "可能是入口机虽然延迟低，但落地端到目标网站拥堵，或者本地运营商 DNS 解析异常。"}
        ]
    },
    {
        "slug": "clash-nodes-all-timeout-solutions",
        "title": "Clash节点全部超时怎么办？5步迅速定位并恢复网络连接",
        "category": "node",
        "recommendationContext": "iepl",
        "tags": ["节点全部超时", "节点红了", "无法联网", "故障排查"],
        "description": "遇到所有节点测速一片红色的紧急自救流程：检查套餐余量、更新订阅、排查防火墙拦截与更换备用专线。",
        "faq": [
            {"q": "所有节点同时超时最常见的原因是什么？", "a": "最常见的是套餐流量已用尽、套餐已到期，或者系统本地时间严重偏离导致 TLS 握手全部失败。"},
            {"q": "如果是机场遭遇突发封锁，用户该怎么做？", "a": "耐心等待机场运维切换入口与中转机器，通常半小时到数小时内会推送新节点，及时刷新订阅即可。"}
        ]
    },
    {
        "slug": "how-to-speed-test-clash-nodes",
        "title": "Clash节点测速：Fast、Speedtest与YouTube实时码率测试指南",
        "category": "node",
        "recommendationContext": "largeTraffic",
        "tags": ["节点测速", "Speedtest", "4K测速", "带宽测试"],
        "description": "科学评估你的 Clash 节点真实性能：避免无效频繁全量测速消耗宝贵流量，用专业工具测出真实下行吞吐。",
        "faq": [
            {"q": "为什么不建议每天使用专业测速脚本全量压测？", "a": "全量测速会在几分钟内跑完数十个节点的峰值带宽，瞬间消耗多达几十 GB 套餐流量，容易被机场判定为异常并发。"},
            {"q": "检验流媒体速度的最佳方法是什么？", "a": "在 YouTube 搜索打开一段 4K 60fps 视频，右键选择‘详细统计信息’（Stats for nerds），观察 Connection Speed 是否稳定在 50,000 Kbps 以上。"}
        ]
    },
    {
        "slug": "what-is-node-multiplier",
        "title": "节点倍率是什么意思？1x、0.1x与3x倍率对套餐流量的影响",
        "category": "node",
        "recommendationContext": "clash",
        "tags": ["节点倍率", "流量倍率", "倍率计算", "省流量技巧"],
        "description": "算清你的流量账本：为什么用了 1GB 流量后台扣除了 3GB？学会挑选高性价比倍率节点大幅延长套餐使用寿命。",
        "faq": [
            {"q": "什么是 0.1x / 0.5x 低倍率节点？", "a": "低倍率节点消耗流量仅为实际下载量的 10% 或 50%，通常用于大文件下载、系统更新等不计较延迟的高吞吐场景。"},
            {"q": "高倍率（如 3x/5x）节点贵在哪里？", "a": "高倍率节点往往部署了成本昂贵的超高带宽专线或高成本的原生商宽住宅 IP，专为严苛解锁设计。"}
        ]
    },
    {
        "slug": "what-is-iplc-node",
        "title": "IPLC节点是什么？国际专线内网传输架构与终极防封机制",
        "category": "node",
        "recommendationContext": "iplc",
        "tags": ["IPLC专线", "IPLC节点", "专线机场", "防封锁机制"],
        "description": "科普专线王牌 IPLC（International Private Leased Circuit）：点对点物理线路如何做到无视敏感期封锁与超低抖动。",
        "faq": [
            {"q": "IPLC 节点为什么能无视防火墙敏感期？", "a": "因为 IPLC 专线是两地机房之间租赁的内网点对点私有物理光纤，流量不过国际公网出口与 GFW 防火墙检测。"},
            {"q": "IPLC 机场的价格通常在什么区间？", "a": "由于专线带宽成本高昂，真正的纯 IPLC 机场月均费用通常在 25 元至 50 元以上。"}
        ]
    },
    {
        "slug": "what-is-iepl-node",
        "title": "IEPL节点是什么？与IPLC的差异、以太网专线性能特点",
        "category": "node",
        "recommendationContext": "iepl",
        "tags": ["IEPL专线", "IEPL节点", "以太网专线", "专线对比"],
        "description": "厘清 IEPL（International Ethernet Private Line）专线概念：二层以太网技术如何在保障专线级品质的同时提升调配灵活性。",
        "faq": [
            {"q": "IEPL 和 IPLC 体验上有区别吗？", "a": "对于终端用户而言，两者体验几乎完全一致，均具备内网过境、低延迟、零公网丢包的特点。"},
            {"q": "为什么现在很多高端机场更倾向于使用 IEPL？", "a": "IEPL 基于现代以太网封装，更容易做动态多入口热备份和智能链路负载均衡，运维容灾能力更强。"}
        ]
    },
    {
        "slug": "what-is-shadowsocks-node",
        "title": "Shadowsocks节点是什么？经典SS协议为何至今仍是中转主力",
        "category": "node",
        "recommendationContext": "clash",
        "tags": ["Shadowsocks", "SS协议", "加密中转", "节点协议"],
        "description": "回顾网络代理开山鼻祖 Shadowsocks：轻量级对称加密、极低的 CPU 运算占用为何使其与专线中转形成绝配。",
        "faq": [
            {"q": "Shadowsocks 现在还会被公网识别封锁吗？", "a": "如果直接在公网单点直连容易受到主动探测干扰；但如果在专线或 BGP 隧道内网作为落地协议传输，其性能与稳定性无与伦比。"},
            {"q": "SS 协议对手机耗电影响大吗？", "a": "SS 协议代码极其轻量，加解密开销很小，是目前移动端最省电、最不发热的协议之一。"}
        ]
    },
    {
        "slug": "what-is-trojan-node",
        "title": "Trojan节点是什么？伪装成普通HTTPS网站的抗封锁利器",
        "category": "node",
        "recommendationContext": "clash",
        "tags": ["Trojan协议", "TLS伪装", "HTTPS穿透", "抗封锁协议"],
        "description": "深入浅出解析 Trojan 特洛伊木马原理：直接利用标准 443 端口与真实 TLS 证书，将代理流量完美融入互联网主流背景噪声。",
        "faq": [
            {"q": "Trojan 和普通 Shadowsocks 相比强在哪里？", "a": "Trojan 在公网环境中抗封锁能力远强于普通 SS，因为它的握手特征与日常访问普通银行或电商 HTTPS 网站毫无二致。"},
            {"q": "Clash 各大客户端支持 Trojan 吗？", "a": "主流的 Clash Verge Rev、Mihomo Party、Shadowrocket 等均完全原生支持 Trojan 协议。"}
        ]
    },
    {
        "slug": "what-is-vless-node",
        "title": "VLESS节点是什么？V2Ray新一代无状态极简高效协议详解",
        "category": "node",
        "recommendationContext": "clash",
        "tags": ["VLESS", "Xray", "V2Ray", "Reality协议"],
        "description": "解读 VLESS 协议的轻量化革命：去掉 VMess 冗余的加密层，结合 XTLS 与 Reality 技术实现接近裸奔的顶级传输速率。",
        "faq": [
            {"q": "VLESS 和 VMess 有什么区别？", "a": "VMess 自身带有强制对称加密，CPU 消耗较大；VLESS 则是无状态协议，将加密全权交给底层的 TLS 标准层，性能和并发吞吐显著提升。"},
            {"q": "旧版 Clash 支持 VLESS 吗？", "a": "原版旧内核不支持，必须使用基于 Clash.Meta / Mihomo 内核的现代客户端才能解析运行 VLESS 节点。"}
        ]
    },

    # 5. Clash问题解决类
    {
        "slug": "clash-connected-but-no-internet",
        "title": "Clash连接了不能上网？99%用户都遇到过的8大根源自查清单",
        "category": "troubleshoot",
        "recommendationContext": "clash",
        "tags": ["连上不能上网", "没有网络", "系统代理", "排障清单"],
        "description": "明明右下角图标绿了节点也有延迟，却打不开网页？从系统代理开关、DNS 污染、TUN 网卡冲突一步步排解。",
        "faq": [
            {"q": "为什么国内网站打不开，海外网站却可以打开？", "a": "检查是否误开了‘全局模式’（Global）且选了不可靠的海外节点，请切换回‘规则分流模式’（Rule）。"},
            {"q": "为什么电脑右下角网络图标显示黄色感叹号或无网络访问？", "a": "这是 Windows 的 NCSI 网络连通性探测被代理拦截所致，通常不影响实际网页浏览；可在客户端配置中开启绕过局域网与系统检测。"}
        ]
    },
    {
        "slug": "clash-system-proxy-cannot-open",
        "title": "Clash系统代理打不开或自动关闭？注册表锁定与软件冲突修复",
        "category": "troubleshoot",
        "recommendationContext": "clash",
        "tags": ["系统代理打不开", "代理自动关闭", "注册表修复", "端口占用"],
        "description": "剖析点击 System Proxy 按钮立刻弹回关闭的顽疾：解决杀软锁定注册表 ProxyServer 项与 7890 端口占用故障。",
        "faq": [
            {"q": "为什么点击开启系统代理一秒后自动跳回关闭？", "a": "通常是因为 7890 端口被本地其他软件（如迅雷、IDM、VMware 或旧代理软件后台残留进程）占用冲突，在设置中更改混合端口为 7895 或其他数字即可。"},
            {"q": "如何清理残留的代理注册表设置？", "a": "打开 Windows 设置 -> 网络和 Internet -> 代理，手动关闭‘使用代理服务器’，或者使用修复脚本一键清空系统代理项。"}
        ]
    },
    {
        "slug": "clash-dns-leak-and-pollution-guide",
        "title": "Clash DNS问题排查：DNS泄漏、解析变慢与Fake-IP工作原理",
        "category": "troubleshoot",
        "recommendationContext": "clash",
        "tags": ["DNS问题", "Fake-IP", "DNS泄漏", "域名解析慢"],
        "description": "理解 Clash 核心的 Fake-IP 与 Redir-Host 模式：如何避免本地运营商劫持，获得毫秒级秒开海外网站的顺滑体验。",
        "faq": [
            {"q": "什么是 Fake-IP 模式？", "a": "客户端收到 DNS 查询请求时直接瞬间返回一个虚构的保留内网 IP（如 198.18.0.x），同时由远端服务器去进行真实解析，彻底根除了本地 DNS 等待时间与污染。"},
            {"q": "玩国内游戏连麦遇到问题和 Fake-IP 有关吗？", "a": "某些老旧游戏或局域网设备可能会因为 Fake-IP 地址段产生冲突，此时可将该游戏域名加入 hosts 规则或切换为 Redir-Host 模式。"}
        ]
    },
    {
        "slug": "clash-update-failed-solutions",
        "title": "Clash更新失败与内核报错：Core Version Mismatch排解指南",
        "category": "troubleshoot",
        "recommendationContext": "clash",
        "tags": ["更新失败", "内核更新", "版本不兼容", "客户端报错"],
        "description": "解决客户端在线更新报错、GitHub API 限制、Mihomo 内核下载中断等问题的有效替代手动升级方案。",
        "faq": [
            {"q": "客户端检查更新总是提示网络错误怎么解决？", "a": "因为客户端更新检查请求的是 GitHub Releases API，若此时系统代理未接管相关域名可能受到公网限速，建议手动前往 GitHub Releases 页面下载安装包覆盖安装。"},
            {"q": "覆盖安装会丢失我已有的订阅配置吗？", "a": "不会，配置数据独立保存在系统的 AppData/Application Support 目录中，覆盖安装仅更新主程序二进制。"}
        ]
    },
    {
        "slug": "clash-cannot-connect-troubleshooting",
        "title": "Clash无法连接服务器？全链路排查：端口、防火墙与运营商封锁",
        "category": "troubleshoot",
        "recommendationContext": "clash",
        "tags": ["无法连接", "连接被拒绝", "网络阻断", "全链路排障"],
        "description": "由浅入深定位连接死结：检查本地 Mixed Port、Loopback 回环隔离、Windows Defender 防火墙与外部网络受限。",
        "faq": [
            {"q": "为什么公司内网或者酒店 WiFi 下 Clash 连不上？", "a": "某些公共网络会严厉封锁非 80/443 的非常规端口或探测代理协议，此时可以尝试连接机场提供的标准 443 端口 Trojan 节点。"},
            {"q": "Windows UWP 应用（如微软商店）连不上网？", "a": "Windows 系统默认对 UWP 应用启用网络沙盒隔离禁止回环访问代理，需要在客户端工具菜单中点击‘UWP 回环代理修复’（Loopback Exemption）一键勾选解除。"}
        ]
    },
    {
        "slug": "clash-subscription-download-failed",
        "title": "Clash订阅下载失败？Invalid YAML、Handshake与404报错解决",
        "category": "troubleshoot",
        "recommendationContext": "clash",
        "tags": ["订阅下载失败", "YAML报错", "404错误", "订阅转换故障"],
        "description": "全面剖析各种订阅下载失败背后的真因：机场后端被反爬拦截、Token 过期、YAML 缩进语法错误与应对策略。",
        "faq": [
            {"q": "提示 Invalid YAML 或格式不符合规范怎么处理？", "a": "说明机场下发的配置文件中存在非法字符或空节点，尝试在机场后台使用‘订阅转换’重新生成标准 Clash 格式后再导入。"},
            {"q": "提示 404 Not Found 或 403 Forbidden 怎么回事？", "a": "通常意味着你的订阅 Token 已经失效、账户由于到期被系统冻结，或者在机场后台重置了订阅未更新到新链接。"}
        ]
    }
]

# This project keeps the published article bodies as hand-edited source files.
# The generator's legacy template writer below is intentionally retired: this
# small, deterministic pass only maintains publication state and never rewrites
# titles, descriptions, FAQs, or article bodies.
PUBLISHED_SLUGS = {
    "what-is-clash-airport",
    "how-to-choose-clash-airport",
    "clash-airport-vs-vpn",
    "clash-verge-rev-tutorial",
    "windows-clash-tutorial",
    "android-clash-tutorial",
    "macos-clash-tutorial",
    "how-to-import-clash-subscription",
    "what-is-clash-subscription",
    "clash-subscription-failed-solutions",
    "clash-nodes-all-timeout-solutions",
    "clash-connected-but-no-internet",
    "what-is-iepl-node",
    "what-is-iplc-node",
    "what-is-node-multiplier",
}

# Retired article routes must never be emitted from a published page.  Keep the
# surrounding prose intact and route each former "read next" target to the
# closest published guide instead.
DRAFT_LINK_REPLACEMENTS = {
    "/posts/cheap-clash-airport-selection/": "/posts/how-to-choose-clash-airport/",
    "/posts/clash-airport-recommendation-guide/": "/posts/how-to-choose-clash-airport/",
    "/posts/clash-cannot-connect-troubleshooting/": "/posts/clash-connected-but-no-internet/",
    "/posts/clash-dns-leak-and-pollution-guide/": "/posts/clash-subscription-failed-solutions/",
    "/posts/clash-subscription-download-failed/": "/posts/how-to-import-clash-subscription/",
    "/posts/clash-system-proxy-cannot-open/": "/posts/windows-clash-tutorial/",
    "/posts/clash-update-failed-solutions/": "/posts/clash-subscription-failed-solutions/",
    "/posts/clash-verge-usage-tutorial/": "/posts/clash-verge-rev-tutorial/",
    "/posts/how-to-buy-clash-airport/": "/posts/how-to-choose-clash-airport/",
    "/posts/how-to-choose-clash-nodes/": "/posts/how-to-choose-clash-airport/",
    "/posts/how-to-speed-test-clash-nodes/": "/posts/how-to-choose-clash-airport/",
    "/posts/how-to-update-clash-subscription/": "/posts/how-to-import-clash-subscription/",
    "/posts/mihomo-party-tutorial/": "/posts/clash-verge-rev-tutorial/",
    "/posts/what-is-airport-node/": "/posts/what-is-clash-airport/",
    "/posts/what-is-clash-meta/": "/posts/clash-verge-rev-tutorial/",
    "/posts/what-is-clash-subconverter/": "/posts/what-is-clash-subscription/",
    "/posts/what-is-clash-subscription-url/": "/posts/what-is-clash-subscription/",
    "/posts/what-is-shadowsocks-node/": "/posts/what-is-clash-airport/",
    "/posts/what-is-trojan-node/": "/posts/what-is-clash-airport/",
    "/posts/what-is-vless-node/": "/posts/what-is-clash-airport/",
}

posts_dir = "src/content/posts"
os.makedirs(posts_dir, exist_ok=True)
for filename in os.listdir(posts_dir):
    if not filename.endswith(".md"):
        continue
    slug = filename[:-3]
    path = os.path.join(posts_dir, filename)
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    if slug in PUBLISHED_SLUGS:
        updated = content.replace("draft: true\n", "", 1)
        for retired_route, published_route in DRAFT_LINK_REPLACEMENTS.items():
            updated = updated.replace(retired_route, published_route)
    elif "draft: true\n" not in content:
        updated = content.replace("---\n", "---\ndraft: true\n", 1)
    else:
        updated = content
    if updated != content:
        with open(path, "w", encoding="utf-8", newline="") as file:
            file.write(updated)

print(f"Publication state updated: {len(PUBLISHED_SLUGS)} published; drafts applied to all other posts.")
raise SystemExit(0)

# Legacy template generator retained below only for historical reference. It is
# unreachable so it cannot overwrite independently edited articles.
os.makedirs('src/content/posts', exist_ok=True)

# Generate detailed markdown for each article
for item in articles:
    slug = item["slug"]
    title = item["title"]
    cat = item["category"]
    rec_ctx = item["recommendationContext"]
    tags_str = ", ".join(f'"{t}"' for t in item["tags"])
    desc = item["description"]
    faq_list = item["faq"]

    faq_frontmatter_lines = []
    for f in faq_list:
        q_clean = f["q"].replace('"', '\\"')
        a_clean = f["a"].replace('"', '\\"')
        faq_frontmatter_lines.append(f'  - q: "{q_clean}"\n    a: "{a_clean}"')
    faq_frontmatter = "\n".join(faq_frontmatter_lines)

    content = f"""---
title: "{title}"
description: "{desc}"
pubDate: 2026-09-28
category: "{cat}"
recommendationContext: "{rec_ctx}"
tags: [{tags_str}]
faq:
{faq_frontmatter}
---

# {title}

在日常使用科学上网与跨境网络访问的过程中，掌握稳定可靠的节点与客户端配置是保障效率的核心基石。本篇指南将从底层原理、实践步骤与常见误区三个层面，为你系统拆解相关核心知识，帮助你彻底告别频繁掉线、打不开网页与订阅失效等痛点。

---

## 核心概念与关键知识点

要真正理解并用好网络代理工具，首先需要厘清其背后的核心运行逻辑。与传统单一的翻墙方案不同，现代代理体系采用的是“**分流规则引擎 + 节点数据库 + 订阅同步**”的三位一体架构。

### 1. 为什么架构设计决定了网络体验
很多用户在遇到网络卡顿时，往往误以为只要换一个客户端就能解决问题。实际上，客户端本质上只是一套解析规则与转发数据包的“本地调度器”。真正决定你访问海外网站快慢、能否秒开 4K 视频以及晚高峰稳定性的，是远端服务商提供的**骨干网络专线质量与落地服务器机房的带宽冗余**。

* **普通公网中转**：数据包通过公网隧道进入海外，容易受到跨境主干网高峰拥堵和国际出口波动的影响。
* **IEPL / IPLC 企业级内网专线**：数据包直接通过租用的点对点光纤内网过境，不经过公网防火墙过滤，延迟不仅更低，而且几乎零丢包。

---

## 详细使用与操作配置步骤

如果你正在配置或优化你的环境，建议按照以下经过严格验证的标准化流程逐步操作：

### 第一步：获取规范且格式正确的订阅
任何客户端正常工作的前提，都是成功拉取到一份合规的配置文件。请登录你的服务商后台，找到专属的 **Clash 订阅地址** 并进行复制。切记不要直接在浏览器乱序下载文件，而是复制以 `http://` 或 `https://` 开头的完整链接。

### 第二步：导入与本地配置解析
打开你的桌面或移动端软件（如 Clash Verge Rev、Mihomo Party 等），进入 `配置 (Profiles)` 页面：
1. 将刚才复制的订阅 URL 粘贴到输入框中；
2. 点击 **下载 (Download)** 按钮，等待进度条完成；
3. 在成功生成的配置卡片上点击右键或左键选中，使其呈现**激活高亮状态**。

### 第三步：合理选择分流模式与节点策略
在代理规则页面，强烈建议选择 **Rule（规则分流）模式**：
* **国内常见站点（百度、淘宝、微信等）**：系统会自动命中直连规则，不消耗机场套餐流量，延迟与平时完全一致。
* **海外受限站点（Google、GitHub、YouTube、ChatGPT）**：数据包自动调度至你选定的海外节点出口。

---

## 常见注意事项与避坑法则

1. **避免轻信“永久免费”或“几元一年”的超低价服务**：网络专线带宽是极其昂贵的实体基础设施成本，明显背离市场规律的方案往往伴随着严重超售、随时跑路与严重的隐私泄漏风险。
2. **坚持“先月付后长付”的基本原则**：不同宽带运营商（电信、联通、移动）在不同地理位置对节点的握手响应存在差异。首次尝试某家服务商时，务必先开通基础月付进行晚高峰压测。
3. **保持系统时间同步**：现代加密协议依赖精准的时间戳验证。如果你的设备本地时间偏差超过 90 秒，会导致所有节点测速全部显示红色的 Timeout。

---

## 选配优质机场的推荐考量

当你解决好本地软件设置后，如果依然面临经常超时或特定流媒体/AI 服务无法访问，往往说明你当前使用的节点网络质量已达到瓶颈。此时选择一家**线路架构完备、协议新颖且拥有明确服务支持**的优质机场便成了当务之急。

"""

    # Each post deliberately receives its own search-intent-specific structure.
    # Keeping this here (rather than a shared body template) prevents thin, duplicate articles.
    focus = item["tags"][0]
    category_labels = {
        "airport": "服务选择", "client": "客户端操作", "subscription": "订阅管理",
        "node": "节点理解", "troubleshoot": "故障排查"
    }
    intent = category_labels.get(cat, "使用说明")
    if cat == "troubleshoot":
        action = "先记录报错原文、当前网络和客户端版本，再按由本地到远端的顺序排除变量"
        checks = ["确认系统代理或 TUN 状态没有被其他软件覆盖", "使用同一订阅切换一个节点，区分单节点与配置问题", "核对账户、订阅链接和服务商状态页的当前提示"]
    elif cat == "client":
        action = "先从客户端官方说明确认版本与系统权限，再导入一条来源明确的订阅"
        checks = ["保存现有配置的备份", "只在确认兼容的内核中导入配置", "通过一个网页访问测试确认设置是否生效"]
    elif cat == "subscription":
        action = "先保护订阅链接，再确认它的格式、到期状态和目标客户端兼容性"
        checks = ["不要把含 Token 的链接发送给他人", "通过服务商页面核对订阅格式", "更新失败时保留原配置，避免反复覆盖"]
    elif cat == "node":
        action = "把节点名称、延迟和实际用途分开看，并以自己的网络环境做小范围测试"
        checks = ["先选择距离和用途相近的节点", "分别测试网页、视频或工作所需服务", "记录异常发生的时间段与节点名称"]
    else:
        action = "把公开资料当作初筛条件，并在付款前向服务商确认不完整字段"
        checks = ["对照套餐周期、流量和退款规则", "确认所用客户端的订阅格式", "以短周期体验验证个人网络环境"]

    checklist = "\n".join(f"{i + 1}. {check}（本文：{title}）。" for i, check in enumerate(checks))
    content = f'''---
title: "{title}"
description: "{desc}"
pubDate: 2026-09-28
category: "{cat}"
recommendationContext: "{rec_ctx}"
tags: [{tags_str}]
faq:
{faq_frontmatter}
---

# {title}

{title}聚焦“{focus}”这一{intent}问题。本文不把单次体验当作普遍结论，而是提供可复核的判断顺序、操作边界和下一步入口。

## {focus}：先确认要解决的是什么

围绕“{title}”，第一步不是直接更改所有设置，而是分清自己面对的是资料选择、配置导入还是连接异常。这个区分能避免把不相关的调整带入同一次排查。

### 本文适用范围

如果你的目标是{desc}，可按下文的检查项逐项记录结果；没有公开字段或无法重复的结果，应保留为“待确认”，而非推断为支持或不支持。

## {title} 的操作顺序

建议{action}。每完成一项，只改变一个变量，并保留上一项状态，以便发现问题时能够回退。

{checklist}

## 如何判断结果是否可靠

“{focus}”的可用性会随设备、网络、套餐和服务端更新而变化。对《{title}》而言，截图、宣传语或一次测速都只能作为线索；应以当前服务商页面、客户端日志和自己的实际访问结果交叉确认。

### 常见误区

不要把订阅兼容、协议名称、线路文字描述或服务列表自动等同于性能、安全性或长期可用性。本文的结论只覆盖“{title}”的说明范围，未列出的字段应在购买或修改前再确认。

## 下一步：选择资料明确的服务或继续学习

完成《{title}》的检查后，可浏览站内的机场资料页核对套餐、客户端和协议字段；涉及付费时优先选择短周期，并以服务商最新页面作为最终依据。
'''

    file_path = os.path.join('src/content/posts', f"{slug}.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Generated {len(articles)} comprehensive articles in src/content/posts/")

# Publication set: these are intentionally authored article-by-article.  The
# remaining source entries stay in the repository as drafts until they receive
# the same treatment; they are not generated as public thin pages.
CORE_BODIES = {
"what-is-clash-airport": '''## Clash 机场到底是什么

“机场”是社区对提供订阅、节点和用户后台的第三方服务的俗称；Clash、Mihomo 或其他客户端只是读取配置并按规则转发流量的本地软件。购买前要把服务商、订阅格式和客户端分开理解，不能把客户端名称当成服务质量证明。

## 一份订阅包含什么

订阅通常会返回节点列表、代理组和规则配置。它可能带有账户 Token，因此和密码一样不应公开。服务商是否提供 Clash 格式、哪些协议能导入、是否限制设备，都应在付款前从当前页面确认。

## 选择服务时核对哪些字段

先看套餐的计费周期、流量、重置方式、退款规则和客服渠道；再核对你的设备对应的客户端是否被明确支持。线路、解锁和带宽类文字属于服务资料描述，不是本站的性能认证。

## 第一次使用的稳妥流程

优先选择短周期套餐，保存订单和订阅链接，在一个设备上导入后测试自己常用的网站与网络环境。发现问题时先确认账户状态、订阅更新和本机代理设置，再向服务商提供具体报错和时间。
''',
"how-to-choose-clash-airport": '''## 先按用途而不是“排名”筛选

网页查资料、远程会议、视频和多设备使用消耗的流量与可接受延迟不同。先写下每月预算、预计流量、使用设备和最常访问的服务，才能看懂套餐字段；没有统一测试数据时，不应把展示顺序当作速度排名。

## 看套餐表的四个位置

确认价格对应月付、年付还是一次性流量包；确认流量是每月重置还是长期有效；确认节点倍率是否会影响实际消耗；最后看设备限制和退款条款。年付折合月价不等于可以按月取消。

## 线路和解锁宣传如何阅读

IPLC、IEPL、BGP 等是服务商的线路描述，不能单独推出延迟、抗封锁或稳定性结论。流媒体和 AI 字段也会随出口 IP 改变，应以服务商当期说明及自己的测试为准。

## 购买前的检查清单

保留短周期试用空间；先确认订阅支持你的客户端；在自己的宽带和常用时段测试；不要因促销一次性预存很长周期。出现资料缺失时，直接咨询服务商而不是自行补全。
''',
"clash-airport-vs-vpn": '''## 两者解决的问题并不完全相同

传统 VPN 常以一个连接承载较多流量；Clash 类客户端更常通过规则把不同域名或应用分到直连、代理组或不同节点。实际体验取决于配置、服务商和网络环境，而不是名称本身。

## 配置方式的差异

VPN 往往在客户端内选择服务器后连接；Clash 通常导入订阅，选择代理组并使用规则模式。规则写错、系统代理未开启或 TUN 冲突，都可能导致“已连接但不能上网”。

## 隐私与信任边界

无论使用哪种服务，提供者都可能处理连接元数据。应阅读服务商政策，不把订阅链接分享给他人，也不要因“加密”“专线”等标签推断绝对安全。

## 如何决定使用哪一种

若你需要按域名分流、管理多个节点或使用兼容订阅，Clash 生态可能更合适；若场景只需要单一企业 VPN，则按组织提供的工具配置。选择前以设备支持、管理方式和政策为准。
''',
"clash-verge-rev-tutorial": '''## 开始前准备

从项目官方发布页获取适合系统架构的安装包，确认来源和版本；不要把未知第三方“整合包”当作客户端更新。准备好服务商提供的订阅链接，并避免把链接截屏发到公开渠道。

## 导入配置

在 Profiles 或配置页新建远程配置，粘贴完整 URL 后下载。若下载失败，先在服务商后台确认套餐未到期、链接未重置，再记录客户端显示的错误，而非反复新建配置。

## 选择模式和节点

初次使用可先选规则模式，再在代理组中选择一个节点。系统代理只影响遵守系统代理的应用；如需 TUN，应先了解权限、路由与其他网络工具是否冲突。

## 维护与回退

更新订阅前保留可工作的配置。软件升级后若网络异常，关闭 TUN、系统代理或其他代理工具逐项验证；不能确认的问题应附上版本、系统和错误信息咨询服务商或客户端社区。
''',
"windows-clash-tutorial": '''## Windows 上先避免软件冲突

安装前退出其他代理、VPN、抓包和可能修改系统代理的软件。Windows 同一时间只能有一套明确的代理设置，多个程序抢写设置时常出现开关立即回弹或浏览器无网络。

## 导入订阅并检查状态

在客户端配置页导入服务商链接，确认下载时间和节点数量正常。账户到期、流量耗尽或订阅 URL 被重置时，先在用户后台解决，而不是只重装客户端。

## 系统代理与 TUN 的区别

系统代理适合浏览器等遵守代理设置的应用；TUN 会影响更广泛的网络路径，也更容易与游戏加速器、虚拟机或安全软件发生冲突。首次配置建议一次只开启一种方式。

## Windows 常见恢复步骤

不能上网时关闭系统代理，退出客户端后确认网络恢复；再检查端口占用、日期时间和防火墙提示。用手机热点交叉测试能帮助区分本机配置与当前网络限制。
''',
"android-clash-tutorial": '''## 选择与订阅格式兼容的应用

Android 客户端的内核和导入格式并不完全相同。先从服务商资料确认是否明确支持目标客户端；未写明时，不要把“通用订阅”自动理解为所有应用都可导入。

## 导入后的关键设置

粘贴订阅 URL，完成下载后选中配置，再按应用说明授权 VPN 权限。先在规则模式下验证一个常用网站；应用分流、绕过局域网等设置应在基本连接成功后再调整。

## 后台被系统关闭怎么办

不同品牌的省电策略不同。可以将客户端设为不受电池优化限制，并允许后台活动；这只是减少被系统结束的可能，不代表网络连接一定持续有效。

## 手机端排错顺序

依次确认套餐与订阅、移动数据或 Wi-Fi、VPN 权限、当前节点和 DNS 设置。切换网络后结果不同，通常说明需要继续检查本地网络，而不能凭一次失败判断服务端故障。
''',
"macos-clash-tutorial": '''## 安装与权限的边界

macOS 会对未签名或首次运行的软件给出安全提示。应从项目发布页获取文件，理解提示后在系统设置中授权；不要为绕过提示关闭整套系统安全机制。

## 添加远程订阅

在客户端配置管理中添加 URL 并下载，确认配置名称、更新时间和节点列表。订阅链接带有账户标识，复制给他人可能造成流量或账户风险。

## 系统代理、增强模式与终端

开启系统代理后，常规应用会按系统设置工作；终端和某些开发工具可能需要各自的代理变量或 TUN 配置。先确认浏览器连接正常，再按实际需要扩展到其他工具。

## 出现断网时如何回退

关闭客户端的系统代理或增强模式，确认 macOS 网络恢复。随后检查是否同时运行了公司 VPN、过滤软件或网络扩展；每次只改一项，以保留可复现的排查结果。
''',
"how-to-import-clash-subscription": '''## 获取正确的订阅地址

从已登录的服务商用户中心复制完整地址，不要使用搜索结果中的同名链接。链接通常包含 Token；泄露后应在后台重置，不应把它提交到在线转换站或公开求助帖。

## 自动导入与手动导入

网页的一键导入依赖浏览器和客户端的协议关联，失败并不一定表示订阅失效。手动方式更可控：复制 URL、在客户端新建远程配置、下载后选中配置。

## 下载失败先看什么

确认套餐状态、流量和 URL 是否仍有效；检查当前网络是否能访问服务商页面；再查看客户端具体错误。若单个客户端失败，可在不暴露链接的前提下咨询服务商其支持的格式。

## 导入成功后的验证

不要立刻开启复杂规则。先在一个设备上选节点、确认系统代理或 VPN 权限，再测试常用站点。保存可工作的配置，订阅更新前避免删除旧配置。
''',
"what-is-clash-subscription": '''## 订阅不是“一个节点”

订阅是一个可更新的配置入口，服务商可通过它下发节点、策略组和规则。客户端拉取后会保存一份本地配置，因此订阅更新、节点选择和本机代理开关是三个不同的环节。

## 为什么格式兼容很重要

不同客户端支持的协议与配置字段不同。服务商写有 Clash、Mihomo 或其他格式时，仍应确认是哪个客户端和内核；没有明确说明时，应在购买前询问而不是尝试猜测。

## Token 与账户安全

订阅 URL 常是账户凭证的一部分。把它发给别人会导致流量被使用或触发设备限制；发现泄露时在服务商后台重置，并在客户端替换旧链接。

## 更新的正确时机

更新用于获得服务商发布的新配置，不是解决所有网络问题的万能操作。更新前保存当前可用配置；更新后若问题出现，比较节点、订阅时间和服务商公告再决定下一步。
''',
"clash-subscription-failed-solutions": '''## 先区分“下载失败”和“导入后失败”

客户端提示下载失败时，问题可能在 URL、账户、网络或 TLS；下载成功但节点不可用，则还要看代理选择和本机设置。把这两类现象分开，能避免无效重装。

## 订阅本身的检查

登录服务商后台确认套餐未到期、流量未耗尽、订阅没有被重置。复制新链接时不要遗漏参数；若后台有公告或维护提示，应优先按公告等待或咨询。

## 本机与网络检查

确认设备日期时间正确，暂时关闭其他 VPN/代理，再用另一网络或手机热点测试。不同网络结果不同，提示问题可能与当前出口、DNS 或网络限制有关。

## 何时联系服务商

提供不含完整 Token 的错误截图、客户端版本、系统、失败时间和网络类型。避免只说“不能用”；具体信息能让对方判断是订阅分发、账户还是客户端兼容问题。
''',
"clash-nodes-all-timeout-solutions": '''## “全部超时”意味着先查共同条件

当所有节点都超时，不应先逐个测速或随机换节点。共同原因更常见：套餐到期、流量耗尽、订阅过期、系统时间异常、当前网络限制或本机代理冲突。

## 从账户和订阅开始

登录用户中心确认有效期和流量；复制当前订阅更新一次，并观察下载是否成功。若连服务商后台都无法访问，记录时间并查看公告，而不是把旧节点名称当成故障证据。

## 本机排查顺序

退出其他 VPN、代理和加速器；确认系统日期时间；检查系统代理与 TUN 是否同时开启；再尝试一个明确可用的节点。DNS 或端口设置只应在基本账户状态确认后调整。

## 用另一网络做交叉判断

切换手机热点或另一 Wi-Fi 后重新测试。若只在某个网络失败，更可能是本地网络条件；若多网络均失败且账户正常，再带上日志和时间联系服务商。
''',
"clash-connected-but-no-internet": '''## 先确认“连接成功”的含义

客户端显示已连接只表示本地进程或 VPN 接口已启动，不等于所有流量都能访问。需要分别测试浏览器、一个规则命中的域名和一个直连域名，判断问题发生在哪一层。

## 规则与代理模式

规则模式依赖配置中的规则集和代理组；全局模式会把更多流量交给当前节点。先选择一个明确的代理组节点，再检查是否误把需要代理的流量设为直连，或反过来把局域网流量交给代理。

## 系统代理和 TUN 的冲突

Windows、macOS 和 Android 的代理机制不同。系统代理无法覆盖所有应用，TUN 又可能与公司 VPN、虚拟机或安全软件冲突。一次只启用一种模式，先验证网络恢复再扩展设置。

## DNS 与网络交叉测试

若域名打不开而 IP 行为不同，才考虑 DNS 设置；不要在没有现象的情况下随意复制公共 DNS 配置。更换 Wi-Fi 或热点可帮助判断是当前网络、节点还是本机规则导致。
''',
"what-is-iepl-node": '''## IEPL 通常指什么

IEPL 是国际以太网专线的行业术语，常用于描述点到点或专用的跨境网络连接服务。机场页面出现 IEPL 并不自动说明每一段链路、所有节点或整个套餐都使用同一种路径。

## 与公网中转和 IPLC 的关系

公网中转、IEPL 和 IPLC 是不同的服务商网络描述，实际网络会包含入口、转发、出口和本地运营商等多个环节。名称不能单独证明延迟、丢包、抗干扰能力或安全性。

## 用户需要核对什么

查看服务商是否说明适用套餐、节点地区、倍率、流量和客户端格式；有固定业务需求时询问是否有对应节点或退款规则。不要把“专线”当成统一质量等级。

## 谁可能需要，谁不必额外付费

对延迟或路径有明确需求的人可将其作为询问项目；普通网页或低频使用者更应先比较套餐周期、流量和兼容性。短周期实测比仅凭线路标签更有参考价值。
''',
"what-is-iplc-node": '''## IPLC 的基本含义

IPLC 常指国际私人租用线路，是电信网络中的一种术语。机场资料使用“IPLC 节点”时，具体的跨境路径、覆盖范围和接入方式仍需由服务商说明，不能只凭标签推断整个网络架构。

## 为什么宣传语需要再核验

一条实际连接通常包含用户本地网络、入口、跨境段和海外出口。即使某一段使用租用线路，最终延迟、可用性和丢包也会受到其他环节影响，因此“IPLC”不是性能或抗封锁承诺。

## 与 IEPL 怎么比较

两个术语在服务商页面的使用并不总是统一。比较时应回到可验证信息：套餐是否明确、节点区域、流量倍率、设备规则、支持客户端与售后说明，而不是制作绝对优劣排序。

## 购买前的问题清单

询问线路描述适用于哪些套餐和地区；确认是否有试用或短周期；记录自己网络下的测试结果；出现不符合预期时按退款或工单规则处理。这样比为一个标签支付溢价更稳妥。
''',
"what-is-node-multiplier": '''## 节点倍率如何影响流量

倍率是服务商用于计算套餐流量消耗的规则。例如 1x 通常表示传输 1GB 记作 1GB，较高倍率则会更快消耗套餐流量。具体算法和四舍五入方式以服务商当前规则为准。

## 不要把倍率和速度混为一谈

倍率描述的是计费，不是带宽、延迟或稳定性评分。一个标注 1x 的节点也不必然更快；选择节点仍需结合目的地、当前网络和业务需求。

## 查看套餐时的实际计算

先确认流量包是否按月重置，再看常用地区的倍率。若每月流量有限，较高倍率节点会缩短可用时间；一次性流量包同样要看是否有有效期、是否会因倍率加速消耗。

## 购买前的核验动作

在服务商文档中找倍率表和变更规则，保存购买时页面截图。字段缺失时先咨询客服；不要依据其他服务商的倍率规则替代当前套餐说明。
'''
}

article_by_slug = {item['slug']: item for item in articles}
CORE_METADATA_OVERRIDES = {
    'what-is-iplc-node': {
        'title': 'IPLC节点是什么？国际专线、线路特点与机场宣传怎么判断',
        'description': '解释 IPLC 的基本概念、与 IEPL/公网中转的区别，以及购买机场时如何核对所谓 IPLC 线路资料。',
        'faq': [
            {'q': 'IPLC 可以无视防火墙吗？', 'a': '不能这样判断。IPLC 通常指国际私人租用线路，但机场所称 IPLC 节点的具体跨境路径需要以服务商实际网络架构为准。'},
            {'q': 'IPLC 标签代表一定更稳定吗？', 'a': '不代表。延迟、丢包和可用性还受本地网络、入口、出口和服务商配置影响。'}
        ]
    },
    'what-is-iepl-node': {
        'title': 'IEPL节点是什么？线路含义、适用场景与购买前核验',
        'description': '说明 IEPL 的基本术语、与 IPLC/公网中转的关系，以及购买前应向服务商确认的实际字段。'
    }
}
for path in os.scandir('src/content/posts'):
    if path.name.endswith('.md') and path.name[:-3] not in CORE_BODIES:
        old = open(path.path, encoding='utf-8').read()
        if 'draft: true' not in old:
            old = old.replace('pubDate:', 'draft: true\npubDate:', 1)
            open(path.path, 'w', encoding='utf-8').write(old)

for slug, body in CORE_BODIES.items():
    item = {**article_by_slug[slug], **CORE_METADATA_OVERRIDES.get(slug, {})}
    faq = '\n'.join(f'  - q: "{x["q"]}"\n    a: "{x["a"]}"' for x in item['faq'])
    tags = ', '.join(f'"{tag}"' for tag in item['tags'])
    markdown = f'''---
title: "{item['title']}"
description: "{item['description']}"
pubDate: 2026-09-28
category: "{item['category']}"
recommendationContext: "{item['recommendationContext']}"
tags: [{tags}]
faq:
{faq}
---

# {item['title']}

{body}
'''
    open(os.path.join('src/content/posts', f'{slug}.md'), 'w', encoding='utf-8').write(markdown)

print(f'Published article set: {len(CORE_BODIES)}; drafts: {len(articles) - len(CORE_BODIES)}')
