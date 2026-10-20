/**
 * Jianpu Piano AI - Frontend Application & Audio Engine
 */

// State
const state = {
    currentSong: null,
    isPlaying: false,
    playbackTimer: null,
    currentStepIndex: 0,
    tempoMultiplier: 1.0,
    audioContext: null,
    geminiApiKey: localStorage.getItem('gemini_api_key') || '',
    rootKey: 'C',
    handMode: 'both', // 'both' or 'rh'
    abortController: null,
    trim: {
        url: '',
        videoId: '',
        title: '',
        duration: 180,
        startTime: 0,
        endTime: 120,
        isPlayingPreview: false,
        previewTimer: null,
        activeDrag: null
    }
};

// Acoustic Piano Sound Engine using Web Audio API
class PianoSynth {
    constructor() {
        this.ctx = null;
        this.activeVoices = new Map();
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playNote(midiPitch, duration = 1.0, velocity = 0.8) {
        this.init();
        if (midiPitch <= 0) return;

        const freq = 440 * Math.pow(2, (midiPitch - 69) / 12);
        const now = this.ctx.currentTime;

        // Master note gain
        const gainNode = this.ctx.createGain();
        gainNode.gain.setValueAtTime(0, now);
        // Fast piano hammer attack
        gainNode.gain.linearRampToValueAtTime(velocity * 0.45, now + 0.006);
        // Piano natural exponential decay & sustain
        gainNode.gain.exponentialRampToValueAtTime(velocity * 0.15, now + 0.25);
        gainNode.gain.exponentialRampToValueAtTime(0.0001, now + Math.max(0.3, duration * 0.95));

        // Low-pass filter simulating wooden piano body resonance
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(Math.min(8000, freq * 4.5), now);
        filter.frequency.exponentialRampToValueAtTime(Math.max(200, freq * 1.5), now + duration);

        // Fundamental oscillator (triangle for acoustic warmth)
        const osc1 = this.ctx.createOscillator();
        osc1.type = 'triangle';
        osc1.frequency.setValueAtTime(freq, now);

        // Harmonic overtone oscillator (sine)
        const osc2 = this.ctx.createOscillator();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(freq * 2, now);

        const osc2Gain = this.ctx.createGain();
        osc2Gain.gain.setValueAtTime(0.3, now);
        osc2.connect(osc2Gain);

        osc1.connect(filter);
        osc2Gain.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(this.ctx.destination);

        osc1.start(now);
        osc2.start(now);

        const stopTime = now + Math.max(0.35, duration);
        osc1.stop(stopTime);
        osc2.stop(stopTime);
    }
}

const synth = new PianoSynth();

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initApiKeyUI();
    initKeyboard();
    loadSampleSong('canon_in_d');

    // Listen to messages from YouTube iframe (detect embed errors like 101/150)
    window.addEventListener('message', (event) => {
        if (!event.data) return;
        try {
            const data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
            if (data.event === 'onError' || data.info === 101 || data.info === 150 || data.info === 100 || data.info === 2) {
                console.warn("YouTube iframe error detected (embedding restricted), switching to audio mode:", data);
                switchToAudioPlayerMode(true);
            }
        } catch (e) {}
    });

    // YouTube Search / Submit Form
    document.getElementById('transcribe-form').addEventListener('submit', (e) => {
        e.preventDefault();
        let url = document.getElementById('youtube-url-input').value.trim();
        if (url) {
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                url = 'https://' + url;
            }
            openTrimModalForUrl(url);
        } else {
            showToast("Vui lòng dán đường link bài hát YouTube vào ô tìm kiếm.", "warning");
        }
    });

    // File Upload listener
    document.getElementById('file-upload-input').addEventListener('change', handleFileUpload);
});

// API Key Modal & UI
async function initApiKeyUI() {
    const keyInput = document.getElementById('api-key-input');
    const keyStatus = document.getElementById('key-status-badge');
    
    // Check server key status
    try {
        const sRes = await fetch('/api/key-status');
        if (sRes.ok) {
            const sData = await sRes.json();
            if (sData.configured && !state.geminiApiKey) {
                state.geminiApiKey = 'SERVER_ENV';
            }
        }
    } catch (e) {}

    if (state.geminiApiKey) {
        if (state.geminiApiKey !== 'SERVER_ENV') {
            keyInput.value = state.geminiApiKey;
        }
        keyStatus.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span> Gemini AI: Đã kết nối ✓';
        keyStatus.className = 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-950 text-emerald-300 border border-emerald-700/50 cursor-pointer hover:bg-emerald-900/60 transition';
    }

    document.getElementById('save-api-key-btn').addEventListener('click', async () => {
        const key = keyInput.value.trim();
        state.geminiApiKey = key;
        localStorage.setItem('gemini_api_key', key);
        if (key) {
            keyStatus.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span> Gemini AI: Đã kết nối ✓';
            keyStatus.className = 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-950 text-emerald-300 border border-emerald-700/50 cursor-pointer hover:bg-emerald-900/60 transition';
            // Save to server .env
            try {
                await fetch('/api/save-key', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ apiKey: key })
                });
            } catch (err) {
                console.warn("Could not persist key to server .env:", err);
            }
        } else {
            keyStatus.innerHTML = '<span class="w-2 h-2 rounded-full bg-amber-400 mr-1.5"></span> Cấu hình Gemini AI (Chưa nhập)';
            keyStatus.className = 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-amber-950 text-amber-300 border border-amber-700/50 cursor-pointer hover:bg-amber-900/60 transition';
        }
        closeApiKeyModal();
    });
}

function openApiKeyModal() {
    document.getElementById('api-key-modal').classList.remove('hidden');
}

function closeApiKeyModal() {
    document.getElementById('api-key-modal').classList.add('hidden');
}

// Quick Try Button Handler
function trySample(songId) {
    loadSampleSong(songId);
}

// Progress Tracking Helpers
function setProgress(percent, message, step = 1, stageName = "Đang xử lý...") {
    const p = Math.min(100, Math.max(0, Math.round(percent)));
    
    // Percent numbers & fill
    const numEl = document.getElementById('progress-percent-number');
    const detailEl = document.getElementById('progress-detail');
    const barEl = document.getElementById('progress-bar-fill');
    if (numEl) numEl.textContent = `${p}%`;
    if (detailEl) detailEl.textContent = `${p}%`;
    if (barEl) barEl.style.width = `${p}%`;

    // Messages
    const msgEl = document.getElementById('loading-msg');
    const stageEl = document.getElementById('progress-stage-name');
    if (msgEl && message) msgEl.textContent = message;
    if (stageEl && stageName) stageEl.textContent = stageName;

    // Update 4 step indicators
    for (let i = 1; i <= 4; i++) {
        const stepCard = document.getElementById(`step-${i}`);
        if (!stepCard) continue;

        const iconEl = stepCard.querySelector('.step-icon i');
        const statusEl = stepCard.querySelector('.step-status');

        if (i < step) {
            // Completed step
            stepCard.className = 'step-card step-completed p-2.5 rounded-xl bg-slate-900/60 border border-white/5 transition-all flex flex-col items-center text-center';
            if (statusEl) statusEl.textContent = 'Hoàn tất';
            if (iconEl) iconEl.className = 'fa-solid fa-check text-emerald-300';
        } else if (i === step) {
            // Active current step
            stepCard.className = 'step-card step-active p-2.5 rounded-xl bg-slate-900/60 border border-white/5 transition-all flex flex-col items-center text-center';
            if (statusEl) statusEl.textContent = p >= 100 ? 'Hoàn tất' : 'Đang xử lý...';
            if (iconEl) iconEl.className = p >= 100 ? 'fa-solid fa-check text-emerald-300' : 'fa-solid fa-spinner fa-spin text-slate-900';
        } else {
            // Pending step
            stepCard.className = 'step-card p-2.5 rounded-xl bg-slate-900/60 border border-white/5 transition-all flex flex-col items-center text-center';
            if (statusEl) statusEl.textContent = 'Chờ xử lý';
            const defaultIcons = ['fa-link', 'fa-download', 'fa-brain', 'fa-music'];
            if (iconEl) iconEl.className = `fa-solid ${defaultIcons[i - 1]}`;
        }
    }
}

