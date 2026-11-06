# GitHub Pages 部署步骤（Windows · 零命令行）

目标：拿到一个 `https://<你的用户名>.github.io/cbct-record/` 的网址，
手机 Safari 打开后「添加到主屏幕」，得到一个全屏、可离线用的 App 图标。

全程约 10 分钟，第一页部署后要等 1–3 分钟生效。

---

## 开始之前，先知道三件事

| 事项 | 说明 |
|---|---|
| **免费版只能公开仓库** | GitHub 免费账户的 Pages 只对 **Public** 仓库生效（Private 要付费 Pro）。仓库公开 = **程序代码公开**，但里面没有任何患者数据，可以接受。 |
| **网址谁都能打开** | 任何静态托管拿到的网址都是公开可访问的。所以 App 里**只放程序，不放数据**；患者编号用 `P001` 这类研究编号，不要填姓名住院号。 |
| **GitHub 是 https** | 这一点很关键：https 才允许注册 Service Worker，才有「断网也能打开」。这也正是它比内网 http 强的地方。 |

> 如果科里要求不能放公网，那就退回内网方案（`serve.py` 或 Django static），代价是断网打不开。见《部署说明.md》。

---

## 第 1 步：注册 GitHub

1. 打开 <https://github.com>
2. 右上角 **Sign up**
3. 邮箱 → 密码 → 用户名（用户名会成为网址的一部分，**建议全小写英文**，例如 `zhangweitech`）
4. 去邮箱收验证码，完成验证

> 用户名一旦定了就会出现在网址里，改起来麻烦，先想好。

---

## 第 2 步：新建仓库

1. 右上角 **+** → **New repository**
2. 填写：

   | 字段 | 填什么 |
   |---|---|
   | Repository name | `cbct-record` （**全小写，不要中文**） |
   | Description | 可不填 |
   | 公开性 | 选 **Public** |
   | Add a README file | 不勾 |
   | .gitignore / license | 都不选 |

3. 点 **Create repository**

成功后你会看到一个空仓库页面，中间有 "Quick setup" 的提示。

---

## 第 3 步：上传文件 ⚠️ 这一步最容易错

**关键：`index.html` 必须直接躺在仓库根目录，不能套一层文件夹。**

如果变成 `仓库/cbct-record/技师记录App/index.html`，网站根目录没有 index.html，打开就是 404。

### 正确操作

1. 在仓库页面点 **Add file** → **Upload files**
   （或者页面中间那行 "uploading an existing file"）
2. 在电脑上打开解压后的 `技师记录App` 文件夹
3. **进到文件夹里面**，`Ctrl+A` 全选**里面的内容**（不是选文件夹本身）
4. 拖进网页的上传框

要上传的东西长这样：

```
index.html
manifest.webmanifest
sw.js
.nojekyll
部署说明.md          ← 可传可不传，不影响功能
serve.py             ← 可传可不传，不影响功能
icons/
├── icon-180.png
├── icon-192.png
├── icon-512.png
└── icon-maskable-512.png
```

> `icons` 文件夹整个拖进去，GitHub 会自动保留目录结构。

5. 拉到页面底部，**Commit changes**

### 上传后必须核对

回到仓库首页，文件列表里**第一层就应该看到 `index.html`**。看到的是「技师记录App」这样的文件夹，说明套了一层，要重来：

- 点进那个文件夹 → 选中所有文件 → 用 **Add file → Upload files** 重新传到根目录
- 再删掉多出来的那层文件夹

**不要上传** `技师记录App.zip`（没用，而且 GitHub 网页上传对 zip 不友好）。

---

## 第 4 步：开启 Pages

1. 仓库页面上方 **Settings**
2. 左侧栏往下找 **Pages**
3. **Source** 选 **Deploy from a branch**
4. **Branch** 选 `main`，右边文件夹选 **/ (root)**
5. 点 **Save**
6. 等 1–3 分钟，刷新页面，顶部会出现一条绿色提示：

   ```
   Your site is live at https://<你的用户名>.github.io/cbct-record/
   ```

7. 同一页面向下，**Enforce HTTPS** 勾上（通常默认已勾）

> 如果 3 分钟后还没生效，去 **Actions** 标签页看 "pages build and deployment" 那条任务是不是绿色的。红色就点进去看错误。

---

## 第 5 步：手机上装成 App

