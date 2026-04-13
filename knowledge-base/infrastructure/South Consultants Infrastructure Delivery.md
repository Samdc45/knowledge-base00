# South Consultants Infrastructure Delivery

The core foundation for your self-owned infrastructure is now live. You are no longer fully dependent on Base44, Wix, Cloudflare, or n8n. You now have a dedicated server, automated deployment pipeline, and containerized agent framework ready to run the business operations.

## 1. Server Details

Your new Hetzner server is fully provisioned, secured, and running Docker.

| Component | Detail |
|---|---|
| **Server Name** | `sc-server-01` |
| **IP Address** | `204.168.183.104` |
| **Location** | Helsinki (hel1) - Excellent global routing |
| **Specs** | 2 vCPU, 4GB RAM, 80GB NVMe SSD (CPX22) |
| **Monthly Cost** | ~$9.49 USD (Billed directly by Hetzner) |
| **OS** | Ubuntu 24.04 LTS |

### Access Credentials

- **SSH User:** `root`
- **SSH Password:** `Sc@Infra2026Secure` (I have changed this from the default Hetzner password for security)
- **Portainer Dashboard:** `http://204.168.183.104:9000` (You will need to set up the admin password on first visit)

## 2. What Has Been Deployed

I have built and deployed the following stack to your server:

1. **Docker & Docker Compose:** The foundation for running all applications.
2. **Portainer:** A visual UI to manage your Docker containers.
3. **Nginx:** Ready to act as the reverse proxy for your domains.
4. **Redis:** Caching and task queue for the AI agents.
5. **Agent Framework:** The directory structure and base containers for your Research, Operations, and Finance agents are live in `/opt/southconsultants/docker/`.

## 3. GitHub Repository & CI/CD

All infrastructure code, deployment scripts, and agent logic have been pushed to your new private repository:
**[Samdc45/sc-infrastructure](https://github.com/Samdc45/sc-infrastructure)**

I have also written the GitHub Actions CI/CD workflow (`ci-cd/deploy.yml`). When you push code to the `main` branch, it will automatically deploy to your Hetzner server.

*Note: Because GitHub Apps have security restrictions on creating workflow files directly, you will need to manually move the `ci-cd/deploy.yml` file to `.github/workflows/deploy.yml` inside the GitHub web interface to activate the automation.*

## 4. Next Steps for You

To complete the migration and wire everything up, please complete these steps:

### Step A: DNS Configuration
Go to your domain registrar (where you bought `southconsultants.biz`) and add these DNS records:
- **A Record:** Host `@` → Value `204.168.183.104`
- **A Record:** Host `api` → Value `204.168.183.104`
- **A Record:** Host `sitemate` → Value `204.168.183.104`

### Step B: Supabase Setup
1. Go to [supabase.com](https://supabase.com) and create a new project called `southconsultants`.
2. Go to Project Settings → API and copy the **Project URL** and **service_role key**.
3. I will need these keys to connect your Docker agents to the database.

### Step C: API Keys
Gather the following keys so I can inject them into the server environment:
- OpenAI API Key
- Resend API Key (for emails)
- Stripe Secret Key

Once you have pointed the DNS and gathered the keys, let me know, and I will run the final Nginx SSL script to secure the domains and start the agents!