let progressStartTime = 0;
let progressTimerInterval = null;

function startProgressTimer() {
    stopProgressTimer();
    progressStartTime = Date.now();
    const timerText = document.getElementById('progress-timer-text');
    if (timerText) timerText.textContent = "00:00";
    progressTimerInterval = setInterval(() => {
        const elapsedSec = Math.floor((Date.now() - progressStartTime) / 1000);
        const mins = Math.floor(elapsedSec / 60);
        const secs = elapsedSec % 60;
        const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        const el = document.getElementById('progress-timer-text');
        if (el) el.textContent = formatted;
    }, 1000);
}

function stopProgressTimer() {
    if (progressTimerInterval) {
        clearInterval(progressTimerInterval);
        progressTimerInterval = null;
    }
}

function showProgressModal(stageName = "Bắt đầu quét...") {
    const el = document.getElementById('loading-overlay');
    if (el) el.classList.remove('hidden');
    const mini = document.getElementById('progress-video-mini');
    if (mini) mini.classList.add('hidden');
    startProgressTimer();
    setProgress(0, "Đang kết nối...", 1, stageName);
}

function hideProgressModal() {
    stopProgressTimer();
    const el = document.getElementById('loading-overlay');
    if (el) el.classList.add('hidden');
}

function cancelTranscription() {
    if (state.abortController) {
        state.abortController.abort();
        state.abortController = null;
    }
    hideProgressModal();
}

async function loadSampleSong(songId) {
    showProgressModal("Đang tải bản nhạc mẫu");
    setProgress(15, "Đang kết nối cơ sở dữ liệu bài hát...", 1, "Tải bản mẫu");
    
    try {
        await new Promise(r => setTimeout(r, 120));
        setProgress(45, "Đang tải cấu trúc cao độ và hợp âm...", 2, "Đọc nốt nhạc");

        const res = await fetch(`/api/samples/${songId}`);
        if (!res.ok) throw new Error("Lỗi khi tải bài hát mẫu");
        const songData = await res.json();

        setProgress(85, "Đang biên dịch bản nhạc Giản Phổ (1=Đô, 2=Rê)...", 3, "Biên soạn");
        await new Promise(r => setTimeout(r, 150));

        setProgress(100, "Sẵn sàng phát nhạc!", 4, "Hoàn tất");
        await new Promise(r => setTimeout(r, 200));

        renderSong(songData);
        showToast(`Đã mở bài hát: ${songData.title || songId}`, 'success');
    } catch (err) {
        showToast("Lỗi khi tải bài hát mẫu: " + err.message, 'error');
    } finally {
        hideProgressModal();
    }
}

// Time formatting utilities
function formatSecondsToMmSs(totalSec) {
    totalSec = Math.max(0, Math.round(totalSec));
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

function parseMmSsToSeconds(str) {
    if (!str) return 0;
    const parts = str.trim().split(':');
    if (parts.length === 2) {
        const m = parseInt(parts[0]) || 0;
        const s = parseInt(parts[1]) || 0;
        return m * 60 + s;
    } else if (parts.length === 1) {
        return parseInt(parts[0]) || 0;
    }
    return 0;
}

// Modern Toast Notification Utility
function showToast(message, type = 'info', duration = 4000) {
    let container = document.getElementById('app-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'app-toast-container';
        container.className = 'fixed bottom-5 right-5 z-[9999] flex flex-col space-y-2.5 max-w-sm w-full pointer-events-none px-4';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto transform transition-all duration-300 ease-out translate-y-3 opacity-0 flex items-start space-x-3 p-3.5 rounded-xl shadow-2xl backdrop-blur-md border text-xs';

    let iconClass = 'fa-info-circle text-teal-400';
    let borderClass = 'bg-[#0b1329]/95 border-teal-500/40 text-slate-200';

    if (type === 'success') {
        iconClass = 'fa-circle-check text-emerald-400';
        borderClass = 'bg-[#061814]/95 border-emerald-500/50 text-emerald-100';
    } else if (type === 'error') {
        iconClass = 'fa-circle-exclamation text-rose-400';
        borderClass = 'bg-[#1c0b12]/95 border-rose-500/50 text-rose-100';
    } else if (type === 'warning') {
        iconClass = 'fa-triangle-exclamation text-amber-400';
        borderClass = 'bg-[#1c1409]/95 border-amber-500/50 text-amber-100';
    }

    toast.className += ` ${borderClass}`;
    toast.innerHTML = `
        <i class="fa-solid ${iconClass} text-base shrink-0 mt-0.5"></i>
        <div class="flex-1 font-medium leading-relaxed">${message}</div>
        <button class="text-slate-400 hover:text-white shrink-0 ml-1 text-sm focus:outline-none" onclick="this.parentElement.remove()">
            <i class="fa-solid fa-xmark"></i>
        </button>
    `;

    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-3', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    });

    // Auto dismiss
    setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-3', 'opacity-0');
        setTimeout(() => toast.remove(), 320);
    }, duration);
}

