# FB Comment Bot — Libertad Financiera Ya

Replies to Facebook page comments automatically as El Profe.

## One-Time: Facebook App Setup

1. Go to developers.facebook.com and create a new App
2. Under App Type select "Business"
3. Add product "Facebook Login for Business"
4. Under Permissions request: `pages_read_engagement`, `pages_manage_comments`
5. Go to Tools > Graph API Explorer
6. Select your app, select your page ("Libertad Financiera Ya"), click "Generate Access Token"
7. Exchange for a long-lived token (valid 60 days, can be renewed):
   ```
   GET https://graph.facebook.com/v21.0/oauth/access_token
     ?grant_type=fb_exchange_token
     &client_id=YOUR_APP_ID
     &client_secret=YOUR_APP_SECRET
     &fb_exchange_token=SHORT_LIVED_TOKEN
   ```
8. Save the long-lived token as `FB_PAGE_ACCESS_TOKEN`
9. Get your Page ID: Graph API Explorer > GET /me?fields=id,name with your page token

Note: Polling (not webhooks) does NOT require App Review.

## Railway Deploy

1. Create a new service in your existing Railway project (same project as the Telegram bot)
2. Set root directory: `bots/facebook`
3. Start command: `python fb_comment_bot.py`
4. Add environment variables:
   - `FB_PAGE_ACCESS_TOKEN` — long-lived page token from step above
   - `FB_PAGE_ID` — numeric ID of "Libertad Financiera Ya"
   - `ANTHROPIC_API_KEY` — your Anthropic key
5. Add a Railway Volume mounted at `/app/bots/facebook` so `replied_ids.json` persists across deploys

## Local Test Run

```bash
cd bots/facebook
pip install -r requirements.txt
FB_PAGE_ACCESS_TOKEN=xxx FB_PAGE_ID=yyy ANTHROPIC_API_KEY=zzz python fb_comment_bot.py
```

The bot will log "Poll cycle starting" every 5 minutes. First run fetches all recent comments and replies to any unprocessed ones.

## Rate Limits

Graph API allows 200 calls/hour per token. With 10 posts x 1 comments request each + 1 posts request = 11 calls per cycle. At 12 cycles/hour = 132 calls/hour. Well within limits.

## Renewing the Page Token

Long-lived tokens expire after ~60 days. Set a calendar reminder to renew via the exchange endpoint above. Future improvement: automate renewal.
