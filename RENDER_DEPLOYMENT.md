# Deploying FastMCP Server to Render

This guide explains how to deploy your ServiceNow FastMCP server to Render.com.

## Prerequisites

- GitHub account
- Render account (free tier available at https://render.com)
- ServiceNow instance credentials
- Git installed locally

## Deployment Steps

### 1. Prepare Your Repository

First, initialize a Git repository and push your code to GitHub:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: FastMCP ServiceNow server"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/servicenow-mcp-server.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Render

#### Option A: Using render.yaml (Recommended)

1. **Sign up/Login to Render**: Go to https://render.com and sign in

2. **Create New Blueprint**:
   - Click "New +" button
   - Select "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables**:
   - In the Render dashboard, go to your service
   - Navigate to "Environment" tab
   - Add the following environment variables:
     ```
     SERVICENOW_INSTANCE=your-instance.service-now.com
     SERVICENOW_USERNAME=your-username
     SERVICENOW_PASSWORD=your-password
     ```
   - Click "Save Changes"

4. **Deploy**:
   - Render will automatically build and deploy your service
   - Wait for the deployment to complete (usually 2-5 minutes)

#### Option B: Manual Setup

1. **Create New Web Service**:
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository
   - Select the repository containing your code

2. **Configure Service**:
   - **Name**: `servicenow-mcp-server`
   - **Region**: Choose closest to you (e.g., Oregon)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python fastmcp_server_render.py`
   - **Plan**: Free (or choose paid plan for better performance)

3. **Add Environment Variables**:
   - Scroll down to "Environment Variables"
   - Add:
     ```
     SERVICENOW_INSTANCE=your-instance.service-now.com
     SERVICENOW_USERNAME=your-username
     SERVICENOW_PASSWORD=your-password
     PORT=10000
     HOST=0.0.0.0
     ```

4. **Create Web Service**:
   - Click "Create Web Service"
   - Render will start building and deploying

### 3. Verify Deployment

Once deployed, Render will provide you with a URL like:
```
https://servicenow-mcp-server.onrender.com
```

Test the deployment:

```bash
# Check health endpoint
curl https://servicenow-mcp-server.onrender.com/health

# Test with MCP client
# Update your MCP client to use the Render URL
```

### 4. Configure MCP Clients

#### For Claude Desktop

Update your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "servicenow": {
      "command": "curl",
      "args": [
        "-N",
        "https://servicenow-mcp-server.onrender.com/sse"
      ]
    }
  }
}
```

#### For Custom MCP Clients

Update the server URL in your client code:

```python
server_url = "https://servicenow-mcp-server.onrender.com"
```

## Configuration Files

### render.yaml

The `render.yaml` file contains the service configuration:

```yaml
services:
  - type: web
    name: servicenow-mcp-server
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: pip install -r requirements.txt
    startCommand: python fastmcp_server_render.py
    envVars:
      - key: SERVICENOW_INSTANCE
        sync: false
      - key: SERVICENOW_USERNAME
        sync: false
      - key: SERVICENOW_PASSWORD
        sync: false
```

### fastmcp_server_render.py

This is a modified version of the FastMCP server that:
- Reads `PORT` from environment variables (Render provides this)
- Binds to `0.0.0.0` to accept external connections
- Includes Render-specific configurations

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SERVICENOW_INSTANCE` | Your ServiceNow instance URL (without https://) | Yes |
| `SERVICENOW_USERNAME` | ServiceNow username | Yes |
| `SERVICENOW_PASSWORD` | ServiceNow password | Yes |
| `PORT` | Port to bind to (Render sets this automatically) | No (auto) |
| `HOST` | Host to bind to | No (default: 0.0.0.0) |

## Monitoring and Logs

### View Logs

1. Go to your Render dashboard
2. Click on your service
3. Navigate to "Logs" tab
4. View real-time logs

### Monitor Performance

1. Go to "Metrics" tab in Render dashboard
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

## Automatic Deployments

Render automatically deploys when you push to your GitHub repository:

```bash
# Make changes to your code
git add .
git commit -m "Update: improved error handling"
git push origin main

# Render will automatically detect the push and redeploy
```

## Troubleshooting

### Deployment Fails

**Problem**: Build fails during deployment

**Solutions**:
1. Check `requirements.txt` for correct dependencies
2. Verify Python version compatibility
3. Check build logs in Render dashboard

### Service Not Starting

**Problem**: Service builds but doesn't start

**Solutions**:
1. Verify `startCommand` in `render.yaml`
2. Check that `fastmcp_server_render.py` exists
3. Review logs for startup errors

### Environment Variables Not Working

**Problem**: ServiceNow connection fails

**Solutions**:
1. Verify environment variables are set correctly
2. Check for typos in variable names
3. Ensure no extra spaces in values
4. Verify ServiceNow credentials are correct

### Connection Timeout

**Problem**: MCP client can't connect

**Solutions**:
1. Verify service is running (check Render dashboard)
2. Check service URL is correct
3. Ensure firewall allows outbound connections
4. Try accessing health endpoint: `https://your-service.onrender.com/health`

### Free Tier Limitations

**Problem**: Service spins down after inactivity

**Solution**: 
- Render's free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Consider upgrading to paid plan for always-on service
- Or implement a keep-alive ping service

## Upgrading to Paid Plan

For production use, consider upgrading:

1. Go to your service in Render dashboard
2. Click "Settings"
3. Under "Instance Type", select a paid plan
4. Benefits:
   - Always-on (no spin-down)
   - Better performance
   - More memory/CPU
   - Custom domains
   - Priority support

## Security Best Practices

1. **Never commit credentials**: Use environment variables only
2. **Use secrets**: Mark sensitive env vars as "secret" in Render
3. **Enable HTTPS**: Render provides free SSL certificates
4. **Restrict access**: Consider adding authentication
5. **Monitor logs**: Regularly check for suspicious activity
6. **Update dependencies**: Keep packages up to date

## Custom Domain (Optional)

To use a custom domain:

1. Go to service settings in Render
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed
5. Render will automatically provision SSL certificate

## Scaling

To handle more traffic:

1. **Vertical Scaling**: Upgrade instance type
2. **Horizontal Scaling**: Add more instances (paid plans)
3. **Caching**: Implement caching for frequent queries
4. **Database**: Consider adding Redis for session management

## Cost Estimation

### Free Tier
- 750 hours/month free
- Spins down after 15 min inactivity
- Good for: Development, testing, demos

### Starter Plan ($7/month)
- Always-on
- 512 MB RAM
- Good for: Small production deployments

### Standard Plan ($25/month)
- 2 GB RAM
- Better performance
- Good for: Production use

## Support

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **FastMCP Issues**: https://github.com/jlowin/fastmcp/issues
- **ServiceNow Docs**: https://developer.servicenow.com

## Next Steps

After deployment:

1. ✅ Test all MCP tools
2. ✅ Configure Claude Desktop
3. ✅ Set up monitoring
4. ✅ Configure custom domain (optional)
5. ✅ Implement authentication (recommended for production)
6. ✅ Set up automated backups
7. ✅ Document API endpoints for your team

## Example: Complete Deployment Workflow

```bash
# 1. Clone/navigate to your project
cd servicenow_sse_demo

# 2. Ensure all files are ready
ls -la

# 3. Initialize git (if needed)
git init

# 4. Add files
git add .

# 5. Commit
git commit -m "Ready for Render deployment"

# 6. Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/servicenow-mcp-server.git
git push -u origin main

# 7. Go to Render.com
# 8. Click "New +" → "Blueprint"
# 9. Connect GitHub repo
# 10. Add environment variables
# 11. Deploy!

# 12. Test deployment
curl https://your-service.onrender.com/health

# 13. Update Claude Desktop config with new URL
# 14. Start using your deployed MCP server!
```

## Conclusion

Your FastMCP ServiceNow server is now deployed on Render and accessible from anywhere! The server will automatically redeploy when you push changes to GitHub, making it easy to maintain and update.