// Open Trim Modal & fetch video duration
async function openTrimModalForUrl(url) {
    showLoading("Đang lấy thông tin video để chọn đoạn...", "Kết nối YouTube");
    try {
        const res = await fetch('/api/youtube-info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        if (!res.ok) throw new Error("Không thể kết nối video YouTube");
        const info = await res.json();

        state.trim.url = url;
        state.trim.videoId = info.videoId || '';
        state.trim.title = info.title || 'Bản Piano YouTube';
        state.trim.channel = info.channel || 'YouTube';
        state.trim.thumbnail = info.thumbnail || (info.videoId ? `https://img.youtube.com/vi/${info.videoId}/hqdefault.jpg` : '');
        state.trim.duration = info.duration || 180;
        state.trim.startTime = 0;
        // Default select first 2 minutes (120s) as in reference screenshot, or full if shorter
        state.trim.endTime = Math.min(state.trim.duration, 120);
        state.trim.playerMode = 'youtube';
        state.trim.audioStreamUrl = info.audioStreamUrl || (`/api/audio-stream?url=${encodeURIComponent(url)}`);

        // Setup Video Title overlay
        const titleEl = document.getElementById('trim-video-title');
        if (titleEl) titleEl.textContent = state.trim.title;

        // Setup Native Audio Player
        const nativeAudio = document.getElementById('trim-native-audio');
        if (nativeAudio) {
            nativeAudio.pause();
            nativeAudio.src = state.trim.audioStreamUrl;
            nativeAudio.load();
        }

        // Setup Audio View Metadata
        const audioTitle = document.getElementById('trim-audio-title');
        const audioArtist = document.getElementById('trim-audio-artist');
        const audioBg = document.getElementById('trim-audio-poster-bg');
        const audioThumb = document.getElementById('trim-audio-disc-thumb');
        if (audioTitle) audioTitle.textContent = state.trim.title;
        if (audioArtist) audioArtist.textContent = state.trim.channel;
        if (audioThumb && state.trim.thumbnail) audioThumb.src = state.trim.thumbnail;
        if (audioBg && state.trim.thumbnail) audioBg.style.backgroundImage = `url('${state.trim.thumbnail}')`;

        // Reset to YouTube View initially
        updateTrimPlayerViewUI('youtube');

        // Setup YouTube Iframe embed
        const iframe = document.getElementById('trim-video-iframe');
        if (iframe) {
            if (info.videoId) {
                const origin = window.location.origin || 'http://127.0.0.1:8000';
                iframe.src = `https://www.youtube.com/embed/${info.videoId}?enablejsapi=1&origin=${encodeURIComponent(origin)}&widget_referrer=${encodeURIComponent(window.location.href)}&playsinline=1&rel=0`;
            } else {
                iframe.src = '';
                updateTrimPlayerViewUI('audio');
            }
        }

        hideLoading();
        document.getElementById('trim-video-modal').classList.remove('hidden');

        initTrimWaveformBars();
        setupTrimDragHandlers();
        updateTrimUI();
    } catch (err) {
        hideLoading();
        console.warn("Could not load trim info, checking server connectivity:", err);
        if (err.message && (err.message.includes("Failed to fetch") || err.message.includes("NetworkError"))) {
            showToast("Không thể kết nối đến máy chủ 127.0.0.1:8000. Đang thử kết nối luồng trực tiếp...", "warning");
        }
        transcribeYouTube(url, 0, null);
    }
}

function toggleTrimPlayerMode() {
    const newMode = state.trim.playerMode === 'youtube' ? 'audio' : 'youtube';
    updateTrimPlayerViewUI(newMode);
}

function updateTrimPlayerViewUI(mode) {
    state.trim.playerMode = mode;
    const iframeView = document.getElementById('trim-iframe-view');
    const audioView = document.getElementById('trim-audio-view');
    const toggleBtnIcon = document.getElementById('trim-toggle-view-icon');
    const toggleBtnText = document.getElementById('trim-toggle-view-text');

    if (mode === 'audio') {
        if (iframeView) iframeView.classList.add('hidden');
        if (audioView) audioView.classList.remove('hidden');
        if (toggleBtnIcon) toggleBtnIcon.className = 'fa-brands fa-youtube text-red-400 text-xs';
        if (toggleBtnText) toggleBtnText.textContent = 'Chuyển sang Video';
    } else {
        if (iframeView) iframeView.classList.remove('hidden');
        if (audioView) audioView.classList.add('hidden');
        if (toggleBtnIcon) toggleBtnIcon.className = 'fa-solid fa-headphones text-teal-300 text-xs';
        if (toggleBtnText) toggleBtnText.textContent = 'Chuyển sang Audio';
    }
}

function switchToAudioPlayerMode(isAuto = false) {
    updateTrimPlayerViewUI('audio');
    if (isAuto) {
        showToast("YouTube hạn chế nhúng video này. Đã tự động kích hoạt Trình phát Audio Gốc để nghe thử mượt mà!", "info", 4500);
        const note = document.getElementById('trim-audio-source-note');
        if (note) {
            note.innerHTML = '<span class="text-amber-400 font-semibold"><i class="fa-solid fa-triangle-exclamation mr-1"></i>Đã kích hoạt chế độ Audio Gốc</span>';
        }
    }
}

function closeTrimModal() {
    stopTrimPreviewPlay();
    const iframe = document.getElementById('trim-video-iframe');
    if (iframe) iframe.src = '';
    const nativeAudio = document.getElementById('trim-native-audio');
    if (nativeAudio) {
        nativeAudio.pause();
        nativeAudio.src = '';
    }
    document.getElementById('trim-video-modal').classList.add('hidden');
}

// Generate organic waveform bars
function initTrimWaveformBars() {
    const barsContainer = document.getElementById('trim-waveform-bars');
    if (!barsContainer) return;
    barsContainer.innerHTML = '';
    
    const numBars = 65;
    for (let i = 0; i < numBars; i++) {
        const bar = document.createElement('div');
        bar.className = 'waveform-bar';
        const baseH = Math.sin((i / numBars) * Math.PI) * 42;
        const noise = (Math.sin(i * 1.8) * 0.5 + 0.5) * 32;
        const height = Math.max(8, Math.min(68, baseH + noise));
        bar.style.height = `${height}px`;
        barsContainer.appendChild(bar);
    }
}

// Setup dual-handle drag & drop
function setupTrimDragHandlers() {
    const wrap = document.getElementById('trim-waveform-wrap');
    const handleStart = document.getElementById('trim-handle-start');
    const handleEnd = document.getElementById('trim-handle-end');
    const zone = document.getElementById('trim-selection-zone');
    if (!wrap || !handleStart || !handleEnd || !zone) return;

    let dragStartX = 0;
    let initialStart = 0;
    let initialEnd = 0;

    function onPointerDown(type, clientX) {
        state.trim.activeDrag = type;
        dragStartX = clientX;
        initialStart = state.trim.startTime;
        initialEnd = state.trim.endTime;
    }

    handleStart.onmousedown = (e) => { e.stopPropagation(); onPointerDown('start', e.clientX); };
    handleStart.ontouchstart = (e) => { e.stopPropagation(); onPointerDown('start', e.touches[0].clientX); };

    handleEnd.onmousedown = (e) => { e.stopPropagation(); onPointerDown('end', e.clientX); };
    handleEnd.ontouchstart = (e) => { e.stopPropagation(); onPointerDown('end', e.touches[0].clientX); };

    zone.onmousedown = (e) => { e.stopPropagation(); onPointerDown('zone', e.clientX); };
    zone.ontouchstart = (e) => { e.stopPropagation(); onPointerDown('zone', e.touches[0].clientX); };

    wrap.onmousedown = (e) => {
        const rect = wrap.getBoundingClientRect();
        const clickRatio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        const clickSec = clickRatio * state.trim.duration;
        const distStart = Math.abs(clickSec - state.trim.startTime);
        const distEnd = Math.abs(clickSec - state.trim.endTime);

        if (distStart < distEnd) {
            state.trim.startTime = Math.min(clickSec, state.trim.endTime - 5);
        } else {
            state.trim.endTime = Math.max(clickSec, state.trim.startTime + 5);
        }
        updateTrimUI();
    };

    function onMove(clientX) {
        if (!state.trim.activeDrag) return;
        const rect = wrap.getBoundingClientRect();
        const deltaX = clientX - dragStartX;
        const deltaSec = (deltaX / rect.width) * state.trim.duration;

        if (state.trim.activeDrag === 'start') {
            let newStart = initialStart + deltaSec;
            newStart = Math.max(0, Math.min(newStart, state.trim.endTime - 5));
            state.trim.startTime = newStart;
        } else if (state.trim.activeDrag === 'end') {
            let newEnd = initialEnd + deltaSec;
            newEnd = Math.min(state.trim.duration, Math.max(newEnd, state.trim.startTime + 5));
            state.trim.endTime = newEnd;
        } else if (state.trim.activeDrag === 'zone') {
            const span = initialEnd - initialStart;
            let newStart = initialStart + deltaSec;
            if (newStart < 0) newStart = 0;
            if (newStart + span > state.trim.duration) newStart = state.trim.duration - span;
            state.trim.startTime = newStart;
            state.trim.endTime = newStart + span;
        }

        updateTrimUI();
    }

    window.onmousemove = (e) => onMove(e.clientX);
    window.ontouchmove = (e) => {
        if (state.trim.activeDrag) {
            onMove(e.touches[0].clientX);
        }
    };

    window.onmouseup = () => { state.trim.activeDrag = null; };
    window.ontouchend = () => { state.trim.activeDrag = null; };
}

function updateTrimUI() {
    const wrap = document.getElementById('trim-waveform-wrap');
    const handleStart = document.getElementById('trim-handle-start');
    const handleEnd = document.getElementById('trim-handle-end');
    const zone = document.getElementById('trim-selection-zone');
    if (!wrap || !handleStart || !handleEnd || !zone) return;

    const dur = Math.max(1, state.trim.duration);
    const startRatio = Math.max(0, Math.min(1, state.trim.startTime / dur));
    const endRatio = Math.max(0, Math.min(1, state.trim.endTime / dur));

    const startPct = (startRatio * 100).toFixed(2);
    const endPct = (endRatio * 100).toFixed(2);
    const widthPct = ((endRatio - startRatio) * 100).toFixed(2);

    handleStart.style.left = `${startPct}%`;
    handleEnd.style.left = `${endPct}%`;
    zone.style.left = `${startPct}%`;
    zone.style.width = `${widthPct}%`;

    const startStr = formatSecondsToMmSs(state.trim.startTime);
    const endStr = formatSecondsToMmSs(state.trim.endTime);
    const diffStr = formatSecondsToMmSs(state.trim.endTime - state.trim.startTime);

    document.getElementById('trim-start-input').value = startStr;
    document.getElementById('trim-end-input').value = endStr;
    document.getElementById('trim-handle-end-text').textContent = endStr;
    document.getElementById('trim-duration-badge').textContent = `${startStr} - ${endStr} (${diffStr})`;

    // Update time indicators in Audio View
    const curTimeEl = document.getElementById('trim-audio-current-time');
    const endTimeEl = document.getElementById('trim-audio-end-time');
    if (curTimeEl && !state.trim.isPlayingPreview) curTimeEl.textContent = startStr;
    if (endTimeEl) endTimeEl.textContent = endStr;

    // Reset Playhead position if not playing
    const playhead = document.getElementById('trim-playhead');
    if (playhead && !state.trim.isPlayingPreview) {
        playhead.style.left = `${startPct}%`;
    }
}

function onTrimInputChange() {
    const startVal = parseMmSsToSeconds(document.getElementById('trim-start-input').value);
    let endVal = parseMmSsToSeconds(document.getElementById('trim-end-input').value);

    if (endVal <= startVal) endVal = startVal + 10;
    if (endVal > state.trim.duration) endVal = state.trim.duration;

    state.trim.startTime = Math.max(0, startVal);
    state.trim.endTime = endVal;
    updateTrimUI();
}

function setTrimPreset(startSec, endSec) {
    state.trim.startTime = startSec || 0;
    if (endSec === null) {
        state.trim.endTime = state.trim.duration;
    } else {
        state.trim.endTime = Math.min(state.trim.duration, endSec);
    }
    updateTrimUI();
}

function toggleTrimPreviewPlay() {
    const playIcon = document.getElementById('trim-play-icon');
    const nativeAudio = document.getElementById('trim-native-audio');
    const iframe = document.getElementById('trim-video-iframe');

    if (state.trim.isPlayingPreview) {
        stopTrimPreviewPlay();
    } else {
        state.trim.isPlayingPreview = true;
        if (playIcon) playIcon.className = 'fa-solid fa-pause';

        const audioView = document.getElementById('trim-audio-view');
        if (audioView) audioView.classList.add('is-playing-audio');

        const liveStatus = document.getElementById('trim-audio-live-status');
        if (liveStatus) liveStatus.textContent = `Đang nghe thử: ${formatSecondsToMmSs(state.trim.startTime)} → ${formatSecondsToMmSs(state.trim.endTime)}`;

        const playhead = document.getElementById('trim-playhead');
        if (playhead) playhead.classList.remove('hidden');

        // 1. Play Native Audio Stream (100% reliable, immune to YouTube embed blocking)
        if (nativeAudio) {
            if (!nativeAudio.src || nativeAudio.src === '' || nativeAudio.src === window.location.href) {
                nativeAudio.src = state.trim.audioStreamUrl || (`/api/audio-stream?url=${encodeURIComponent(state.trim.url)}`);
            }
            try {
                nativeAudio.currentTime = Math.max(0, state.trim.startTime);
            } catch (seekErr) {
                console.warn("Audio seek error before play:", seekErr);
            }

            const playPromise = nativeAudio.play();
            if (playPromise !== undefined) {
                playPromise.catch((e) => {
                    console.warn("Native audio play deferred / buffering:", e);
                    if (liveStatus) liveStatus.textContent = "Đang kết nối luồng âm thanh...";
                });
            }

            nativeAudio.ontimeupdate = () => {
                if (!state.trim.isPlayingPreview) return;
                const cur = nativeAudio.currentTime;

                // Update live timer in Audio View
                const curTimeEl = document.getElementById('trim-audio-current-time');
                if (curTimeEl) curTimeEl.textContent = formatSecondsToMmSs(cur);

                // Update moving playhead along the waveform
                if (playhead && state.trim.duration > 0) {
                    const pct = Math.max(0, Math.min(100, (cur / state.trim.duration) * 100));
                    playhead.style.left = `${pct}%`;
                }

                // If end time reached, stop
                if (cur >= state.trim.endTime) {
                    stopTrimPreviewPlay();
                }
            };

            nativeAudio.onended = () => {
                stopTrimPreviewPlay();
            };

            nativeAudio.onerror = (e) => {
                console.warn("Native audio stream warning:", e);
            };
        }

        // 2. Also command YouTube iframe to seek & play if available
        if (iframe && iframe.contentWindow) {
            try {
                iframe.contentWindow.postMessage(JSON.stringify({
                    event: 'command',
                    func: 'seekTo',
                    args: [state.trim.startTime, true]
                }), '*');
                iframe.contentWindow.postMessage(JSON.stringify({
                    event: 'command',
                    func: 'playVideo',
                    args: ''
                }), '*');
            } catch (err) {}
        }

        // 3. Fallback safety timer
        const durationMs = Math.max(500, (state.trim.endTime - state.trim.startTime) * 1000);
        clearTimeout(state.trim.previewTimer);
        state.trim.previewTimer = setTimeout(() => {
            stopTrimPreviewPlay();
        }, durationMs + 800);
    }
}

function stopTrimPreviewPlay() {
    state.trim.isPlayingPreview = false;
    clearTimeout(state.trim.previewTimer);

    const playIcon = document.getElementById('trim-play-icon');
    if (playIcon) playIcon.className = 'fa-solid fa-play ml-0.5';

    const audioView = document.getElementById('trim-audio-view');
    if (audioView) audioView.classList.remove('is-playing-audio');

    const liveStatus = document.getElementById('trim-audio-live-status');
    if (liveStatus) liveStatus.textContent = 'Sẵn sàng nghe thử đoạn đã chọn';

    const playhead = document.getElementById('trim-playhead');
    if (playhead) {
        if (state.trim.duration > 0) {
            const startPct = Math.max(0, Math.min(100, (state.trim.startTime / state.trim.duration) * 100));
            playhead.style.left = `${startPct}%`;
        }
        playhead.classList.add('hidden');
    }

    const nativeAudio = document.getElementById('trim-native-audio');
    if (nativeAudio) {
        try {
            nativeAudio.pause();
        } catch (e) {}
    }

    const iframe = document.getElementById('trim-video-iframe');
    if (iframe && iframe.contentWindow) {
        try {
            iframe.contentWindow.postMessage(JSON.stringify({
                event: 'command',
                func: 'pauseVideo',
                args: ''
            }), '*');
        } catch (e) {}
    }
}

function confirmTrimAndTranscribe() {
    const url = state.trim.url;
    const start = state.trim.startTime;
    const end = state.trim.endTime;
    closeTrimModal();
    transcribeYouTube(url, start, end);
}

function skipTrimAndTranscribeAll() {
    const url = state.trim.url;
    closeTrimModal();
    transcribeYouTube(url, 0, null);
}

// Transcribe YouTube Video with Live Real-Time % Progress Streaming
async function transcribeYouTube(url, startTime = 0, endTime = null) {
    stopPlayback();
    showProgressModal("Quét link YouTube");
    state.abortController = new AbortController();

    const payload = {
        url: url,
        gemini_api_key: state.geminiApiKey === 'SERVER_ENV' ? '' : state.geminiApiKey,
        keySignature: `1=${state.rootKey}`,
        mode: state.handMode,
        startTime: startTime || 0,
        endTime: endTime || null
    };

    let finalSongData = null;

    try {
        let res;
        let useStream = true;

        try {
            res = await fetch('/api/transcribe-youtube-stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                signal: state.abortController.signal
            });
        } catch (streamConnErr) {
            console.warn("SSE stream failed to connect, attempting standard POST fallback...", streamConnErr);
            useStream = false;
            setProgress(35, "Đang chuyển sang cổng kết nối trực tiếp...", 2, "Kết nối lại");
            
            // Fallback to standard /api/transcribe-youtube endpoint
            res = await fetch('/api/transcribe-youtube', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                signal: state.abortController.signal
            });
            if (!res.ok) throw new Error(`Lỗi máy chủ (${res.status})`);
            finalSongData = await res.json();
        }

        if (useStream && !finalSongData && res && res.body) {
            if (!res.ok) {
                throw new Error(`Lỗi máy chủ (${res.status})`);
            }

            const reader = res.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n\n');
                buffer = lines.pop(); // keep last chunk if incomplete

                for (const line of lines) {
                    const trimmed = line.trim();
                    if (trimmed.startsWith('data:')) {
                        try {
                            const event = JSON.parse(trimmed.replace('data:', '').trim());
                            
                            // Update Progress with %
                            setProgress(
                                event.percent || 0,
                                event.message || '',
                                event.step || 1,
                                event.stageName || 'Đang xử lý...'
                            );

                            // Mini video info preview
                            if (event.title || event.thumbnail) {
                                const miniCard = document.getElementById('progress-video-mini');
                                if (miniCard) {
                                    miniCard.classList.remove('hidden');
                                    if (event.thumbnail) {
                                        document.getElementById('progress-video-mini-thumb').src = event.thumbnail;
                                    }
                                    if (event.title) {
                                        document.getElementById('progress-video-mini-title').textContent = event.title;
                                    }
                                    if (event.channel) {
                                        document.getElementById('progress-video-mini-channel').textContent = event.channel;
                                    }
                                }
                            }

                            if (event.result) {
                                finalSongData = event.result;
                            }

                            if (event.error) {
                                console.warn("Stream event warning:", event.message);
                            }
                        } catch (e) {
                            console.warn("Parse stream event error:", e);
                        }
                    }
                }
            }
        }

        if (finalSongData) {
            setProgress(100, "Hoàn tất! Đang mở sheet nhạc...", 4, "Hoàn tất!");
            await new Promise(r => setTimeout(r, 450));
            renderSong(finalSongData);
            showToast(`Biên dịch thành công: ${finalSongData.title || 'Bản Piano'}`, 'success');
        } else {
            throw new Error("Không nhận được dữ liệu sheet nhạc từ máy chủ.");
        }

    } catch (err) {
        if (err.name === 'AbortError') {
            console.log("Hủy quét bởi người dùng.");
            showToast("Đã hủy quá trình quét.", "info");
            return;
        }
        console.error("Transcribe error:", err);
        let errorMsg = err.message || 'Lỗi khi quét video.';
        if (errorMsg.includes('Failed to fetch') || errorMsg.includes('NetworkError')) {
            errorMsg = "Không thể kết nối đến máy chủ (127.0.0.1:8000). Vui lòng đảm bảo uvicorn đang chạy trên máy của bạn.";
        }
        showToast(errorMsg, "error", 6000);
    } finally {
        state.abortController = null;
        hideProgressModal();
    }
}

