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
                            setTimeout(function() {
                                button.textContent = '复制';
                            }, 2000);
                        },
                        function(err) {
                            // 复制失败
                            console.error('无法复制文本: ', err);
                            button.textContent = '复制失败';
                            setTimeout(function() {
                                button.textContent = '复制';
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
}); 