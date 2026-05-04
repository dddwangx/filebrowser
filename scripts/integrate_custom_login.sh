#!/bin/bash
# 集成自定义登录页面到Filebrowser

set -e

echo "=========================================="
echo "Filebrowser 自定义登录页面集成"
echo "=========================================="
echo ""

# 方案1: 使用Nginx反向代理
cat > nginx-filebrowser.conf << 'NGINX_EOF'
server {
    listen 8080;
    server_name localhost;

    # 自定义登录页面
    location = / {
        root /var/www/filebrowser;
        try_files /custom-login.html =404;
    }

    location /logos/ {
        root /var/www/filebrowser;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # 代理到Filebrowser
    location /filebrowser {
        proxy_pass http://localhost:8300;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API请求
    location /api/ {
        proxy_pass http://localhost:8300;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX_EOF

echo "✓ Nginx配置文件已创建: nginx-filebrowser.conf"
echo ""

# 方案2: 创建Docker Compose配置（带Nginx）
cat > docker-compose-with-nginx.yml << 'COMPOSE_EOF'
version: '3'

services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    restart: unless-stopped
    volumes:
      - ./data:/srv
      - ./config:/config
      - ./database:/database
    environment:
      - FB_BASEURL=/filebrowser
    networks:
      - filebrowser-net

  nginx:
    image: nginx:alpine
    container_name: filebrowser-nginx
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ./nginx-filebrowser.conf:/etc/nginx/conf.d/default.conf
      - ./frontend/public:/var/www/filebrowser
    depends_on:
      - filebrowser
    networks:
      - filebrowser-net

networks:
  filebrowser-net:
    driver: bridge
COMPOSE_EOF

echo "✓ Docker Compose配置已创建: docker-compose-with-nginx.yml"
echo ""

# 方案3: 修改登录页面的表单提交地址
cat > frontend/public/custom-login-integrated.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Filebrowser - 登录</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            height: 100vh;
            overflow: hidden;
            position: relative;
        }

        .animated-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 25%, 
                #f093fb 50%, 
                #4facfe 75%, 
                #00f2fe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite, breathe 8s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes breathe {
            0%, 100% { opacity: 0.9; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.05); }
        }

        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 20px;
        }

        .login-box {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 100%;
            max-width: 420px;
            animation: slideIn 0.6s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .logo-container {
            text-align: center;
            margin-bottom: 30px;
            position: relative;
            height: 120px;
            overflow: hidden;
        }

        .logo-image {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid transparent;
            background: linear-gradient(white, white) padding-box,
                        linear-gradient(135deg, #667eea, #764ba2, #f093fb) border-box;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            animation: logoFadeIn 1s ease-in-out;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
        }

        @keyframes logoFadeIn {
            0% { opacity: 0; transform: translateX(-50%) scale(0.8); }
            100% { opacity: 1; transform: translateX(-50%) scale(1); }
        }

        .title {
            text-align: center;
            margin-bottom: 30px;
        }

        .title h1 {
            font-size: 32px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            animation: titlePulse 3s ease-in-out infinite;
        }

        @keyframes titlePulse {
            0%, 100% { opacity: 0.9; }
            50% { opacity: 1; }
        }

        .title p {
            color: #666;
            font-size: 14px;
            font-weight: 600;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 700;
            font-size: 14px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 15px;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .login-button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .login-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        .login-button:active {
            transform: translateY(0);
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
            font-weight: 600;
        }

        .error-message {
            display: none;
            background: #fee;
            color: #c33;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 14px;
            font-weight: 600;
        }

        .error-message.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="animated-background"></div>
    
    <div class="login-container">
        <div class="login-box">
            <div class="logo-container">
                <img id="logo" class="logo-image" src="/logos/logo_01.jpg" alt="Logo">
            </div>
            
            <div class="title">
                <h1>Filebrowser</h1>
                <p>安全的文件管理系统</p>
            </div>

            <div id="errorMessage" class="error-message"></div>
            
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input type="text" id="username" name="username" required autocomplete="username">
                </div>
                
                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" name="password" required autocomplete="current-password">
                </div>
                
                <button type="submit" class="login-button">登录</button>
            </form>
            
            <div class="footer">
                <p>© 2026 Filebrowser - Powered by Nature</p>
            </div>
        </div>
    </div>

    <script>
        // Logo轮播
        const logoImages = [
            '/logos/logo_01.jpg', '/logos/logo_02.jpg', '/logos/logo_03.jpg',
            '/logos/logo_04.jpg', '/logos/logo_05.jpg', '/logos/logo_06.jpg',
            '/logos/logo_07.jpg', '/logos/logo_08.jpg', '/logos/logo_09.jpg',
            '/logos/logo_10.jpg', '/logos/logo_11.jpg', '/logos/logo_12.jpg',
            '/logos/logo_13.jpg', '/logos/logo_14.jpg', '/logos/logo_15.jpg'
        ];
        
        let currentLogoIndex = 0;
        const logoElement = document.getElementById('logo');
        
        function changeLogo() {
            currentLogoIndex = (currentLogoIndex + 1) % logoImages.length;
            logoElement.style.animation = 'none';
            setTimeout(() => {
                logoElement.src = logoImages[currentLogoIndex];
                logoElement.style.animation = 'logoFadeIn 1s ease-in-out';
            }, 50);
        }
        
        setInterval(changeLogo, 5000);
        
        // 表单提交 - 调用Filebrowser API
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('errorMessage');
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    // 保存token并跳转
                    localStorage.setItem('auth', data.token || data);
                    window.location.href = '/filebrowser';
                } else {
                    errorMessage.textContent = '用户名或密码错误';
                    errorMessage.classList.add('show');
                    setTimeout(() => {
                        errorMessage.classList.remove('show');
                    }, 3000);
                }
            } catch (error) {
                errorMessage.textContent = '登录失败，请稍后重试';
                errorMessage.classList.add('show');
                setTimeout(() => {
                    errorMessage.classList.remove('show');
                }, 3000);
            }
        });
    </script>
</body>
</html>
HTML_EOF

echo "✓ 集成版登录页面已创建: frontend/public/custom-login-integrated.html"
echo ""

echo "=========================================="
echo "集成方案"
echo "=========================================="
echo ""
echo "方案1: 使用Nginx反向代理（推荐）"
echo "  1. 安装Nginx: sudo apt-get install nginx"
echo "  2. 复制配置: sudo cp nginx-filebrowser.conf /etc/nginx/sites-available/"
echo "  3. 创建软链接: sudo ln -s /etc/nginx/sites-available/nginx-filebrowser.conf /etc/nginx/sites-enabled/"
echo "  4. 测试配置: sudo nginx -t"
echo "  5. 重启Nginx: sudo systemctl restart nginx"
echo "  6. 访问: http://localhost:8080"
echo ""
echo "方案2: 使用Docker Compose + Nginx"
echo "  1. 停止当前容器: docker stop filebrowser"
echo "  2. 启动新配置: docker-compose -f docker-compose-with-nginx.yml up -d"
echo "  3. 访问: http://localhost:8080"
echo ""
echo "方案3: 直接访问自定义页面（仅预览）"
echo "  访问: http://localhost:8080/custom-login.html"
echo "  注意: 需要手动配置API端点"
echo ""
echo "=========================================="