// Handle File Upload (MIDI, MP3, WAV) with Progress
async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    showProgressModal(`Xử lý tệp: ${file.name}`);
    setProgress(15, `Đang đọc dữ liệu tệp ${file.name}...`, 1, "Tải tệp");
    stopPlayback();

    const formData = new FormData();
    formData.append('file', file);
    formData.append('gemini_api_key', state.geminiApiKey);
    formData.append('keySignature', `1=${state.rootKey}`);

    try {
        await new Promise(r => setTimeout(r, 150));
        setProgress(45, "Đang gửi lên máy chủ và phân tích cấu trúc nốt...", 2, "Phân tích");

        const res = await fetch('/api/upload-file', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({ detail: "Lỗi khi xử lý file" }));
            throw new Error(errData.detail || "Không thể xử lý file này.");
        }

        setProgress(85, "Đang tạo sheet Giản Phổ & ánh xạ phím đàn...", 3, "Tạo Sheet");
        const songData = await res.json();
        
        setProgress(100, "Hoàn tất!", 4, "Sẵn sàng");
        await new Promise(r => setTimeout(r, 200));

        renderSong(songData);
        showToast(`Đã mở bài hát: ${songData.title || songId}`, 'success');
    } catch (err) {
        showToast("Lỗi khi tải bài hát mẫu: " + err.message, 'error');
    } finally {
        hideProgressModal();
        e.target.value = '';
    }
}

