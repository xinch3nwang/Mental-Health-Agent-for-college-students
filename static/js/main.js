// 主JavaScript文件
// 处理前端交互逻辑

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 导航栏滚动效果
    initNavbarScroll();

    // 平滑滚动
    initSmoothScroll();

    // 表单验证
    initFormValidation();

    // 音频录制功能 (如果页面上有录音按钮)
    if (document.getElementById('record-btn')) {
        initAudioRecording();
    }

    // 初始化图表 (如果页面上有图表容器)
    initCharts();

    // 初始化模态框
    initModals();
});

// 导航栏滚动效果
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 10) {
            navbar.classList.add('nav-scrolled');
        } else {
            navbar.classList.remove('nav-scrolled');
        }
    });
}

// 平滑滚动
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// 表单验证
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // 基本验证 - 确保必填字段不为空
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    // 显示错误消息 (如果有)
                    const errorElement = field.nextElementSibling;
                    if (errorElement && errorElement.classList.contains('text-red-500')) {
                        errorElement.textContent = '此字段为必填项';
                    }
                } else {
                    field.classList.remove('border-red-500');
                    // 清除错误消息 (如果有)
                    const errorElement = field.nextElementSibling;
                    if (errorElement && errorElement.classList.contains('text-red-500')) {
                        errorElement.textContent = '';
                    }
                }
            });

            // 如果表单无效，阻止提交
            if (!isValid) {
                e.preventDefault();
                // 滚动到第一个错误字段
                const firstErrorField = this.querySelector('.border-red-500');
                if (firstErrorField) {
                    firstErrorField.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
            }
        });

        // 实时验证 - 当用户输入时移除错误状态
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.classList.contains('border-red-500')) {
                    if (this.value.trim()) {
                        this.classList.remove('border-red-500');
                        // 清除错误消息 (如果有)
                        const errorElement = this.nextElementSibling;
                        if (errorElement && errorElement.classList.contains('text-red-500')) {
                            errorElement.textContent = '';
                        }
                    }
                }
            });
        });
    });
}

// 音频录制功能
function initAudioRecording() {
    const recordBtn = document.getElementById('record-btn');
    const recordingStatus = document.getElementById('recording-status');
    const audioPreview = document.getElementById('audio-preview');
    const audioPlayer = document.getElementById('audio-player');
    const audioData = document.getElementById('audio-data');
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    if (!recordBtn) return;

    recordBtn.addEventListener('click', function() {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });

    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener('stop', () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioPlayer.src = audioUrl;

                    // Convert blob to base64 for form submission
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = function() {
                        audioData.value = reader.result;
                    };

                    audioPreview.classList.remove('hidden');
                });

                mediaRecorder.start();
                isRecording = true;
                recordBtn.innerHTML = '<i class="fas fa-stop mr-2"></i>停止录音';
                recordBtn.classList.remove('bg-red-500', 'hover:bg-red-600');
                recordBtn.classList.add('bg-green-500', 'hover:bg-green-600');
                recordingStatus.classList.remove('hidden');
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                alert('无法访问麦克风。请确保您已授予麦克风权限。');
            });
    }

    function stopRecording() {
        mediaRecorder.stop();
        isRecording = false;
        recordBtn.innerHTML = '<i class="fas fa-microphone mr-2"></i>开始录音';
        recordBtn.classList.remove('bg-green-500', 'hover:bg-green-600');
        recordBtn.classList.add('bg-red-500', 'hover:bg-red-600');
        recordingStatus.classList.add('hidden');

        // Stop all audio tracks
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
}

// 初始化图表
function initCharts() {
    // 检查Chart.js是否已加载
    if (typeof Chart === 'undefined') return;

    // 情绪趋势图表
    const emotionTrendCtx = document.getElementById('emotionTrendChart');
    if (emotionTrendCtx) {
        // 这里只是初始化图表框架，实际数据应该从后端获取
        new Chart(emotionTrendCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: '情绪出现次数'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '时间'
                        }
                    }
                }
            }
        });
    }

    // 情绪分布图表
    const emotionDistributionCtx = document.getElementById('emotionDistributionChart');
    if (emotionDistributionCtx) {
        // 这里只是初始化图表框架，实际数据应该从后端获取
        new Chart(emotionDistributionCtx, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                },
                cutout: '65%'
            }
        });
    }
}

// 初始化模态框
function initModals() {
    const modalTriggers = document.querySelectorAll('[data-modal-target]');
    const modalCloseButtons = document.querySelectorAll('[data-modal-close]');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal-target');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove('hidden');
                document.body.classList.add('overflow-hidden');
            }
        });
    });

    modalCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('[data-modal]');
            if (modal) {
                modal.classList.add('hidden');
                document.body.classList.remove('overflow-hidden');
            }
        });
    });

    // 点击模态框外部关闭
    document.addEventListener('click', function(e) {
        if (e.target.hasAttribute('data-modal')) {
            e.target.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }
    });
}

// 工具函数：获取URL参数
function getUrlParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// 工具函数：显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg transform transition-all duration-500 ease-in-out translate-x-full z-50
        ${type === 'success' ? 'bg-green-500 text-white'
        : type === 'error' ? 'bg-red-500 text-white'
        : type === 'warning' ? 'bg-yellow-500 text-white'
        : 'bg-blue-500 text-white'}`;

    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${type === 'success' ? 'fa-check-circle'
                : type === 'error' ? 'fa-exclamation-circle'
                : type === 'warning' ? 'fa-exclamation-triangle'
                : 'fa-info-circle'} mr-2"></i>
            <span>${message}</span>
        </div>
    `;

    // 添加到文档
    document.body.appendChild(notification);

    // 显示通知
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);

    // 自动关闭
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

// 工具函数：加载数据
async function loadData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error loading data:', error);
        showNotification('加载数据失败: ' + error.message, 'error');
        return null;
    }
}