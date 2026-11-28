# -*- coding: utf-8 -*-
"""
Script to build enhanced AVCD6 app with dedicated 'BÍ KÍP & MẸO 3S' tab.
"""
import json, re, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load questions
with open(os.path.join(BASE_DIR, 'enriched_questions_v2.json'), 'r', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions:
    q['qNum'] = int(q.get('qNum', 1))
    q['exam'] = int(q.get('exam', 1))

questions.sort(key=lambda x: (x['exam'], x['qNum']))
json_data_str = json.dumps(questions, ensure_ascii=False)

# Define TIPS DATA
tips_catalog = [
    # ==================== VIẾT LẠI CÂU ====================
    {
        "id": "trans_1",
        "category": "trans",
        "categoryName": "Viết Lại Câu",
        "icon": "🔄",
        "badge": "BỊ ĐỘNG (PASSIVE)",
        "badgeColor": "amber",
        "title": "1. Câu Bị Động (Đảo tân ngữ lên đầu)",
        "signal": "Đáp án đưa người/vật bị tác động lên làm chủ ngữ mới (VD câu gốc: <em>They will release <u>the film</u></em> → Đáp án bắt đầu bằng: <em><u>The film</u>...</em>).",
        "formula": "Bắt buộc phải có <strong>BE + V3/ed</strong> đúng theo thì câu gốc:<br>• <strong>Hiện tại đơn:</strong> am / is / are + V3/ed<br>• <strong>Hiện tại tiếp diễn:</strong> am / is / are + being + V3/ed<br>• <strong>Quá khứ đơn:</strong> was / were + V3/ed<br>• <strong>Hiện tại hoàn thành:</strong> have / has + been + V3/ed<br>• <strong>Tương lai (will) / Modal verbs:</strong> will / can / must + be + V3/ed",
        "trap": "⚠️ <strong>Bẫy danh từ số ít/nhiều:</strong> Khi đảo tân ngữ lên làm chủ ngữ mới, động từ to-be phải chia theo chủ ngữ mới (VD: <em>He bought <u>many books</u></em> → <em>Many books <u>were</u> bought</em>, KHÔNG dùng <em>was</em>).",
        "example": "<strong>Gốc:</strong> Someone cleans the windows every morning.<br><strong>Đổi:</strong> The windows are cleaned every morning.",
        "exampleTrans": "Cửa sổ được lau dọn vào mỗi buổi sáng.",
        "practiceTarget": {"type": "part", "val": "TRANSFORMATION"}
    },
    {
        "id": "trans_2",
        "category": "trans",
        "categoryName": "Viết Lại Câu",
        "icon": "💬",
        "badge": "GIÁN TIẾP (REPORTED)",
        "badgeColor": "amber",
        "title": "2. Câu Gián Tiếp (Kể lại lời người khác)",
        "signal": "Câu gốc có dấu ngoặc kép <strong>\"...\" said / asked / told</strong>.",
        "formula": "<strong>3 BƯỚC THẦN TỐC:</strong><br>① <strong>Lùi thì:</strong> Hiện tại đơn → Quá khứ đơn; Quá khứ đơn / HTHT → Quá khứ hoàn thành (had + V3); will → would; can → could.<br>② <strong>Đổi trạng từ & thời gian:</strong><br>&nbsp;&nbsp;• <em>tomorrow</em> → <em>the following day / the next day</em><br>&nbsp;&nbsp;• <em>yesterday</em> → <em>the day before / the previous day</em><br>&nbsp;&nbsp;• <em>today / tonight</em> → <em>that day / that night</em><br>&nbsp;&nbsp;• <em>now</em> → <em>then</em>; <em>here</em> → <em>there</em>; <em>this/these</em> → <em>that/those</em><br>③ <strong>Nếu là câu hỏi:</strong> Thêm <strong>if / whether</strong> (câu hỏi Yes/No) hoặc giữ từ để hỏi (What/Where/Why) + <strong>S + V</strong>.",
        "trap": "⚠️ <strong>CỰC KỲ QUAN TRỌNG:</strong> Trong câu gián tiếp, tuyệt đối KHÔNG đảo trợ động từ <em>do / does / did</em> ra trước chủ ngữ! (Phải là <em>... where I lived</em>, cấm chọn <em>... where did I live</em>).",
        "example": "<strong>Gốc:</strong> \"Will you attend the workshop tomorrow?\" Mary asked me.<br><strong>Đổi:</strong> Mary asked me if I would attend the workshop the following day.",
        "exampleTrans": "Mary hỏi tôi xem tôi có tham gia buổi hội thảo vào ngày hôm sau hay không.",
        "practiceTarget": {"type": "part", "val": "TRANSFORMATION"}
    },
    {
        "id": "trans_3",
        "category": "trans",
        "categoryName": "Viết Lại Câu",
        "icon": "🌿",
        "badge": "CÂU ĐIỀU KIỆN (IF / UNLESS)",
        "badgeColor": "amber",
        "title": "3. Câu Điều Kiện (If loại 2, loại 3 & Unless)",
        "signal": "Câu gốc dùng <strong>because / so / since</strong> diễn tả nguyên nhân - kết quả ở hiện tại hoặc quá khứ.",
        "formula": "• <strong>Nếu câu gốc ở HIỆN TẠI</strong> (don't, can't, is, are, V1) → Dùng <strong>IF LOẠI 2</strong> (trái ngược hiện tại):<br>&nbsp;&nbsp;👉 <em>If + S + V2/ed (tất cả ngôi dùng were), S + would / could + V(nguyên mẫu)</em><br>• <strong>Nếu câu gốc ở QUÁ KHỨ</strong> (didn't, wasn't, were, V2) → Dùng <strong>IF LOẠI 3</strong> (trái ngược quá khứ):<br>&nbsp;&nbsp;👉 <em>If + S + had + V3/ed, S + would / could + have + V3/ed</em><br>• <strong>Thấy 'You should + V' (lời khuyên):</strong> → <em>If I were you, I would + V</em><br>• <strong>Unless = If ... not</strong> (Sau Unless luôn là mệnh đề khẳng định, không dùng phủ định).",
        "trap": "⚠️ <strong>Đảo ngược nghĩa:</strong> Thực tế KHÔNG có tiền → NẾU có tiền; Thực tế BỊ TRỄ XE do dậy muộn → NẾU KHÔNG dậy muộn thì ĐÃ KHÔNG trễ xe.",
        "example": "<strong>Gốc:</strong> I don't have enough money, so I can't buy that laptop.<br><strong>Đổi:</strong> If I had enough money, I could buy that laptop.",
        "exampleTrans": "Nếu tôi có đủ tiền, tôi đã có thể mua chiếc laptop đó.",
        "practiceTarget": {"type": "part", "val": "TRANSFORMATION"}
    },
    {
        "id": "trans_4",
        "category": "trans",
        "categoryName": "Viết Lại Câu",
        "icon": "⚡",
        "badge": "ĐỘNG TỪ KHUYẾT THIẾU",
        "badgeColor": "amber",
        "title": "4. Động Từ Khuyết Thiếu (Modal Verbs)",
        "signal": "Câu gốc chứa các cụm từ diễn tả sự cần thiết, khả năng, cấm đoán hoặc suy đoán chắc chắn.",
        "formula": "<strong>BẢNG ĐỔI CẶP TƯƠNG ĐƯƠNG 100% ĂN ĐIỂM:</strong><br>• <em>It isn't necessary for sb to V</em> (không cần thiết) = <strong>S + don't / doesn't have to + V</strong><br>• <em>You are not allowed to V / It is forbidden</em> (cấm) = <strong>S + mustn't + V</strong><br>• <em>I'm sure / certain ... isn't</em> (chắc chắn không phải) = <strong>S + can't be + ...</strong><br>• <em>I'm sure / certain ... is</em> (chắc chắn là) = <strong>S + must be + ...</strong><br>• <em>Perhaps / Maybe / It is possible</em> (có lẽ) = <strong>S + might / may + V</strong><br>• <em>couldn't + V</em> (quá khứ không thể) = <strong>wasn't / weren't able to + V</strong>",
        "trap": "⚠️ <strong>BẪY TỬ THẦN:</strong> <em>don't have to</em> = không cần làm (làm hay không tùy bạn); còn <em>mustn't</em> = TUYỆT ĐỐI CẤM LÀM. Thấy 'isn't necessary' mà chọn 'mustn't' là mất điểm ngay!",
        "example": "<strong>Gốc:</strong> It isn't necessary for students to wear uniforms on Fridays.<br><strong>Đổi:</strong> Students don't have to wear uniforms on Fridays.",
        "exampleTrans": "Học sinh không phải mặc đồng phục vào các ngày thứ Sáu.",
        "practiceTarget": {"type": "part", "val": "TRANSFORMATION"}
    },
    {
        "id": "trans_5",
        "category": "trans",
        "categoryName": "Viết Lại Câu",
        "icon": "⏳",
        "badge": "QUÁ KHỨ ↔ HOÀN THÀNH",
        "badgeColor": "amber",
        "title": "5. Quá Khứ Đơn ↔ Hiện Tại Hoàn Thành (Last... ago)",
        "signal": "Câu gốc có <strong>last + V2 ... ago</strong> hoặc <strong>The last time + S + V2 was ... ago</strong> (lần cuối cùng làm việc gì là cách đây bao lâu).",
        "formula": "👉 Đổi sang phủ định Hiện tại hoàn thành:<br><strong>S + haven't / hasn't + V3/ed + for + khoảng thời gian</strong><br><em>Hoặc:</em> <strong>It is + khoảng thời gian + since + S + last + V2/ed</strong><br><em>Hoặc:</em> <strong>S + started / began + V-ing / to V + khoảng thời gian + ago</strong> = <strong>S + have/has + V3/ed + for...</strong>",
        "trap": "⚠️ <strong>DÙNG FOR HAY SINCE:</strong> <em>FOR</em> đi với khoảng thời gian (for 4 years, for a long time); <em>SINCE</em> chỉ đi với mốc thời gian (since 2020, since yesterday). CẤM chọn 'since four years'!",
        "example": "<strong>Gốc:</strong> He last played tennis four years ago.<br><strong>Đổi:</strong> He hasn't played tennis for four years.",
        "exampleTrans": "Anh ấy đã không chơi quần vợt suốt 4 năm nay.",
        "practiceTarget": {"type": "part", "val": "TRANSFORMATION"}
    },
    {
        "id": "trans_6",
        "category": "trans",
        "categoryName": "Viết Lại Câu",
        "icon": "⚖️",
        "badge": "MẪU TƯƠNG ĐƯƠNG KINH ĐIỂN",
        "badgeColor": "amber",
        "title": "6. Mặc Dù (Although ↔ Despite) & Các Cấu Trúc Hay Gặp",
        "signal": "Câu có <em>Although, In spite of, Prefer, Find it, Describe</em>.",
        "formula": "• <strong>Although / Though / Even though + S + V (mệnh đề)</strong><br>&nbsp;&nbsp;= <strong>In spite of / Despite + Cụm danh từ / V-ing</strong> (hoặc the fact that + S + V)<br>• <strong>prefer A to B</strong> = <strong>like A more than B</strong> (Thích A hơn B)<br>• <strong>find it + adj + to V</strong> = <strong>It is + adj + for sb + to V</strong> (Thấy cái gì như thế nào khi làm gì)<br>• <strong>Đồng tình khẳng định:</strong> S + V, too = <strong>So + trợ động từ + S</strong> (VD: So do I)<br>• <strong>Hỏi miêu tả tính chất (describe):</strong> = <strong>What is / are ... like?</strong>",
        "trap": "⚠️ <strong>DESPITE KHÔNG CÓ 'OF':</strong> Chỉ có <em>In spite OF</em> hoặc <em>Despite</em> (KHÔNG có 'Despite of').",
        "example": "<strong>Gốc:</strong> Although it rained heavily, they enjoyed the outdoor concert.<br><strong>Đổi:</strong> Despite the heavy rain, they enjoyed the outdoor concert.",
        "exampleTrans": "Mặc dù trời mưa to, họ vẫn tận hưởng buổi hòa nhạc ngoài trời.",
        "practiceTarget": {"type": "part", "val": "TRANSFORMATION"}
    },
    {
        "id": "trans_7",
        "category": "trans",
        "categoryName": "Viết Lại Câu",
        "icon": "🎯",
        "badge": "SO / SUCH / ENOUGH / TOO",
        "badgeColor": "amber",
        "title": "7. Cấu Trúc Quá Đến Nỗi (So... that, Such... that, Too, Enough)",
        "signal": "Câu gốc có tính từ miêu tả mức độ cao, nguyên nhân dẫn đến kết quả không thể thực hiện.",
        "formula": "• <strong>So ... that:</strong> S + V + <em>so + adj / adv + that</em> + S + V<br>• <strong>Such ... that:</strong> S + V + <em>such + (a/an) + adj + Noun + that</em> + S + V<br>• <strong>Too ... to V (quá... không thể):</strong> S + be + <em>too + adj + (for sb) + to V</em><br>• <strong>Enough to V (đủ... để làm gì):</strong> S + be + <em>adj + enough + (for sb) + to V</em>",
        "trap": "⚠️ <strong>Vị trí của ENOUGH:</strong> Tính từ luôn đứng <u>TRƯỚC</u> enough (VD: <em>warm enough</em>, <em>tall enough</em>, KHÔNG viết <em>enough warm</em>). Danh từ mới đứng <u>SAU</u> enough (<em>enough money</em>).",
        "example": "<strong>Gốc:</strong> The coffee is so hot that I can't drink it.<br><strong>Đổi:</strong> The coffee is too hot for me to drink.",
        "exampleTrans": "Cà phê quá nóng khiến tôi không thể uống được.",
        "practiceTarget": {"type": "part", "val": "TRANSFORMATION"}
    },

    # ==================== NGỮ PHÁP 3S ====================
    {
        "id": "gram_1",
        "category": "gram",
        "categoryName": "Ngữ Pháp 3s",
        "icon": "⏱️",
        "badge": "12 THÌ TIẾNG ANH",
        "badgeColor": "indigo",
        "title": "8. Nhận Biết Các Thì Trong 3 Giây (Keyword Vàng)",
        "signal": "Nhìn trạng từ chỉ thời gian ở cuối hoặc đầu câu:",
        "formula": "• <strong>Quá khứ đơn:</strong> <em>yesterday, ago, last (night/week), in + năm quá khứ (in 2018)</em> → Chọn <strong>V2/ed</strong> hoặc <strong>didn't + V</strong>.<br>• <strong>Hiện tại hoàn thành:</strong> <em>since, for, already, just, yet, recently, so far, ever, never</em> → Chọn <strong>have / has + V3/ed</strong>.<br>• <strong>Quá khứ hoàn thành:</strong> <em>by the time + mốc quá khứ, before, after</em> (hành động xảy ra trước 1 hành động quá khứ khác) → Chọn <strong>had + V3/ed</strong>.<br>• <strong>Quá khứ tiếp diễn:</strong> <em>at this time yesterday, at 8 PM last night, when/while</em> (đang xảy ra thì việc khác cắt ngang) → <strong>was / were + V-ing</strong>.<br>• <strong>Tương lai đơn:</strong> <em>tomorrow, next week, in the future, think, hope</em> → <strong>will + V</strong>.",
        "trap": "⚠️ <em>SINCE</em> đi với mốc thời gian (since 2015), sau Since chia Quá khứ đơn; Mệnh đề chính trước Since chia Hiện tại hoàn thành.",
        "example": "By the time we arrived at the cinema, the movie <u>had already started</u>.",
        "exampleTrans": "Trước khi chúng tôi đến rạp chiếu phim, bộ phim đã bắt đầu rồi.",
        "practiceTarget": {"type": "part", "val": "GRAMMAR"}
    },
    {
        "id": "gram_2",
        "category": "gram",
        "categoryName": "Ngữ Pháp 3s",
        "icon": "🔗",
        "badge": "MỆNH ĐỀ QUAN HỆ",
        "badgeColor": "indigo",
        "title": "9. Mệnh Đề Quan Hệ & Quy Tắc CẤM DÙNG 'THAT'",
        "signal": "Chỗ trống nối 2 mệnh đề đứng sau 1 danh từ.",
        "formula": "• <strong>WHO:</strong> Thay cho Người làm Chủ ngữ (sau Who là Động từ: <em>Người + WHO + V</em>)<br>• <strong>WHOM:</strong> Thay cho Người làm Tân ngữ (sau Whom là Chủ ngữ: <em>Người + WHOM + S + V</em>)<br>• <strong>WHICH:</strong> Thay cho Đồ vật, Con vật, Sự việc<br>• <strong>WHOSE:</strong> Chỉ sở hữu (sau Whose là Danh từ: <em>WHOSE + Noun</em>)<br>• <strong>WHERE:</strong> Chỉ nơi chốn (= in / at which + S + V)",
        "trap": "🚫 <strong>HAI ĐIỀU CẤM KỴ KHI DÙNG 'THAT':</strong><br>1. Có dấu phẩy (,) phía trước → <strong>TUYỆT ĐỐI KHÔNG DÙNG THAT</strong>!<br>2. Có giới từ (in, on, at, with, about...) đứng ngay trước chỗ trống → <strong>TUYỆT ĐỐI KHÔNG DÙNG THAT</strong> (phải dùng <em>in which</em> hoặc <em>with whom</em>)!",
        "example": "Mr. David, <u>whom</u> you met yesterday, is our new marketing manager.",
        "exampleTrans": "Ông David, người mà bạn đã gặp hôm qua, là trưởng phòng tiếp thị mới của chúng tôi.",
        "practiceTarget": {"type": "part", "val": "GRAMMAR"}
    },
    {
        "id": "gram_3",
        "category": "gram",
        "categoryName": "Ngữ Pháp 3s",
        "icon": "✂️",
        "badge": "RÚT GỌN MỆNH ĐỀ",
        "badgeColor": "indigo",
        "title": "10. Rút Gọn Mệnh Đề Quan Hệ (V-ing vs V3/ed)",
        "signal": "Hai mệnh đề chung chủ ngữ, hoặc sau danh từ cần lược bỏ đại từ quan hệ (who, which, that).",
        "formula": "• <strong>CHỦ ĐỘNG</strong> (Tự thực hiện hành động) → Rút gọn thành <strong>V-ing</strong><br>&nbsp;&nbsp;VD: <em>The man <u>who is standing</u> there</em> → <em>The man <u>standing</u> there</em>.<br>• <strong>BỊ ĐỘNG</strong> (Được / bị tác động) → Rút gọn thành <strong>V3/ed</strong><br>&nbsp;&nbsp;VD: <em>The bridge <u>which was built</u> in 1990</em> → <em>The bridge <u>built</u> in 1990</em>.",
        "trap": "⚠️ Nhìn xem đối tượng là Người hay Vật và có tự làm được hành động không. Đồ vật / tòa nhà / cuốn sách... đi với động từ như build, write, publish luôn là BỊ ĐỘNG (V3/ed).",
        "example": "The documents <u>sent</u> by email this morning require your immediate signature.",
        "exampleTrans": "Các tài liệu được gửi qua email sáng nay cần chữ ký ngay lập tức của bạn.",
        "practiceTarget": {"type": "part", "val": "GRAMMAR"}
    },
    {
        "id": "gram_4",
        "category": "gram",
        "categoryName": "Ngữ Pháp 3s",
        "icon": "📝",
        "badge": "V-ING HAY TO-V",
        "badgeColor": "indigo",
        "title": "11. Danh Động Từ & Động Từ Nguyên Mẫu (V-ing vs To-V)",
        "signal": "Sau một động từ chính, cần chọn dạng của động từ thứ hai đứng sau.",
        "formula": "• <strong>NHÓM LUÔN ĐI VỚI V-ING:</strong><br><em>enjoy, avoid (tránh), mind (phiền), practice, suggest (gợi ý), consider (cân nhắc), postpone (hoãn), finish, admit, deny, keep, can't help, look forward to (mong đợi)</em>.<br>• <strong>NHÓM LUÔN ĐI VỚI TO-V:</strong><br><em>want, decide, hope, plan, promise, agree, refuse (từ chối), afford (đủ khả năng chi trả), expect, manage, offer, tend</em>.",
        "trap": "⚠️ <strong>ĐẶC BIỆT (REMEMBER / FORGET / STOP):</strong><br>• <em>+ V-ing:</em> Việc ĐÃ LÀM trong quá khứ (VD: I remember locking the door - nhớ đã khóa cửa rồi).<br>• <em>+ To-V:</em> Nhớ / Dừng lại ĐỂ LÀM một việc tiếp theo (VD: Remember to lock the door - nhớ phải khóa cửa nhé).",
        "example": "He decided <u>to apply</u> for the scholarship after consulting his teacher.",
        "exampleTrans": "Anh ấy quyết định nộp hồ sơ xin học bổng sau khi tham khảo ý kiến giáo viên.",
        "practiceTarget": {"type": "part", "val": "GRAMMAR"}
    },
    {
        "id": "gram_5",
        "category": "gram",
        "categoryName": "Ngữ Pháp 3s",
        "icon": "🔺",
        "badge": "GIỚI TỪ IN - ON - AT",
        "badgeColor": "indigo",
        "title": "12. Kim Tự Tháp Giới Từ Thời Gian (IN - ON - AT)",
        "signal": "Chỗ trống đứng trước mốc thời gian, tháng, năm, thứ, giờ.",
        "formula": "• <strong>IN (Đỉnh rộng - Khái quát, dài):</strong> Năm (<em>in 2024</em>), Tháng (<em>in July</em>), Mùa (<em>in summer</em>), Buổi trong ngày (<em>in the morning</em>).<br>• <strong>ON (Thân kim tự tháp - Cụ thể vừa):</strong> Thứ trong tuần (<em>on Monday</em>), Ngày cụ thể (<em>on October 10th</em>), Ngày lễ có chữ Day (<em>on Christmas Day</em>).<br>• <strong>AT (Đáy hẹp - Chính xác, mốc cụ thể):</strong> Giờ giấc (<em>at 8:30</em>), Ban đêm (<em>at night</em>), Dịp lễ không có chữ Day (<em>at Christmas, at Tet</em>), Cuối tuần (<em>at the weekend</em>).",
        "trap": "⚠️ Thấy vừa có ngày vừa có tháng (VD: <em>... 15th July</em>) → Phải ưu tiên theo NGÀY, chọn <strong>ON</strong>!",
        "example": "The final examination will take place <u>on</u> Monday morning <u>at</u> 8:00 AM.",
        "exampleTrans": "Kỳ thi cuối kỳ sẽ diễn ra vào sáng thứ Hai lúc 8:00 đúng.",
        "practiceTarget": {"type": "part", "val": "GRAMMAR"}
    },

    # ==================== TỪ VỰNG & COLLOCATIONS ====================
    {
        "id": "vocab_1",
        "category": "vocab",
        "categoryName": "Từ Vựng & Cụm Cố Định",
        "icon": "💡",
        "badge": "MAKE VS DO",
        "badgeColor": "emerald",
        "title": "13. Cặp Bài Trùng MAKE vs DO (Đề nào cũng có)",
        "signal": "Trước các danh từ như decision, progress, effort, mistake hay homework, research, business.",
        "formula": "• <strong>DÙNG MAKE (Khi tạo ra cái mới hoặc tác động kết quả):</strong><br>&nbsp;&nbsp;• <em>make a decision</em> (ra quyết định)<br>&nbsp;&nbsp;• <em>make progress</em> (tiến bộ)<br>&nbsp;&nbsp;• <em>make an effort</em> (nỗ lực, cố gắng)<br>&nbsp;&nbsp;• <em>make a mistake</em> (phạm sai lầm)<br>&nbsp;&nbsp;• <em>make an appointment</em> (đặt lịch hẹn)<br>&nbsp;&nbsp;• <em>make money / a profit</em> (kiếm tiền, sinh lời)<br>• <strong>DÙNG DO (Khi thực hiện công việc, nhiệm vụ hoặc hoạt động thường ngày):</strong><br>&nbsp;&nbsp;• <em>do homework</em> (làm bài tập về nhà)<br>&nbsp;&nbsp;• <em>do research</em> (làm nghiên cứu)<br>&nbsp;&nbsp;• <em>do business</em> (kinh doanh)<br>&nbsp;&nbsp;• <em>do harm / do good</em> (gây hại / làm điều tốt)<br>&nbsp;&nbsp;• <em>do someone a favor</em> (giúp đỡ ai một việc)",
        "trap": "⚠️ Đề thi rất hay gài: <em>make research</em> (SAI! phải là <em>do research</em>), hoặc <em>do a decision</em> (SAI! phải là <em>make a decision</em>).",
        "example": "Despite facing many difficulties, she <u>made</u> great progress in her studies.",
        "exampleTrans": "Dù gặp nhiều khó khăn, cô ấy đã có tiến bộ vượt bậc trong học tập.",
        "practiceTarget": {"type": "part", "val": "VOCABULARY"}
    },
    {
        "id": "vocab_2",
        "category": "vocab",
        "categoryName": "Từ Vựng & Cụm Cố Định",
        "icon": "📌",
        "badge": "CỤM TỪ ĂN ĐIỂM",
        "badgeColor": "emerald",
        "title": "14. Cụm Động Từ & Thành Ngữ 'Tủ' Trong Đề Thi AVCD6",
        "signal": "Các cụm từ đi liền không thể tách rời xuất hiện lặp đi lặp lại trong cả 5 đề.",
        "formula": "• <strong>take part in</strong> = participate in (tham gia)<br>• <strong>take advantage of</strong> = tận dụng, lợi dụng lợi thế<br>• <strong>take responsibility for</strong> = chịu trách nhiệm cho<br>• <strong>keep in touch with</strong> = giữ liên lạc với ai<br>• <strong>catch up with</strong> = theo kịp, bắt kịp ai<br>• <strong>pay attention to</strong> = chú ý lắng nghe, để tâm đến<br>• <strong>look forward to + V-ing</strong> = rất mong đợi, trông ngóng<br>• <strong>run out of</strong> = cạn kiệt, hết sạch (run out of fuel / time)",
        "trap": "⚠️ Sau <em>look forward to</em> bắt buộc là <strong>V-ING</strong> (hoặc danh từ), không dùng V-nguyên mẫu!",
        "example": "We are looking forward to <u>hearing</u> from you soon.",
        "exampleTrans": "Chúng tôi rất mong sớm nhận được phản hồi từ bạn.",
        "practiceTarget": {"type": "part", "val": "VOCABULARY"}
    },
    {
        "id": "vocab_3",
        "category": "vocab",
        "categoryName": "Từ Vựng & Cụm Cố Định",
        "icon": "🎯",
        "badge": "TÍNH TỪ + GIỚI TỪ",
        "badgeColor": "emerald",
        "title": "15. Trọn Bộ Tính Từ Đi Kèm Giới Từ Cố Định",
        "signal": "Nhìn ngay giới từ đứng sau chỗ trống để chọn tính từ đúng:",
        "formula": "• <strong>IN:</strong> interested <em>in</em> (thích), succeed <em>in</em> (thành công)<br>• <strong>OF:</strong> proud <em>of</em> (tự hào), fond <em>of</em> (thích), afraid <em>of</em> (sợ), aware <em>of</em> (nhận thức), capable <em>of</em> (có khả năng)<br>• <strong>AT:</strong> good <em>at</em> (giỏi về), bad <em>at</em> (dở về), surprised <em>at</em> (ngạc nhiên)<br>• <strong>FOR:</strong> famous <em>for</em> (nổi tiếng vì), responsible <em>for</em> (chịu trách nhiệm), late <em>for</em> (trễ)<br>• <strong>WITH:</strong> satisfied <em>with</em> (hài lòng), crowded <em>with</em> (đông đúc), familiar <em>with</em> (quen thuộc)",
        "trap": "⚠️ Nhớ: Giỏi môn gì là <em>good AT</em>, KHÔNG dùng <em>good in</em>!",
        "example": "The city is famous <u>for</u> its historical monuments and delicious local food.",
        "exampleTrans": "Thành phố này nổi tiếng nhờ các di tích lịch sử và ẩm thực địa phương thơm ngon.",
        "practiceTarget": {"type": "part", "val": "VOCABULARY"}
    },

    # ==================== ĐIỀN TỪ ĐOẠN VĂN ====================
    {
        "id": "cloze_1",
        "category": "cloze",
        "categoryName": "Điền Từ Đoạn Văn",
        "icon": "🧩",
        "badge": "KỸ THUẬT QUAN SÁT",
        "badgeColor": "rose",
        "title": "16. Kỹ Thuật 'Nhìn Trước Ngó Sau' Xác Định Loại Từ",
        "signal": "Vị trí của chỗ trống trong câu đoạn văn.",
        "formula": "• <strong>Trước là a/an/the, my/his, giới từ (of, in)</strong> → Chỗ trống cần <strong>DANH TỪ</strong> (hoặc cụm Tính từ + Danh từ).<br>• <strong>Trước Danh từ</strong> → Cần <strong>TÍNH TỪ</strong> để bổ nghĩa cho danh từ đó.<br>• <strong>Đứng đầu câu trước dấu phẩy (..., S + V)</strong> hoặc sau trợ động từ trước V chính → Cần <strong>TRẠNG TỪ</strong> (thường có đuôi <em>-ly</em>).<br>• <strong>Sau To-be hoặc Linking verbs (feel, seem, look, become)</strong> → Cần <strong>TÍNH TỪ</strong> (VD: <em>It becomes important...</em>).",
        "trap": "⚠️ Đọc kỹ từ ngay trước và ngay sau chỗ trống, không cần mất thời gian dịch cả đoạn dài!",
        "example": "Pollution is having a serious <u>impact</u> (danh từ) on marine life.",
        "exampleTrans": "Sự ô nhiễm đang gây ra tác động nghiêm trọng lên đời sống sinh vật biển.",
        "practiceTarget": {"type": "part", "val": "CLOZE"}
    },
    {
        "id": "cloze_2",
        "category": "cloze",
        "categoryName": "Điền Từ Đoạn Văn",
        "icon": "🔀",
        "badge": "BỘ TỨ LIÊN TỪ",
        "badgeColor": "rose",
        "title": "17. Phân Biệt Các Liên Từ Chuyển Ý Trong Đoạn Văn",
        "signal": "Đoạn văn nối 2 ý có quan hệ tương phản, nguyên nhân hoặc kết quả.",
        "formula": "• <strong>TƯƠNG PHẢN (Nhưng / Mặc dù):</strong><br>&nbsp;&nbsp;• <em>However, ...</em> (Tuy nhiên - đứng đầu câu, sau có dấu phẩy)<br>&nbsp;&nbsp;• <em>Although / Even though + S + V</em> (Mặc dù)<br>&nbsp;&nbsp;• <em>In spite of / Despite + Noun / V-ing</em><br>• <strong>NGUYÊN NHÂN (Bởi vì):</strong><br>&nbsp;&nbsp;• <em>Because / Since / As + S + V</em><br>&nbsp;&nbsp;• <em>Because of / Due to + Noun phrase</em><br>• <strong>KẾT QUẢ (Do đó / Vì vậy):</strong><br>&nbsp;&nbsp;• <em>Therefore, ... / As a result, ...</em> (Do đó - có dấu phẩy)<br>&nbsp;&nbsp;• <em>So + S + V</em><br>• <strong>BỔ SUNG (Hơn nữa):</strong><br>&nbsp;&nbsp;• <em>Moreover, ... / In addition, ... / Furthermore, ...</em>",
        "trap": "⚠️ Nhìn dấu câu: Thấy chỗ trống đứng đầu câu có dấu phẩy ngay sau (VD: <em>[___], he passed the exam</em>) → Thường là <strong>However</strong> hoặc <strong>Therefore</strong>, KHÔNG THỂ là <em>Although</em> hay <em>Because</em>!",
        "example": "The team worked tirelessly; <u>however</u>, they couldn't meet the tight deadline.",
        "exampleTrans": "Cả đội đã làm việc không ngừng nghỉ; tuy nhiên, họ đã không thể kịp thời hạn gấp gáp.",
        "practiceTarget": {"type": "part", "val": "CLOZE"}
    },

    # ==================== ĐỌC HIỂU ====================
    {
        "id": "read_1",
        "category": "read",
        "categoryName": "Đọc Hiểu (Reading)",
        "icon": "🔍",
        "badge": "KỸ THUẬT SCANNING",
        "badgeColor": "cyan",
        "title": "18. Tuyệt Chiêu Quét Từ Khóa (Scan Keyword) Không Cần Dịch Hết",
        "signal": "Các câu hỏi chi tiết về ai, cái gì, ở đâu, khi nào (What, Where, When, Who).",
        "formula": "① <strong>Đọc câu hỏi trước:</strong> Gạch chân từ khóa đặc biệt (Tên riêng viết hoa, số liệu, năm tháng, thuật ngữ).<br>② <strong>Quét mắt nhanh lên bài:</strong> Tìm đúng vị trí xuất hiện của từ khóa đó.<br>③ <strong>Đọc kỹ 1 câu trước & 1 câu sau:</strong> Đáp án nằm ngay tại đó, thường được paraphrase (dùng từ đồng nghĩa) so với bài đọc.",
        "trap": "⚠️ Đừng bao giờ ngồi đọc và dịch từng từ từ đầu bài đến cuối bài — vừa tốn thời gian vừa dễ bị rối!",
        "example": "Câu hỏi: \"What happened in <u>1969</u>?\" → Quét ngay con số 1969 trong bài để tìm câu trả lời.",
        "exampleTrans": "Tìm trực tiếp con số hoặc từ in hoa để định vị đáp án trong vòng 5 giây.",
        "practiceTarget": {"type": "part", "val": "READING"}
    },
    {
        "id": "read_2",
        "category": "read",
        "categoryName": "Đọc Hiểu (Reading)",
        "icon": "👑",
        "badge": "Ý CHÍNH & TIÊU ĐỀ",
        "badgeColor": "cyan",
        "title": "19. Mẹo Làm Câu Ý Chính (Main Idea / Best Title)",
        "signal": "Câu hỏi: <em>What is the main idea of the passage? / What is the best title for this passage?</em>",
        "formula": "• <strong>LUÔN LÀM CÂU NÀY SAU CÙNG:</strong> Sau khi đã làm hết các câu chi tiết, bạn đã hiểu 70-80% nội dung bài rồi, làm câu này cực nhanh!<br>• <strong>VỊ TRÍ VÀNG:</strong> Đọc kỹ <strong>1-2 câu đầu đoạn 1</strong> và <strong>câu kết luận cuối bài</strong>. 90% ý chính nằm ở đây.<br>• <strong>LOẠI TRỪ:</strong> Loại ngay đáp án quá hẹp (chỉ nói về 1 chi tiết nhỏ) hoặc quá rộng (vượt ra ngoài phạm vi bài đọc).",
        "trap": "⚠️ Đáp án đúng thường mang tính khái quát cao và bao trùm được toàn bộ các đoạn trong bài.",
        "example": "Đoạn đầu nói về tác hại rác thải nhựa, đoạn cuối kêu gọi tái chế → Tiêu đề phải là: \"Solutions to Plastic Pollution\".",
        "exampleTrans": "Ý chính luôn bao quát toàn bộ bài, không chọn đáp án chỉ nói về 1 đoạn đơn lẻ.",
        "practiceTarget": {"type": "part", "val": "READING"}
    },
    {
        "id": "read_3",
        "category": "read",
        "categoryName": "Đọc Hiểu (Reading)",
        "icon": "❌",
        "badge": "NOT TRUE / EXCEPT",
        "badgeColor": "cyan",
        "title": "20. Mẹo Xử Lý Câu Hỏi 'NOT true / EXCEPT' (Tìm Ý Sai)",
        "signal": "Câu hỏi có chữ in hoa: <em>Which of the following is NOT true? / All of the following are mentioned EXCEPT...?</em>",
        "formula": "• Đọc lướt 4 lựa chọn A, B, C, D.<br>• Đối chiếu từng lựa chọn lên bài đọc:<br>&nbsp;&nbsp;👉 3 lựa chọn nào có thông tin đúng trong bài → <strong>GẠCH BỎ (LOẠI)</strong>.<br>&nbsp;&nbsp;👉 Lựa chọn nào mang thông tin <strong>TRÁI NGƯỢC</strong> hoặc bài <strong>HOÀN TOÀN KHÔNG NHẮC ĐẾN</strong> → <strong>CHỌN NGAY ĐÁP ÁN ĐÓ</strong>!",
        "trap": "⚠️ Đề thi thường hay bẫy bằng cách đổi <em>always</em> thành <em>sometimes</em>, hoặc đổi số liệu để làm câu đó bị sai sự thật.",
        "example": "Bài đọc: \"Students can borrow up to 3 books.\" → Lựa chọn nói: \"Students can borrow unlimited books\" là SAI sự thật → Chọn lựa chọn này!",
        "exampleTrans": "3 câu đúng trong bài thì gạch bỏ, câu nào sai sự thật hoặc không nhắc tới là đáp án cần chọn.",
        "practiceTarget": {"type": "part", "val": "READING"}
    },
    {
        "id": "read_4",
        "category": "read",
        "categoryName": "Đọc Hiểu (Reading)",
        "icon": "👉",
        "badge": "ĐẠI TỪ THAM CHIẾU",
        "badgeColor": "cyan",
        "title": "21. Mẹo Câu Hỏi Đại Từ Thay Thế ('it / they' refers to...)",
        "signal": "Câu hỏi: <em>The word 'it' / 'they' / 'them' in paragraph 2 refers to...</em>",
        "formula": "• <strong>QUY TẮC NHÌN NGƯỢC VỀ PHÍA TRƯỚC:</strong> Đại từ luôn thay thế cho danh từ đứng <u>NGAY TRƯỚC NÓ</u> (ở câu trước hoặc vế trước).<br>• Nếu từ được hỏi là <strong>IT</strong> → Tìm danh từ <strong>số ít</strong> hoặc <strong>đồ vật / sự việc</strong> đứng gần nhất phía trước.<br>• Nếu từ được hỏi là <strong>THEY / THEM</strong> → Tìm danh từ <strong>số nhiều</strong> (thường có đuôi <em>-s / -es</em>) đứng gần nhất phía trước.",
        "trap": "⚠️ Đừng nhìn về phía sau! Thay thế danh từ tìm được vào chỗ của đại từ xem câu có xuôi nghĩa không.",
        "example": "Solar panels absorb sunlight. <u>They</u> convert it into electricity. → \"They\" refers to: <em>Solar panels</em> (số nhiều).",
        "exampleTrans": "Nhìn ngay danh từ số nhiều đứng ở câu phía trước để chọn.",
        "practiceTarget": {"type": "part", "val": "READING"}
    }
]

tips_data_str = json.dumps(tips_catalog, ensure_ascii=False)

print(f"Loaded {len(questions)} questions and {len(tips_catalog)} comprehensive tips.")