// Transpose / Change Key
async function transposeKey(targetKey) {
    if (!state.currentSong) return;
    showLoading(`Đang dịch giọng sang 1=${targetKey}...`);
    try {
        const res = await fetch('/api/transpose', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                songData: state.currentSong,
                targetKey: targetKey
            })
        });

        if (!res.ok) throw new Error("Lỗi khi dịch giọng");
        const newSong = await res.json();
        renderSong(newSong);
        showToast(`Đã chuyển giọng thành công: 1=${targetKey}`, 'success');
    } catch (err) {
        showToast("Lỗi khi dịch giọng: " + err.message, 'error');
    } finally {
        hideLoading();
    }
}

// Render Song & Sheet Music
function renderSong(songData) {
    state.currentSong = songData;
    state.rootKey = (songData.keySignature || '1=C').replace('1=', '').trim();
    
    // Update Song Header Info
    document.getElementById('song-title').textContent = songData.title || "Bản nhạc Piano";
    document.getElementById('song-artist').textContent = songData.artist || songData.channel || "Không rõ tác giả";
    document.getElementById('key-sig-badge').textContent = songData.keySignature || '1=C';
    document.getElementById('time-sig-badge').textContent = songData.timeSignature || '4/4';
    document.getElementById('tempo-badge').textContent = `${songData.tempo || 80} BPM`;

    const sheetTimeSig = document.getElementById('sheet-time-sig');
    const sheetTempo = document.getElementById('sheet-tempo');
    if (sheetTimeSig) sheetTimeSig.textContent = songData.timeSignature || '4/4';
    if (sheetTempo) sheetTempo.textContent = `${songData.tempo || 80} BPM`;

    // Update Trimmed Range Badge in Sheet Header
    const trimBadge = document.getElementById('sheet-trim-badge-wrap');
    const trimRangeEl = document.getElementById('sheet-trim-range');
    if (songData.trimmedInfo && trimBadge && trimRangeEl) {
        trimBadge.classList.remove('hidden');
        trimRangeEl.textContent = `${songData.trimmedInfo.startStr || '0:00'} - ${songData.trimmedInfo.endStr || ''}`;
    } else if (trimBadge) {
        trimBadge.classList.add('hidden');
    }

    // Video preview if YouTube
    const previewContainer = document.getElementById('video-preview-card');
    if (songData.thumbnail) {
        previewContainer.classList.remove('hidden');
        document.getElementById('video-thumb-img').src = songData.thumbnail;
        const vTitle = (songData.videoTitle && songData.videoTitle !== 'Bản Piano YouTube')
            ? songData.videoTitle
            : (songData.title || 'Bản Piano YouTube');
        document.getElementById('video-preview-title').textContent = vTitle;
        const vChannel = (songData.channel && songData.channel !== 'YouTube')
            ? songData.channel
            : (songData.artist || 'YouTube');
        document.getElementById('video-preview-channel').textContent = vChannel;
    } else {
        previewContainer.classList.add('hidden');
    }

    // Update Transpose select
    const transposeSelect = document.getElementById('key-select');
    if (transposeSelect) {
        transposeSelect.value = state.rootKey;
    }

    // Render Jianpu HTML Sheet
    renderJianpuSheet(songData);
    updateKeyboardKeyLabels();
    stopPlayback();
}

