# IBM SPSS Assistant

> **[English](#english)** · **[中文](#中文)** · **[日本語](#日本語)** · **[한국어](#한국어)** · **[Español](#español)** · **[Français](#français)** · **[Deutsch](#deutsch)** · **[Português](#português)** · **[Русский](#русский)** · **[العربية](#العربية)** · **[ภาษาไทย](#ภาษาไทย)** · **[Tiếng Việt](#tiếng-việt)** · **[हिन्दी](#हिन्दी)** · **[Türkçe](#türkçe)** · **[Italiano](#italiano)** · **[Bahasa Indonesia](#bahasa-indonesia)** · **[Bahasa Melayu](#bahasa-melayu)** · **[Polski](#polski)** · **[Nederlands](#nederlands)**

---

<a id="english"></a>
## 🇬🇧 English

**IBM SPSS Statistics Intelligent Assistant** — 6 skills based on the [Agent Skills Open Standard](https://agentskills.io), covering the entire workflow from data cleaning to paper submission. Compatible with 40+ AI agents.

> **This is an AI companion for IBM SPSS Statistics users.** You need a working IBM SPSS installation on your computer. This skill helps you use SPSS more effectively — it generates SPSS Syntax for you to run in your local SPSS, interprets your SPSS output, and writes up results for your paper. All data analysis is performed inside IBM SPSS.

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

```bash
# Claude Code
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant

# Clone for any agent
git clone https://github.com/chengamki-tech/ibm-spss-assistant.git
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
2. **You tell the skill what you need** — describe your data, your research question, or paste your SPSS output
3. **The skill generates SPSS Syntax** — copy it into your SPSS Syntax Editor and run it
4. **You paste the SPSS output back** — the skill interprets the results in plain language
5. **The skill writes up your results** — formatted for your paper (APA 7 / Chinese academic / other)

All statistical analysis is performed by your local IBM SPSS. The AI skill only assists with syntax generation, result interpretation, and report writing.

---

<a id="中文"></a>
## 🇨🇳 中文

**IBM SPSS Statistics 智能助手** — 基于 [Agent Skills 开放标准](https://agentskills.io) 的 6 个 Skill，覆盖从数据清洗到论文投稿的全流程。兼容 40+ 种 AI Agent。支持 20+ 种语言。

> **这是 IBM SPSS 的 AI 辅助工具。** 你需要在电脑上安装 IBM SPSS。这个 skill 帮你更高效地使用 SPSS — 生成 SPSS Syntax 供你在本地 SPSS 中运行，解读你的 SPSS 输出，帮你撰写论文段落。所有数据分析都在 IBM SPSS 中完成。

### 工作流程

1. **你有本地 SPSS** — Windows / macOS / Linux 版均可
2. **你告诉 skill 需要什么** — 描述数据、研究问题，或粘贴 SPSS 输出
3. **skill 生成 SPSS Syntax** — 复制到 SPSS Syntax Editor 中运行
4. **你把 SPSS 输出贴回来** — skill 用通俗语言解读结果
5. **skill 帮你写论文段落** — 按规范格式输出（APA 7 / 中文学术规范）

### 6 个 Skill

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

> **IBM SPSS Statistics の AI アシスタントツールです。** お使いのコンピュータに IBM SPSS が必要です。このスキルは SPSS をより効率的に使うための支援をします — SPSS Syntax を生成し、SPSS 出力を解釈し、論文のセクションを作成します。すべての統計分析はローカルの IBM SPSS で実行されます。

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

> **IBM SPSS Statistics의 AI 보조 도구입니다.** 컴퓨터에 IBM SPSS가 설치되어 있어야 합니다. SPSS를 더 효율적으로 사용할 수 있도록 도와줍니다 — SPSS Syntax를 생성하고, SPSS 출력을 해석하고, 논문 섹션을 작성합니다. 모든 통계 분석은 로컬 IBM SPSS에서 수행됩니다.

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

> **Outil d'assistance IA pour IBM SPSS Statistics.** Vous devez avoir IBM SPSS installé sur votre ordinateur. Cette compétence vous aide à utiliser SPSS plus efficacement — elle génère la syntaxe SPSS à exécuter dans votre SPSS local, interprète les résultats et rédige les sections de votre article.

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

> **KI-Assistent für IBM SPSS Statistics.** Sie benötigen IBM SPSS auf Ihrem Computer installiert. Dieses Skill hilft Ihnen, SPSS effektiver zu nutzen — es generiert SPSS Syntax für Ihre lokale SPSS-Installation, interpretiert die Ergebnisse und schreibt Abschnitte für Ihre Arbeit.

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

> **Ferramenta de assistência com IA para IBM SPSS Statistics.** Você precisa ter o IBM SPSS instalado em seu computador. Esta habilidade ajuda você a usar o SPSS de forma mais eficiente — gera sintaxe SPSS para executar no seu SPSS local, interpreta os resultados e redige seções do artigo.

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

> **ИИ-ассистент для IBM SPSS Statistics.** Необходимо установить IBM SPSS на вашем компьютере. Этот навык помогает эффективнее использовать SPSS — генерирует синтаксис SPSS для запуска в локальном SPSS, интерпретирует результаты и помогает написать текст статьи.

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

> **أداة مساعدة بالذكاء الاصطناعي لـ IBM SPSS Statistics.** تحتاج إلى تثبيت IBM SPSS على جهاز الكمبيوتر الخاص بك. يساعدك هذا المهارة على استخدام SPSS بشكل أكثر كفاءة — يتم إنشاء بناء جملة SPSS للتشغيل في SPSS المحلي الخاص بك، وتفسير النتائج، وكتابة أقسام البحث.

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

> **เครื่องมือช่วยเหลือด้วย AI สำหรับ IBM SPSS Statistics.** คุณจำเป็นต้องติดตั้ง IBM SPSS บนคอมพิวเตอร์ของคุณ ทักษะนี้ช่วยให้คุณใช้ SPSS ได้อย่างมีประสิทธิภาพยิ่งขึ้น — สร้าง SPSS Syntax สำหรับรันใน SPSS บนเครื่องของคุณ ตีความผลลัพธ์ และเขียนส่วนบทความ

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

> **Công cụ hỗ trợ AI cho IBM SPSS Statistics.** Bạn cần cài đặt IBM SPSS trên máy tính. Kỹ năng này giúp bạn sử dụng SPSS hiệu quả hơn — tạo cú pháp SPSS để chạy trên SPSS cục bộ, diễn giải kết quả và viết các phần bài báo.

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

> **IBM SPSS Statistics के लिए AI सहायक उपकरण।** आपके कंप्यूटर पर IBM SPSS इंस्टॉल होना आवश्यक है। यह कौशल आपको SPSS को अधिक प्रभावी ढंग से उपयोग करने में मदद करता है — आपके स्थानीय SPSS में चलाने के लिए SPSS Syntax उत्पन्न करता है, परिणामों की व्याख्या करता है और पेपर लिखने में मदद करता है।

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

> **IBM SPSS Statistics için AI asistan aracı.** Bilgisayarınızda IBM SPSS kurulu olmalıdır. Bu beceri, SPSS'i daha verimli kullanmanıza yardımcı olur — yerel SPSS'inizde çalıştırmak için SPSS Sözdizimi oluşturur, sonuçları yorumlar ve makale bölümleri yazar.

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

> **Strumento di assistenza AI per IBM SPSS Statistics.** È necessario avere IBM SPSS installato sul computer. Questa competenza aiuta a usare SPSS in modo più efficiente — genera sintassi SPSS da eseguire nel SPSS locale, interpreta i risultati e redige sezioni dell'articolo.

### Installazione

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="bahasa-indonesia"></a>
## 🇮🇩 Bahasa Indonesia

**Asisten IBM SPSS Statistics** — 6 keterampilan berdasarkan [Standar Terbuka Agent Skills](https://agentskills.io). Mencakup seluruh alur kerja dari pembersihan data hingga penulisan makalah. Kompatibel dengan lebih dari 40 agen AI.

> **Alat bantu AI untuk IBM SPSS Statistics.** Anda perlu menginstal IBM SPSS di komputer Anda. Keterampilan ini membantu Anda menggunakan SPSS secara lebih efisien — menghasilkan SPSS Syntax untuk dijalankan di SPSS lokal Anda, menginterpretasi hasil, dan menulis bagian makalah.

### Instalasi

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="bahasa-melayu"></a>
## 🇲🇾 Bahasa Melayu

**Pembantu IBM SPSS Statistics** — 6 kemahiran berdasarkan [Standard Terbuka Agent Skills](https://agentskills.io). Meliputi keseluruhan aliran kerja dari pembersihan data hingga penulisan makalah. Serasi dengan lebih daripada 40 ejen AI.

> **Alat bantuan AI untuk IBM SPSS Statistics.** Anda perlu memasang IBM SPSS di komputer anda. Kemahiran ini membantu anda menggunakan SPSS dengan lebih cekap — menjana SPSS Syntax untuk dijalankan dalam SPSS tempatan anda, mentafsirkan hasil, dan menulis bahagian makalah.

### Pemasangan

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="polski"></a>
## 🇵🇱 Polski

**Asystent IBM SPSS Statistics** — 6 umiejętności opartych na [Otwartym Standardzie Agent Skills](https://agentskills.io). Obejmuje cały przepływ pracy od czyszczenia danych po pisanie artykułów. Kompatybilny z ponad 40 agentami AI.

> **Narzędzie wspomagane AI dla IBM SPSS Statistics.** Wymagany zainstalowany IBM SPSS na komputerze. To umiejętności pomaga efektywniej korzystać z SPSS — generuje składnię SPSS do uruchomienia w lokalnym SPSS, interpretuje wyniki i pomaga pisać sekcje artykułu.

### Instalacja

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

---

<a id="nederlands"></a>
## 🇳🇱 Nederlands

**IBM SPSS Statistics Assistent** — 6 vaardigheden gebaseerd op de [Agent Skills Open Standaard](https://agentskills.io). Dekkt de volledige workflow van gegevensopruiming tot artikelpublicatie. Compatibel met meer dan 40 AI-agenten.

> **AI-hulpmiddel voor IBM SPSS Statistics.** U heeft IBM SPSS op uw computer geïnstalleerd nodig. Dit skill helpt u SPSS efficiënter te gebruiken — genereert SPSS Syntax om uit te voeren in uw lokale SPSS, interpreteert de resultaten en helpt secties van het artikel te schrijven.

### Installatie

```bash
claude --plugin-dir https://github.com/chengamki-tech/ibm-spss-assistant
```

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

- **Standard**: [Agent Skills Open Standard](https://agentskills.io/specification)
- **Compatible agents**: Claude Code, OpenAI Codex, Gemini CLI, Cursor, VS Code, GitHub Copilot, JetBrains Junie, Roo Code, Goose, OpenHands, Amp, Databricks, Snowflake, OpenCode, and 40+ more
- **Language**: Auto-detects user language, responds in the same language (20+ languages supported)
- **Requirements**: IBM SPSS Statistics installed locally (v24+ recommended). No other dependencies, no network requests.
- **License**: MIT

## License

[MIT License](LICENSE)
