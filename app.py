import streamlit as st
import feedparser
import re
import time
import calendar

st.set_page_config(page_title="AI News Dashboard", page_icon="📰", layout="wide")

# カスタムCSSでシンプルなリスト型デザインを適用
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.news-list-item {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: background-color 0.2s;
    display: block;
    text-decoration: none !important;
    color: inherit !important;
}
.news-list-item:hover {
    background-color: #f8f9fa;
    border-color: #007bff;
}
.news-title {
    color: #0056b3;
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 6px;
    line-height: 1.4;
}
.news-date {
    color: #6c757d;
    font-size: 0.85rem;
    margin-bottom: 8px;
}
.news-summary {
    color: #333;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* ダークモード対応 */
@media (prefers-color-scheme: dark) {
    .news-list-item {
        background-color: #1e1e1e;
        border-color: #333;
    }
    .news-list-item:hover {
        background-color: #2a2a2a;
        border-color: #4da3ff;
    }
    .news-title {
        color: #66b2ff;
    }
    .news-summary {
        color: #cccccc;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("📰 国産 AI Tech News Dashboard")

# フィルター設定
NOISE_KEYWORDS = [
    "株", "決算", "市場", "政府", "規制", "国税", "株式", "取引", "投資",
    "stock", "shares", "market", "policy", "government", "regulation", "revenue", "earnings"
]

def is_noise(text):
    if not text:
        return False
    text_lower = text.lower()
    for kw in NOISE_KEYWORDS:
        if kw in text_lower:
            return True
    return False

# データソース定義
source_options = {
    # Google 公式系
    "Google Developers Japan": "https://developers-jp.googleblog.com/feeds/posts/default?alt=rss",
    "Google Cloud JP (Zenn)": "https://zenn.dev/p/google_cloud_jp/feed",
    
    # note 個別
    "note (akira_papa_ai)": "https://note.com/akira_papa_ai/rss",
    
    # note タグ
    "note (#生成AI)": "https://note.com/hashtag/生成AI/rss",
    "note (#LLM)": "https://note.com/hashtag/LLM/rss",
    "note (#自動化)": "https://note.com/hashtag/自動化/rss",
    "note (#AntiGravity)": "https://note.com/hashtag/AntiGravity/rss",
    "note (#AgentSkills)": "https://note.com/hashtag/AgentSkills/rss",
    "note (#OpenClaw)": "https://note.com/hashtag/OpenClaw/rss",
    
    # 技術ブログ
    "Zenn (AIトピック)": "https://zenn.dev/topics/ai/feed"
}

st.sidebar.header("⚙️ データソース選択")
selected_source = st.sidebar.selectbox("ニュース取得元", list(source_options.keys()))

st.sidebar.markdown("---")
st.sidebar.info("💡 **ノイズ除外フィルター有効**\n「株」「決算」などのビジネス・国家関連ワードを自動で非表示にしています。")

rss_url = source_options[selected_source]

st.write(f"**{selected_source}** の最新記事リスト")

with st.spinner("記事を読み込み中..."):
    feed = feedparser.parse(rss_url)
    
    if hasattr(feed, 'entries') and len(feed.entries) > 0:
        valid_entries = []
        
        for entry in feed.entries:
            title = entry.get('title', 'タイトルなし')
            summary = entry.get('summary', '')
            
            # ノイズチェック
            if is_noise(title) or is_noise(summary):
                continue
                
            # 日付でのフィルタリング（過去2ヶ月＝60日以内）
            published_parsed = entry.get('published_parsed')
            if published_parsed:
                entry_ts = calendar.timegm(published_parsed)
                now_ts = time.time()
                if (now_ts - entry_ts) > 60 * 24 * 3600:
                    continue
                
            link = entry.get('link', '#')
            published = entry.get('published', '')
            
            # 要約文のクリーニングと重複排除
            clean_summary = re.sub('<[^<]+>', '', summary).strip()
            
            # 要約がタイトルと全く同じ、もしくは冒頭が同じ場合は非表示
            if clean_summary == title or clean_summary.startswith(title[:30]):
                clean_summary = ""
                
            # 長すぎる場合はトリミング
            if len(clean_summary) > 200:
                clean_summary = clean_summary[:200] + "..."
                
            valid_entries.append({
                "title": title,
                "link": link,
                "published": published,
                "summary": clean_summary
            })
            
        if not valid_entries:
            st.warning("フィルタリングの結果、表示できる記事がありませんでした。")
        else:
            # リスト形式で表示（全体リンク化）
            for article in valid_entries:
                summary_tag = f'<div class="news-summary">{article["summary"]}</div>' if article["summary"] else ''
                
                st.markdown(f"""
                <a href="{article["link"]}" target="_blank" class="news-list-item">
                    <div class="news-title">{article['title']}</div>
                    <div class="news-date">📅 {article['published']}</div>
                    {summary_tag}
                </a>
                """, unsafe_allow_html=True)
    else:
        st.warning("記事が見つかりませんでした。別のソースをお試しください。")