// Render Jianpu Measures
function renderJianpuSheet(songData) {
    const container = document.getElementById('jianpu-sheet-content');
    container.innerHTML = '';

    const measures = songData.measures || [];
    if (measures.length === 0) {
        container.innerHTML = '<div class="text-gray-400 p-8 text-center">Không có nốt nhạc nào được ghi nhận.</div>';
        return;
    }

    measures.forEach((m, mIdx) => {
        const measureEl = document.createElement('div');
        measureEl.className = 'measure-box';
        measureEl.id = `measure-${m.measureNumber || mIdx + 1}`;

        // Measure number badge
        const mNumBadge = document.createElement('div');
        mNumBadge.className = 'measure-number';
        mNumBadge.textContent = m.measureNumber || (mIdx + 1);
        measureEl.appendChild(mNumBadge);

        // Right Hand Section
        const rhContainer = document.createElement('div');
        rhContainer.className = 'flex flex-wrap items-center w-full mb-1';

        (m.rightHand || []).forEach((n, nIdx) => {
            const noteEl = createNoteElement(n, `rh-${mIdx}-${nIdx}`, 'text-emerald-800');
            rhContainer.appendChild(noteEl);
        });
        measureEl.appendChild(rhContainer);

        // Left Hand Section (if mode is both)
        if (state.handMode === 'both' && (m.leftHand || []).length > 0) {
            const lhDivider = document.createElement('div');
            lhDivider.className = 'w-full border-t border-slate-200 my-1';
            measureEl.appendChild(lhDivider);

            const lhContainer = document.createElement('div');
            lhContainer.className = 'flex flex-wrap items-center w-full';

            (m.leftHand || []).forEach((n, nIdx) => {
                const noteEl = createNoteElement(n, `lh-${mIdx}-${nIdx}`, 'text-indigo-800');
                lhContainer.appendChild(noteEl);
            });
            measureEl.appendChild(lhContainer);
        }

        container.appendChild(measureEl);
    });
}

function createNoteElement(note, elementId, colorClass) {
    const el = document.createElement('div');
    el.className = `jianpu-note-block ${colorClass}`;
    el.id = `note-${elementId}`;
    el.dataset.midi = note.midi || 0;

    const num = String(note.number || '0');
    const oct = parseInt(note.octave || 0);
    const acc = note.accidental || '';
    const dur = parseFloat(note.duration || 1.0);

    // Octave dots above
    const dotsAbove = document.createElement('div');
    dotsAbove.className = 'octave-dots-above';
    if (oct === 1) {
        dotsAbove.innerHTML = '<div class="octave-dot"></div>';
    } else if (oct >= 2) {
        dotsAbove.innerHTML = '<div class="octave-dot"></div><div class="octave-dot"></div>';
    }
    el.appendChild(dotsAbove);

    // Digit + Accidental
    const digitWrap = document.createElement('div');
    digitWrap.className = 'note-digit';
    if (acc) {
        const accSpan = document.createElement('span');
        accSpan.className = 'note-accidental';
        accSpan.textContent = acc === '#' ? '♯' : '♭';
        digitWrap.appendChild(accSpan);
    }
    digitWrap.appendChild(document.createTextNode(num));
    
    // Sustained hyphen or dot
    if (dur >= 4.0) {
        digitWrap.appendChild(document.createTextNode(' - - -'));
    } else if (dur >= 3.0) {
        digitWrap.appendChild(document.createTextNode(' - -'));
    } else if (dur >= 2.0) {
        digitWrap.appendChild(document.createTextNode(' -'));
    } else if (dur === 1.5) {
        digitWrap.appendChild(document.createTextNode('.'));
    }

    el.appendChild(digitWrap);

    // Octave dots below
    const dotsBelow = document.createElement('div');
    dotsBelow.className = 'octave-dots-below';
    if (oct === -1) {
        dotsBelow.innerHTML = '<div class="octave-dot"></div>';
    } else if (oct <= -2) {
        dotsBelow.innerHTML = '<div class="octave-dot"></div><div class="octave-dot"></div>';
    }
    el.appendChild(dotsBelow);

    // Rhythm underlines (eighth, sixteenth)
    if (dur <= 0.25) {
        const uLines = document.createElement('div');
        uLines.className = 'rhythm-underlines';
        uLines.innerHTML = '<div class="rhythm-line"></div><div class="rhythm-line"></div>';
        el.appendChild(uLines);
    } else if (dur <= 0.5) {
        const uLines = document.createElement('div');
        uLines.className = 'rhythm-underlines';
        uLines.innerHTML = '<div class="rhythm-line"></div>';
        el.appendChild(uLines);
    }

    // Note pitch letter for beginners
    if (note.midi > 0) {
        const badge = document.createElement('div');
        badge.className = 'pitch-badge';
        badge.textContent = midiToNoteName(note.midi);
        el.appendChild(badge);
    }

    // Click to play this note
    el.addEventListener('click', () => {
        if (note.midi > 0) {
            synth.playNote(note.midi, 0.8);
            const hand = elementId.startsWith('lh') ? 'lh' : 'rh';
            highlightPianoKey(note.midi, hand);
            setTimeout(() => unhighlightPianoKey(note.midi), 500);
        }
    });

    return el;
}

