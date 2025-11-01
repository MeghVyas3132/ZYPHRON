# Zyphron - Frequently Asked Questions

## General Questions

### What is Zyphron?
Zyphron is a production-ready deployment platform that enables users to deploy any type of repository (frontend, backend, full-stack, databases) with a single click. It automatically detects technologies, manages infrastructure, and provides comprehensive DevOps/SRE monitoring and control.

### How is it different from Vercel/Heroku/Railway?
- **Multi-language support**: Supports any language and framework
- **Full-stack deployments**: Frontend + Backend + Database in one
- **Self-hosted capable**: Deploy on your own infrastructure
- **No vendor lock-in**: Use standard Docker and Nginx
- **DevOps-oriented**: Built for SRE professionals
- **Transparent orchestration**: See what's happening under the hood

### Who should use Zyphron?
- Developers wanting simple deployments
- DevOps/SRE professionals learning infrastructure
- Teams wanting full control over infrastructure
- Organizations with specific compliance needs
- Startups wanting to reduce DevOps overhead

## Technical Questions

### What languages does Zyphron support?
- **Frontend**: React, Vue, Angular, Next.js, Svelte, etc.
- **Backend**: Python (FastAPI, Django), Node.js (Express, NestJS), Go, Rust, Java, PHP, etc.
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, SQLite, etc.

### How does the environment variable detection work?
The platform scans your repository for patterns like:
- `process.env.VARIABLE` (JavaScript)
- `os.getenv('VARIABLE')` (Python)
- Environment configuration files
- Docker env sections

When deployment starts, users are prompted to provide values for detected variables.

### Can I use my own Dockerfile?
Yes! If you have a custom Dockerfile in your repository, Zyphron will use it. Otherwise, it generates one based on detected technologies.

### How do subdomains work?
- Each deployment gets a unique subdomain: `project-name.zyphron.space`
- If taken, system suggests alternatives (project-name1, project-name-app, etc.)
- SSL certificates are auto-provisioned via Let's Encrypt
- Custom domains supported in future versions

### What happens if my container crashes?
Zyphron automatically:
1. Detects the crash (health check failure)
2. Logs the error
3. Attempts to restart the container
4. If still failing, initiates rollback to previous working version
5. Notifies you immediately

## Deployment Questions

### How long does a deployment take?
Typical deployment timeline:
- Detection: 30 seconds
- Building: 1-3 minutes (depends on size)
- Testing: 30 seconds - 1 minute
- Deployment: 30 seconds
- **Total**: 2-5 minutes

### Can I deploy multiple services together?
Yes! For full-stack apps:
- Upload your monorepo or connect multiple repos
- System detects frontend, backend, database
- Creates separate containers for each
- Connects them via Docker networking
- Accessible via single subdomain

### What if my build fails?
The system provides:
- Detailed build logs
- Error messages
- Suggestions for fixes
- Rollback to previous working version
- Support documentation links

### How do I add environment variables?
1. **Automatic Detection**: System detects required variables
2. **Manual Addition**: Add via dashboard
3. **Upload .env**: Upload environment file (encrypted)
4. **Git Secret Management**: Support for GitHub Secrets (future)

### Can I have multiple versions deployed?
Not simultaneously, but:
- Every deployment is versioned
- Instant rollback to previous versions
- Blue-green deployments (future feature)
- Canary deployments (future feature)

## Monitoring Questions

### What monitoring is included?
- 24/7 health checks (every 30 seconds)
- Uptime percentage tracking
- Response time monitoring
- Container resource usage (CPU, Memory)
- Error rate tracking
- Deployment logs and metrics

### How do I know if something goes wrong?
Real-time notifications via:
- Dashboard alerts
- Email notifications
- Slack integration (future)
- SMS alerts (future)
- Webhook notifications (future)

### Can I set up custom alerts?
Currently: Manual checking
Future: Custom alert rules for specific metrics

### What's the uptime SLA?
- MVP: 99% uptime guarantee
- Production: 99.9% uptime guarantee
- Enterprise: 99.99% uptime guarantee

