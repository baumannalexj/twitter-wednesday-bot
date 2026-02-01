# Twitter Client

## Twitter API Free Tier Rate Limits

| Tier | Monthly Price | Monthly Post Limit | Monthly Read Limit |
|------|--------------|-------------------|-------------------|
| Free | $0 | 500 writes/month | 100 reads/month |

### Implications for this bot

- **Cron handler** (`post-about-wednesday`): Runs once daily = ~30 writes/month. Well within limits.
- **Listener handler** (`reply-to-wednesday-hashtags`): Runs every 3 minutes = ~14,400 reads/month. Far exceeds the 100 reads/month limit, causing 429 (Too Many Requests) errors.
