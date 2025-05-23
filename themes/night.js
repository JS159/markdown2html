document.addEventListener('DOMContentLoaded', function() {
    // 标记文档为暗黑模式
    document.body.setAttribute('data-theme', 'dark');
    
    // 添加复制按钮到所有代码块
    const codeBlocks = document.querySelectorAll('pre');
    codeBlocks.forEach(block => {
        if (!block.querySelector('.copy-button')) {
            const button = document.createElement('button');
            button.className = 'copy-button';
            button.textContent = '复制';
            
            button.addEventListener('click', function() {
                const code = block.querySelector('code');
                if (code) {
                    const textToCopy = code.innerText;
                    navigator.clipboard.writeText(textToCopy).then(
                        function() {
                            // 复制成功
                            button.textContent = '已复制!';
                            button.style.backgroundColor = '#3a3a3a';
                            button.style.color = '#00fff5';
                            setTimeout(function() {
                                button.textContent = '复制';
                                button.style.backgroundColor = '';
                                button.style.color = '';
                            }, 2000);
                        },
                        function(err) {
                            // 复制失败
                            console.error('无法复制文本: ', err);
                            button.textContent = '复制失败';
                            button.style.backgroundColor = '#442c2d';
                            button.style.color = '#ff7b72';
                            setTimeout(function() {
                                button.textContent = '复制';
                                button.style.backgroundColor = '';
                                button.style.color = '';
                            }, 2000);
                        }
                    );
                }
            });
            
            block.style.position = 'relative';
            block.appendChild(button);
        }
    });
    
    // 生成目录
    if (document.querySelector('.toc-placeholder')) {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        if (headings.length > 0) {
            let toc = '<div class="table-of-contents">';
            toc += '<h2>目录</h2>';
            toc += '<ul>';
            
            headings.forEach(function(heading, index) {
                const id = `heading-${index}`;
                heading.id = id;
                
                const level = parseInt(heading.tagName.substring(1));
                toc += `<li class="h${level}"><a href="#${id}">${heading.textContent}</a></li>`;
            });
            
            toc += '</ul></div>';
            
            document.querySelectorAll('.toc-placeholder').forEach(placeholder => {
                placeholder.outerHTML = toc;
            });
        }
    }
    
    // 添加悬浮效果到图片
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        
        img.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.02)';
            this.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.5)';
        });
        
        img.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.3)';
        });
    });
    
    // 为标题添加鼠标悬停效果
    const allHeadings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    allHeadings.forEach(heading => {
        heading.style.transition = 'color 0.3s ease';
        
        heading.addEventListener('mouseover', function() {
            const originalColor = this.style.color;
            this.setAttribute('data-original-color', originalColor);
            
            // 根据标签选择高亮颜色
            if (this.tagName === 'H1' || this.tagName === 'H2') {
                this.style.color = '#cf9fff'; // 更亮的紫色
            } else if (this.tagName === 'H3') {
                this.style.color = '#ff879d'; // 更亮的粉红色
            } else {
                this.style.color = '#4fffeb'; // 更亮的青色
            }
        });
        
        heading.addEventListener('mouseout', function() {
            const originalColor = this.getAttribute('data-original-color');
            this.style.color = originalColor;
        });
    });
}); 