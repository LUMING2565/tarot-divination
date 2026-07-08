@echo off
echo ================================
echo   🔮 塔罗牌占卜 - 后端服务
echo ================================
echo.
pip install -r requirements.txt -q
echo.
echo 🚀 启动 API 服务: http://localhost:8000
echo 📖 API 文档: http://localhost:8000/docs
echo.
python main.py
pause
