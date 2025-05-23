document.addEventListener('DOMContentLoaded', function() {
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
                            button.style.backgroundColor = '#dbc396';
                            button.style.color = '#47320f';
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
                            button.style.backgroundColor = '#d7bca2';
                            button.style.color = '#6b3a16';
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
    
    // 为链接添加下划线效果
    const links = document.querySelectorAll('a:not(.table-of-contents a)');
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.borderBottomColor = this.style.color;
            this.style.transition = 'border-bottom-color 0.3s, color 0.3s';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.borderBottomColor = 'transparent';
        });
    });
    
    // 为图片添加点击放大查看效果
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.title = '点击查看大图';
        
        img.addEventListener('click', function() {
            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.backgroundColor = 'rgba(91, 70, 54, 0.9)';
            overlay.style.zIndex = '1000';
            overlay.style.display = 'flex';
            overlay.style.alignItems = 'center';
            overlay.style.justifyContent = 'center';
            overlay.style.cursor = 'zoom-out';
            
            const imgClone = document.createElement('img');
            imgClone.src = this.src;
            imgClone.style.maxHeight = '90%';
            imgClone.style.maxWidth = '90%';
            imgClone.style.boxShadow = '0 5px 25px rgba(0, 0, 0, 0.4)';
            imgClone.style.borderRadius = '6px';
            imgClone.style.border = '8px solid #f5efe0';
            
            overlay.appendChild(imgClone);
            document.body.appendChild(overlay);
            
            overlay.addEventListener('click', function() {
                document.body.removeChild(overlay);
            });
        });
    });
    
    // 应用舒适阅读体验（轻微增加字间距）
    document.querySelectorAll('p, li').forEach(element => {
        element.style.wordSpacing = '0.05em';
        element.style.letterSpacing = '0.01em';
    });
}); 