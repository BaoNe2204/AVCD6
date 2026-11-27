# -*- coding: utf-8 -*-
import json, re, os

with open('g:\\AVCD6\\enriched_questions_v2.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Ensure numeric qNum and exam are ints
for q in questions:
    q['qNum'] = int(q.get('qNum', 1))
    q['exam'] = int(q.get('exam', 1))

# Sort questions strictly by exam, then by qNum
questions.sort(key=lambda x: (x['exam'], x['qNum']))

json_data_str = json.dumps(questions, ensure_ascii=False)

html_template = '''<!DOCTYPE html>
<html lang="vi" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AVCD6 PASS MÔN - Chia Theo Đề & Chuyên Đề Tổng Hợp 5 Đề</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
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
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    .dark ::-webkit-scrollbar-thumb { background: #334155; }
    
    .glass {
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    .dark .glass {
      background: rgba(15, 23, 42, 0.94);
    }
    .badge-pill {
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.025em;
      text-transform: uppercase;
      padding: 0.25rem 0.65rem;
      border-radius: 9999px;
    }
    .active-tab {
      background: #4f46e5 !important;
      color: #ffffff !important;
      border-color: #4f46e5 !important;
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    }
  </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-screen flex flex-col transition-colors duration-200">

  <!-- TOP HEADER -->
  <header class="sticky top-0 z-40 glass border-b border-slate-200 dark:border-slate-800 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
      <div class="flex items-center justify-between gap-4 flex-wrap">
        
        <!-- Logo & Title -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20 font-black text-xl">
            A6
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="text-lg font-black tracking-tight text-slate-900 dark:text-white">AVCD6 PASS MÔN</h1>
              <span class="badge-pill bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300">5 ĐỀ CHUẨN</span>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400">Chia theo từng đề riêng biệt • Chuyên đề tổng hợp 5 bài • Dịch từng từ</p>
          </div>
        </div>

        <!-- Mode Selector -->
        <div class="flex items-center bg-slate-100 dark:bg-slate-900 p-1 rounded-xl border border-slate-200 dark:border-slate-800 text-xs font-bold">
          <button id="modeStudyBtn" onclick="setMode('study')" class="px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm">
            <span>📖</span> Ôn Tập (Xem Lý Do Sai)
          </button>
          <button id="modeExamBtn" onclick="setMode('exam')" class="px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white">
            <span>⏱️</span> Thi Thử (Bấm Giờ)
          </button>
          <button id="modeWrongBtn" onclick="setMode('wrong')" class="px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white">
            <span>❌</span> Sổ Tay Câu Sai (<span id="wrongCountBadge">0</span>)
          </button>
        </div>

        <!-- Toggles & Tools -->
        <div class="flex items-center gap-2">
          <!-- Shuffle Choices Button -->
          <button id="shuffleChoicesBtn" onclick="toggleShuffleChoices()" class="p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold flex items-center gap-1 text-slate-700 dark:text-slate-300 shadow-sm" title="Đảo ngẫu nhiên vị trí các lựa chọn A, B, C, D để chống học vẹt">
            <span class="text-base">🔀</span> <span class="hidden sm:inline">Đảo đáp án</span>
            <span id="shuffleChoicesStatus" class="w-2 h-2 rounded-full bg-emerald-500 inline-block ml-0.5"></span>
          </button>

          <!-- Admin Panel Button -->
          <button onclick="toggleAdminModal()" class="p-2 rounded-xl border border-amber-300 dark:border-amber-700/50 bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 hover:bg-amber-100 text-xs font-bold flex items-center gap-1 shadow-sm">
            <span>⚙️</span> <span class="hidden md:inline">Admin</span>
          </button>

          <!-- Dark/Light Mode -->
          <button onclick="toggleDarkMode()" class="p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-sm shadow-sm">
            <span id="themeIcon">🌙</span>
          </button>
        </div>

      </div>

      <!-- TIMER STRIP (Exam Mode) -->
      <div id="examBar" class="hidden mt-2 pt-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between flex-wrap gap-3">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2 text-rose-600 dark:text-rose-400 font-mono font-bold text-lg bg-rose-50 dark:bg-rose-950/40 px-3 py-1 rounded-lg border border-rose-200 dark:border-rose-900/50">
            <span>⏳</span> <span id="timerText">60:00</span>
          </div>
          <div class="text-xs text-slate-500 dark:text-slate-400">
            Đã làm: <span id="examAnsweredCount" class="font-bold text-slate-800 dark:text-white">0</span> / <span id="examTotalCount">50</span> câu
          </div>
        </div>
        <button onclick="submitExam()" class="px-4 py-1.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold text-xs rounded-lg shadow hover:from-emerald-700 hover:to-teal-700 transition-all flex items-center gap-1.5">
          <span>🚀</span> Nộp Bài Chấm Điểm
        </button>
      </div>

    </div>
  </header>

  <!-- NAVIGATION TABS: CHIA THEO ĐỀ & CHUYÊN ĐỀ TỔNG HỢP -->
  <div class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shadow-sm sticky top-[61px] z-30">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-col gap-2.5">
      
      <!-- ROW 1: LUYỆN THEO TỪNG ĐỀ (Exam 1 -> 5) -->
      <div class="flex items-center justify-between gap-3 flex-wrap">
        <div class="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none">
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1 flex items-center gap-1">
            <span>📝</span> ĐỀ THI:
          </span>
          <button onclick="selectCategory('exam', 1)" id="tab_exam_1" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all active-tab">
            Đề 1 (50 câu)
          </button>
          <button onclick="selectCategory('exam', 2)" id="tab_exam_2" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
            Đề 2 (50 câu)
          </button>
          <button onclick="selectCategory('exam', 3)" id="tab_exam_3" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
            Đề 3 (50 câu)
          </button>
          <button onclick="selectCategory('exam', 4)" id="tab_exam_4" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
            Đề 4 (50 câu)
          </button>
          <button onclick="selectCategory('exam', 5)" id="tab_exam_5" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
            Đề 5 (50 câu)
          </button>
          <button onclick="selectCategory('all', 'all')" id="tab_all_all" class="cat-tab px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all">
            Tất cả 5 Đề (250 câu)
          </button>
        </div>

        <!-- Search input -->
        <div class="relative flex-1 sm:max-w-xs">
          <input type="text" id="searchInput" oninput="handleSearch(this.value)" placeholder="Tìm từ vựng, mẹo 3s, dịch nghĩa..." class="w-full text-xs pl-8 pr-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:outline-none focus:border-brand-500">
          <span class="absolute left-2.5 top-2 text-slate-400 text-xs">🔍</span>
        </div>
      </div>

      <!-- ROW 2: CHUYÊN ĐỀ TỔNG HỢP CẢ 5 BÀI (Topic Mastery across all 5 exams) -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none pt-1 border-t border-slate-100 dark:border-slate-800/80">
        <span class="text-xs font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider mr-1 flex items-center gap-1">
          <span>🎯</span> TỔNG HỢP 5 ĐỀ:
        </span>
        <button onclick="selectCategory('part', 'GRAMMAR')" id="tab_part_GRAMMAR" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center gap-1">
          <span>📘</span> Tổng Ngữ Pháp (50 câu)
        </button>
        <button onclick="selectCategory('part', 'VOCABULARY')" id="tab_part_VOCABULARY" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center gap-1">
          <span>📗</span> Tổng Từ Vựng (50 câu)
        </button>
        <button onclick="selectCategory('part', 'TRANSFORMATION')" id="tab_part_TRANSFORMATION" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center gap-1">
          <span>📙</span> Tổng Viết Lại Câu (50 câu)
        </button>
        <button onclick="selectCategory('part', 'CLOZE')" id="tab_part_CLOZE" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center gap-1">
          <span>📕</span> Tổng Điền Từ (50 câu)
        </button>
        <button onclick="selectCategory('part', 'READING')" id="tab_part_READING" class="cat-tab px-3 py-1 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center gap-1">
          <span>📖</span> Tổng Đọc Hiểu (50 câu)
        </button>
      </div>

    </div>
  </div>

  <!-- MAIN CONTENT CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full flex flex-col lg:flex-row gap-6">

    <!-- LEFT: QUESTION LIST -->
    <div class="flex-1 min-w-0 flex flex-col gap-5">
      
      <!-- CURRENT VIEW BANNER -->
      <div id="viewBanner" class="bg-gradient-to-r from-brand-600 to-indigo-600 rounded-2xl p-4 text-white shadow-sm flex items-center justify-between flex-wrap gap-3">
        <div>
          <div class="text-[11px] font-bold uppercase tracking-wider text-indigo-200" id="viewSubTitle">CHẾ ĐỘ LUYỆN THEO ĐỀ</div>
          <h2 class="text-lg font-black" id="viewMainTitle">ĐỀ ÔN TẬP 1 (50 CÂU CHUẨN ĐỀ THI)</h2>
        </div>
        <div class="flex items-center gap-3 text-xs bg-white/10 px-3 py-1.5 rounded-xl border border-white/20">
          <div>Tiến độ: <strong id="statAnswered">0</strong> / <strong id="statTotal">50</strong> câu</div>
          <div>•</div>
          <div class="text-emerald-300 font-bold">Đúng: <span id="statCorrect">0</span></div>
          <div>•</div>
          <div class="text-rose-300 font-bold">Sai: <span id="statWrong">0</span></div>
        </div>
      </div>

      <!-- EXAM RESULT BANNER -->
      <div id="examResultBanner" class="hidden bg-gradient-to-r from-brand-700 to-indigo-800 rounded-2xl p-6 text-white shadow-xl flex items-center justify-between flex-wrap gap-4">
        <div>
          <span class="badge-pill bg-white/20 text-white mb-2 inline-block">KẾT QUẢ THI THỬ</span>
          <h2 class="text-2xl font-black" id="examResultTitle">Bạn đạt 8.5 / 10 điểm!</h2>
          <p class="text-sm text-indigo-100 mt-1" id="examResultDesc">Số câu đúng: 42/50 • Tỷ lệ chính xác: 84% • KẾT QUẢ: ĐỖ QUA MÔN XUẤT SẮC!</p>
        </div>
        <div class="flex items-center gap-3">
          <button onclick="reviewMistakesAfterExam()" class="px-4 py-2 bg-white text-brand-700 font-bold text-xs rounded-xl shadow hover:bg-indigo-50 transition-all">
            Xem Các Câu Làm Sai
          </button>
          <button onclick="setMode('study')" class="px-4 py-2 bg-indigo-900/60 text-white font-bold text-xs rounded-xl hover:bg-indigo-900 transition-all">
            Về Chế Độ Ôn Tập
          </button>
        </div>
      </div>

      <!-- QUESTIONS CONTAINER -->
      <div id="questionsContainer" class="flex flex-col gap-5">
        <!-- Rendered dynamically by JavaScript -->
      </div>

      <!-- PAGINATION -->
      <div id="paginationControls" class="flex items-center justify-between bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 text-xs font-semibold">
        <button id="prevPageBtn" onclick="changePage(-1)" class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800">← Trang trước</button>
        <span id="pageInfo" class="text-slate-500">Trang 1 / 4</span>
        <button id="nextPageBtn" onclick="changePage(1)" class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800">Trang sau →</button>
      </div>

    </div>

    <!-- RIGHT: QUESTION PALETTE GRID (Grouped Numerically by Section) -->
    <div class="w-full lg:w-80 flex-shrink-0">
      <div class="sticky top-[135px] bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col gap-3.5 max-h-[calc(100vh-160px)] overflow-hidden">
        
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
          <h3 class="font-black text-xs uppercase tracking-wider text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
            <span>📑</span> BẢNG CÂU HỎI (<span id="paletteFilteredCount">0</span>)
          </h3>
          <span class="text-[10px] text-slate-400">Thứ tự chuẩn 1 - 50</span>
        </div>

        <!-- Legend -->
        <div class="flex items-center gap-3 text-[11px] text-slate-500 flex-wrap">
          <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-slate-200 dark:bg-slate-700 inline-block"></span> Chưa làm</div>
          <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Đúng</div>
          <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Sai</div>
        </div>

        <!-- Palette Grid with Section Groups (Scrollable) -->
        <div id="paletteGrid" class="flex flex-col gap-3 overflow-y-auto pr-1 flex-1">
          <!-- Rendered dynamically by sections -->
        </div>

        <!-- Quick Tips Box in Palette -->
        <div class="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40 rounded-xl p-3 text-[11px] text-amber-900 dark:text-amber-200">
          <div class="font-bold flex items-center gap-1 mb-1">
            <span>💡</span> BÍ QUYẾT QUA MÔN:
          </div>
          <p class="leading-relaxed">
            Bạn có thể chọn <strong>"Tổng Ngữ Pháp"</strong> hoặc <strong>"Tổng Từ Vựng"</strong> ở hàng trên để luyện liền mạch 50 câu trọng tâm của cả 5 đề!
          </p>
        </div>

      </div>
    </div>

  </main>

  <!-- ADMIN MANAGEMENT MODAL -->
  <div id="adminModal" class="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden">
      
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950">
        <div class="flex items-center gap-2">
          <span class="text-xl">⚙️</span>
          <div>
            <h3 class="font-black text-slate-900 dark:text-white">BẢNG QUẢN TRỊ ADMIN - DỮ LIỆU ĐỀ THI</h3>
            <p class="text-xs text-slate-500">Chỉnh sửa câu hỏi, đáp án đúng, dịch nghĩa, lời giải, mẹo nhận biết nhanh</p>
          </div>
        </div>
        <button onclick="toggleAdminModal()" class="text-slate-400 hover:text-slate-600 dark:hover:text-white text-xl p-1">✕</button>
      </div>

      <div class="p-6 overflow-y-auto flex-1 flex flex-col gap-6">
        <div class="flex items-center justify-between gap-3 flex-wrap bg-slate-100 dark:bg-slate-800 p-3 rounded-2xl text-xs font-semibold">
          <div class="flex items-center gap-2">
            <button onclick="openAddQuestionForm()" class="px-3 py-1.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 font-bold flex items-center gap-1">
              <span>➕</span> Thêm câu hỏi mới
            </button>
            <button onclick="exportDataJSON()" class="px-3 py-1.5 bg-brand-600 text-white rounded-lg hover:bg-brand-700 flex items-center gap-1">
              <span>💾</span> Xuất file JSON (Backup)
            </button>
            <label class="px-3 py-1.5 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-lg hover:bg-slate-300 cursor-pointer flex items-center gap-1">
              <span>📂</span> Nhập file JSON
              <input type="file" id="importJsonInput" accept=".json" onchange="importDataJSON(event)" class="hidden">
            </label>
          </div>
          <button onclick="resetDefaultData()" class="px-3 py-1.5 text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 rounded-lg">
            Khôi phục mặc định gốc
          </button>
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-xs font-bold text-slate-700 dark:text-slate-300">Chọn câu hỏi cần chỉnh sửa:</label>
          <div class="flex items-center gap-2">
            <select id="adminQuestionSelect" onchange="loadQuestionToEdit(this.value)" class="flex-1 p-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs font-mono">
            </select>
            <button onclick="deleteSelectedQuestion()" class="px-3 py-2 bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 rounded-xl font-bold text-xs hover:bg-rose-200">
              Xóa câu này
            </button>
          </div>
        </div>

        <div id="adminEditForm" class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="flex flex-col gap-1.5 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Nội dung câu hỏi (Question Text):</label>
            <textarea id="editQuestionText" rows="2" class="p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white font-medium"></textarea>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn A:</label>
            <input type="text" id="editOptA" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn B:</label>
            <input type="text" id="editOptB" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn C:</label>
            <input type="text" id="editOptC" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="font-bold text-slate-700 dark:text-slate-300">Lựa chọn D:</label>
            <input type="text" id="editOptD" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="font-bold text-emerald-600 dark:text-emerald-400">Đáp án ĐÚNG (A, B, C, hoặc D):</label>
            <select id="editCorrectAnswer" class="p-2 rounded-lg border border-emerald-300 dark:border-emerald-700 bg-emerald-50 dark:bg-emerald-950/40 font-bold text-sm">
              <option value="A">A</option>
              <option value="B">B</option>
              <option value="C">C</option>
              <option value="D">D</option>
            </select>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="font-bold text-slate-700 dark:text-slate-300">Chủ điểm ngữ pháp / Từ vựng:</label>
            <input type="text" id="editTopic" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
          </div>
          <div class="flex flex-col gap-1.5 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Dịch nghĩa tiếng Việt nguyên câu:</label>
            <textarea id="editTrans" rows="2" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"></textarea>
          </div>
          <div class="flex flex-col gap-1.5 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Giải thích chi tiết TẠI SAO CHỌN:</label>
            <textarea id="editWhy" rows="2" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"></textarea>
          </div>
          <div class="flex flex-col gap-1.5 md:col-span-2">
            <label class="font-bold text-slate-700 dark:text-slate-300">Tại sao các đáp án khác SAI:</label>
            <textarea id="editWrong" rows="2" class="p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800"></textarea>
          </div>
          <div class="flex flex-col gap-1.5 md:col-span-2">
            <label class="font-bold text-amber-600 dark:text-amber-400">MẸO QUA MÔN 3s (Cách nhận biết nhanh trắc nghiệm):</label>
            <textarea id="editTip" rows="2" class="p-2 rounded-lg border border-amber-300 dark:border-amber-700 bg-amber-50 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200 font-semibold"></textarea>
          </div>
        </div>
      </div>

      <div class="px-6 py-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end gap-3 bg-slate-50 dark:bg-slate-950">
        <button onclick="toggleAdminModal()" class="px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-100">
          Đóng
        </button>
        <button onclick="saveAdminChanges()" class="px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold shadow-md shadow-brand-500/20">
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
    
    // Category selection: type = 'exam' | 'part' | 'all', value = 1..5 | 'GRAMMAR'.. | 'all'
    let currentCatType = 'exam'; 
    let currentCatValue = 1; // Default to Đề 1
    
    let searchQuery = '';
    let shuffleChoicesEnabled = true;
    let inlineTransEnabled = false;
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

      // Ensure proper numeric types
      questionsData.forEach(q => {
        q.qNum = parseInt(q.qNum, 10);
        q.exam = parseInt(q.exam, 10);
      });

      // Natural numeric sort
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

    function toggleInlineTrans() {
      inlineTransEnabled = !inlineTransEnabled;
      const dot = document.getElementById('inlineTransStatus');
      dot.className = inlineTransEnabled ? 'w-2 h-2 rounded-full bg-emerald-500 inline-block ml-0.5' : 'w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-700 inline-block ml-0.5';
      renderApp();
    }

    function setMode(mode) {
      currentMode = mode;
      
      const studyBtn = document.getElementById('modeStudyBtn');
      const examBtn = document.getElementById('modeExamBtn');
      const wrongBtn = document.getElementById('modeWrongBtn');
      const examBar = document.getElementById('examBar');
      const examResultBanner = document.getElementById('examResultBanner');

      [studyBtn, examBtn, wrongBtn].forEach(b => {
        b.className = 'px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white';
      });

      if (mode === 'study') {
        studyBtn.className = 'px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm font-bold';
        examBar.classList.add('hidden');
        examResultBanner.classList.add('hidden');
        clearInterval(examTimerInterval);
      } else if (mode === 'exam') {
        examBtn.className = 'px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm font-bold';
        examBar.classList.remove('hidden');
        startExam();
      } else if (mode === 'wrong') {
        wrongBtn.className = 'px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 bg-white dark:bg-slate-800 text-brand-600 dark:text-brand-400 shadow-sm font-bold';
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
      dot.className = shuffleChoicesEnabled ? 'w-2 h-2 rounded-full bg-emerald-500 inline-block ml-0.5' : 'w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-700 inline-block ml-0.5';
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

    // ==========================================
    // CATEGORY SELECTION: BY EXAM OR BY TOPIC
    // ==========================================
    function selectCategory(type, val) {
      currentCatType = type;
      currentCatValue = val;
      currentPage = 1;

      updateCategoryUI();
      renderApp();
    }

    function updateCategoryUI() {
      // Remove active-tab from all
      document.querySelectorAll('.cat-tab').forEach(el => {
        el.classList.remove('active-tab');
      });

      // Highlight active
      const activeId = `tab_${currentCatType}_${currentCatValue}`;
      const activeBtn = document.getElementById(activeId);
      if (activeBtn) activeBtn.classList.add('active-tab');

      // Update banner text
      const subTitle = document.getElementById('viewSubTitle');
      const mainTitle = document.getElementById('viewMainTitle');

      if (currentCatType === 'exam') {
        subTitle.textContent = 'CHẾ ĐỘ LUYỆN THEO ĐỀ';
        mainTitle.textContent = `ĐỀ ÔN TẬP ${currentCatValue} (50 CÂU CHUẨN ĐỀ THI)`;
      } else if (currentCatType === 'part') {
        subTitle.textContent = 'CHUYÊN ĐỀ TỔNG HỢP CẢ 5 BÀI';
        const partNames = {
          'GRAMMAR': 'TỔNG HỢP TOÀN BỘ NGỮ PHÁP (50 CÂU CỦA 5 ĐỀ)',
          'VOCABULARY': 'TỔNG HỢP TOÀN BỘ TỪ VỰNG (50 CÂU CỦA 5 ĐỀ)',
          'TRANSFORMATION': 'TỔNG HỢP TOÀN BỘ VIẾT LẠI CÂU (50 CÂU CỦA 5 ĐỀ)',
          'CLOZE': 'TỔNG HỢP TOÀN BỘ ĐIỀN TỪ CLOZE TEST (50 CÂU CỦA 5 ĐỀ)',
          'READING': 'TỔNG HỢP TOÀN BỘ ĐỌC HIỂU READING (50 CÂU CỦA 5 ĐỀ)'
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

    // Natural numeric-ordered filtering
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

      // Always maintain numeric sort
      list.sort((a, b) => (a.exam - b.exam) || (a.qNum - b.qNum));

      return list;
    }

    function getSpecificWrongReason(q, chosenKey) {
      if (!chosenKey || chosenKey === q.correctAnswer) return "";
      
      const chosenMeaning = (q.choice_breakdown && q.choice_breakdown[chosenKey]) ? q.choice_breakdown[chosenKey] : '';
      if (chosenMeaning && !chosenMeaning.includes('phương án:')) {
        return `Bạn chọn [${chosenKey}] "${q.options[chosenKey]}" mang nghĩa là: "${chosenMeaning}". Nghĩa này HOÀN TOÀN KHÔNG PHÙ HỢP với ngữ cảnh của câu!`;
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

    function changePage(delta) {
      const filtered = getFilteredQuestions();
      const totalPages = Math.ceil(filtered.length / PAGE_SIZE) || 1;
      currentPage = Math.max(1, Math.min(totalPages, currentPage + delta));
      renderApp();
      window.scrollTo({ top: 120, behavior: 'smooth' });
    }

    // ==========================================
    // RENDER QUESTIONS & PALETTE
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

      document.getElementById('examAnsweredCount').textContent = answeredCount;
      document.getElementById('examTotalCount').textContent = totalQuestions;

      document.getElementById('pageInfo').textContent = `Trang ${currentPage} / ${totalPages} (Câu ${totalQuestions > 0 ? startIndex + 1 : 0} - ${endIndex} trong tổng số ${totalQuestions})`;
      document.getElementById('prevPageBtn').disabled = currentPage <= 1;
      document.getElementById('nextPageBtn').disabled = currentPage >= totalPages;

      const container = document.getElementById('questionsContainer');
      if (pageQuestions.length === 0) {
        container.innerHTML = `
          <div class="bg-white dark:bg-slate-900 rounded-3xl p-12 text-center border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-4xl mb-3">🎉</div>
            <h3 class="text-lg font-bold text-slate-800 dark:text-white">Không có câu hỏi nào!</h3>
            <p class="text-xs text-slate-500 mt-1">Bạn đã hoàn thành hết các câu trong mục này hoặc không tìm thấy kết quả phù hợp.</p>
          </div>
        `;
      } else {
        container.innerHTML = pageQuestions.map((q, idx) => {
          const userChoice = userAnswers[q.id];
          const hasAnswered = !!userChoice;
          const isCorrect = userChoice === q.correctAnswer;
          const showAnswerDetail = (currentMode === 'study' && hasAnswered) || (currentMode === 'exam' && examSubmitted);

          const choices = shuffledChoicesMap[q.id] || [
            { displayKey: 'A', originalKey: 'A', text: q.options.A, meaning: q.choice_breakdown?.A || '' },
            { displayKey: 'B', originalKey: 'B', text: q.options.B, meaning: q.choice_breakdown?.B || '' },
            { displayKey: 'C', originalKey: 'C', text: q.options.C, meaning: q.choice_breakdown?.C || '' },
            { displayKey: 'D', originalKey: 'D', text: q.options.D, meaning: q.choice_breakdown?.D || '' }
          ];

          const userChoiceText = userChoice ? (q.options[userChoice] || '') : '';
          const correctText = q.options[q.correctAnswer] || '';
          const specificWrongReason = (!isCorrect && userChoice) ? getSpecificWrongReason(q, userChoice) : '';

          return `
            <div id="card_${q.id}" class="bg-white dark:bg-slate-900 rounded-2xl p-5 border ${hasAnswered && !isCorrect && showAnswerDetail ? 'border-rose-300 dark:border-rose-900 shadow-rose-100 dark:shadow-none' : 'border-slate-200 dark:border-slate-800'} shadow-sm transition-all duration-200 hover:shadow-md">
              
              <!-- Card Header -->
              <div class="flex items-center justify-between gap-3 mb-3.5 flex-wrap">
                <div class="flex items-center gap-2">
                  <span class="w-8 h-8 rounded-xl bg-brand-100 dark:bg-brand-950/80 text-brand-700 dark:text-brand-300 font-mono font-bold text-xs flex items-center justify-center shadow-sm">
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
                  <div class="flex items-center gap-1.5 text-xs font-bold ${isCorrect ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}">
                    <span>${isCorrect ? '✔ BẠN ĐÃ CHỌN ĐÚNG' : '✖ BẠN ĐÃ CHỌN SAI'}</span>
                  </div>
                ` : ''}
              </div>

              <!-- Passage (if Cloze / Reading) -->
              ${q.passage ? `
                <div class="mb-4 bg-slate-50 dark:bg-slate-950/60 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-sans max-h-48 overflow-y-auto">
                  <div class="font-bold text-[10px] uppercase text-slate-400 tracking-wider mb-1 flex items-center gap-1">
                    <span>📄</span> Đoạn văn bài đọc:
                  </div>
                  <div class="whitespace-pre-line">${q.passage}</div>
                </div>
              ` : ''}

              <!-- Question text -->
              <h4 class="text-sm font-semibold text-slate-900 dark:text-white leading-relaxed mb-4">
                ${q.question}
              </h4>

              <!-- Options Grid (2x2 on desktop, 1 col on mobile) -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                ${choices.map(c => {
                  let btnStyle = "border-slate-200 dark:border-slate-800 hover:border-brand-400 dark:hover:border-brand-600 bg-slate-50/70 dark:bg-slate-950/50 text-slate-700 dark:text-slate-200";
                  let badgeStyle = "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300";
                  let statusTag = "";

                  if (hasAnswered) {
                    if (currentMode === 'study' || (currentMode === 'exam' && examSubmitted)) {
                      if (c.originalKey === q.correctAnswer) {
                        btnStyle = "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 font-bold ring-2 ring-emerald-500 shadow-sm";
                        badgeStyle = "bg-emerald-600 text-white border-emerald-600";
                        statusTag = `<span class="badge-pill bg-emerald-200 text-emerald-900 dark:bg-emerald-800 dark:text-emerald-100 text-[10px] ml-auto">✔ ĐÁP ÁN ĐÚNG</span>`;
                      } else if (userChoice === c.originalKey && !isCorrect) {
                        btnStyle = "border-rose-500 bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 ring-2 ring-rose-500 shadow-sm";
                        badgeStyle = "bg-rose-600 text-white border-rose-600";
                        statusTag = `<span class="badge-pill bg-rose-200 text-rose-900 dark:bg-rose-800 dark:text-rose-100 text-[10px] ml-auto">❌ BẠN ĐÃ CHỌN - SAI</span>`;
                      }
                    } else if (currentMode === 'exam' && !examSubmitted) {
                      if (userChoice === c.originalKey) {
                        btnStyle = "border-brand-500 bg-brand-50 dark:bg-brand-950/40 text-brand-900 dark:text-brand-200 font-bold ring-2 ring-brand-500";
                        badgeStyle = "bg-brand-600 text-white border-brand-600";
                      }
                    }
                  }

                  return `
                    <button onclick="selectAnswer('${q.id}', '${c.originalKey}')" class="w-full text-left p-3 rounded-xl border text-xs transition-all flex flex-col gap-1 ${btnStyle}">
                      <div class="flex items-start gap-2.5 w-full">
                        <span class="w-5 h-5 rounded-md border flex items-center justify-center font-bold font-mono text-[11px] flex-shrink-0 ${badgeStyle}">
                          ${c.displayKey}
                        </span>
                        <span class="flex-1 leading-snug pt-0.5 font-medium">${c.text}</span>
                        ${statusTag}
                      </div>

                      
                    </button>
                  `;
                }).join('')}
              </div>

              <!-- INSTANT WHY-WRONG ALERT -->
              ${showAnswerDetail ? `
                <div id="feedback_${q.id}" class="mt-4">
                  ${!isCorrect ? `
                    <div class="p-4 bg-rose-50/90 dark:bg-rose-950/50 border-2 border-rose-400 dark:border-rose-800 rounded-2xl shadow-sm flex flex-col gap-2.5">
                      <div class="flex items-center gap-2 text-rose-700 dark:text-rose-300 font-black text-xs uppercase tracking-wide">
                        <span class="text-base">❌</span> BẠN VỪA CHỌN: [${userChoice}] "${userChoiceText}" — TẠI SAO SAI?
                      </div>
                      <p class="text-xs text-rose-900 dark:text-rose-200 font-semibold leading-relaxed pl-6 border-l-2 border-rose-300 dark:border-rose-700 ml-1">
                        ${specificWrongReason}
                      </p>
                      <div class="mt-1 pt-2 border-t border-rose-200/80 dark:border-rose-900/60 flex items-start gap-2 text-xs font-bold text-emerald-800 dark:text-emerald-300 pl-1">
                        <span class="text-sm">👉</span>
                        <div>
                          <span>ĐÁP ÁN ĐÚNG PHẢI LÀ: </span>
                          <span class="underline decoration-2">[${q.correctAnswer}] "${correctText}"</span>
                          <span class="font-normal text-slate-600 dark:text-slate-300"> — ${q.explanation?.why || ''}</span>
                        </div>
                      </div>
                    </div>
                  ` : `
                    <div class="p-4 bg-emerald-50/90 dark:bg-emerald-950/50 border-2 border-emerald-400 dark:border-emerald-800 rounded-2xl shadow-sm flex flex-col gap-2">
                      <div class="flex items-center gap-2 text-emerald-700 dark:text-emerald-300 font-black text-xs uppercase tracking-wide">
                        <span class="text-base">🎉</span> CHÍNH XÁC! BẠN ĐÃ CHỌN ĐÚNG: [${q.correctAnswer}] "${correctText}"
                      </div>
                      <p class="text-xs text-emerald-900 dark:text-emerald-200 font-medium leading-relaxed pl-6">
                        ${q.explanation?.why || 'Lựa chọn hoàn toàn chính xác về cả ngữ pháp và ngữ cảnh.'}
                      </p>
                    </div>
                  `}
                </div>

                <!-- COMPREHENSIVE STUDY BOX -->
                <div class="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-col gap-3.5">
                  
                  <!-- 1. DỊCH NGUYÊN VĂN CẢ CÂU HOÀN CHỈNH -->
                  <div class="bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-900/60 rounded-xl p-3.5 text-xs shadow-sm">
                    <div class="font-bold text-indigo-950 dark:text-indigo-200 flex items-center gap-1.5 mb-1 text-[13px]">
                      <span>🇻🇳</span> DỊCH NGUYÊN VĂN TOÀN BỘ CÂU:
                    </div>
                    <p class="text-indigo-900 dark:text-indigo-100 leading-relaxed font-semibold text-xs">
                      "${q.explanation?.translation || 'Bản dịch đang được cập nhật.'}"
                    </p>
                  </div>

                  <!-- 2. NGHĨA CỦA CẢ 4 PHƯƠNG ÁN A, B, C, D -->
                  <div class="bg-slate-50 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-800 rounded-xl p-3.5 text-xs">
                    <div class="font-bold text-slate-800 dark:text-slate-200 flex items-center gap-1.5 mb-2">
                      <span>📚</span> NGHĨA CHI TIẾT CỦA CẢ 4 ĐÁP ÁN:
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <span class="font-mono font-bold text-brand-600 dark:text-brand-400">A. ${q.options.A}:</span>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.A || ''}</span>
                      </div>
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <span class="font-mono font-bold text-brand-600 dark:text-brand-400">B. ${q.options.B}:</span>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.B || ''}</span>
                      </div>
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <span class="font-mono font-bold text-brand-600 dark:text-brand-400">C. ${q.options.C}:</span>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.C || ''}</span>
                      </div>
                      <div class="bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                        <span class="font-mono font-bold text-brand-600 dark:text-brand-400">D. ${q.options.D}:</span>
                        <span class="text-slate-700 dark:text-slate-300 ml-1 font-medium">${q.choice_breakdown?.D || ''}</span>
                      </div>
                    </div>
                  </div>

                  <!-- 3. TRA NGHĨA CÁC TỪ VỰNG QUAN TRỌNG TRONG CÂU -->
                  ${q.vocab_in_question && q.vocab_in_question.length > 0 ? `
                    <div class="bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50 rounded-xl p-3 text-xs">
                      <div class="font-bold text-amber-900 dark:text-amber-200 flex items-center gap-1 mb-1.5">
                        <span>🔍</span> TỪ VỰNG TRỌNG TÂM XUẤT HIỆN TRONG ĐỀ:
                      </div>
                      <div class="flex flex-wrap gap-2">
                        ${q.vocab_in_question.map(item => `
                          <span class="inline-flex items-center gap-1 bg-white dark:bg-slate-800 px-2.5 py-1 rounded-md border border-amber-200 dark:border-amber-800 text-[11px]">
                            <strong class="font-mono text-amber-800 dark:text-amber-300">${item.word}</strong>: 
                            <span class="text-slate-700 dark:text-slate-300">${item.meaning}</span>
                          </span>
                        `).join('')}
                      </div>
                    </div>
                  ` : ''}

                  <!-- 4. FAST TEST-TAKING TIP (3 SECONDS TO PASS) -->
                  <div class="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-950/40 dark:to-orange-950/30 border border-amber-200 dark:border-amber-900/50 rounded-xl p-3.5 text-xs">
                    <div class="font-black text-amber-900 dark:text-amber-200 flex items-center gap-1.5 mb-1 tracking-wide">
                      <span class="text-base">⚡</span> ${q.explanation?.tip ? q.explanation.tip.split(':')[0] : 'MẸO QUA MÔN 3s'}
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

    // =========================================================================
    // RENDER GROUPED PALETTE (GROUPED BY SECTIONS / EXAMS IN NATURAL 1..50 ORDER)
    // =========================================================================
    function renderGroupedPalette(filtered) {
      const palette = document.getElementById('paletteGrid');
      document.getElementById('paletteFilteredCount').textContent = filtered.length;

      // Group questions by section
      let groups = {};

      if (currentCatType === 'exam') {
        // Group by 5 parts of the exam
        groups = {
          'I. Từ vựng (Câu 1 - 10)': filtered.filter(q => q.qNum >= 1 && q.qNum <= 10),
          'II. Ngữ pháp (Câu 11 - 20)': filtered.filter(q => q.qNum >= 11 && q.qNum <= 20),
          'III. Viết lại câu (Câu 21 - 30)': filtered.filter(q => q.qNum >= 21 && q.qNum <= 30),
          'IV. Điền từ (Câu 31 - 40)': filtered.filter(q => q.qNum >= 31 && q.qNum <= 40),
          'V. Đọc hiểu (Câu 41 - 50)': filtered.filter(q => q.qNum >= 41 && q.qNum <= 50)
        };
      } else if (currentCatType === 'part') {
        // Group by Exam 1 -> 5
        groups = {
          'Đề 1': filtered.filter(q => q.exam === 1),
          'Đề 2': filtered.filter(q => q.exam === 2),
          'Đề 3': filtered.filter(q => q.exam === 3),
          'Đề 4': filtered.filter(q => q.exam === 4),
          'Đề 5': filtered.filter(q => q.exam === 5)
        };
      } else {
        // All: group by Exam 1 -> 5
        groups = {
          'Đề 1 (50 câu)': filtered.filter(q => q.exam === 1),
          'Đề 2 (50 câu)': filtered.filter(q => q.exam === 2),
          'Đề 3 (50 câu)': filtered.filter(q => q.exam === 3),
          'Đề 4 (50 câu)': filtered.filter(q => q.exam === 4),
          'Đề 5 (50 câu)': filtered.filter(q => q.exam === 5)
        };
      }

      palette.innerHTML = Object.entries(groups).map(([groupTitle, groupQuestions]) => {
        if (groupQuestions.length === 0) return '';

        // Strict numeric sort within group
        groupQuestions.sort((a, b) => a.qNum - b.qNum);

        return `
          <div class="bg-slate-50/70 dark:bg-slate-950/40 p-2.5 rounded-xl border border-slate-200/80 dark:border-slate-800">
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
                  <button onclick="scrollToQuestion('${q.id}')" class="h-8 rounded-lg border text-xs font-mono font-bold flex items-center justify-center transition-all ${colorClass}" title="Đề ${q.exam} - Câu ${q.qNum}">
                    ${q.qNum}
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).join('');
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
        <option value="${q.id}">[Đề ${q.exam} - Câu ${q.qNum}] (${q.part}) ${q.question.substring(0, 75)}...</option>
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
      alert('Đã lưu thay đổi thành công vào trình duyệt!');
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
      alert('Đã tạo câu hỏi mới! Bạn hãy nhập nội dung và bấm "Lưu Thay Đổi".');
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
            alert('File JSON không đúng định dạng mảng câu hỏi!');
          }
        } catch(err) {
          alert('Lỗi đọc file JSON: ' + err.message);
        }
      };
      reader.readAsText(file);
    }

    function resetDefaultData() {
      if (confirm('Khôi phục toàn bộ 250 câu hỏi về dữ liệu gốc ban đầu?')) {
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

print('Updated index.html with EXAM & TOPIC tabs + Natural numeric ordering! Size:', os.path.getsize('g:\\AVCD6\\index.html'))
