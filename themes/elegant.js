// Elegant Theme JS

document.addEventListener('DOMContentLoaded', function() {
    // 为代码块添加复制按钮
    addCopyButtons();
    
    // 处理目录
    processToc();
    
    // 为图片添加点击放大效果
    addImageZoom();
    
    // 平滑滚动
    enableSmoothScroll();
    
    // 添加表格响应式支持
    makeTablesResponsive();
});

// 为代码块添加复制按钮
function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(codeBlock) {
        const pre = codeBlock.parentNode;
        if (!pre.querySelector('.copy-button')) {
            const button = document.createElement('button');
            button.className = 'copy-button';
            button.textContent = '复制';
            
            button.addEventListener('click', function() {
                const code = codeBlock.textContent;
                navigator.clipboard.writeText(code).then(function() {
                    // 复制成功后的视觉反馈
                    const originalText = button.textContent;
                    button.textContent = '已复制!';
                    button.style.backgroundColor = '#48bb78';
                    button.style.color = 'white';
                    
                    setTimeout(function() {
                        button.textContent = originalText;
                        button.style.backgroundColor = '';
                        button.style.color = '';
                    }, 2000);
                }).catch(function(err) {
                    console.error('复制失败:', err);
                    button.textContent = '复制失败';
                    button.style.backgroundColor = '#f56565';
                    button.style.color = 'white';
                    
                    setTimeout(function() {
                        button.textContent = '复制';
                        button.style.backgroundColor = '';
                        button.style.color = '';
                    }, 2000);
                });
            });
            
            pre.appendChild(button);
            pre.style.position = 'relative';
        }
    });
}

// 处理目录
function processToc() {
    const tocPlaceholder = document.querySelector('.toc-placeholder');
    if (tocPlaceholder) {
        const toc = document.createElement('div');
        toc.className = 'table-of-contents';
        
        const tocTitle = document.createElement('h2');
        tocTitle.textContent = '目录';
        toc.appendChild(tocTitle);
        
        const tocList = document.createElement('ul');
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        
        headings.forEach(function(heading, index) {
            if (!heading.id) {
                heading.id = 'heading-' + index;
            }
            
            const listItem = document.createElement('li');
            listItem.className = heading.tagName.toLowerCase();
            
            const link = document.createElement('a');
            link.href = '#' + heading.id;
            link.textContent = heading.textContent;
            
            listItem.appendChild(link);
            tocList.appendChild(listItem);
        });
        
        toc.appendChild(tocList);
        tocPlaceholder.parentNode.replaceChild(toc, tocPlaceholder);
    }
}

// 为图片添加点击放大效果
function addImageZoom() {
    const images = document.querySelectorAll('.container img:not(.no-zoom)');
    
    images.forEach(function(img) {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            overlay.style.display = 'flex';
            overlay.style.alignItems = 'center';
            overlay.style.justifyContent = 'center';
            overlay.style.zIndex = '9999';
            overlay.style.cursor = 'zoom-out';
            
            const zoomedImg = document.createElement('img');
            zoomedImg.src = img.src;
            zoomedImg.style.maxWidth = '90%';
            zoomedImg.style.maxHeight = '90%';
            zoomedImg.style.objectFit = 'contain';
            zoomedImg.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.5)';
            zoomedImg.style.transition = 'transform 0.3s ease';
            zoomedImg.style.transform = 'scale(0.9)';
            
            setTimeout(function() {
                zoomedImg.style.transform = 'scale(1)';
            }, 50);
            
            overlay.appendChild(zoomedImg);
            document.body.appendChild(overlay);
            
            overlay.addEventListener('click', function() {
                zoomedImg.style.transform = 'scale(0.9)';
                
                setTimeout(function() {
                    document.body.removeChild(overlay);
                }, 200);
            });
        });
    });
}

// 启用平滑滚动
function enableSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 使表格响应式
function makeTablesResponsive() {
    const tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        const wrapper = document.createElement('div');
        wrapper.style.overflow = 'auto';
        wrapper.style.marginBottom = '1.5em';
        
        // 在小屏幕上添加指示器
        if (window.innerWidth < 768) {
            wrapper.style.background = 
                'linear-gradient(to right, white 30%, rgba(255, 255, 255, 0)), ' +
                'linear-gradient(to left, white 30%, rgba(255, 255, 255, 0)) 100% 0, ' +
                'radial-gradient(farthest-side at 0 50%, rgba(0, 0, 0, .2), rgba(0, 0, 0, 0)), ' +
                'radial-gradient(farthest-side at 100% 50%, rgba(0, 0, 0, .2), rgba(0, 0, 0, 0)) 100% 0';
            wrapper.style.backgroundRepeat = 'no-repeat';
            wrapper.style.backgroundSize = '40px 100%, 40px 100%, 14px 100%, 14px 100%';
            wrapper.style.backgroundAttachment = 'local, local, scroll, scroll';
        }
        
        // 将表格包装起来
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
}

// 检测深色模式
function detectDarkMode() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        // 如果用户系统设置为深色模式，可在此处添加额外的样式处理
        console.log('用户偏好深色模式');
    }
}

// 添加代码高亮行
function highlightCodeLines() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(codeBlock) {
        const lines = codeBlock.innerHTML.split('\n');
        let highlightedHTML = '';
        
        lines.forEach(function(line, index) {
            if (line.trim().startsWith('// highlight') || line.trim().startsWith('# highlight')) {
                highlightedHTML += '<div class="highlight-line">' + line + '</div>';
            } else {
                highlightedHTML += '<div>' + line + '</div>';
            }
        });
        
        codeBlock.innerHTML = highlightedHTML;
    });
} 