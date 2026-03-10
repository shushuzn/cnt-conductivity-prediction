@echo off
REM 推送 CNT 研究到 GitHub
REM 用法：双击运行此脚本

echo ===============================================
echo 推送 CNT 研究到 GitHub
echo ===============================================
echo.

REM 设置仓库 URL
set REPO_URL=https://github.com/shushuzn/cnt-conductivity-prediction.git

echo 步骤 1: 添加远程仓库...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo 步骤 2: 推送到 GitHub...
git push -u origin main

echo.
echo ===============================================
echo 完成！
echo ===============================================
echo.
echo 请访问：https://github.com/shushuzn/cnt-conductivity-prediction
echo.
pause
