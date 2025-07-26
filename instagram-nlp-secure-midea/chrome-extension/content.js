const API_URL = "http://localhost:8000/analyze";
let commentObserver = null;

function isEmojiOnly(text) {
    const emojiRegex = /^[\p{Emoji}\s]+$/u;
    return emojiRegex.test(text);
}

function isInsideAnchorOrButton(element) {
    return (
        element.closest('a') !== null || 
        element.closest('button') !== null
    );
}

async function analyzeAndHighlight(comment, index) {
    const text = comment.textContent.trim();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const data = await response.json();
        console.log(`[DEBUG][${index}] API result:`, data);

        if (data.is_political) {
            comment.style.borderLeft = '3px solid red';
            comment.style.paddingLeft = '5px';
            comment.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
            console.log(`[✅ UNDERLINED] ${text}`);
        } else {
            console.log(`[DEBUG][${index}] ❌ Not political: "${text}"`);
        }
    } catch (error) {
        console.error(`[ERROR][${index}] API call failed:`, error);
    }
}

function processComments() {
    const comments = document.querySelectorAll(
        'div[role="dialog"] span[dir="auto"], div[role="article"] span[dir="auto"]'
    );

    console.log(`[DEBUG] Found ${comments.length} potential comment elements`);

    comments.forEach((comment, index) => {
        const text = comment.textContent.trim();

        if (
            text.length < 2 ||
            text.split(/\s+/).length < 2 ||
            isInsideAnchorOrButton(comment) ||
            isEmojiOnly(text) ||
            /^@[\w.]+$/.test(text)
        ) {
            console.log(`[DEBUG][${index}] Skipped: "${text}"`);
            return;
        }

        analyzeAndHighlight(comment, index);
    });
}

function observeWhenCommentsOpen() {
    const target = document.body;

    const sectionObserver = new MutationObserver(() => {
        const commentSection = document.querySelector('div[role="dialog"]');
        if (commentSection && !commentObserver) {
            console.log('[🎯] Comment section detected — starting observer.');

            commentObserver = new MutationObserver(() => {
                console.log('[DEBUG] DOM changed — checking comments');
                processComments();
            });

            commentObserver.observe(commentSection, {
                childList: true,
                subtree: true
            });

            processComments(); // Initial run
        }

        if (!commentSection && commentObserver) {
            console.log('[🛑] Comment section closed — stopping observer.');
            commentObserver.disconnect();
            commentObserver = null;
        }
    });

    sectionObserver.observe(target, {
        childList: true,
        subtree: true
    });
}

observeWhenCommentsOpen();
