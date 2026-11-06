# -*- coding: utf-8 -*-
"""
在局域网里把「技师记录 App」跑起来，供手机访问。

用法（在本文件所在目录打开 PowerShell）：
    python serve.py
    python serve.py 8080

然后把打印出来的 http://192.168.x.x:8000 地址在手机 Safari 里打开，
再用「分享 → 添加到主屏幕」。

注意：http 局域网地址下，iOS 不允许注册 Service Worker，
所以「断网也能打开」不会生效（但功能完全正常，只要连在同一个网里）。
要真离线，请把这个文件夹放到任意 https 静态托管上，见《部署说明.md》。
"""
import http.server
import mimetypes
import os
import socket
import socketserver
import sys

mimetypes.add_type("application/manifest+json", ".webmanifest")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("image/png", ".png")


def lan_ips():
    ips = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except OSError:
        pass
    return sorted(ips)


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 开发时避免缓存困扰；Service Worker 本身也不缓存 index
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("  %s\n" % (fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.ThreadingTCPServer(("0.0.0.0", port), Handler)
    except OSError as e:
        print(f"端口 {port} 起不来：{e}\n换个端口试试：python serve.py {port + 1}")
        return

    print("=" * 56)
    print(" 增强CBCT术中记录 —— 局域网服务已启动")
    print("=" * 56)
    print(f" 目录: {os.getcwd()}")
    print(" 手机 Safari 打开下面任一地址：")
    for ip in lan_ips():
        print(f"     http://{ip}:{port}/index.html")
    print(f"     http://127.0.0.1:{port}/index.html   （本机测试）")
    print()
    print(" 手机与这台电脑必须在同一个 Wi-Fi / 内网。")
    print(" 打开后：分享按钮 → 添加到主屏幕 → 之后从桌面图标进。")
    print()
    print(" 提示：http 地址下离线缓存不生效；要断网可用请用 https 托管。")
    print(" 按 Ctrl+C 停止。")
    print("=" * 56)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
