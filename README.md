# nis7024-labs-template
SJTU NIS7024 课程实验模板
## 系统及软件要求
- 类 Linux 系统
- conda
## 实验要求与说明
1. 克隆本项目到本地：
`git clone https://github.com/odymit/nis7024-labs-template.git`
2. 本地新建 `conda` 环境，根据所使用的 Python 版本修改 `.env` 中的版本信息，并安装依赖 `pip install -r requirements.txt`
3. 在 `./code` 文件夹中，实现论文复现，详细要求如下：  
    - 论文实验的入口文件必须为 `main.py`
    - 论文实验的函数入口必须为 `train()`
    - `train` 函数的参数使用 `params` 传递，如模板所示
    - 在 `class Parameters` 定义所有所需参数
    - 在 `train` 函数中执行训练/攻击/检测/防御的全部过程
4. 完成实验后，使用 `test.py` 文件进行测试： `python test.py`
5. 将课程报告文档和复现的论文文档(pdf)放到 `docs` 文件夹 
6. 将整个项目打包压缩为 `.zip` 格式，重命名为你的学号，如： `022039910009.zip`，上传到服务器