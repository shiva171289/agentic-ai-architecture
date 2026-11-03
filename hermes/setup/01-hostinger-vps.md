# Hostinger VPS setup (Ubuntu 24.04)

Use a **Plain OS** Ubuntu server for this hub. The runbooks in [02-hermes-install.md](02-hermes-install.md), [03-telegram-gateway.md](03-telegram-gateway.md), and [../cron.md](../cron.md) assume a native Hermes install under Linux user `hermes`, not Hostinger’s Docker **Hermes Agent** application template.

## 1. Provision

1. Hostinger → VPS → **KVM 1** (1 vCPU, 4 GB) or KVM 2
2. At checkout or first activation, open the **Plain OS** tab. Select **Ubuntu 24.04** only.
3. Do **not** pick **Application** (including the **Hermes Agent** one-click template), **Control Panel**, or **Docker Application** stacks for this project.
4. Region: India or Singapore
5. hPanel → VPS → Settings → **SSH keys** → add your `id_ed25519` public key
6. hPanel → VPS → **Security → Firewall**. If you create or activate a Hostinger firewall group, add an **Accept** rule for **SSH** (TCP port 22) from **Anywhere**. An active group with no SSH rule blocks port 22 before traffic reaches Ubuntu.
7. Set a **root password** when Hostinger prompts at checkout or first activation. You cannot skip this step in hPanel. Store the password in a password manager. Use it only for **Browser terminal / Web console** recovery if SSH keys fail. After hardening (section 4), do not use that password for normal SSH login.

Hostinger calls a clean Ubuntu image **Plain OS** (base OS only). That is the correct “direct” OS install for SSH hardening and the steps below.

Hostinger does **not** offer a panel toggle to “turn off passwords” for SSH. You disable password login **on the VPS** in `sshd_config` (and Hostinger’s cloud-init drop-in). The root password in hPanel can remain for console access; that is separate from SSH password authentication.

If the VPS already runs the Hermes Agent application template, either rebuild to **Plain OS → Ubuntu 24.04** (this wipes the disk) or adapt Hostinger’s container workflow yourself. Rebuilding to Plain OS matches this repo with less friction.

## 2. First login

```bash
ssh root@<VPS_IP>
```

On your laptop, use the **same public key** you added in hPanel. OpenSSH does not try custom key file names (for example `id_ed25519_personal`) unless you pass `-i` or set `IdentityFile` in `~/.ssh/config`.

After section 4 (harden SSH), `PermitRootLogin no` is set. Use `hermes@<VPS_IP>` (or a config `Host` alias) for normal login. Root over SSH stays off by design.

## 3. Non-root user (no login password)

Create `hermes` with **no password**. Login uses your SSH key only. Allow non-interactive `sudo` so automation and the verify step in section 6 work without a TTY password prompt.

```bash
adduser --disabled-password --gecos "" hermes
usermod -aG sudo hermes
install -d -m 700 -o hermes -g hermes /home/hermes/.ssh
install -m 600 -o hermes -g hermes /root/.ssh/authorized_keys /home/hermes/.ssh/authorized_keys
printf '%s\n' 'hermes ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/hermes
chmod 440 /etc/sudoers.d/hermes
visudo -cf /etc/sudoers.d/hermes
```

Do not run interactive `adduser hermes` without `--disabled-password`. That sets a login password you do not need for key-only SSH.

## 4. Harden SSH (key only)

1. Open a **second** SSH session as `root` before you change SSH settings. Keep it open until section 6 passes.
2. Confirm key login works: `ssh -o BatchMode=yes hermes@<VPS_IP> true`

```bash
apt update && apt upgrade -y
apt install -y ufw fail2ban git curl unattended-upgrades
ufw allow OpenSSH
ufw allow 22/tcp
ufw --force enable
ufw status verbose
```

Repeated failed SSH attempts (for example `root@` after hardening) can trigger **fail2ban**. Your client then sees **Connection timed out**, not “Permission denied”.

Edit `/etc/ssh/sshd_config` (uncomment or add as needed):

- `PermitRootLogin no`
- `PubkeyAuthentication yes`
- `PasswordAuthentication no`
- `KbdInteractiveAuthentication no` (Ubuntu 24.04; older docs use `ChallengeResponseAuthentication no`)

On Hostinger, cloud-init may re-enable password auth. Set the same value in `/etc/ssh/sshd_config.d/50-cloud-init.conf` if that file contains `PasswordAuthentication yes`.

```bash
sshd -t && systemctl reload ssh
```

After reload, password SSH login is off **on this server**. Hostinger hPanel may still show a root password for console use; that does not re-enable SSH passwords by itself.

## 5. Swap (4 GB RAM)

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

## 6. Verify

```bash
su - hermes
whoami   # hermes
sudo -n true && echo ok
```

## 7. If SSH times out (Browser terminal)

Use this when `ping <VPS_IP>` works but `ssh` hangs or times out on port 22.

1. hPanel → VPS → **Browser terminal**. Log in as **root** with your stored root password.
2. Run:

```bash
ufw status verbose
ss -tlnp | grep ':22'
systemctl is-active ssh
fail2ban-client status sshd 2>/dev/null || true
```

3. If fail2ban lists your laptop public IP, unban it (replace with your IP from [https://api.ipify.org](https://api.ipify.org)):

```bash
fail2ban-client set sshd unbanip YOUR_PUBLIC_IP
```

4. If UFW is active and port 22 is not allowed:

```bash
ufw allow OpenSSH
ufw allow 22/tcp
ufw reload
```

5. In hPanel → **Security → Firewall**, confirm an **Accept SSH** rule exists and the firewall is not dropping port 22.
6. From your laptop, use the `hermes` user and your personal key (not `root`):

```bash
ssh -o BatchMode=yes -i ~/.ssh/id_ed25519_personal hermes@<VPS_IP> true
```

Next: [02-hermes-install.md](02-hermes-install.md)
