# IBM SPSS Assistant

> **[English](#english)** · **[中文](#中文)** · **[日本語](#日本語)** · **[한국어](#한국어)** · **[Español](#español)** · **[Français](#français)** · **[Deutsch](#deutsch)** · **[Português](#português)** · **[Русский](#русский)** · **[العربية](#العربية)** · **[ภาษาไทย](#ภาษาไทย)** · **[Tiếng Việt](#tiếng-việt)** · **[हिन्दी](#हिन्दी)** · **[Türkçe](#türkçe)** · **[Italiano](#italiano)** · **[Bahasa Indonesia](#bahasa-indonesia)** · **[Bahasa Melayu](#bahasa-melayu)** · **[Polski](#polski)** · **[Nederlands](#nederlands)**

---

<a id="english"></a>
## 🇬🇧 English

**IBM SPSS Statistics Intelligent Assistant** — 6 skills based on the [Agent Skills Open Standard](https://agentskills.io), covering the entire workflow from data cleaning to paper submission. Compatible with 40+ AI agents. **Now with MCP Server for automated SPSS execution (Max Mode).**

> **IBM SPSS does ALL the computation.** This project is an AI interface to your local IBM SPSS — it sends SPSS Syntax to your SPSS, IBM SPSS executes the analysis, and the AI reads the output to help you understand it. The AI never performs any statistical calculation itself. Every number, every p-value, every test statistic comes from IBM SPSS.

> **Two modes**: **Skill mode** (any AI agent — generates SPSS Syntax for you to run in SPSS) · **MCP mode** (directly sends syntax to your local IBM SPSS — SPSS executes, AI reads output)

> **IBM SPSS performs ALL computation.** This tool is an AI interface to your local IBM SPSS — it generates SPSS Syntax, sends it to your IBM SPSS, and reads the output. The AI never calculates any statistic. Every result comes from IBM SPSS.

### Skills

| Skill | Purpose | What it does |
|-------|---------|-------------|
| `/spss-interpreter` | **Result Interpretation** | Paste SPSS output → explain every indicator in plain language |
| `/spss-what-test` | **Test Recommendation** | Describe variables & research question → recommend the right statistical method |
| `/spss-guide` | **Workflow Guide** | Step-by-step: Data Check → Descriptives → Testing → Modeling → Reporting |
| `/spss-syntax` | **Syntax Generator** | Describe analysis need → generate reproducible SPSS Syntax with comments |
| `/spss-cleaning` | **Data Cleaning** | Missing values, outliers, encoding checks → generate cleaning script |
| `/spss-report` | **Paper Writing** | Analysis results → publish-ready Results section + Discussion draft |

### Supported Analysis Methods

**Basic**: Descriptives, t-tests, ANOVA, Correlation, Chi-square, Non-parametric tests
**Regression**: Linear, Logistic (binary/ordinal/multinomial), Hierarchical, Stepwise, Curve Estimation
**Advanced**: MANOVA, Mediation, Moderation, Mixed/HLM Models, Survival Analysis, ROC Curve, Bootstrap
**Classification**: K-Means, Hierarchical Cluster, Discriminant Analysis, Decision Trees (CHAID/CRT), Neural Networks
**Other**: Generalized Linear Models (Poisson/NB), Correspondence Analysis, Complex Samples, Custom Tables, OMS

### Installation

**Quick start (Skill mode — works with any AI agent):**

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant

# Or clone for any agent
git clone https://github.com/chengamki-tech/ibm-spss-assistant.git
```

**Max mode (MCP Server — automated SPSS execution):**

```bash
# 1. Clone and install the MCP Server
git clone https://github.com/chengamki-tech/ibm-spss-assistant.git
cd ibm-spss-assistant/mcp-server
pip install -e .

# 2. The .mcp.json in the project enables automated execution
# 3. Open SPSS → Utilities → Install Python Plug-in (one-time setup)
# 4. Restart your AI agent → say "connect to my SPSS and run a t-test"
```

Works with: Claude Code · OpenAI Codex · Gemini CLI · Cursor · VS Code · GitHub Copilot · JetBrains Junie · Roo Code · Goose · OpenHands · Amp · and any [Agent Skills](https://agentskills.io/clients) compatible tool.

### Usage Examples

```
/spss-what-test  I have two groups (control vs treatment) and want to compare their anxiety scores. What test should I use?
/spss-interpreter Can you explain this regression output? [paste SPSS table]
/spss-syntax      Generate syntax for independent samples t-test, IV: gender (1=M 2=F), DV: motivation score
/spss-cleaning    Check my data for missing values and outliers
/spss-report      Write up these results for my paper: t(98)=3.42, p=.001, Cohen's d=0.66
```

### How it works

1. **You have IBM SPSS installed** on your computer (Windows / macOS / Linux)
2. **You tell the AI what you need** — describe your data, your research question, or paste your SPSS output
3. **The AI generates SPSS Syntax** — copy it into your SPSS Syntax Editor and run it
4. **IBM SPSS performs the analysis** — all computation happens inside SPSS, not in the AI
5. **You paste the SPSS output back** — the AI interprets the results in plain language

**Important**: The AI never calculates statistics. It only generates syntax and reads IBM SPSS output. Every result comes from IBM SPSS.

---

<a id="中文"></a>
## 🇨🇳 中文

**IBM SPSS Statistics 智能助手** — 基于 [Agent Skills 开放标准](https://agentskills.io) 的 6 个 Skill，覆盖从数据清洗到论文投稿的全流程。兼容 40+ 种 AI Agent。**支持 MCP Server 全自动执行（Max 版）**。

> **IBM SPSS 负责所有计算。** 本项目是 AI 到本地 IBM SPSS 的接口 — AI 发送 SPSS Syntax 给你的 SPSS，IBM SPSS 执行分析，AI 读取输出帮你理解。AI 本身不做任何统计计算。每一个数字、每一个 p 值、每一个检验统计量都来自 IBM SPSS。

> **两种模式**：**Skill 模式**（任何 AI Agent — 生成 SPSS Syntax 供你在 SPSS 中运行）+ **MCP 模式**（直接发送语法给本地 SPSS — SPSS 执行，AI 读取输出）

### 安装

**快速开始（Skill 模式 — 任何 AI Agent 可用）：**

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

**Max 模式（MCP Server — 自动执行 SPSS）：**

```bash
# 1. 克隆仓库并安装 MCP Server
git clone https://github.com/chengamki-tech/ibm-spss-assistant.git
cd ibm-spss-assistant/mcp-server
pip install -e .

# 2. 项目中的 .mcp.json 启用自动执行
# 3. 打开 SPSS → Utilities → Install Python Plug-in（一次性配置）
# 4. 重启 AI Agent → 说"连上我的 SPSS，做个 t 检验"
```

| Skill | 定位 | 核心功能 |
|-------|------|---------|
| `/spss-interpreter` | **结果解读** | 贴入 SPSS 输出 → 逐项解释指标含义 |
| `/spss-what-test` | **检验推荐** | 描述变量和研究问题 → 推荐最合适的统计方法 |
| `/spss-guide` | **流程向导** | 数据检查→描述统计→假设检验→建模→报告 |
| `/spss-syntax` | **语法生成** | 描述分析需求 → 生成可复现的 SPSS Syntax |
| `/spss-cleaning` | **数据清洗** | 缺失值/异常值/编码检查 → 生成清洗脚本 |
| `/spss-report` | **论文报告** | 统计结果 → 中文论文"结果"段落 + 讨论草稿 |

### 安装

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### 使用示例

```
/spss-what-test  我有两组学生（翻转课堂 vs 传统教学），想比较期末成绩，该用什么检验？
/spss-interpreter 帮我看看这个回归分析结果：[粘贴 SPSS 输出]
/spss-report     帮我把这个 t 检验结果写成论文里的结果段落：t(98)=3.42, p=.001, d=0.66
```

---

<a id="日本語"></a>
## 🇯🇵 日本語

**IBM SPSS Statistics アシスタント** — [Agent Skills 開放標準](https://agentskills.io) に基づく 6 つのスキル。データクレンジングから論文投稿までの全ワークフローをカバー。40 以上の AI エージェントに対応。

> **IBM SPSS Statistics の AI アシスタントツールです。** お使いのコンピュータに IBM SPSS が必要です。このスキルは SPSS をより効率的に使うための支援をします — SPSS Syntax を生成し、SPSS 出力を解釈し、論文のセクションを作成します。**すべての統計計算はローカルの IBM SPSS で実行されます。AI は一切の計算を行いません。**

### インストール

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### 使用例

```
/spss-what-test  2群（実験群と統制群）のテストスコアを比較したい。どの検定を使えばいい？
/spss-interpreter この回帰分析の結果を解説してください：[SPSS出力を貼り付け]
/spss-report     この t 検定の結果を論文の結果セクションに書いて：t(98)=3.42, p=.001, d=0.66
```

---

<a id="한국어"></a>
## 🇰🇷 한국어

**IBM SPSS Statistics 어시스턴트** — [Agent Skills 개방 표준](https://agentskills.io) 기반 6개 스킬. 데이터 정리부터 논문 제출까지 전체 워크플로우를 지원. 40개 이상의 AI 에이전트와 호환. 20개 이상의 언어 지원.

> **IBM SPSS Statistics의 AI 보조 도구입니다.** 컴퓨터에 IBM SPSS가 설치되어 있어야 합니다. SPSS를 더 효율적으로 사용할 수 있도록 도와줍니다 — SPSS Syntax를 생성하고, SPSS 출력을 해석하고, 논문 섹션을 작성합니다. **모든 통계 계산은 로컬 IBM SPSS에서 수행됩니다. AI는 어떠한 계산도 수행하지 않습니다.**

### 설치

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### 사용 예시

```
/spss-what-test  두 집단(실험군 vs 통제군)의 시험 점수를 비교하고 싶습니다. 어떤 검정을 사용해야 하나요?
/spss-interpreter 이 회귀분석 결과를 해석해 주세요: [SPSS 출력 붙여넣기]
```

---

<a id="español"></a>
## 🇪🇸 Español

**Asistente de IBM SPSS Statistics** — 6 habilidades basadas en el [Estándar Abierto Agent Skills](https://agentskills.io). Cubre todo el flujo de trabajo desde la limpieza de datos hasta la redacción del artículo. Compatible con más de 40 agentes de IA.

> **Herramienta de asistencia con IA para IBM SPSS Statistics.** Necesita IBM SPSS instalado en su computadora. Esta habilidad le ayuda a usar SPSS de manera más eficiente — genera sintaxis de SPSS para ejecutar en su SPSS local, interpreta los resultados y redacta secciones del artículo. Todos los análisis estadísticos se realizan dentro de IBM SPSS.

### Instalación

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### Ejemplo de uso

```
/spss-what-test  Tengo dos grupos (control vs tratamiento) y quiero comparar sus puntuaciones de ansiedad. ¿Qué prueba debo usar?
/spss-interpreter ¿Puedes explicar este resultado de regresión? [pegar tabla de SPSS]
/spss-report     Redacta estos resultados para mi artículo: t(98)=3.42, p=.001, d de Cohen=0.66
```

---

<a id="français"></a>
## 🇫🇷 Français

**Assistant IBM SPSS Statistics** — 6 compétences basées sur le [standard ouvert Agent Skills](https://agentskills.io). Couvre l'ensemble du flux de travail, du nettoyage des données à la rédaction d'articles. Compatible avec plus de 40 agents IA.

> **Outil d'assistance IA pour IBM SPSS Statistics.** Vous devez avoir IBM SPSS installé sur votre ordinateur. Cette compétence vous aide à utiliser SPSS plus efficacement — elle génère la syntaxe SPSS à exécuter dans votre SPSS local, interprète les résultats et rédige les sections de votre article. **Tous les calculs statistiques sont effectués par IBM SPSS. L'IA n'effectue aucun calcul.**

### Installation

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### Exemple d'utilisation

```
/spss-what-test  J'ai deux groupes (contrôle vs traitement) et je veux comparer leurs scores d'anxiété. Quel test dois-je utiliser ?
/spss-interpreter Peux-tu expliquer ce résultat de régression ? [coller le tableau SPSS]
```

---

<a id="deutsch"></a>
## 🇩🇪 Deutsch

**IBM SPSS Statistics Assistent** — 6 Fähigkeiten basierend auf dem [Agent Skills Open Standard](https://agentskills.io). Deckt den gesamten Workflow von der Datenbereinigung bis zur Manuskripterstellung ab. Kompatibel mit über 40 KI-Agenten.

> **KI-Assistent für IBM SPSS Statistics.** Sie benötigen IBM SPSS auf Ihrem Computer installiert. Dieses Skill hilft Ihnen, SPSS effektiver zu nutzen — es generiert SPSS Syntax für Ihre lokale SPSS-Installation, interpretiert die Ergebnisse und schreibt Abschnitte für Ihre Arbeit. **Alle statistischen Berechnungen werden von IBM SPSS durchgeführt. Die KI führt keine Berechnungen durch.**

### Installation

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### Beispiel

```
/spss-what-test  Ich habe zwei Gruppen (Kontrolle vs. Behandlung) und möchte ihre Angstwerte vergleichen. Welchen Test soll ich verwenden?
```

---

<a id="português"></a>
## 🇧🇷 Português

**Assistente IBM SPSS Statistics** — 6 habilidades baseadas no [Padrão Aberto Agent Skills](https://agentskills.io). Cobrindo todo o fluxo de trabalho, da limpeza de dados à redação do artigo. Compatível com mais de 40 agentes de IA.

> **Ferramenta de assistência com IA para IBM SPSS Statistics.** Você precisa ter o IBM SPSS instalado em seu computador. Esta habilidade ajuda você a usar o SPSS de forma mais eficiente — gera sintaxe SPSS para executar no seu SPSS local, interpreta os resultados e redige seções do artigo. **Todos os cálculos estatísticos são realizados pelo IBM SPSS. A IA não realiza nenhum cálculo.**

### Instalação

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### Exemplo

```
/spss-what-test  Tenho dois grupos (controle vs tratamento) e quero comparar seus escores de ansiedade. Que teste devo usar?
```

---

<a id="русский"></a>
## 🇷🇺 Русский

**Ассистент IBM SPSS Statistics** — 6 навыков на основе [открытого стандарта Agent Skills](https://agentskills.io). Охватывает весь рабочий процесс от очистки данных до написания статьи. Совместим с более чем 40 ИИ-агентами.

> **ИИ-ассистент для IBM SPSS Statistics.** Необходимо установить IBM SPSS на вашем компьютере. Этот навык помогает эффективнее использовать SPSS — генерирует синтаксис SPSS для запуска в локальном SPSS, интерпретирует результаты и помогает написать текст статьи. **Все статистические расчёты выполняются IBM SPSS. ИИ не производит никаких расчётов.**

### Установка

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### Пример

```
/spss-what-test  У меня две группы (контрольная и экспериментальная), и я хочу сравнить их показатели тревожности. Какой тест использовать?
```

---

<a id="العربية"></a>
## 🇸🇦 العربية

**مساعد IBM SPSS Statistics** — 6 مهارات بناءً على [المعيار المفتوح Agent Skills](https://agentskills.io). يغطي سير العمل بالكامل من تنظيف البيانات إلى كتابة البحث. متوافق مع أكثر من 40 وكيل ذكاء اصطناعي.

> **أداة مساعدة بالذكاء الاصطناعي لـ IBM SPSS Statistics.** تحتاج إلى تثبيت IBM SPSS على جهاز الكمبيوتر الخاص بك. يساعدك هذا المهارة على استخدام SPSS بشكل أكثر كفاءة — يتم إنشاء بناء جملة SPSS للتشغيل في SPSS المحلي الخاص بك، وتفسير النتائج، وكتابة أقسام البحث. **جميع العمليات الإحصائية يتم تنفيذها بواسطة IBM SPSS. لا يقوم الذكاء الاصطناعي بأي حسابات.**

### التثبيت

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### مثال

```
/spss-what-test  لدي مجموعتان (ضابطة وتجريبية) وأريد مقارنة درجات القلق. أي اختبار يجب أن أستخدم؟
```

---

<a id="ภาษาไทย"></a>
## 🇹🇭 ภาษาไทย

**ผู้ช่วย IBM SPSS Statistics** — 6 ทักษะตาม [มาตรฐานเปิด Agent Skills](https://agentskills.io) ครอบคลุมขั้นตอนการทำงานทั้งหมดตั้งแต่การล้างข้อมูลไปจนถึงการเขียนบทความ รองรับเอเจนต์ AI กว่า 40 ตัว

> **เครื่องมือช่วยเหลือด้วย AI สำหรับ IBM SPSS Statistics.** คุณจำเป็นต้องติดตั้ง IBM SPSS บนคอมพิวเตอร์ของคุณ ทักษะนี้ช่วยให้คุณใช้ SPSS ได้อย่างมีประสิทธิภาพยิ่งขึ้น — สร้าง SPSS Syntax สำหรับรันใน SPSS บนเครื่องของคุณ ตีความผลลัพธ์ และเขียนส่วนบทความ **การคำนวณทางสถิติทั้งหมดดำเนินการโดย IBM SPSS AI ไม่ทำการคำนวณใดๆ**

### การติดตั้ง

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### ตัวอย่าง

```
/spss-what-test  มีสองกลุ่ม (กลุ่มควบคุมกับกลุ่มทดลอง) อยากเปรียบเทียบคะแนนความวิตกกังวล ควรใช้การทดสอบอะไร?
```

---

<a id="tiếng-việt"></a>
## 🇻🇳 Tiếng Việt

**Trợ lý IBM SPSS Statistics** — 6 kỹ năng dựa trên [Tiêu chuẩn mở Agent Skills](https://agentskills.io). Bao gồm toàn bộ quy trình từ làm sạch dữ liệu đến viết bài báo khoa học. Tương thích với hơn 40 AI agent.

> **Công cụ hỗ trợ AI cho IBM SPSS Statistics.** Bạn cần cài đặt IBM SPSS trên máy tính. Kỹ năng này giúp bạn sử dụng SPSS hiệu quả hơn — tạo cú pháp SPSS để chạy trên SPSS cục bộ, diễn giải kết quả và viết các phần bài báo. **Tất cả các phép tính thống kê được thực hiện bởi IBM SPSS. AI không thực hiện bất kỳ phép tính nào.**

### Cài đặt

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### Ví dụ

```
/spss-what-test  Tôi có hai nhóm (kiểm chứng vs thực nghiệm) và muốn so sánh điểm lo âu. Nên dùng kiểm định nào?
```

---

<a id="हिन्दी"></a>
## 🇮🇳 हिन्दी

**IBM SPSS Statistics सहायक** — [Agent Skills खुले मानक](https://agentskills.io) पर आधारित 6 कौशल। डेटा सफाई से लेकर पेपर लेखन तक संपूर्ण वर्कफ़्लो कवर करता है। 40+ AI एजेंट्स के साथ संगत।

> **IBM SPSS Statistics के लिए AI सहायक उपकरण।** आपके कंप्यूटर पर IBM SPSS इंस्टॉल होना आवश्यक है। यह कौशल आपको SPSS को अधिक प्रभावी ढंग से उपयोग करने में मदद करता है — आपके स्थानीय SPSS में चलाने के लिए SPSS Syntax उत्पन्न करता है, परिणामों की व्याख्या करता है और पेपर लिखने में मदद करता है। **सभी सांख्यिकीय गणनाएँ IBM SPSS द्वारा की जाती हैं। AI कोई गणना नहीं करता।**

### इंस्टॉलेशन

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### उदाहरण

```
/spss-what-test  मेरे पास दो समूह हैं (नियंत्रण बनाम उपचार) और मैं उनके चिंता स्कोर की तुलना करना चाहता हूं। कौन सा परीक्षण उपयोग करना चाहिए?
```

---

<a id="türkçe"></a>
## 🇹🇷 Türkçe

**IBM SPSS Statistics Asistanı** — [Agent Skills Açık Standardı](https://agentskills.io) tabanlı 6 beceri. Veri temizliğinden makale yazımına kadar tüm iş akışını kapsar. 40'tan fazla AI ajanıyla uyumlu.

> **IBM SPSS Statistics için AI asistan aracı.** Bilgisayarınızda IBM SPSS kurulu olmalıdır. Bu beceri, SPSS'i daha verimli kullanmanıza yardımcı olur — yerel SPSS'inizde çalıştırmak için SPSS Sözdizimi oluşturur, sonuçları yorumlar ve makale bölümleri yazar. **Tüm istatistiksel hesaplamalar IBM SPSS tarafından yapılır. AI herhangi bir hesaplama yapmaz.**

### Kurulum

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

### Örnek

```
/spss-what-test  İki grubum (kontrol vs tedavi) var ve kaygı puanlarını karşılaştırmak istiyorum. Hangi testi kullanmalıyım?
```

---

<a id="italiano"></a>
## 🇮🇹 Italiano

**Assistente IBM SPSS Statistics** — 6 competenze basate sullo [Standard Aperto Agent Skills](https://agentskills.io). Copre l'intero workflow dalla pulizia dei dati alla stesura dell'articolo. Compatibile con oltre 40 agenti IA.

> **Strumento di assistenza AI per IBM SPSS Statistics.** È necessario avere IBM SPSS installato sul computer. Questa competenza aiuta a usare SPSS in modo più efficiente — genera sintassi SPSS da eseguire nel SPSS locale, interpreta i risultati e redige sezioni dell'articolo. **Tutti i calcoli statistici vengono eseguiti da IBM SPSS. L'IA non esegue alcun calcolo.**

### Installazione

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="bahasa-indonesia"></a>
## 🇮🇩 Bahasa Indonesia

**Asisten IBM SPSS Statistics** — 6 keterampilan berdasarkan [Standar Terbuka Agent Skills](https://agentskills.io). Mencakup seluruh alur kerja dari pembersihan data hingga penulisan makalah. Kompatibel dengan lebih dari 40 agen AI.

> **Alat bantu AI untuk IBM SPSS Statistics.** Anda perlu menginstal IBM SPSS di komputer Anda. Keterampilan ini membantu Anda menggunakan SPSS secara lebih efisien — menghasilkan SPSS Syntax untuk dijalankan di SPSS lokal Anda, menginterpretasi hasil, dan menulis bagian makalah. **Semua perhitungan statistik dilakukan oleh IBM SPSS. AI tidak melakukan perhitungan apapun.**

### Instalasi

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="bahasa-melayu"></a>
## 🇲🇾 Bahasa Melayu

**Pembantu IBM SPSS Statistics** — 6 kemahiran berdasarkan [Standard Terbuka Agent Skills](https://agentskills.io). Meliputi keseluruhan aliran kerja dari pembersihan data hingga penulisan makalah. Serasi dengan lebih daripada 40 ejen AI.

> **Alat bantuan AI untuk IBM SPSS Statistics.** Anda perlu memasang IBM SPSS di komputer anda. Kemahiran ini membantu anda menggunakan SPSS dengan lebih cekap — menjana SPSS Syntax untuk dijalankan dalam SPSS tempatan anda, mentafsirkan hasil, dan menulis bahagian makalah. **Semua pengiraan statistik dilakukan oleh IBM SPSS. AI tidak melakukan sebarang pengiraan.**

### Pemasangan

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="polski"></a>
## 🇵🇱 Polski

**Asystent IBM SPSS Statistics** — 6 umiejętności opartych na [Otwartym Standardzie Agent Skills](https://agentskills.io). Obejmuje cały przepływ pracy od czyszczenia danych po pisanie artykułów. Kompatybilny z ponad 40 agentami AI.

> **Narzędzie wspomagane AI dla IBM SPSS Statistics.** Wymagany zainstalowany IBM SPSS na komputerze. To umiejętności pomaga efektywniej korzystać z SPSS — generuje składnię SPSS do uruchomienia w lokalnym SPSS, interpretuje wyniki i pomaga pisać sekcje artykułu. **Wszystkie obliczenia statystyczne są wykonywane przez IBM SPSS. AI nie wykonuje żadnych obliczeń.**

### Instalacja

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="nederlands"></a>
## 🇳🇱 Nederlands

**IBM SPSS Statistics Assistent** — 6 vaardigheden gebaseerd op de [Agent Skills Open Standaard](https://agentskills.io). Dekkt de volledige workflow van gegevensopruiming tot artikelpublicatie. Compatibel met meer dan 40 AI-agenten.

> **AI-hulpmiddel voor IBM SPSS Statistics.** U heeft IBM SPSS op uw computer geïnstalleerd nodig. Dit skill helpt u SPSS efficiënter te gebruiken — genereert SPSS Syntax om uit te voeren in uw lokale SPSS, interpreteert de resultaten en helpt secties van het artikel te schrijven. **Alle statistische berekeningen worden uitgevoerd door IBM SPSS. De AI voert geen berekeningen uit.**

### Installatie

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

## MCP Server (Max Mode) — 让 IBM SPSS 直接执行

除了 Skill（手动复制粘贴语法），本项目还包含一个 **MCP Server**，可以让 AI Agent **直接把 SPSS Syntax 发送给你的本地 IBM SPSS 执行**。所有计算仍然 100% 由 IBM SPSS 完成，AI 只是自动发送语法和读取输出。

```
Skill 模式:  你 → AI 生成 Syntax → 你复制到 IBM SPSS → IBM SPSS 执行 → 你贴回输出 → AI 解读
MCP 模式:    你说需求 → AI 发送 Syntax → IBM SPSS 执行 → 输出自动返回 → AI 解读
```

两种模式下，**统计计算都完全由 IBM SPSS 执行**。区别只是谁把语法交给 SPSS。

### MCP 安装

```bash
# 1. 确保有 Python 3.9+ 和 IBM SPSS v24+
# 2. 安装 MCP Server
cd mcp-server
pip install -e .

# 3. 在 Claude Code 中配置
# 创建 .mcp.json (已包含在项目中):
{
  "mcpServers": {
    "spss": {
      "command": "python",
      "args": ["-m", "spss_mcp"]
    }
  }
}
```

### MCP 提供的 26 个工具

| 类别 | 工具 | 功能 |
|------|------|------|
| 系统 | `spss_connect` | 连接本地 SPSS |
| 数据 | `spss_open_data` | 打开 .sav / .csv / .xlsx |
| 数据 | `spss_get_variables` | 获取所有变量信息 |
| 数据 | `spss_get_summary` | 描述统计摘要 |
| 数据 | `spss_save_data` | 保存数据文件 |
| 分析 | `spss_descriptives` | 描述统计 |
| 分析 | `spss_frequency` | 频率分析 + 条形图 |
| 分析 | `spss_explore` | 探索性分析 + 正态性检验 |
| 分析 | `spss_normality` | Shapiro-Wilk / K-S 正态性检验 |
| 分析 | `spss_levenes` | Levene 方差齐性检验 |
| 分析 | `spss_ttest` | 独立样本 t 检验 |
| 分析 | `spss_ttest_paired` | 配对样本 t 检验 |
| 分析 | `spss_anova` | 单因素 ANOVA + 事后检验 |
| 分析 | `spss_correlation` | 相关分析（Pearson / Spearman） |
| 分析 | `spss_regression` | 线性回归 + VIF + 残差诊断 |
| 分析 | `spss_crosstab` | 交叉表 + 卡方检验 |
| 分析 | `spss_reliability` | Cronbach's α 信度分析 |
| 分析 | `spss_factor` | 探索性因子分析（EFA） |
| 分析 | `spss_logistic` | 逻辑回归 |
| 分析 | `spss_means_compare` | 均值比较 |
| 通用 | `spss_execute_syntax` | 执行任意 SPSS Syntax |
| 通用 | `spss_run_analysis` | 按类型执行（支持 19 种分析） |
| 导出 | `spss_export_output` | 导出 HTML / Word / PDF / PNG |
| 导出 | `spss_export_chart` | 导出图表 |

> 完整文档见 `mcp-server/README.md`

---

## Statistics Methods Covered / 统计方法覆盖

| Category | Methods |
|----------|---------|
| **Basic** | Descriptives, t-tests (1/2/paired), ANOVA (1-way/2-way/repeated), Correlation (Pearson/Spearman/Kendall), Chi-square, Fisher exact, Non-parametric (Mann-Whitney/Wilcoxon/Kruskal-Wallis/Friedman) |
| **Regression** | Linear (simple/multiple/hierarchical/stepwise), Logistic (binary/ordinal/multinomial), Curve estimation, Partial Least Squares |
| **Scale Development** | Reliability (Cronbach's α), Factor Analysis (EFA), CFA (reference to AMOS) |
| **Advanced** | MANOVA, Mediation (Baron-Kenny + Bootstrap), Moderation, Mixed/HLM Models, GLM (Poisson/NB/GEE), Survival (Kaplan-Meier/Cox), ROC Curve, Bootstrap |
| **Classification** | K-Means Cluster, Hierarchical Cluster, TwoStep Cluster, Discriminant Analysis, Decision Trees (CHAID/CRT/QUEST), Neural Networks (MLP/RBF) |
| **Other** | Correspondence Analysis, Complex Samples, Custom Tables, OMS, Multiple Imputation, Quality Control Charts, Ratio Statistics |

## References / 参考文档

| File | Content |
|------|---------|
| `test-selection-guide.md` | Statistical test selection decision tree (7 branches) |
| `interpretation-templates.md` | Result interpretation templates for 12+ analysis types |
| `paper-expressions.md` | Chinese paper statistical expression templates + Discussion |
| `questionnaire-template.md` | Questionnaire analysis standard workflow |
| `syntax-reference.md` | SPSS Syntax quick reference card |
| `advanced-analysis-guide.md` | Mediation/Moderation/MANOVA/Power/Regression diagnostics |
| `advanced-procedures.md` | 18 advanced SPSS procedures (cluster/survival/ROC/GLM/trees/NN/etc.) |
| `visualization-guide.md` | Complete chart creation guide with 20+ syntax examples |
| `error-troubleshooting.md` | SPSS common error troubleshooting manual |
| `power-analysis-sample-size.md` | Statistical power & sample size calculation guide |

## Technical / 技术规格

- **Standard**: [Agent Skills Open Standard](https://agentskills.io/specification) + MCP (Model Context Protocol)
- **Skills**: 6 universal Agent Skills (work with any compatible AI agent)
- **MCP Server**: 26 tools for direct SPSS execution (requires Python 3.9+, SPSS Python Plug-in)
- **Compatible agents**: Claude Code, OpenAI Codex, Gemini CLI, Cursor, VS Code, GitHub Copilot, JetBrains Junie, Roo Code, Goose, OpenHands, Amp, Databricks, Snowflake, OpenCode, and 40+ more
- **Language**: Auto-detects user language, responds in the same language (20+ languages supported)
- **Requirements**: IBM SPSS Statistics v24+ installed locally. MCP Server additionally requires Python 3.9+.
- **License**: MIT

## Project Structure / 项目结构

```
ibm-spss-assistant/
├── .claude-plugin/plugin.json        # Claude Code 插件清单
├── .mcp.json                          # MCP Server 配置
├── mcp-server/                        # MCP Server 源码 (Max 版)
│   ├── src/spss_mcp/
│   │   ├── server.py                  # MCP 主入口 — 26 个工具
│   │   ├── spss_engine.py             # SPSS 引擎 — 三级回退连接
│   │   └── tools/                     # 数据分析/导出工具
│   ├── pyproject.toml                 # Python 包配置
│   └── README.md                      # MCP 安装文档
├── skills/                            # 6 个通用 Skill
│   ├── spss-interpreter/ SKILL.md
│   ├── spss-what-test/   SKILL.md
│   ├── spss-guide/       SKILL.md
│   ├── spss-syntax/      SKILL.md
│   ├── spss-cleaning/    SKILL.md
│   └── spss-report/      SKILL.md
├── references/                        # 10 份参考文档
├── README.md
└── LICENSE
```