// Convert MIDI number to Note Name (e.g. 60 -> C4)
function midiToNoteName(midi) {
    const names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const octave = Math.floor(midi / 12) - 1;
    return `${names[midi % 12]}${octave}`;
}

// Build Full 88-Key Virtual Piano (from A0 (21) to C8 (108))
function initKeyboard() {
    const container = document.getElementById('piano-keyboard');
    if (!container) return;
    container.innerHTML = '';

    const startMidi = 21;  // A0 (Lowest key on 88-key piano)
    const endMidi = 108;  // C8 (Highest key on 88-key piano)

    const whiteKeyWidth = 23;
    const blackKeyWidth = 14.5;
    let whiteKeyIndex = 0;

    for (let midi = startMidi; midi <= endMidi; midi++) {
        const isBlack = [1, 3, 6, 8, 10].includes(midi % 12);
        const keyEl = document.createElement('div');
        keyEl.id = `key-${midi}`;
        keyEl.dataset.midi = midi;

        if (isBlack) {
            keyEl.className = 'black-key';
            // Black key is positioned at the boundary between current white keys
            const leftPos = (whiteKeyIndex * whiteKeyWidth) - (blackKeyWidth / 2);
            keyEl.style.left = `${leftPos}px`;
        } else {
            keyEl.className = 'white-key';
            if (midi === 60) {
                keyEl.classList.add('is-middle-c'); // C4 Middle C marker
                keyEl.title = 'Đô Trung Tâm (Middle C4)';
            }
            whiteKeyIndex++;
        }

        const noteName = midiToNoteName(midi);
        keyEl.innerHTML = `
            <span class="jianpu-key-num" id="key-jianpu-${midi}"></span>
            <span class="text-[9px] opacity-75 leading-tight">${noteName}</span>
        `;

        // Interactive mouse click
        keyEl.addEventListener('mousedown', (e) => {
            e.preventDefault();
            synth.playNote(midi, 0.8);
            keyEl.classList.add('active-key-rh');
        });
        keyEl.addEventListener('mouseup', () => {
            keyEl.classList.remove('active-key-rh');
        });
        keyEl.addEventListener('mouseleave', () => {
            keyEl.classList.remove('active-key-rh');
        });

        // Touch support
        keyEl.addEventListener('touchstart', (e) => {
            e.preventDefault();
            synth.playNote(midi, 0.8);
            keyEl.classList.add('active-key-rh');
        }, { passive: false });
        keyEl.addEventListener('touchend', () => {
            keyEl.classList.remove('active-key-rh');
        });

        container.appendChild(keyEl);
    }

    // Set total container width for horizontal scrolling (52 white keys * 23px = 1196px)
    container.style.width = `${whiteKeyIndex * whiteKeyWidth}px`;

    updateKeyboardKeyLabels();

    // Default scroll to Middle C4
    setTimeout(() => {
        scrollToPianoSection('mid');
    }, 150);
}

// Update Jianpu Numbers on all 88 Piano Keys based on 1=Key
function updateKeyboardKeyLabels() {
    const semitones = {
        "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4,
        "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
        "A#": 10, "Bb": 10, "B": 11
    };
    const degreeMap = {
        0: "1", 1: "♯1", 2: "2", 3: "♯2", 4: "3",
        5: "4", 6: "♯4", 7: "5", 8: "♯5", 9: "6", 10: "♯6", 11: "7"
    };

    const rootSemi = semitones[state.rootKey] || 0;
    const refRootMidi = 60 + rootSemi; // Middle C reference

    for (let midi = 21; midi <= 108; midi++) {
        const labelEl = document.getElementById(`key-jianpu-${midi}`);
        if (labelEl) {
            const pitchClass = (midi - rootSemi) % 12;
            const deg = degreeMap[(pitchClass + 12) % 12] || "";

            // Calculate octave offset relative to middle octave
            const octDiff = Math.floor((midi - refRootMidi) / 12);

            let displayDeg = deg;
            if (octDiff === 1) displayDeg += "\u0307";
            else if (octDiff === 2) displayDeg += "\u0308";
            else if (octDiff >= 3) displayDeg += "\u0308\u0307";
            else if (octDiff === -1) displayDeg += "\u0323";
            else if (octDiff === -2) displayDeg += "\u0324";
            else if (octDiff <= -3) displayDeg += "\u0324\u0323";

            labelEl.textContent = displayDeg;
        }
    }
}

// Quick jump to section across 88 keys: 'bass', 'mid', 'treble'
function scrollToPianoSection(section) {
    const scrollWrap = document.getElementById('piano-keyboard-scroll-wrap');
    if (!scrollWrap) return;

    if (section === 'bass') {
        scrollWrap.scrollTo({ left: 0, behavior: 'smooth' });
    } else if (section === 'mid') {
        const c4Key = document.getElementById('key-60');
        if (c4Key) {
            const targetLeft = c4Key.offsetLeft - (scrollWrap.clientWidth / 2) + (c4Key.offsetWidth / 2);
            scrollWrap.scrollTo({ left: Math.max(0, targetLeft), behavior: 'smooth' });
        }
    } else if (section === 'treble') {
        scrollWrap.scrollTo({ left: scrollWrap.scrollWidth, behavior: 'smooth' });
    }
}

// Toggle Fit 88 keys to container vs scroll
function togglePianoFitMode() {
    const scrollWrap = document.getElementById('piano-keyboard-scroll-wrap');
    const toggleText = document.getElementById('toggle-fit-text');
    if (!scrollWrap) return;

    const isFit = scrollWrap.classList.toggle('fit-mode');
    if (isFit) {
        if (toggleText) toggleText.textContent = "Cuộn Chuẩn";
    } else {
        if (toggleText) toggleText.textContent = "Thu Vừa Khung";
        scrollToPianoSection('mid');
    }
}

function highlightPianoKey(midi, hand = 'rh') {
    const key = document.getElementById(`key-${midi}`);
    if (key) {
        // Remove previous active classes
        key.classList.remove('active-key', 'active-key-rh', 'active-key-lh');

        // Apply distinct color: Green for Right Hand, Orange for Left Hand
        if (hand === 'lh') {
            key.classList.add('active-key-lh');
        } else {
            key.classList.add('active-key-rh');
        }

        // Smoothly bring active key into view if out of visible area
        const scrollWrap = document.getElementById('piano-keyboard-scroll-wrap');
        if (scrollWrap && !scrollWrap.classList.contains('fit-mode')) {
            const keyLeft = key.offsetLeft;
            const keyRight = keyLeft + key.offsetWidth;
            const scrollLeft = scrollWrap.scrollLeft;
            const scrollRight = scrollLeft + scrollWrap.clientWidth;

            if (keyLeft < scrollLeft + 40 || keyRight > scrollRight - 40) {
                scrollWrap.scrollTo({
                    left: keyLeft - (scrollWrap.clientWidth / 2) + (key.offsetWidth / 2),
                    behavior: 'smooth'
                });
            }
        }

        setTimeout(() => {
            key.classList.remove('active-key', 'active-key-rh', 'active-key-lh');
        }, 280);
    }
}