**必须用 Safari**，不要用微信、不要用 Chrome。

1. Safari 打开：`https://<你的用户名>.github.io/cbct-record/`
2. 页面正常显示「患者编号 / 日期 / 技师 / 设备」
3. 点底部 **「导出 / 交接」→「历史台次」**，确认最后一行写着：

   ```
   离线缓存：已启用（断网也能打开）
   ```

   看到这句才说明离线可用。如果显示「需通过 https」，检查地址栏是不是 https。

4. 点 Safari **分享**按钮（方框带向上箭头）
5. 往下滑，选 **添加到主屏幕**
6. 名字会自动填「CBCT记录」，点右上角 **添加**

回桌面，图标出现。**以后从图标进，不要再用 Safari 开。**

---

## 第 6 步：验证真的能离线

1. 打开手机的**飞行模式**
2. 从桌面点图标
3. 能正常打开、能加记录 → 成功

---

## 以后怎么更新

### 方式一：网页上传（不用装任何工具）

1. 仓库 → **Add file** → **Upload files**
2. 拖入改动过的文件（同名会覆盖）
3. **Commit changes**
4. 等 1–2 分钟

### 方式二：GitHub Desktop（改得勤的话更省事）

1. 装 [GitHub Desktop](https://desktop.github.com/)，登录
2. **File → Clone repository** → 选 `cbct-record`
3. 以后直接把文件夹里的文件复制进克隆下来的目录
4. 在 GitHub Desktop 里填一句说明 → **Commit to main** → **Push origin**

### ⚠️ 更新后手机上要刷新

Service Worker 会缓存旧版本，所以手机上看不到新内容。两个办法：

- **简单**：删掉主屏图标 → 浏览器打开网址 → 重新「添加到主屏幕」
- **规范**：把 `sw.js` 里的 `const CACHE = "cbct-record-v1"` 改成 `v2`，提交后再重装

---

## 常见问题

**Q：打开是 404**
A：`index.html` 不在仓库根目录。检查仓库首页第一层有没有 `index.html`。

**Q：打开显示的是 README**
A：创建仓库时勾了 "Add a README"，而 index.html 没上传成功。确认根目录有 `index.html`。

**Q：显示「离线缓存：未启用（需 https）」**
A：地址不是 https，或者是用了 IP 地址访问。GitHub Pages 强制 https，检查是不是输成了 `http://`。

**Q：Safari 里找不到「添加到主屏幕」**
A：① 在无痕模式 → 退出无痕；② 页面没加载完；③ 用的是微信/其他浏览器内置内核。

**Q：图标是灰的 / 是个网址截图**
A：iOS 缓存了旧的 apple-touch-icon。删掉图标，清一下 Safari 该站点数据，重新添加。

**Q：Actions 里那条任务红了**
A：点进去看日志。绝大多数是文件路径大小写不一致（`icons/` vs `Icons/`）。GitHub Pages 区分大小写。

**Q：能不能设成私密，只有我们科能看**
A：GitHub Pages 没有访问控制。要限制访问得换 Cloudflare Access 之类的方案，或者放内网。但记住：**App 里没有数据，只有程序**，公开的风险很低。

**Q：网址太长，技师记不住**
A：不需要记。装到主屏幕后从图标进；或者把网址发到科室群里。

---

## 一次性核对清单

上传前：

- [ ] 解压 `技师记录App.zip`
- [ ] 确认 `index.html` 和 `icons` 是同一层
- [ ] 准备好 GitHub 账号（邮箱已验证）

上传后：

- [ ] 仓库首页第一层能看到 `index.html`
- [ ] Settings → Pages 已开，Source = main / (root)
- [ ] 绿色提示里有你的网址
- [ ] 浏览器打开该网址，页面正常
- [ ] 「历史台次」里显示「离线缓存：已启用」

手机：

- [ ] 用 Safari（不是微信）打开
- [ ] 分享 → 添加到主屏幕
- [ ] 飞行模式下从图标打开正常

---

## 附：命令行版（熟悉 git 的话更快）

```bash
git clone https://github.com/<用户名>/cbct-record.git
# 把 技师记录App 里的文件复制进去（index.html 与 icons 同级）
cd cbct-record
git add .
git commit -m "更新"
git push origin main
```

推上去后 Pages 会自动重新构建，1–2 分钟生效。