## Cost & Scaling Questions

### Is Zyphron free?
MVP phase: Free with usage limits
- 2 free deployments
- 1GB storage per deployment
- Basic monitoring

Future pricing:
- **Hobby**: Free (2 deployments)
- **Pro**: $29/month (unlimited deployments, advanced monitoring)
- **Enterprise**: Custom pricing

### How much will my deployment cost?
Costs depend on:
1. **Compute**: $0.02-0.05 per deployed hour
2. **Storage**: $0.10 per GB/month
3. **Bandwidth**: $0.01 per GB transferred
4. **Monitoring**: Included in deployment cost

Example: $5-15/month for typical app

### Can I deploy to my own infrastructure?
Yes! Options:
1. **Self-hosted**: Run Zyphron on your own server
2. **Private cloud**: Deploy to AWS/GCP/Azure
3. **Hybrid**: Mix of public and private

### What happens when I scale to many deployments?
System automatically:
- Increases container resources
- Optimizes database queries
- Enables caching
- Balances load across servers
- Scales to multi-region (future)

## Security Questions

### Is my code safe?
Yes:
- Encrypted transmission (HTTPS/TLS)
- Encrypted storage at rest
- Non-root container execution
- Network isolation between deployments
- Regular security audits

### How are environment variables stored?
- Encrypted in database (AES-256)
- Accessible only to deployment owner
- No plaintext storage
- Audit logs for all access
- Automatic rotation (future)

### Can I use private repositories?
Yes:
- GitHub/GitLab personal access tokens
- SSH key support
- OAuth2 integration (future)
- Private container registry support

### What about compliance?
- GDPR compliant (future certification)
- SOC 2 compliance (future)
- Audit logging available
- Data retention policies configurable

## Support Questions

### How do I get help?
- Documentation: docs.zyphron.space
- Community Forum: forum.zyphron.space
- Email Support: support@zyphron.space
- GitHub Issues: github.com/zyphron/zyphron

### What's the response time for support?
- MVP: Best effort
- Pro: < 24 hours
- Enterprise: < 2 hours (future)

### Is there a community?
Yes! Join us:
- GitHub Discussions
- Discord Server
- Slack Community
- Weekly community calls

## Troubleshooting

### "Subdomain already taken" error
- Try alternative: project-1, project-app, project-dev
- Check availability before creating deployment
- Contact support if it's your project

### "Build failed" error
- Check build logs for details
- Ensure all dependencies listed in package.json/requirements.txt
- Verify Dockerfile (if using custom)
- Check repository permissions

### "Container won't start" error
- Review application startup logs
- Check environment variables are correct
- Verify port is exposed correctly
- Check application doesn't crash immediately

### "Low uptime" alerts
- Check error logs in monitoring dashboard
- Review container resource usage
- Check if deployment is getting too much traffic
- Consider scaling or optimizing code

## Advanced Questions

### Can I use Docker Compose?
Not yet - but planned for Phase 2. Currently:
- Upload docker-compose.yml
- System converts to individual containers
- Creates networking automatically

### Can I use private dependencies?
Yes:
- Add SSH keys for private repos
- Use build args for credentials (careful!)
- Support for private package registries (future)

### Can I customize Nginx configuration?
Advanced: Yes
- Edit Nginx template in dashboard
- Create custom configuration
- Requires manual setup currently

### How do I integrate CI/CD?
Options:
1. **Webhook**: Push to GitHub → Auto-deploy
2. **Manual**: Use CLI or dashboard
3. **API**: Use REST API for custom pipelines

### Can I deploy to multiple regions?
Currently: Single region
Future: Multi-region deployments with:
- Geo-routing
- Regional failover
- Multi-cloud support

---

## Still have questions?

- Check documentation: https://docs.zyphron.space
- Ask in community: https://forum.zyphron.space
- Email us: support@zyphron.space
- Create GitHub issue: https://github.com/zyphron/zyphron/issues
