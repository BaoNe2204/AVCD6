# -*- coding: utf-8 -*-
import json, re, os

with open('g:\\AVCD6\\enriched_questions_v2.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions:
    q['qNum'] = int(q.get('qNum', 1))
    q['exam'] = int(q.get('exam', 1))

questions.sort(key=lambda x: (x['exam'], x['qNum']))

json_data_str = json.dumps(questions, ensure_ascii=False)

html_template = '''<!DOCTYPE html>
<html lang="vi" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>AVCD6 PASS MÔN - Ôn Thi Tiếng Anh Trên Điện Thoại & Máy Tính</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#eef2ff',
              100: '#e0e7ff',
              200: '#c7d2fe',
              300: '#a5b4fc',
              400: '#818cf8',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
              800: '#3730a3',
              900: '#312e81',
            }
          }
        }
      }
    }
  </script>
  <style>
    /* Custom scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    .dark ::-webkit-scrollbar-thumb { background: #334155; }
    
    .scrollbar-none::-webkit-scrollbar { display: none; }
    .scrollbar-none { -ms-overflow-style: none; scrollbar-width: none; }

    .glass {
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    .dark .glass {
      background: rgba(15, 23, 42, 0.95);
    }
    .badge-pill {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.025em;
      text-transform: uppercase;
      padding: 0.2rem 0.55rem;
      border-radius: 9999px;
    }
    .active-tab {
      background: #4f46e5 !important;
      color: #ffffff !important;
      border-color: #4f46e5 !important;
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    /* Touch optimization */
    button, input, select, textarea {
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    .pb-safe {
      padding-bottom: env(safe-area-inset-bottom, 16px);
    }
  </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-screen flex flex-col transition-colors duration-200 pb-20 lg:pb-0">

  <!-- TOP HEADER (Mobile friendly) -->
  <header class="sticky top-0 z-40 glass border-b border-slate-200 dark:border-slate-800 shadow-sm">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-2.5">
      <div class="flex items-center justify-between gap-2.5">
        
        <!-- Logo & Title -->
        <div class="flex items-center gap-2 sm:gap-3">
          <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20 font-black text-lg sm:text-xl flex-shrink-0">
            A6
          </div>
          <div>
            <div class="flex items-center gap-1.5">
              <h1 class="text-base sm:text-lg font-black tracking-tight text-slate-900 dark:text-white leading-tight">AVCD6 PASS</h1>
              <span class="badge-pill bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300 text-[10px]">5 ĐỀ</span>
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 hidden sm:block">Ôn thi trên điện thoại • Tại sao sai • Mẹo 3s qua môn</p>
          </div>
        </div>

        <!-- Mode Selector on Header -->
        <div class="flex items-center bg-slate-100 dark:bg-slate-900 p-1 rounded-xl border border-slate-200 dark:border-slate-800 text-[11px] sm:text-xs font-bold overflow-x-auto scrollbar-none">
          <button id="modeStudyBtn" onclick="setMode('study')" class="px-2.5 sm:px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm whitespace-nowrap">
            <span>📖</span> <span class="hidden xs:inline">Ôn Tập</span>
          </button>
          <button id="modeExamBtn" onclick="setMode('exam')" class="px-2.5 sm:px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white whitespace-nowrap">
            <span>⏱️</span> <span class="hidden xs:inline">Thi Thử</span>
          </button>
          <button id="modeWrongBtn" onclick="setMode('wrong')" class="px-2.5 sm:px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white whitespace-nowrap">
            <span>❌</span> <span id="wrongCountBadge">0</span>
          </button>
        </div>

        <!-- Toggles & Tools -->
        <div class="flex items-center gap-1.5">
          <!-- Shuffle Choices Button -->
          <button id="shuffleChoicesBtn" onclick="toggleShuffleChoices()" class="p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold flex items-center gap-1 text-slate-700 dark:text-slate-300 shadow-sm" title="Đảo ngẫu nhiên vị trí các lựa chọn A, B, C, D">
            <span class="text-sm">🔀</span>
            <span id="shuffleChoicesStatus" class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
          </button>

          <!-- Admin Button -->
          <button onclick="toggleAdminModal()" class="p-2 rounded-xl border border-amber-300 dark:border-amber-700/50 bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 hover:bg-amber-100 text-xs font-bold shadow-sm" title="Chế độ Admin">
            <span>⚙️</span>
          </button>

          <!-- Dark/Light Mode -->
          <button onclick="toggleDarkMode()" class="p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-sm shadow-sm">
            <span id="themeIcon">🌙</span>
          </button>
        </div>

      </div>

      <!-- TIMER STRIP (Exam Mode) -->
      <div id="examBar" class="hidden mt-2 pt-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1.5 text-rose-600 dark:text-rose-400 font-mono font-bold text-base bg-rose-50 dark:bg-rose-950/40 px-2.5 py-1 rounded-lg border border-rose-200 dark:border-rose-900/50">
            <span>⏳</span> <span id="timerText">60:00</span>
          </div>
          <div class="text-[11px] text-slate-500 dark:text-slate-400">
            Đã làm: <span id="examAnsweredCount" class="font-bold text-slate-800 dark:text-white">0</span>/<span id="examTotalCount">50</span>
          </div>
        </div>
        <button onclick="submitExam()" class="px-3.5 py-1.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold text-xs rounded-lg shadow hover:from-emerald-700 hover:to-teal-700 transition-all flex items-center gap-1">
          <span>🚀</span> Nộp Bài
        </button>
      </div>

    </div>
  </header>

  <!-- NAVIGATION TABS: SWIPEABLE ON PHONE -->
  <div class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shadow-sm sticky top-[57px] sm:top-[61px] z-30">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-2.5 flex flex-col gap-2">
      
      <!-- ROW 1: LUYỆN THEO ĐỀ (Exam 1 -> 5) -->
      <div class="flex items-center gap-1.5 overflow-x-auto scrollbar-none py-0.5 flex-nowrap -mx-3 px-3 sm:mx-0 sm:px-0">
        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex-shrink-0 mr-1 flex items-center gap-1">
          <span>📝</span> ĐỀ:
        </span>
        <button onclick="selectCategory('exam', 1)" id="tab_exam_1" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex-shrink-0 active-tab">
          Đề 1 (50 câu)
        </button>
        <button onclick="selectCategory('exam', 2)" id="tab_exam_2" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex-shrink-0">
          Đề 2 (50 câu)
        </button>
        <button onclick="selectCategory('exam', 3)" id="tab_exam_3" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex-shrink-0">
          Đề 3 (50 câu)
        </button>
        <button onclick="selectCategory('exam', 4)" id="tab_exam_4" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex-shrink-0">
          Đề 4 (50 câu)
        </button>
        <button onclick="selectCategory('exam', 5)" id="tab_exam_5" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex-shrink-0">
          Đề 5 (50 câu)
        </button>
        <button onclick="selectCategory('all', 'all')" id="tab_all_all" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all flex-shrink-0">
          Tất cả 5 Đề (250 câu)
        </button>
      </div>

      <!-- ROW 2: CHUYÊN ĐỀ TỔNG HỢP CẢ 5 BÀI -->
      <div class="flex items-center gap-1.5 overflow-x-auto scrollbar-none py-0.5 flex-nowrap -mx-3 px-3 sm:mx-0 sm:px-0 pt-1.5 border-t border-slate-100 dark:border-slate-800/80">
        <span class="text-[11px] font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider flex-shrink-0 mr-1 flex items-center gap-1">
          <span>🎯</span> TỔNG HỢP:
        </span>
        <button onclick="selectCategory('part', 'GRAMMAR')" id="tab_part_GRAMMAR" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex-shrink-0 flex items-center gap-1">
          <span>📘</span> Tổng Ngữ Pháp (50 câu)
        </button>
        <button onclick="selectCategory('part', 'VOCABULARY')" id="tab_part_VOCABULARY" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex-shrink-0 flex items-center gap-1">
          <span>📗</span> Tổng Từ Vựng (50 câu)
        </button>
        <button onclick="selectCategory('part', 'TRANSFORMATION')" id="tab_part_TRANSFORMATION" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex-shrink-0 flex items-center gap-1">
          <span>📙</span> Tổng Viết Lại Câu (50 câu)
        </button>
        <button onclick="selectCategory('part', 'CLOZE')" id="tab_part_CLOZE" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex-shrink-0 flex items-center gap-1">
          <span>📕</span> Tổng Điền Từ (50 câu)
        </button>
        <button onclick="selectCategory('part', 'READING')" id="tab_part_READING" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex-shrink-0 flex items-center gap-1">
          <span>📖</span> Tổng Đọc Hiểu (50 câu)
        </button>
      </div>

    </div>
  </div>

  <!-- MAIN CONTENT CONTAINER -->
  <main class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6 flex-1 w-full flex flex-col lg:flex-row gap-5">

    <!-- LEFT: QUESTION LIST -->
    <div class="flex-1 min-w-0 flex flex-col gap-4 sm:gap-5">
      
      <!-- CURRENT VIEW BANNER -->
      <div id="viewBanner" class="bg-gradient-to-r from-brand-600 to-indigo-600 rounded-2xl p-3.5 sm:p-4 text-white shadow-sm flex items-center justify-between flex-wrap gap-2.5">
        <div>
          <div class="text-[10px] sm:text-[11px] font-bold uppercase tracking-wider text-indigo-200" id="viewSubTitle">CHẾ ĐỘ LUYỆN THEO ĐỀ</div>
          <h2 class="text-base sm:text-lg font-black leading-snug" id="viewMainTitle">ĐỀ ÔN TẬP 1 (50 CÂU CHUẨN ĐỀ THI)</h2>
        </div>
        <div class="flex items-center gap-2.5 text-xs bg-white/10 px-3 py-1 rounded-xl border border-white/20">
          <div><strong id="statAnswered">0</strong>/<strong id="statTotal">50</strong></div>
          <div>•</div>
          <div class="text-emerald-300 font-bold">✔ <span id="statCorrect">0</span></div>
          <div>•</div>
          <div class="text-rose-300 font-bold">✖ <span id="statWrong">0</span></div>
        </div>
      </div>

      <!-- EXAM RESULT BANNER -->
      <div id="examResultBanner" class="hidden bg-gradient-to-r from-brand-700 to-indigo-800 rounded-2xl p-5 text-white shadow-xl flex items-center justify-between flex-wrap gap-4">
        <div>
          <span class="badge-pill bg-white/20 text-white mb-2 inline-block">KẾT QUẢ THI THỬ</span>
          <h2 class="text-xl sm:text-2xl font-black" id="examResultTitle">Bạn đạt 8.5 / 10 điểm!</h2>
          <p class="text-xs sm:text-sm text-indigo-100 mt-1" id="examResultDesc">Số câu đúng: 42/50 • Tỷ lệ chính xác: 84% • KẾT QUẢ: ĐỖ QUA MÔN XUẤT SẮC!</p>
        </div>
        <div class="flex items-center gap-2.5">
          <button onclick="reviewMistakesAfterExam()" class="px-3.5 py-2 bg-white text-brand-700 font-bold text-xs rounded-xl shadow hover:bg-indigo-50 transition-all">
            Xem Câu Sai
          </button>
          <button onclick="setMode('study')" class="px-3.5 py-2 bg-indigo-900/60 text-white font-bold text-xs rounded-xl hover:bg-indigo-900 transition-all">
            Về Ôn Tập
          </button>
        </div>
      </div>

      <!-- QUESTIONS CONTAINER -->
      <div id="questionsContainer" class="flex flex-col gap-4 sm:gap-5">
        <!-- Rendered dynamically by JavaScript -->
      </div>

      <!-- PAGINATION -->
      <div id="paginationControls" class="flex items-center justify-between bg-white dark:bg-slate-900 p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800 text-xs font-semibold">
        <button id="prevPageBtn" onclick="changePage(-1)" class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 active:bg-slate-200">← Trang trước</button>
        <span id="pageInfo" class="text-slate-500 text-[11px] sm:text-xs">Trang 1 / 4</span>
        <button id="nextPageBtn" onclick="changePage(1)" class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 active:bg-slate-200">Trang sau →</button>
      </div>

    </div>

    <!-- RIGHT: QUESTION PALETTE GRID (Visible on Desktop) -->
    <div class="hidden lg:block w-80 flex-shrink-0">
      <div class="sticky top-[135px] bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col gap-3.5 max-h-[calc(100vh-160px)] overflow-hidden">
        
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
          <h3 class="font-black text-xs uppercase tracking-wider text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
            <span>📑</span> BẢNG CÂU HỎI (<span id="paletteFilteredCount">0</span>)
          </h3>
          <span class="text-[10px] text-slate-400">1 - 50</span>
        </div>

        <!-- Legend -->
        <div class="flex items-center gap-3 text-[11px] text-slate-500 flex-wrap">
          <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-slate-200 dark:bg-slate-700 inline-block"></span> Chưa làm</div>
          <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Đúng</div>
          <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Sai</div>
        </div>

        <!-- Palette Grid with Section Groups -->
        <div id="paletteGridDesktop" class="flex flex-col gap-3 overflow-y-auto pr-1 flex-1">
          <!-- Rendered dynamically -->
        </div>

        <div class="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40 rounded-xl p-3 text-[11px] text-amber-900 dark:text-amber-200">
          <div class="font-bold flex items-center gap-1 mb-1">
            <span>💡</span> BÍ QUYẾT QUA MÔN:
          </div>
          <p class="leading-relaxed">
            Chọn <strong>"Tổng Ngữ Pháp"</strong> hoặc <strong>"Tổng Từ Vựng"</strong> ở hàng trên để luyện liền mạch 50 câu của cả 5 đề!
          </p>
        </div>

      </div>
    </div>

  </main>

  <!-- MOBILE STICKY BOTTOM BAR (Always easy to tap on phone) -->
  <div class="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-t border-slate-200 dark:border-slate-800 p-2.5 px-4 flex items-center justify-between shadow-xl pb-safe">
    <!-- Quick Stat -->
    <div class="flex items-center gap-2 text-xs font-bold text-slate-600 dark:text-slate-400">
      <span class="text-emerald-600 dark:text-emerald-400">✔ <span id="mobileStatCorrect">0</span></span>
      <span>•</span>
      <span class="text-rose-600 dark:text-rose-400">✖ <span id="mobileStatWrong">0</span></span>
    </div>

    <!-- Center Button: Open Question Palette Drawer -->
    <button onclick="toggleMobilePalette(true)" class="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-md shadow-brand-500/25 active:scale-95 transition-transform">
      <span>📑</span> Bảng Câu Hỏi (<span id="mobilePaletteBtnCount">50</span>)
    </button>

    <!-- Next Question Button -->
    <button onclick="jumpToNextUnanswered()" class="px-3 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold active:bg-slate-200 dark:active:bg-slate-700">
      Tiếp ➔
    </button>
  </div>

  <!-- MOBILE BOTTOM SHEET DRAWER FOR QUESTION PALETTE -->
  <div id="mobilePaletteDrawer" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm hidden flex flex-col justify-end transition-opacity">
    <div onclick="toggleMobilePalette(false)" class="flex-1"></div>
    <div class="bg-white dark:bg-slate-900 rounded-t-3xl max-h-[80vh] flex flex-col shadow-2xl border-t border-slate-200 dark:border-slate-800 overflow-hidden pb-safe">
      
      <!-- Drawer Handle & Header -->
      <div class="p-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-1 h-4 bg-brand-600 rounded-full"></div>
          <h3 class="font-black text-sm text-slate-900 dark:text-white uppercase tracking-wide">
            BẢNG CÂU HỎI (<span id="mobileDrawerCount">50</span> CÂU)
          </h3>
        </div>
        <button onclick="toggleMobilePalette(false)" class="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 flex items-center justify-center text-sm font-bold">
          ✕
        </button>
      </div>

      <!-- Drawer Content (Scrollable Grid) -->
      <div id="paletteGridMobile" class="p-4 overflow-y-auto flex flex-col gap-3">
        <!-- Rendered dynamically -->
      </div>

    </div>
  </div>

  <!-- ADMIN MANAGEMENT MODAL -->
  <div id="adminModal" class="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-sm hidden flex items-center justify-center p-3 sm:p-4">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden">
      
      <div class="px-5 py-3.5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950">
        <div class="flex items-center gap-2">
          <span class="text-xl">⚙️</span>
          <div>
            <h3 class="font-black text-sm sm:text-base text-slate-900 dark:text-white">BẢNG QUẢN TRỊ ADMIN</h3>
            <p class="text-[11px] text-slate-500">Chỉnh sửa câu hỏi, đáp án, dịch nghĩa, mẹo nhận biết</p>
          </div>
        </div>
        <button onclick="toggleAdminModal()" class="text-slate-400 hover:text-slate-600 dark:hover:text-white text-xl p-1">✕</button>
      </div>

      <div class="p-4 sm:p-6 overflow-y-auto flex-1 flex flex-col gap-5 text-xs">
        <div class="flex items-center justify-between gap-2.5 flex-wrap bg-slate-100 dark:bg-slate-800 p-3 rounded-2xl font-semibold">
          <div class="flex items-center gap-2">
            <button onclick="openAddQuestionForm()" class="px-3 py-1.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 font-bold flex items-center gap-1">
              <span>➕</span> Thêm câu
            </button>
            <button onclick="exportDataJSON()" class="px-3 py-1.5 bg-brand-600 text-white rounded-lg hover:bg-brand-700 flex items-center gap-1">
              <span>💾</span> Xuất JSON
            </button>
            <label class="px-3 py-1.5 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-lg cursor-pointer flex items-center gap-1">
              <span>📂</span> Nhập JSON
              <input type="file" id="importJsonInput" accept=".json" onchange="importDataJSON(event)" class="hidden">
            </label>
          </div>
          <button onclick="resetDefaultData()" class="px-2.5 py-1 text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 rounded-lg">
            Khôi phục gốc
          </button>
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="font-bold text-slate-700 dark:text-slate-300">Chọn câu hỏi cần chỉnh sửa:</label>
          <div class="flex items-center gap-2">
            <select id="adminQuestionSelect" onchange="loadQuestionToEdit(this.value)" class="flex-1 p-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 font-mono text-xs">
            </select>
            <button onclick="deleteSelectedQuestion()" class="px-3 py-2 bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 rounded-xl font-bold hover:bg-rose-200">
              Xóa
            </button>
          </div>
        </div>

        <div id="adminEditForm" class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          <div class="flex flex-col gap-1 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Nội dung câu hỏi (Question Text):</label>
            <textarea id="editQuestionText" rows="2" class="p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white font-medium"></textarea>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn A:</label>
            <input type="text" id="editOptA" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn B:</label>
            <input type="text" id="editOptB" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn C:</label>
            <input type="text" id="editOptC" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn D:</label>
            <input type="text" id="editOptD" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-bold text-emerald-600 dark:text-emerald-400">Đáp án ĐÚNG (A, B, C, hoặc D):</label>
            <select id="editCorrectAnswer" class="p-2 rounded-lg border border-emerald-300 dark:border-emerald-700 bg-emerald-50 dark:bg-emerald-950/40 font-bold text-sm">
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Chủ điểm ngữ pháp / Từ vựng:</label>
            <input type="text" id="editTopic" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Dịch nghĩa tiếng Việt nguyên câu:</label>
            <textarea id="editTrans" rows="2" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"></textarea>
          </div>
          <div class="flex flex-col gap-1 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Giải thích chi tiết TẠI SAO CHỌN:</label>
            <textarea id="editWhy" rows="2" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"></textarea>
          </div>
          <div class="flex flex-col gap-1 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Tại sao các đáp án khác SAI:</label>
            <textarea id="editWrong" rows="2" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"></textarea>
          </div>
          <div class="flex flex-col gap-1 md:col-span-2">
            <label class="font-bold text-amber-600 dark:text-amber-400">MẸO QUA MÔN 3s:</label>
            <textarea id="editTip" rows="2" class="p-2 rounded-lg border border-amber-300 dark:border-amber-700 bg-amber-50 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200 font-semibold"></textarea>
          </div>
        </div>
      </div>

      <div class="px-5 py-3.5 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end gap-2.5 bg-slate-50 dark:bg-slate-950">
        <button onclick="toggleAdminModal()" class="px-3.5 py-2 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-semibold text-slate-700 dark:text-slate-300">
          Đóng
        </button>
        <button onclick="saveAdminChanges()" class="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold shadow">
          Lưu Thay Đổi
        </button>
      </div>

    </div>
  </div>

  <!-- EMBEDDED JAVASCRIPT APP -->
  <script>
    const DEFAULT_DATA = ''' + json_data_str + ''';

    // Application State
    let questionsData = [];
    let userAnswers = {};
    let mistakes = new Set();
    let currentMode = 'study';
    let currentCatType = 'exam'; 
    let currentCatValue = 1;
    let searchQuery = '';
    let shuffleChoicesEnabled = true;
    let shuffledChoicesMap = {}; 
    let currentPage = 1;
    const PAGE_SIZE = 15;
    let examTimerInterval = null;
    let examSecondsRemaining = 60 * 60;
    let examSubmitted = false;

    function initApp() {
      const stored = localStorage.getItem('avcd6_custom_data');
      if (stored) {
        try {
          questionsData = JSON.parse(stored);
        } catch(e) {
          questionsData = JSON.parse(JSON.stringify(DEFAULT_DATA));
        }
      } else {
        questionsData = JSON.parse(JSON.stringify(DEFAULT_DATA));
      }

      questionsData.forEach(q => {
        q.qNum = parseInt(q.qNum, 10);
        q.exam = parseInt(q.exam, 10);
      });

      questionsData.sort((a, b) => (a.exam - b.exam) || (a.qNum - b.qNum));

      const storedMistakes = localStorage.getItem('avcd6_mistakes');
      if (storedMistakes) {
        try {
          mistakes = new Set(JSON.parse(storedMistakes));
        } catch(e) {}
      }

      if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        document.getElementById('themeIcon').textContent = '☀️';
      } else {
        document.documentElement.classList.remove('dark');
        document.getElementById('themeIcon').textContent = '🌙';
      }

      updateMistakesBadge();
      buildShuffledChoices();
      updateCategoryUI();
      renderApp();
      populateAdminSelect();
    }

    function toggleDarkMode() {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      document.getElementById('themeIcon').textContent = isDark ? '☀️' : '🌙';
    }

    function toggleMobilePalette(show) {
      const drawer = document.getElementById('mobilePaletteDrawer');
      if (show) {
        drawer.classList.remove('hidden');
      } else {
        drawer.classList.add('hidden');
      }
    }

    function setMode(mode) {
      currentMode = mode;
      
      const studyBtn = document.getElementById('modeStudyBtn');
      const examBtn = document.getElementById('modeExamBtn');
      const wrongBtn = document.getElementById('modeWrongBtn');
      const examBar = document.getElementById('examBar');
      const examResultBanner = document.getElementById('examResultBanner');

      [studyBtn, examBtn, wrongBtn].forEach(b => {
        b.className = 'px-2.5 sm:px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white whitespace-nowrap';
      });

      if (mode === 'study') {
        studyBtn.className = 'px-2.5 sm:px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm font-bold whitespace-nowrap';
        examBar.classList.add('hidden');
        examResultBanner.classList.add('hidden');
        clearInterval(examTimerInterval);
      } else if (mode === 'exam') {
        examBtn.className = 'px-2.5 sm:px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm font-bold whitespace-nowrap';
        examBar.classList.remove('hidden');
        startExam();
      } else if (mode === 'wrong') {
        wrongBtn.className = 'px-2.5 sm:px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm font-bold whitespace-nowrap';
        examBar.classList.add('hidden');
        examResultBanner.classList.add('hidden');
        clearInterval(examTimerInterval);
      }

      currentPage = 1;
      renderApp();
    }

    function startExam() {
      examSubmitted = false;
      userAnswers = {};
      examSecondsRemaining = 60 * 60;
      document.getElementById('examResultBanner').classList.add('hidden');
      clearInterval(examTimerInterval);
      
      examTimerInterval = setInterval(() => {
        examSecondsRemaining--;
        if (examSecondsRemaining <= 0) {
          clearInterval(examTimerInterval);
          submitExam();
        } else {
          const mins = Math.floor(examSecondsRemaining / 60);
          const secs = examSecondsRemaining % 60;
          document.getElementById('timerText').textContent = 
            `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        }
      }, 1000);
    }

    function submitExam() {
      if (examSubmitted) return;
      examSubmitted = true;
      clearInterval(examTimerInterval);

      const filtered = getFilteredQuestions();
      let correctCount = 0;
      filtered.forEach(q => {
        if (userAnswers[q.id] === q.correctAnswer) {
          correctCount++;
        } else {
          mistakes.add(q.id);
        }
      });

      saveMistakes();
      updateMistakesBadge();

      const total = filtered.length;
      const score10 = total > 0 ? ((correctCount / total) * 10).toFixed(1) : 0;
      const pct = total > 0 ? Math.round((correctCount / total) * 100) : 0;
      const isPass = score10 >= 5.0;

      const banner = document.getElementById('examResultBanner');
      const title = document.getElementById('examResultTitle');
      const desc = document.getElementById('examResultDesc');

      banner.classList.remove('hidden');
      title.textContent = `Bạn đạt ${score10} / 10 Điểm! (${isPass ? 'ĐẠT QUA MÔN 🎉' : 'CHƯA ĐẠT - CẦN ÔN LẠI ⚠️'})`;
      desc.textContent = `Số câu đúng: ${correctCount} / ${total} câu • Tỷ lệ chính xác: ${pct}% • ${isPass ? 'Xin chúc mừng! Nắm chắc các câu này là bạn tự tin qua môn 100%!' : 'Hãy xem lại các câu sai và ôn tập kỹ các mẹo 3s bên dưới!'}`;

      renderApp();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function reviewMistakesAfterExam() {
      setMode('wrong');
    }

    function toggleShuffleChoices() {
      shuffleChoicesEnabled = !shuffleChoicesEnabled;
      const dot = document.getElementById('shuffleChoicesStatus');
      dot.className = shuffleChoicesEnabled ? 'w-2 h-2 rounded-full bg-emerald-500 inline-block' : 'w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-700 inline-block';
      buildShuffledChoices();
      renderApp();
    }

    function buildShuffledChoices() {
      shuffledChoicesMap = {};
      questionsData.forEach(q => {
        const keys = ['A', 'B', 'C', 'D'];
        let list = keys.map(k => ({
          originalKey: k,
          text: q.options[k] || '',
          meaning: q.choice_breakdown ? q.choice_breakdown[k] : ''
        }));

        if (shuffleChoicesEnabled) {
          for (let i = list.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [list[i], list[j]] = [list[j], list[i]];
          }
        }

        shuffledChoicesMap[q.id] = list.map((item, idx) => ({
          displayKey: ['A', 'B', 'C', 'D'][idx],
          originalKey: item.originalKey,
          text: item.text,
          meaning: item.meaning
        }));
      });
    }

    function selectCategory(type, val) {
      currentCatType = type;
      currentCatValue = val;
      currentPage = 1;

      updateCategoryUI();
      renderApp();
    }

    function updateCategoryUI() {
      document.querySelectorAll('.cat-tab').forEach(el => {
        el.classList.remove('active-tab');
      });

      const activeId = `tab_${currentCatType}_${currentCatValue}`;
      const activeBtn = document.getElementById(activeId);
      if (activeBtn) activeBtn.classList.add('active-tab');

      const subTitle = document.getElementById('viewSubTitle');
      const mainTitle = document.getElementById('viewMainTitle');

      if (currentCatType === 'exam') {
        subTitle.textContent = 'CHẾ ĐỘ LUYỆN THEO ĐỀ';
        mainTitle.textContent = `ĐỀ ÔN TẬP ${currentCatValue} (50 CÂU CHUẨN ĐỀ THI)`;
      } else if (currentCatType === 'part') {
        subTitle.textContent = 'CHUYÊN ĐỀ TỔNG HỢP CẢ 5 BÀI';
        const partNames = {
          'GRAMMAR': 'TỔNG HỢP TOÀN BỘ NGỮ PHÁP (50 CÂU)',
          'VOCABULARY': 'TỔNG HỢP TOÀN BỘ TỪ VỰNG (50 CÂU)',
          'TRANSFORMATION': 'TỔNG HỢP TOÀN BỘ VIẾT LẠI CÂU (50 CÂU)',
          'CLOZE': 'TỔNG HỢP TOÀN BỘ ĐIỀN TỪ (50 CÂU)',
          'READING': 'TỔNG HỢP TOÀN BỘ ĐỌC HIỂU (50 CÂU)'
        };
        mainTitle.textContent = partNames[currentCatValue] || 'CHUYÊN ĐỀ TỔNG HỢP';
      } else {
        subTitle.textContent = 'TỔNG ÔN TOÀN DIỆN';
        mainTitle.textContent = 'TẤT CẢ 5 ĐỀ ÔN TẬP (250 CÂU)';
      }
    }

    function handleSearch(val) {
      searchQuery = val.trim().toLowerCase();
      currentPage = 1;
      renderApp();
    }

    function getFilteredQuestions() {
      let list = questionsData.filter(q => {
        if (currentMode === 'wrong' && !mistakes.has(q.id)) {
          return false;
        }

        if (currentCatType === 'exam') {
          if (q.exam !== currentCatValue) return false;
        } else if (currentCatType === 'part') {
          if (q.part !== currentCatValue) return false;
        }

        if (searchQuery) {
          const matchQ = q.question.toLowerCase().includes(searchQuery);
          const matchTip = (q.explanation?.tip || '').toLowerCase().includes(searchQuery);
          const matchTrans = (q.explanation?.translation || '').toLowerCase().includes(searchQuery);
          const matchOpts = Object.values(q.options || {}).some(v => v.toLowerCase().includes(searchQuery));
          if (!matchQ && !matchTip && !matchTrans && !matchOpts) return false;
        }

        return true;
      });

      list.sort((a, b) => (a.exam - b.exam) || (a.qNum - b.qNum));
      return list;
    }

    function getSpecificWrongReason(q, chosenKey) {
      if (!chosenKey || chosenKey === q.correctAnswer) return "";
      
      const chosenMeaning = (q.choice_breakdown && q.choice_breakdown[chosenKey]) ? q.choice_breakdown[chosenKey] : '';
      if (chosenMeaning && !chosenMeaning.includes('phương án:')) {
        return `Bạn chọn [${chosenKey}] "${q.options[chosenKey]}" mang nghĩa là: "${chosenMeaning}". Nghĩa này HOÀN TOÀN KHÔNG PHÙ HỢP với ngữ cảnh câu!`;
      }

      if (q.explanation?.wrong) {
        return q.explanation.wrong;
      }
      return `Lựa chọn '${chosenKey}' (${q.options[chosenKey]}) không đúng ngữ cảnh câu, sai thì động từ hoặc sai cấu trúc so với đáp án chính xác [${q.correctAnswer}].`;
    }

    function selectAnswer(qId, chosenOriginalKey) {
      if (currentMode === 'exam' && examSubmitted) return;

      userAnswers[qId] = chosenOriginalKey;
      const q = questionsData.find(item => item.id === qId);

      if (q) {
        if (chosenOriginalKey !== q.correctAnswer) {
          mistakes.add(qId);
        }
        saveMistakes();
        updateMistakesBadge();
      }

      renderApp();

      if (currentMode === 'study') {
        setTimeout(() => {
          const banner = document.getElementById(`feedback_${qId}`);
          if (banner) {
            banner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        }, 50);
      }
    }

    function saveMistakes() {
      localStorage.setItem('avcd6_mistakes', JSON.stringify(Array.from(mistakes)));
    }

    function updateMistakesBadge() {
      document.getElementById('wrongCountBadge').textContent = mistakes.size;
    }

    function scrollToQuestion(qId) {
      toggleMobilePalette(false); // Close mobile drawer if open

      const filtered = getFilteredQuestions();
      const idx = filtered.findIndex(q => q.id === qId);
      if (idx !== -1) {
        const targetPage = Math.floor(idx / PAGE_SIZE) + 1;
        if (targetPage !== currentPage) {
          currentPage = targetPage;
          renderApp();
        }
        setTimeout(() => {
          const el = document.getElementById(`card_${qId}`);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            el.classList.add('ring-2', 'ring-brand-500');
            setTimeout(() => el.classList.remove('ring-2', 'ring-brand-500'), 1500);
          }
        }, 100);
      }
    }

    function jumpToNextUnanswered() {
      const filtered = getFilteredQuestions();
      const nextQ = filtered.find(q => !userAnswers[q.id]);
      if (nextQ) {
        scrollToQuestion(nextQ.id);
      } else {
        alert('Chúc mừng! Bạn đã hoàn thành tất cả câu hỏi trong mục này!');
      }
    }

    function changePage(delta) {
      const filtered = getFilteredQuestions();
      const totalPages = Math.ceil(filtered.length / PAGE_SIZE) || 1;
      currentPage = Math.max(1, Math.min(totalPages, currentPage + delta));
      renderApp();
      window.scrollTo({ top: 100, behavior: 'smooth' });
    }

    // ==========================================
    // RENDER QUESTIONS & PALETTES
    // ==========================================
    function renderApp() {
      const filtered = getFilteredQuestions();
      const totalQuestions = filtered.length;
      const totalPages = Math.ceil(totalQuestions / PAGE_SIZE) || 1;
      if (currentPage > totalPages) currentPage = totalPages;

      const startIndex = (currentPage - 1) * PAGE_SIZE;
      const endIndex = Math.min(startIndex + PAGE_SIZE, totalQuestions);
      const pageQuestions = filtered.slice(startIndex, endIndex);

      let answeredCount = 0;
      let correctCount = 0;
      let wrongCount = 0;
      filtered.forEach(q => {
        if (userAnswers[q.id]) {
          answeredCount++;
          if (userAnswers[q.id] === q.correctAnswer) correctCount++;
          else wrongCount++;
        }
      });

      document.getElementById('statAnswered').textContent = answeredCount;
      document.getElementById('statTotal').textContent = totalQuestions;
      document.getElementById('statCorrect').textContent = correctCount;
      document.getElementById('statWrong').textContent = wrongCount;

      document.getElementById('mobileStatCorrect').textContent = correctCount;
      document.getElementById('mobileStatWrong').textContent = wrongCount;

      document.getElementById('examAnsweredCount').textContent = answeredCount;
      document.getElementById('examTotalCount').textContent = totalQuestions;
      document.getElementById('mobilePaletteBtnCount').textContent = `${answeredCount}/${totalQuestions}`;

      document.getElementById('pageInfo').textContent = `Trang ${currentPage} / ${totalPages} (Câu ${totalQuestions > 0 ? startIndex + 1 : 0} - ${endIndex} / ${totalQuestions})`;
      document.getElementById('prevPageBtn').disabled = currentPage <= 1;
      document.getElementById('nextPageBtn').disabled = currentPage >= totalPages;

      const container = document.getElementById('questionsContainer');
      if (pageQuestions.length === 0) {
        container.innerHTML = `
          <div class="bg-white dark:bg-slate-900 rounded-3xl p-10 text-center border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-4xl mb-3">🎉</div>
            <h3 class="text-base sm:text-lg font-bold text-slate-800 dark:text-white">Không có câu hỏi nào!</h3>
            <p class="text-xs text-slate-500 mt-1">Bạn đã hoàn thành hết các câu trong mục này.</p>
          </div>
        `;
      } else {
        container.innerHTML = pageQuestions.map((q, idx) => {
          const userChoice = userAnswers[q.id];
          const hasAnswered = !!userChoice;
          const isCorrect = userChoice === q.correctAnswer;
          const showAnswerDetail = (currentMode === 'study' && hasAnswered) || (currentMode === 'exam' && examSubmitted);

          const choices = shuffledChoicesMap[q.id] || [
            { displayKey: 'A', originalKey: 'A', text: q.options.A },
            { displayKey: 'B', originalKey: 'B', text: q.options.B },
            { displayKey: 'C', originalKey: 'C', text: q.options.C },
            { displayKey: 'D', originalKey: 'D', text: q.options.D }
          ];

          const userChoiceText = userChoice ? (q.options[userChoice] || '') : '';
          const correctText = q.options[q.correctAnswer] || '';
          const specificWrongReason = (!isCorrect && userChoice) ? getSpecificWrongReason(q, userChoice) : '';

          return `
            <div id="card_${q.id}" class="bg-white dark:bg-slate-900 rounded-2xl p-4 sm:p-5 border ${hasAnswered && !isCorrect && showAnswerDetail ? 'border-rose-300 dark:border-rose-900 shadow-rose-100 dark:shadow-none' : 'border-slate-200 dark:border-slate-800'} shadow-sm transition-all duration-200 hover:shadow-md">
              
              <!-- Card Header -->
              <div class="flex items-center justify-between gap-2.5 mb-3 flex-wrap">
                <div class="flex items-center gap-1.5 sm:gap-2">
                  <span class="w-7 h-7 sm:w-8 sm:h-8 rounded-xl bg-brand-100 dark:bg-brand-950/80 text-brand-700 dark:text-brand-300 font-mono font-bold text-xs flex items-center justify-center shadow-sm">
                    #${q.qNum}
                  </span>
                  <span class="badge-pill bg-indigo-50 text-indigo-700 dark:bg-indigo-950/50 dark:text-indigo-300">
                    Đề ${q.exam}
                  </span>
                  <span class="badge-pill bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                    ${q.partName || q.part}
                  </span>
                </div>

                ${showAnswerDetail ? `
                  <div class="flex items-center gap-1 text-xs font-bold ${isCorrect ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}">
                    <span>${isCorrect ? '✔ ĐÚNG' : '✖ SAI'}</span>
                  </div>
                ` : ''}
              </div>

              <!-- Passage (if Cloze / Reading) -->
              ${q.passage ? `
                <div class="mb-3.5 bg-slate-50 dark:bg-slate-950/60 p-3 rounded-xl border border-slate-200/80 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-sans max-h-44 overflow-y-auto">
                  <div class="font-bold text-[10px] uppercase text-slate-400 tracking-wider mb-1 flex items-center gap-1">
                    <span>📄</span> Đoạn văn bài đọc:
                  </div>
                  <div class="whitespace-pre-line">${q.passage}</div>
                </div>
              ` : ''}

              <!-- Question text -->
              <h4 class="text-sm font-semibold text-slate-900 dark:text-white leading-relaxed mb-3.5">
                ${q.question}
              </h4>

              <!-- Options Grid (Clean, Touch-Friendly, No inline meaning) -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-2.5">
                ${choices.map(c => {
                  let btnStyle = "border-slate-200 dark:border-slate-800 hover:border-brand-400 dark:hover:border-brand-600 bg-slate-50/70 dark:bg-slate-950/50 text-slate-700 dark:text-slate-200 active:bg-slate-100 dark:active:bg-slate-800";
                  let badgeStyle = "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300";
                  let statusTag = "";

                  if (hasAnswered) {
                    if (currentMode === 'study' || (currentMode === 'exam' && examSubmitted)) {
                      if (c.originalKey === q.correctAnswer) {
                        btnStyle = "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 font-bold ring-2 ring-emerald-500 shadow-sm";
                        badgeStyle = "bg-emerald-600 text-white border-emerald-600";
                        statusTag = `<span class="badge-pill bg-emerald-200 text-emerald-900 dark:bg-emerald-800 dark:text-emerald-100 text-[10px] ml-auto">✔ ĐÚNG</span>`;
                      } else if (userChoice === c.originalKey && !isCorrect) {
                        btnStyle = "border-rose-500 bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 ring-2 ring-rose-500 shadow-sm";
                        badgeStyle = "bg-rose-600 text-white border-rose-600";
                        statusTag = `<span class="badge-pill bg-rose-200 text-rose-900 dark:bg-rose-800 dark:text-rose-100 text-[10px] ml-auto">❌ ĐÃ CHỌN</span>`;
                      }
                    } else if (currentMode === 'exam' && !examSubmitted) {
                      if (userChoice === c.originalKey) {
                        btnStyle = "border-brand-500 bg-brand-50 dark:bg-brand-950/40 text-brand-900 dark:text-brand-200 font-bold ring-2 ring-brand-500";
                        badgeStyle = "bg-brand-600 text-white border-brand-600";
                      }
                    }
                  }

                  return `
                    <button onclick="selectAnswer('${q.id}', '${c.originalKey}')" class="w-full text-left p-3 rounded-xl border text-xs transition-all flex items-start gap-2.5 min-h-[46px] ${btnStyle}">
                      <span class="w-5 h-5 rounded-md border flex items-center justify-center font-bold font-mono text-[11px] flex-shrink-0 ${badgeStyle}">
                        ${c.displayKey}
                      </span>
                      <span class="flex-1 leading-snug pt-0.5 font-medium">${c.text}</span>
                      ${statusTag}
                    </button>
                  `;
                }).join('')}
              </div>

              <!-- INSTANT FEEDBACK BANNER (WHY WRONG / WHY RIGHT) -->
              ${showAnswerDetail ? `
                <div id="feedback_${q.id}" class="mt-3.5">
                  ${!isCorrect ? `
                    <div class="p-3.5 bg-rose-50/95 dark:bg-rose-950/50 border-2 border-rose-400 dark:border-rose-800 rounded-2xl shadow-sm flex flex-col gap-2">
                      <div class="flex items-center gap-1.5 text-rose-700 dark:text-rose-300 font-black text-xs uppercase tracking-wide">
                        <span class="text-sm">❌</span> BẠN VỪA CHỌN: [${userChoice}] "${userChoiceText}" — TẠI SAO SAI?
                      </div>
                      <p class="text-xs text-rose-900 dark:text-rose-200 font-semibold leading-relaxed pl-5 border-l-2 border-rose-300 dark:border-rose-700 ml-1">
                        ${specificWrongReason}
                      </p>
                      <div class="mt-0.5 pt-2 border-t border-rose-200/80 dark:border-rose-900/60 flex items-start gap-1.5 text-xs font-bold text-emerald-800 dark:text-emerald-300 pl-1">
                        <span class="text-sm">👉</span>
                        <div>
                          <span>ĐÁP ÁN ĐÚNG PHẢI LÀ: </span>
                          <span class="underline decoration-2">[${q.correctAnswer}] "${correctText}"</span>
                          <span class="font-normal text-slate-600 dark:text-slate-300"> — ${q.explanation?.why || ''}</span>
                        </div>
                      </div>
                    </div>
                  ` : `
                    <div class="p-3.5 bg-emerald-50/95 dark:bg-emerald-950/50 border-2 border-emerald-400 dark:border-emerald-800 rounded-2xl shadow-sm flex flex-col gap-1.5">
                      <div class="flex items-center gap-1.5 text-emerald-700 dark:text-emerald-300 font-black text-xs uppercase tracking-wide">
                        <span class="text-sm">🎉</span> CHÍNH XÁC! BẠN ĐÃ CHỌN ĐÚNG: [${q.correctAnswer}] "${correctText}"
                      </div>
                      <p class="text-xs text-emerald-900 dark:text-emerald-200 font-medium leading-relaxed pl-5">
                        ${q.explanation?.why || 'Lựa chọn hoàn toàn chính xác.'}
                      </p>
                    </div>
                  `}
                </div>

                <!-- COMPREHENSIVE STUDY BOX (Sentence Translation + Choice Breakdown + 3s Pass Tip) -->
                <div class="mt-3.5 pt-3.5 border-t border-slate-100 dark:border-slate-800 flex flex-col gap-3">
                  
                  <!-- 1. DỊCH NGUYÊN VĂN CẢ CÂU HOÀN CHỈNH -->
                  <div class="bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-900/60 rounded-xl p-3 text-xs shadow-sm">
                    <div class="font-bold text-indigo-950 dark:text-indigo-200 flex items-center gap-1 mb-1 text-[12px]">
                      <span>🇻🇳</span> DỊCH NGUYÊN VĂN TOÀN BỘ CÂU:
                    </div>
                    <p class="text-indigo-900 dark:text-indigo-100 leading-relaxed font-semibold text-xs">
                      "${q.explanation?.translation || 'Bản dịch đang được cập nhật.'}"
                    </p>
                  </div>

                  <!-- 2. NGHĨA CỦA CẢ 4 PHƯƠNG ÁN A, B, C, D -->
                  <div class="bg-slate-50 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-800 rounded-xl p-3 text-xs">
                    <div class="font-bold text-slate-800 dark:text-slate-200 flex items-center gap-1 mb-2">
                      <span>📚</span> NGHĨA CHI TIẾT CỦA CẢ 4 ĐÁP ÁN:
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs">
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <strong class="font-mono text-brand-600 dark:text-brand-400">A. ${q.options.A}:</strong>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.A || ''}</span>
                      </div>
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <strong class="font-mono text-brand-600 dark:text-brand-400">B. ${q.options.B}:</strong>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.B || ''}</span>
                      </div>
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <strong class="font-mono text-brand-600 dark:text-brand-400">C. ${q.options.C}:</strong>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.C || ''}</span>
                      </div>
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <strong class="font-mono text-brand-600 dark:text-brand-400">D. ${q.options.D}:</strong>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.D || ''}</span>
                      </div>
                    </div>
                  </div>

                  <!-- 3. MẸO QUA MÔN 3s -->
                  <div class="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-950/40 dark:to-orange-950/30 border border-amber-200 dark:border-amber-900/50 rounded-xl p-3 text-xs">
                    <div class="font-black text-amber-900 dark:text-amber-200 flex items-center gap-1.5 mb-1 tracking-wide">
                      <span class="text-sm">⚡</span> ${q.explanation?.tip ? q.explanation.tip.split(':')[0] : 'MẸO QUA MÔN 3s'}
                    </div>
                    <p class="text-amber-800 dark:text-amber-200 font-bold leading-relaxed">
                      ${q.explanation?.tip ? (q.explanation.tip.includes(':') ? q.explanation.tip.split(':')[1] : q.explanation.tip) : 'Xác định từ khóa trước và sau chỗ trống để chọn nhanh!'}
                    </p>
                  </div>

                </div>
              ` : ''}

            </div>
          `;
        }).join('');
      }

      renderGroupedPalette(filtered);
    }

    function renderGroupedPalette(filtered) {
      document.getElementById('paletteFilteredCount').textContent = filtered.length;
      document.getElementById('mobileDrawerCount').textContent = filtered.length;

      let groups = {};

      if (currentCatType === 'exam') {
        groups = {
          'I. Từ vựng (Câu 1 - 10)': filtered.filter(q => q.qNum >= 1 && q.qNum <= 10),
          'II. Ngữ pháp (Câu 11 - 20)': filtered.filter(q => q.qNum >= 11 && q.qNum <= 20),
          'III. Viết lại câu (Câu 21 - 30)': filtered.filter(q => q.qNum >= 21 && q.qNum <= 30),
          'IV. Điền từ (Câu 31 - 40)': filtered.filter(q => q.qNum >= 31 && q.qNum <= 40),
          'V. Đọc hiểu (Câu 41 - 50)': filtered.filter(q => q.qNum >= 41 && q.qNum <= 50)
        };
      } else if (currentCatType === 'part') {
        groups = {
          'Đề 1': filtered.filter(q => q.exam === 1),
          'Đề 2': filtered.filter(q => q.exam === 2),
          'Đề 3': filtered.filter(q => q.exam === 3),
          'Đề 4': filtered.filter(q => q.exam === 4),
          'Đề 5': filtered.filter(q => q.exam === 5)
        };
      } else {
        groups = {
          'Đề 1 (50 câu)': filtered.filter(q => q.exam === 1),
          'Đề 2 (50 câu)': filtered.filter(q => q.exam === 2),
          'Đề 3 (50 câu)': filtered.filter(q => q.exam === 3),
          'Đề 4 (50 câu)': filtered.filter(q => q.exam === 4),
          'Đề 5 (50 câu)': filtered.filter(q => q.exam === 5)
        };
      }

      const html = Object.entries(groups).map(([groupTitle, groupQuestions]) => {
        if (groupQuestions.length === 0) return '';
        groupQuestions.sort((a, b) => a.qNum - b.qNum);

        return `
          <div class="bg-slate-50/80 dark:bg-slate-950/50 p-2.5 rounded-xl border border-slate-200/80 dark:border-slate-800">
            <div class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2 flex items-center justify-between">
              <span>${groupTitle}</span>
              <span class="font-normal text-[9px] text-slate-400">${groupQuestions.length} câu</span>
            </div>
            <div class="grid grid-cols-5 gap-1.5">
              ${groupQuestions.map(q => {
                const userChoice = userAnswers[q.id];
                let colorClass = "bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-brand-500";
                
                if (userChoice) {
                  if (currentMode === 'study' || (currentMode === 'exam' && examSubmitted)) {
                    if (userChoice === q.correctAnswer) {
                      colorClass = "bg-emerald-500 text-white border-emerald-600 font-bold shadow-sm";
                    } else {
                      colorClass = "bg-rose-500 text-white border-rose-600 font-bold shadow-sm";
                    }
                  } else if (currentMode === 'exam' && !examSubmitted) {
                    colorClass = "bg-brand-600 text-white border-brand-700 font-bold shadow-sm";
                  }
                }

                return `
                  <button onclick="scrollToQuestion('${q.id}')" class="h-8 rounded-lg border text-xs font-mono font-bold flex items-center justify-center transition-all ${colorClass}">
                    ${q.qNum}
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).join('');

      const desktopEl = document.getElementById('paletteGridDesktop');
      if (desktopEl) desktopEl.innerHTML = html;

      const mobileEl = document.getElementById('paletteGridMobile');
      if (mobileEl) mobileEl.innerHTML = html;
    }

    // ==================== ADMIN FUNCTIONS ====================
    function toggleAdminModal() {
      const modal = document.getElementById('adminModal');
      const isHidden = modal.classList.toggle('hidden');
      if (!isHidden) {
        populateAdminSelect();
        const firstId = questionsData[0]?.id;
        if (firstId) loadQuestionToEdit(firstId);
      }
    }

    function populateAdminSelect() {
      const select = document.getElementById('adminQuestionSelect');
      select.innerHTML = questionsData.map(q => `
        <option value="${q.id}">[Đề ${q.exam} - Câu ${q.qNum}] (${q.part}) ${q.question.substring(0, 65)}...</option>
      `).join('');
    }

    function loadQuestionToEdit(qId) {
      const q = questionsData.find(item => item.id === qId);
      if (!q) return;

      document.getElementById('editQuestionText').value = q.question || '';
      document.getElementById('editOptA').value = q.options?.A || '';
      document.getElementById('editOptB').value = q.options?.B || '';
      document.getElementById('editOptC').value = q.options?.C || '';
      document.getElementById('editOptD').value = q.options?.D || '';
      document.getElementById('editCorrectAnswer').value = q.correctAnswer || 'A';
      document.getElementById('editTopic').value = q.explanation?.topic || q.partName || '';
      document.getElementById('editTrans').value = q.explanation?.translation || '';
      document.getElementById('editWhy').value = q.explanation?.why || '';
      document.getElementById('editWrong').value = q.explanation?.wrong || '';
      document.getElementById('editTip').value = q.explanation?.tip || '';
    }

    function saveAdminChanges() {
      const qId = document.getElementById('adminQuestionSelect').value;
      const q = questionsData.find(item => item.id === qId);
      if (!q) return;

      q.question = document.getElementById('editQuestionText').value.trim();
      q.options.A = document.getElementById('editOptA').value.trim();
      q.options.B = document.getElementById('editOptB').value.trim();
      q.options.C = document.getElementById('editOptC').value.trim();
      q.options.D = document.getElementById('editOptD').value.trim();
      q.correctAnswer = document.getElementById('editCorrectAnswer').value;
      
      if (!q.explanation) q.explanation = {};
      q.explanation.topic = document.getElementById('editTopic').value.trim();
      q.explanation.translation = document.getElementById('editTrans').value.trim();
      q.explanation.why = document.getElementById('editWhy').value.trim();
      q.explanation.wrong = document.getElementById('editWrong').value.trim();
      q.explanation.tip = document.getElementById('editTip').value.trim();

      localStorage.setItem('avcd6_custom_data', JSON.stringify(questionsData));
      buildShuffledChoices();
      renderApp();
      alert('Đã lưu thay đổi thành công!');
    }

    function deleteSelectedQuestion() {
      const qId = document.getElementById('adminQuestionSelect').value;
      if (confirm(`Bạn có chắc muốn xóa câu hỏi ${qId} này không?`)) {
        questionsData = questionsData.filter(q => q.id !== qId);
        localStorage.setItem('avcd6_custom_data', JSON.stringify(questionsData));
        buildShuffledChoices();
        populateAdminSelect();
        if (questionsData.length > 0) loadQuestionToEdit(questionsData[0].id);
        renderApp();
        alert('Đã xóa câu hỏi thành công!');
      }
    }

    function openAddQuestionForm() {
      const newId = 'custom_' + Date.now();
      const newQ = {
        id: newId,
        exam: 1,
        qNum: questionsData.length + 1,
        part: 'VOCABULARY',
        partName: 'Từ vựng (Vocabulary)',
        question: 'Câu hỏi mới tạo...',
        options: { A: 'Đáp án A', B: 'Đáp án B', C: 'Đáp án C', D: 'Đáp án D' },
        correctAnswer: 'A',
        passage: '',
        explanation: {
          translation: 'Dịch nghĩa câu hỏi mới...',
          why: 'Giải thích tại sao chọn đáp án này...',
          wrong: 'Giải thích tại sao các câu khác sai...',
          tip: 'MẸO QUA MÔN: Dấu hiệu nhận biết nhanh...',
          topic: 'Từ vựng'
        }
      };

      questionsData.push(newQ);
      localStorage.setItem('avcd6_custom_data', JSON.stringify(questionsData));
      buildShuffledChoices();
      populateAdminSelect();
      document.getElementById('adminQuestionSelect').value = newId;
      loadQuestionToEdit(newId);
      alert('Đã tạo câu hỏi mới!');
    }

    function exportDataJSON() {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(questionsData, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "avcd6_5de_backup.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    }

    function importDataJSON(event) {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          const parsed = JSON.parse(e.target.result);
          if (Array.isArray(parsed) && parsed.length > 0) {
            questionsData = parsed;
            localStorage.setItem('avcd6_custom_data', JSON.stringify(questionsData));
            buildShuffledChoices();
            populateAdminSelect();
            renderApp();
            alert(`Đã nhập thành công ${parsed.length} câu hỏi!`);
          } else {
            alert('File JSON không đúng định dạng!');
          }
        } catch(err) {
          alert('Lỗi đọc file JSON: ' + err.message);
        }
      };
      reader.readAsText(file);
    }

    function resetDefaultData() {
      if (confirm('Khôi phục toàn bộ 250 câu hỏi về dữ liệu gốc?')) {
        localStorage.removeItem('avcd6_custom_data');
        questionsData = JSON.parse(JSON.stringify(DEFAULT_DATA));
        buildShuffledChoices();
        populateAdminSelect();
        renderApp();
        alert('Đã khôi phục dữ liệu gốc chuẩn 5 đề!');
      }
    }

    window.addEventListener('DOMContentLoaded', initApp);
  </script>

</body>
</html>
'''

with open('g:\\AVCD6\\index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Updated index.html with FULL MOBILE RESPONSIVE UI! Size:', os.path.getsize('g:\\AVCD6\\index.html'))