// Moves vertical scanner playhead line over active note
function moveScannerToEvent(noteEvent) {
    const scanner = document.getElementById('sheet-scanner-line');
    const container = document.getElementById('jianpu-sheet-content');
    if (!scanner || !container) return;

    // Find the note element by noteId or fallback
    let noteEl = noteEvent.noteId ? document.getElementById(`note-${noteEvent.noteId}`) : null;
    const measureEl = document.getElementById(`measure-${noteEvent.measure}`);

    if (!noteEl && measureEl) {
        const handSelector = noteEvent.hand === 'lh' ? '.text-indigo-800' : '.text-emerald-800';
        noteEl = measureEl.querySelector(handSelector) || measureEl.querySelector('.jianpu-note-block');
    }

    if (noteEl && measureEl) {
        // Pulse note element
        document.querySelectorAll('.jianpu-note-block.active-playing').forEach(el => el.classList.remove('active-playing'));
        noteEl.classList.add('active-playing');
        setTimeout(() => noteEl.classList.remove('active-playing'), 280);

        // Position vertical scanner line
        scanner.classList.remove('hidden');
        const cRect = container.getBoundingClientRect();
        const nRect = noteEl.getBoundingClientRect();
        const mRect = measureEl.getBoundingClientRect();

        const topPos = mRect.top - cRect.top;
        const leftPos = nRect.left - cRect.left + (nRect.width / 2) - 1.75;
        const heightVal = mRect.height;

        scanner.style.top = `${Math.round(topPos)}px`;
        scanner.style.left = `${Math.round(leftPos)}px`;
        scanner.style.height = `${Math.round(heightVal)}px`;
    }
}

// Playback Engine
function togglePlayback() {
    if (state.isPlaying) {
        pausePlayback();
    } else {
        startPlayback();
    }
}

function startPlayback() {
    if (!state.currentSong || !state.currentSong.playableTimeline) return;
    synth.init();

    state.isPlaying = true;
    document.getElementById('play-btn-icon').className = 'fa-solid fa-pause';
    document.getElementById('play-btn-text').textContent = 'Tạm Dừng';

    const timeline = state.currentSong.playableTimeline;
    if (state.currentStepIndex >= timeline.length) {
        state.currentStepIndex = 0;
    }

    const startTimestamp = performance.now() - (timeline[state.currentStepIndex].time * 1000 / state.tempoMultiplier);

    function step() {
        if (!state.isPlaying) return;

        const currentSec = (performance.now() - startTimestamp) / 1000 * state.tempoMultiplier;

        while (state.currentStepIndex < timeline.length && timeline[state.currentStepIndex].time <= currentSec) {
            const noteEvent = timeline[state.currentStepIndex];
            synth.playNote(noteEvent.midi, noteEvent.duration, noteEvent.hand === 'rh' ? 0.9 : 0.7);
            
            // Visual highlight: Tay Phải = XANH LÁ, Tay Trái = CAM
            highlightPianoKey(noteEvent.midi, noteEvent.hand || 'rh');
            highlightMeasure(noteEvent.measure);

            // Đường kẻ dọc quét qua các số
            moveScannerToEvent(noteEvent);

            state.currentStepIndex++;
        }

        if (state.currentStepIndex >= timeline.length) {
            stopPlayback();
            return;
        }

        state.playbackTimer = requestAnimationFrame(step);
    }

    state.playbackTimer = requestAnimationFrame(step);
}

function pausePlayback() {
    state.isPlaying = false;
    cancelAnimationFrame(state.playbackTimer);
    document.getElementById('play-btn-icon').className = 'fa-solid fa-play';
    document.getElementById('play-btn-text').textContent = 'Phát Nhạc';
    clearHighlights();
}

function stopPlayback() {
    state.isPlaying = false;
    state.currentStepIndex = 0;
    cancelAnimationFrame(state.playbackTimer);
    document.getElementById('play-btn-icon').className = 'fa-solid fa-play';
    document.getElementById('play-btn-text').textContent = 'Phát Nhạc';
    clearHighlights();
}

function replaySong() {
    stopPlayback();
    startPlayback();
}

function unhighlightPianoKey(midi) {
    const key = document.getElementById(`key-${midi}`);
    if (key) {
        key.classList.remove('active-key', 'active-key-rh', 'active-key-lh');
    }
}

function highlightMeasure(measureNum) {
    document.querySelectorAll('.measure-box').forEach(el => el.classList.remove('active-measure'));
    const mEl = document.getElementById(`measure-${measureNum}`);
    if (mEl) {
        mEl.classList.add('active-measure');
    }
}

function clearHighlights() {
    document.querySelectorAll('.active-key, .active-key-rh, .active-key-lh').forEach(el => {
        el.classList.remove('active-key', 'active-key-rh', 'active-key-lh');
    });
    document.querySelectorAll('.measure-box').forEach(el => el.classList.remove('active-measure'));
    document.querySelectorAll('.jianpu-note-block').forEach(el => el.classList.remove('active-playing'));
    const scanner = document.getElementById('sheet-scanner-line');
    if (scanner) scanner.classList.add('hidden');
}

// Hand Mode Switch
function setHandMode(mode) {
    state.handMode = mode;
    document.querySelectorAll('.hand-mode-btn').forEach(btn => {
        if (btn.dataset.mode === mode) {
            btn.className = 'hand-mode-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white shadow-sm';
        } else {
            btn.className = 'hand-mode-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-gray-300 hover:bg-slate-800';
        }
    });
    if (state.currentSong) {
        renderJianpuSheet(state.currentSong);
    }
}

// Export & Print Actions
function printSheet() {
    window.print();
}

function copyJianpuText() {
    if (!state.currentSong || !state.currentSong.formattedText) {
        showToast("Chưa có nội dung sheet để sao chép.", "warning");
        return;
    }
    navigator.clipboard.writeText(state.currentSong.formattedText).then(() => {
        showToast("Đã sao chép văn bản Giản Phổ (Jianpu) vào bộ nhớ tạm!", "success");
    }).catch(err => {
        showToast("Không thể sao chép: " + err, "error");
    });
}

async function downloadMidi() {
    if (!state.currentSong) {
        showToast("Chưa có bài hát để tải MIDI.", "warning");
        return;
    }
    showProgressModal("Đang chuẩn bị file MIDI...");
    setProgress(30, "Đang trích xuất cao độ...", 2, "Xuất MIDI");
    try {
        const res = await fetch('/api/export-midi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(state.currentSong)
        });
        if (!res.ok) throw new Error("Lỗi khi xuất file MIDI");

        setProgress(85, "Đang đóng gói file .mid...", 3, "Đóng gói");
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${state.currentSong.title || 'sheet_jianpu'}.mid`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        setProgress(100, "Đã tải xuống thành công!", 4, "Hoàn tất");
        await new Promise(r => setTimeout(r, 200));
        showToast("Đã tải xuống file MIDI thành công!", "success");
    } catch (err) {
        showToast("Lỗi khi xuất MIDI: " + err.message, "error");
    } finally {
        hideProgressModal();
    }
}

// Backward-compatible helpers
function showLoading(msg = "Đang xử lý...", stageName = "Đang xử lý...") {
    showProgressModal(stageName);
    setProgress(20, msg, 1, stageName);
}

function hideLoading() {
    hideProgressModal();
}
