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
                            button.textContent = '已复制!';
                            button.style.backgroundColor = '#dafbe1';
                            button.style.color = '#1a7f37';
                            setTimeout(function() {
                                button.textContent = '复制';
                                button.style.backgroundColor = '';
                                button.style.color = '';
                            }, 2000);
                        },
                        function(err) {
                            console.error('无法复制文本: ', err);
                            button.textContent = '复制失败';
                            button.style.backgroundColor = '#ffebe9';
                            button.style.color = '#cf222e';
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
    
    // 添加锚点链接到标题
    document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(heading => {
        if (heading.id) {
            const anchor = document.createElement('a');
            anchor.className = 'anchor';
            anchor.href = `#${heading.id}`;
            anchor.innerHTML = '<svg class="octicon octicon-link" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg>';
            heading.insertBefore(anchor, heading.firstChild);
            
            heading.style.position = 'relative';
            anchor.style.position = 'absolute';
            anchor.style.left = '-20px';
            anchor.style.visibility = 'hidden';
            
            heading.addEventListener('mouseenter', function() {
                anchor.style.visibility = 'visible';
            });
            
            heading.addEventListener('mouseleave', function() {
                anchor.style.visibility = 'hidden';
            });
        }
    });
}); 