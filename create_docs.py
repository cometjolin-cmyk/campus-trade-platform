import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout_box(doc, title, content_lines, border_color="1E3A8A", bg_color="F8FAFC"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left thick border
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📌 {title}")
    run_t.bold = True
    run_t.font.size = Pt(11)
    run_t.font.color.rgb = RGBColor(30, 58, 138)
    
    for line in content_lines:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        run_c = p2.add_run(line)
        run_c.font.size = Pt(10)
        run_c.font.color.rgb = RGBColor(55, 65, 81)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, header_bg="1E3A8A"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        is_header = (i == 0)
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        for j, cell in enumerate(row.cells):
            cell.width = col_widths[j]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            
            # Subtle cell borders
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
                f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
                f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
                f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)
            
            if is_header:
                set_cell_background(cell, header_bg)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(10)
                        r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                else:
                    set_cell_background(cell, "F9FAFB")
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(31, 41, 55)

def build_reflection_document(output_path):
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69) # A4
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("全國大學生二手物品交換與買賣平台 · AI 協作反思報告")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(156, 163, 175)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("— 專題成果繳交文件 · 第 PAGE 頁 —")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(156, 163, 175)

    # Document Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Microsoft JhengHei'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(31, 41, 55)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(6)

    # ------------------ Header & Title Block ------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    title_run = title_p.add_run("全國大學生二手物品交換與買賣平台")
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(30, 58, 138) # Dark Navy

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    sub_run = sub_p.add_run("AI 協作反思與軟體工程實踐報告 (AI Collaboration Reflection)")
    sub_run.font.size = Pt(14)
    sub_run.font.bold = True
    sub_run.font.color.rgb = RGBColor(217, 119, 6) # Amber

    # Metadata Panel
    meta_table = doc.add_table(rows=1, cols=1)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(6.5)
    m_cell = meta_table.cell(0, 0)
    set_cell_background(m_cell, "F1F5F9")
    set_cell_margins(m_cell, top=100, bottom=100, left=140, right=140)
    mp = m_cell.paragraphs[0]
    mp.paragraph_format.space_before = Pt(0)
    mp.paragraph_format.space_after = Pt(0)
    m_run = mp.add_run(
        "【專案性質】大專院校課堂專題成果繳交檔　|　【協作模式】Human-AI Pair Programming (人機結對敏捷開發)\n"
        "【架構核心】Python Flask + SQLite + Vercel Serverless + Neubrutalism 漫畫風 UI\n"
        "【驗證指標】50 筆真實校園種子資料、28 項 Unit/E2E 自動化測試 100% 通過"
    )
    m_run.font.size = Pt(9.5)
    m_run.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ------------------ Section 1: Prompt Evolution ------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    r1 = h1.add_run("一、AI 協作使用的核心提示詞演化歷程 (Prompt Engineering Evolution)")
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(30, 58, 138)

    p_intro = doc.add_paragraph(
        "在整個專案開發生命週期中，我們徹底摒棄了單向模糊的詢問指令，改採「目標導向、規格邊界約束、結構化驗收」的系統性提示詞工程策略。"
        "團隊將提示詞依據軟體工程生命週期劃分為五大演進階段，每一次提示詞迭代皆精確推動架構與功能的躍升："
    )

    # Prompt Evolution Table
    prompt_table = doc.add_table(rows=5, cols=4)
    headers = ["演化階段", "核心提示詞 (Prompt 策略)", "設計意圖與約束條件", "AI 產出與工程價值"]
    for j, h in enumerate(headers):
        prompt_table.cell(0, j).paragraphs[0].text = h
        
    p_data = [
        ("階段 1：規格拆解", "「根據兩份教材 PDF，嚴格拆解入門 1-10、中階 11-20 與 4 大 AI 功能清單，以輕量級全端架構實作。」", "要求 AI 以系統工程維度定義 24 項規格，而非直接寫代碼。", "產出 PRD.md、資料庫 9 張關聯表 Schema 與 RESTful API 藍圖。"),
        ("階段 2：UIUX 升級", "「請更改 UIUX 我希望整個是漫畫風格，遵循 ui-ux-pro-max 規範，使用粗墨線、硬陰影與波普配色。」", "打破千篇一律的呆板模板，鎖定大學生喜好營造冒險沉浸感。", "建立 Comic Neubrutalism 設計系統，實作對話氣泡與顏文字空狀態。"),
        ("階段 3：相片與 AI", "「照片應該可以直接從電腦選取，AI 是要自動辨識品項名稱，生成 50 筆真實測試資料證明規格正確。」", "從靜態預設範本升級為真實本機照片選取，並建立強固測試驗證集。", "實作 FileReader 本機預覽、AI 視覺多模態語意辨識與 50 筆種子資料庫。"),
        ("階段 4：雲端適配", "「我想用 Vercel 部署請幫我或告訴我怎麼做，出現 404 Not Found 該如何解決？」", "針對 Vercel Serverless 與唯讀 Lambda 容器環境進行生產級除錯。", "建立 api/index.py、修正 vercel.json 轉發，並在 database.py 實作 /tmp 冷啟動同步。")
    ]
    for i, row in enumerate(p_data, start=1):
        for j, val in enumerate(row):
            prompt_table.cell(i, j).paragraphs[0].text = val

    format_table(prompt_table, [Inches(1.2), Inches(2.2), Inches(1.5), Inches(1.6)], header_bg="1E3A8A")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Deep dive into prompt strategy
    add_callout_box(doc, "關鍵提示詞工程心得：高階提示詞三要素", [
        "1. Context (明確情境)：提供技術棧約束（Flask+SQLite）、目標使用者（大專院校學生）與風格準則（ui-ux-pro-max）。",
        "2. Constraint (嚴格約束)：明確規定防呆校驗、WCAG 2.1 AA 無障礙高對比、個資正則過濾、AI 行情標示「估算值」。",
        "3. Verification (自動化驗收)：要求 AI 同步撰寫 UnitTest 與 E2E 測試腳本，以 28 項自動化測試通過作為完成的唯一標準。"
    ], border_color="2563EB", bg_color="EFF6FF")

    # ------------------ Section 2: Obstacles & Debugging ------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    r2 = h2.add_run("二、遭遇之核心技術痛點與修正過程 (Obstacles & Debugging Journey)")
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "在敏捷協作過程中，人機結對開發展現出極高的問題診斷與修復效率。以下梳理開發過程遭遇的四大核心技術難點及其根因排查與修正軌跡："
    )

    debug_table = doc.add_table(rows=5, cols=4)
    d_headers = ["技術痛點現象", "根本原因診斷 (Root Cause)", "工程修正解決方案", "驗收與防回歸手段"]
    for j, h in enumerate(d_headers):
        debug_table.cell(0, j).paragraphs[0].text = h
        
    d_data = [
        ("macOS 5000 埠啟動衝突", "macOS Monterey 以後預設啟用 AirPlay Receiver 監聽 5000 埠，造成 Flask Address already in use。", "將本地埠統一調整為 5050，並支援動態環境變數 os.environ.get('PORT', 5050)。", "後台持續守護程序監聽 http://127.0.0.1:5050 穩定運行。"),
        ("50 筆商品擴充後搜尋斷言失敗", "擴充種子資料後，新加入的工程計算機（ID 37）在描述中提及「微積分」，依 id DESC 排在第一，舊測試只斷言第一筆品名。", "重構 test_platform.py，改為驗證全體回傳項目皆在 title 或 desc 匹配，且至少一筆品名包含微積分。", "測試強韌度提升，28 項自動化測試全數回傳 OK。"),
        ("Vercel 部署 404 Not Found", "vercel.json 轉發帶有 .py 副檔名，且內部重寫路徑為 /api/index，Flask 原先僅監聽 / 造成路由未命中。", "修正 vercel.json 為 destination: '/api/index'，在 app.py 補齊別名路由並加上 @app.errorhandler(404)。", "以 Python 模擬多路徑測試，/、/api/index、/app.py 皆 100% 回傳 200 OK。"),
        ("Vercel SQLite 唯讀限制", "Vercel 雲端 Lambda 容器根目錄為 Read-Only，SQLite 執行 INSERT 或建立 WAL 鎖定時拋出 attempt to write a readonly database。", "在 database.py 建立智慧相容層：檢測到 VERCEL 環境時，自動將 50 筆種子 DB 複製至唯道具讀寫權限的 /tmp/campus_trade.db。", "成功在 Vercel 雲端執行登入、刊登寶物與留言寫入，毫無報錯。")
    ]
    for i, row in enumerate(d_data, start=1):
        for j, val in enumerate(row):
            debug_table.cell(i, j).paragraphs[0].text = val

    format_table(debug_table, [Inches(1.4), Inches(1.8), Inches(1.8), Inches(1.5)], header_bg="0D9488")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ------------------ Section 3: Compliance & Ethics ------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)
    r3 = h3.add_run("三、教學提醒與校園安全合規落實 (Compliance & Ethics)")
    r3.font.size = Pt(14)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "依據教育部與專題教材指引，校園二手交易平台涉及學生真實隱私與金錢往來，正式公開上線前必須嚴肅處理資訊安全與倫理防護。"
        "本平台在架構層面 100% 落實了以下五大合規機制："
    )

    comp_table = doc.add_table(rows=6, cols=3)
    c_headers = ["合規檢驗項目", "平台設計與技術落實方案", "合規效益與法律防禦"]
    for j, h in enumerate(c_headers):
        comp_table.cell(0, j).paragraphs[0].text = h
        
    c_data = [
        ("1. 個資隱私防護\n(PII Protection)", "商品公開問答留言板內建正則攔截器，自動將手機號碼（09xx-xxx-xxx）與宿舍房號門牌（如「女一舍301」）屏蔽為星號（***）。", "防範學生在未達成交易前私密資訊外洩，杜絕外部爬蟲惡意抓取個資或電話騷擾。"),
        ("2. 校園身分真偽認證\n(.edu.tw Identity)", "僅允許台灣大專院校標準網域名稱後綴 .edu.tw 之信箱通過認證，通過者展示專屬「🛡️ 校園已認證勇者」防偽綠色勳章。", "阻絕校外人士冒用學生身分混入校園詐騙，顯著提升交易互信基礎。"),
        ("3. AI 估價責任聲明\n(AI Disclaimer)", "所有 AI 價格分析與建議行情區塊，均以高對比綠色標籤強制標註「【AI 估算值】僅供參考，非絕對成交保證」。", "符合消保與 AI 倫理規範，避免學生將演算法推估數值誤認為官方定價，保障買賣雙方議價自由。"),
        ("4. 交易狀態防詐鎖定\n(Trade Lock)", "買家於私訊發起出價後，賣家點擊「接受出價」，系統即自動將商品鎖定為「預約中 (Reserved)」，面交驗收後才轉為「完成」。", "杜絕一物多賣、二手搶標毀約紛爭，保障校內面交履約安全。"),
        ("5. 糾察隊管理仲裁\n(Moderation)", "建立商品檢舉機制與「糾察隊本部」管理後台，管理員可即時查閱檢舉理由，並執行「駁回檢舉」或「違規強制下架」。", "健全社群自治與爭議仲裁管道，維護校園健康純淨的交流風氣。")
    ]
    for i, row in enumerate(c_data, start=1):
        for j, val in enumerate(row):
            comp_table.cell(i, j).paragraphs[0].text = val

    format_table(comp_table, [Inches(1.5), Inches(2.7), Inches(2.3)], header_bg="B45309")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ------------------ Section 4: Learning & Takeaways ------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)
    r4 = h4.add_run("四、AI 結對編程學習心得與反思 (Key Takeaways & Reflection)")
    r4.font.size = Pt(14)
    r4.font.bold = True
    r4.font.color.rgb = RGBColor(30, 58, 138)

    takeaways = [
        ("1. 從「程式碼碼農」躍升為「系統架構設計師」：", 
         "在傳統開發中，工程師常耗費 80% 的精力在處理樣板代碼、CSS 微調與重複的 CRUD 撰寫。透過 AI 協作，人類工程師的角色轉移為『架構邊界把控、驗收規則定義與異常邊界決策』。向 AI 提問的精準度，決定了軟體系統的健壯度。"),
        
        ("2. 自動化測試是人機協作最強大的安全防線 (Safety Net)：", 
         "AI 的生成速度極快，但也容易在重構介面或增加新功能時引入非預期的回歸問題。本次專案堅持『測試驅動驗收』，編寫了 28 項自動化單元與 E2E 測試，在每次 UI 大改（升級漫畫風格）或資料庫擴充（生成 50 筆商品）時，只需 0.04 秒即可確認全功能零破壞，這是高敏捷開發的致勝關鍵。"),
         
        ("3. 現代雲端原生 (Cloud Native) 與無伺服器架構思維：", 
         "從本地 localhost 到 Vercel Serverless 的部署歷程，讓我們深切體會到本機環境與雲端微服務的鴻溝。唯讀檔案系統、無狀態函式（Stateless Function）與反向代理重寫等概念，在本次實踐中轉化為扎實的工程能力。"),

        ("4. 兼具科技溫度與人文倫理的產品思考：", 
         "AI 功能不應只是炫技，更應服務於人性需求。透過照片自動提取品名、自然語言幫新生找平價裝備，同時嚴謹標註『估算值』並在問答板中過濾隱私電話，讓平台在科技便利與道德防護之間取得了最佳平衡點。")
    ]

    for title, desc in takeaways:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(4)
        p_t.paragraph_format.space_after = Pt(2)
        r_title = p_t.add_run(title)
        r_title.bold = True
        r_title.font.size = Pt(11)
        r_title.font.color.rgb = RGBColor(30, 58, 138)
        
        p_d = doc.add_paragraph()
        p_d.paragraph_format.space_before = Pt(0)
        p_d.paragraph_format.space_after = Pt(6)
        r_desc = p_d.add_run(desc)
        r_desc.font.size = Pt(10)
        r_desc.font.color.rgb = RGBColor(55, 65, 81)

    # Sign-off box
    add_callout_box(doc, "專題結語 (Conclusion)", [
        "本專案『全國大學生二手物品交換與買賣平台 · 熱血校園漫畫版』完美達成兩份教材規格之 20 項基礎中階功能與 4 大 AI 智慧模組。",
        "藉由 Human-AI Pair Programming，我們在極短時間內完成全端架構、Neubrutalism 漫畫視覺重構、50 筆種子資料庫建立、28 項自動化測試套件，以及 Vercel 雲端正式上線，充分體現了現代化 Vibe Coding 的極致敏捷與工程嚴謹性。"
    ], border_color="059669", bg_color="ECFDF5")

    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    out_dir = "/Users/comet/.gemini/antigravity/scratch/campus_trade_platform"
    target_docx = os.path.join(out_dir, "AI協作反思報告_全國大學生二手交易平台.docx")
    build_reflection_document(target_docx)
    
    # Also save as REFLECTION.docx for easy reference
    target_docx_en = os.path.join(out_dir, "REFLECTION.docx")
    build_reflection_document(target_docx_en)
