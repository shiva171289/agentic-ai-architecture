# Hostinger VPS setup (Ubuntu 24.04)

## 1. Provision

1. Hostinger → VPS → **KVM 1** (1 vCPU, 4 GB) or KVM 2
2. OS: **Ubuntu 24.04** plain template
3. Region: India or Singapore
4. hPanel → VPS → Settings → **SSH keys** → add your `id_ed25519` public key

## 2. First login

```bash
ssh root@<VPS_IP>
```

## 3. Non-root user

```bash
adduser hermes
usermod -aG sudo hermes
rsync --archive --chown=hermes:hermes ~/.ssh /home/hermes/
```

## 4. Harden

```bash
apt update && apt upgrade -y
apt install -y ufw fail2ban git curl unattended-upgrades
ufw allow OpenSSH
ufw enable
```

Edit `/etc/ssh/sshd_config`:

- `PermitRootLogin no`
- `PasswordAuthentication no`

```bash
systemctl restart ssh
```

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

Next: [02-hermes-install.md](02-hermes-install.md)
