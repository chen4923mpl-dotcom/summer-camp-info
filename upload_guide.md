GitHub上传指南：

由于当前环境无法直接通过GitHub CLI上传，您可以手动上传：

1. 创建新的GitHub仓库：
   - 访问 https://github.com/new
   - 创建名为 "summer-camp-info" 或类似名称的仓库

2. 上传文件：
   - 点击 "Add file" → "Upload files"
   - 上传以下文件：
     - README.md
     - 夏令营汇总.docx.md
     - 夏令营信息.csv
     - 夏令营信息.xlsx.md

3. 或者使用Git命令行：
git clone <your-repository-url>
cp /root/.openclaw/workspace/github_files/* .
git add .
git commit -m "添加985高校和中科院生物相关专业夏令营信息"
git push
