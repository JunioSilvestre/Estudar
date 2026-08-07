# Simulado LFCS (Linux Foundation Certified System Administrator)

**Formato oficial:** 2h, performance-based (terminal real, sem múltipla escolha), 24 tasks com sub-tasks, nota mínima 67%, man pages permitidas, docs externas não.

**Domínios e pesos oficiais (2026):**

| Domínio | Peso |
|---|---|
| Operations Deployment | 25% |
| Networking | 25% |
| Storage | 20% |
| Essential Commands | 20% |
| Users and Groups | 10% |

Regra de prova real: **toda configuração precisa sobreviver a reboot**. Se você editar algo "na mão" sem persistir (ex: `ip addr add` sem netplan/NetworkManager, ou `sysctl -w` sem `.conf`), a tarefa é considerada incompleta mesmo funcionando no momento.

---

## DOMÍNIO 1 — Essential Commands (20%)

### Q1. Encontre todos os arquivos maiores que 100MB modificados nos últimos 7 dias em `/var`
```bash
find /var -type f -size +100M -mtime -7
```
**Pegadinha:** `-mtime -7` = modificado há menos de 7 dias. `-mtime +7` seria mais de 7 dias. Sinal errado é erro clássico de prova.

### Q2. Conte quantas linhas contêm a palavra "error" (case insensitive) em todos os `.log` de `/var/log`, recursivo
```bash
grep -ril "error" /var/log --include="*.log" | wc -l
```
Ou contagem total de ocorrências (não arquivos):
```bash
grep -rio "error" /var/log --include="*.log" | wc -l
```

### Q3. Substitua todas as ocorrências de `old-server` por `new-server` em `/etc/hosts` (in-place)
```bash
sed -i 's/old-server/new-server/g' /etc/hosts
```
**Backup antes (boa prática de prova):**
```bash
sed -i.bak 's/old-server/new-server/g' /etc/hosts
```

### Q4. Compacte `/opt/app` em `.tar.gz` preservando permissões, exclua depois via find
```bash
tar -czvf app-backup.tar.gz /opt/app
find /opt/app -type f -mtime +30 -exec rm -f {} \;
```

### Q5. Configure hard link e symbolic link para `/etc/nginx/nginx.conf`
```bash
ln /etc/nginx/nginx.conf /root/nginx-hard.conf        # hard link
ln -s /etc/nginx/nginx.conf /root/nginx-soft.conf     # symbolic link
```
**Pegadinha de prova:** hard link não funciona entre filesystems diferentes (nem symlink de diretório sem `-s` funciona pra diretórios em geral). `ls -li` mostra o mesmo inode para hard links.

### Q6. Aplique SUID, SGID e sticky bit
```bash
chmod u+s /usr/local/bin/app       # SUID (executa como dono)
chmod g+s /shared/project          # SGID (arquivos novos herdam grupo do dir)
chmod +t /shared/tmp               # sticky bit (só dono apaga o próprio arquivo)
```
Numérico equivalente: `chmod 4755`, `chmod 2775`, `chmod 1777`.

### Q7. Redirecione stdout e stderr para arquivos separados, e depois para o mesmo arquivo
```bash
comando > out.log 2> err.log
comando > all.log 2>&1
comando &> all.log        # equivalente moderno (bash)
```
**Pegadinha:** `2>&1 > file` (ordem errada) NÃO redireciona stderr pro file — precisa ser `> file 2>&1`.

### Q8. Use `awk` para extrair coluna 1 e 3 de um CSV separado por vírgula, ignorando header
```bash
awk -F',' 'NR>1 {print $1, $3}' arquivo.csv
```

### Q9. Ordene um arquivo por segunda coluna numérica, decrescente, removendo duplicatas
```bash
sort -t' ' -k2,2 -nr arquivo.txt | uniq
```

### Q10. Crie um pipe: liste processos, filtre por "nginx", mostre PID e mate o processo
```bash
ps aux | grep nginx | grep -v grep | awk '{print $2}' | xargs kill -9
```
Melhor prática (evita grep -v):
```bash
pkill -9 nginx
```

---

## DOMÍNIO 2 — Users and Groups (10%)

### Q11. Crie usuário `devops` com home em `/opt/devops`, shell `/bin/bash`, grupo secundário `docker`
```bash
useradd -m -d /opt/devops -s /bin/bash -G docker devops
passwd devops
```

### Q12. Force troca de senha no próximo login, e expire a conta em 90 dias
```bash
chage -d 0 devops               # força troca no próximo login
chage -M 90 devops              # expira em 90 dias de senha
chage -l devops                 # verifica
```

### Q13. Dê a `devops` sudo sem senha apenas para `systemctl restart nginx`
```bash
visudo -f /etc/sudoers.d/devops
```
Conteúdo do arquivo:
```
devops ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```
**Pegadinha:** sempre editar via `visudo` (valida sintaxe). Editar `/etc/sudoers` direto com `vi` pode travar o sudo do sistema se der erro de sintaxe.

### Q14. Crie grupo `webteam`, adicione usuários existentes sem remover grupos atuais
```bash
groupadd webteam
usermod -aG webteam devops
usermod -aG webteam junio
```
**Pegadinha clássica:** `usermod -G webteam devops` (sem `-a`) SUBSTITUI todos os grupos secundários. Sempre `-aG` para adicionar.

### Q15. Bloqueie e depois desbloqueie a conta `devops`
```bash
usermod -L devops       # bloqueia (passwd -l também funciona)
usermod -U devops       # desbloqueia
```

### Q16. Configure quota de disco: 500MB soft, 600MB hard para usuário `devops` em `/home`
```bash
# /etc/fstab precisa ter usrquota na partição
mount -o remount /home
quotacheck -cum /home
quotaon /home
edquota -u devops
# dentro do editor: ajustar blocks soft=512000 hard=614400 (em KB)
```
Verificar:
```bash
repquota /home
```

### Q17. Onde ficam as informações de expiração de conta e hash de senha?
```
/etc/shadow    → hash da senha, datas de expiração
/etc/passwd    → UID, GID, home, shell
/etc/group     → grupos e membros
/etc/gshadow   → senhas de grupo (raro)
```

---

## DOMÍNIO 3 — Storage (20%)

### Q18. Crie uma partição LVM completa: PV → VG → LV → filesystem → montagem persistente
```bash
pvcreate /dev/sdb
vgcreate vg_data /dev/sdb
lvcreate -L 10G -n lv_app vg_data
mkfs.ext4 /dev/vg_data/lv_app
mkdir -p /mnt/app
echo '/dev/vg_data/lv_app  /mnt/app  ext4  defaults  0 2' >> /etc/fstab
mount -a
```
**Pegadinha:** esquecer `/etc/fstab` = não sobrevive a reboot = tarefa incompleta na prova.

### Q19. Estenda um LV existente + filesystem sem perder dados (ext4 e xfs)
```bash
lvextend -L +5G /dev/vg_data/lv_app
resize2fs /dev/vg_data/lv_app      # ext4
# ou, se for xfs:
xfs_growfs /mnt/app
```
**Pegadinha:** `xfs_growfs` usa o **mountpoint**, não o device. `resize2fs` usa o **device**.

### Q20. Configure RAID1 por software com mdadm, persistente
```bash
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdc /dev/sdd
mkfs.ext4 /dev/md0
mdadm --detail --scan >> /etc/mdadm/mdadm.conf   # Debian/Ubuntu
update-initramfs -u
echo '/dev/md0  /mnt/raid  ext4  defaults  0 2' >> /etc/fstab
mount -a
```

### Q21. Configure swap adicional de 2GB via arquivo (não partição)
```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Q22. Verifique e repare um filesystem ext4 com erros (device desmontado)
```bash
umount /dev/sdb1
fsck -y /dev/sdb1
```

### Q23. Monte um filesystem em modo somente leitura, e remonte como leitura/escrita sem desmontar
```bash
mount -o remount,ro /mnt/app
mount -o remount,rw /mnt/app
```

### Q24. Crie um filesystem criptografado com LUKS
```bash
cryptsetup luksFormat /dev/sdc1
cryptsetup luksOpen /dev/sdc1 secure_vol
mkfs.ext4 /dev/mapper/secure_vol
mount /dev/mapper/secure_vol /mnt/secure
```
Persistência exige entrada em `/etc/crypttab` + `/etc/fstab`.

### Q25. Verifique uso de espaço por diretório, top 5 maiores subpastas
```bash
du -sh /var/* 2>/dev/null | sort -rh | head -5
```

### Q26. Monte um compartilhamento NFS de forma persistente
```bash
mkdir -p /mnt/nfsshare
mount -t nfs 192.168.1.10:/export/share /mnt/nfsshare
echo '192.168.1.10:/export/share  /mnt/nfsshare  nfs  defaults  0 0' >> /etc/fstab
```

---

## DOMÍNIO 4 — Networking (25%)

### Q27. Configure IP estático persistente (Ubuntu netplan)
```yaml
# /etc/netplan/01-netcfg.yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses: [192.168.1.50/24]
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```
```bash
netplan apply
```
**RHEL/CentOS equivalente (nmcli):**
```bash
nmcli con mod eth0 ipv4.addresses 192.168.1.50/24
nmcli con mod eth0 ipv4.gateway 192.168.1.1
nmcli con mod eth0 ipv4.dns "8.8.8.8 1.1.1.1"
nmcli con mod eth0 ipv4.method manual
nmcli con up eth0
```

### Q28. Configure hostname persistente e resolução local
```bash
hostnamectl set-hostname app01.jcscode.local
echo '192.168.1.50 app01.jcscode.local app01' >> /etc/hosts
```

### Q29. Configure SSH: desabilite login root, mude a porta para 2222, force chave pública
```bash
# /etc/ssh/sshd_config
PermitRootLogin no
Port 2222
PasswordAuthentication no
PubkeyAuthentication yes
```
```bash
sshd -t                     # valida sintaxe antes de reiniciar!
systemctl restart sshd
```
**Pegadinha crítica de prova:** sempre `sshd -t` antes de restart — erro de sintaxe derruba SSH e te tranca fora da máquina (se for exame remoto, é fatal).

### Q30. Configure firewall: libere porta 2222/tcp e 443/tcp, persistente (firewalld e ufw)
```bash
# firewalld (RHEL)
firewall-cmd --permanent --add-port=2222/tcp
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --reload

# ufw (Ubuntu)
ufw allow 2222/tcp
ufw allow 443/tcp
ufw enable
```

### Q31. Configure NAT/masquerade básico com iptables persistente
```bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
apt install iptables-persistent -y
netfilter-persistent save
```

### Q32. Sincronize horário via NTP (chrony) e force sync imediato
```bash
systemctl enable --now chronyd
chronyc sources -v
chronyc makestep
timedatectl set-ntp true
```

### Q33. Diagnostique: host não resolve DNS mas ping por IP funciona
```bash
cat /etc/resolv.conf              # verificar nameserver configurado
systemd-resolve --status          # se usando systemd-resolved
dig @8.8.8.8 google.com           # testa resolução direta contra DNS público
nslookup google.com 8.8.8.8
```
Causa comum de prova: `/etc/resolv.conf` sobrescrito ou `nsswitch.conf` com ordem errada em `hosts:`.

### Q34. Configure bonding de duas interfaces (active-backup), persistente
```bash
nmcli con add type bond ifname bond0 mode active-backup
nmcli con add type ethernet ifname eth0 master bond0
nmcli con add type ethernet ifname eth1 master bond0
nmcli con mod bond0 ipv4.addresses 192.168.1.60/24 ipv4.method manual
nmcli con up bond0
```

### Q35. Capture tráfego na interface eth0, filtrando porta 80, salvando em arquivo
```bash
tcpdump -i eth0 port 80 -w capture.pcap
```
Ler depois:
```bash
tcpdump -r capture.pcap
```

### Q36. Verifique quais processos estão escutando em quais portas
```bash
ss -tulpn
```
(equivalente antigo: `netstat -tulpn`, geralmente não vem instalado por padrão hoje).

---

## DOMÍNIO 5 — Operations Deployment (25%)

### Q37. Crie um cron job que roda backup diário às 2h, e um `@reboot`
```bash
crontab -e
```
```
0 2 * * *  /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
@reboot    /usr/local/bin/startup-check.sh
```
Cron de sistema (para usuário específico sem editar como ele):
```bash
echo "0 2 * * * root /usr/local/bin/backup.sh" > /etc/cron.d/backup
```

### Q38. Crie um systemd timer equivalente a um cron (forma moderna, cobrada na prova)
```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Backup diário

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Timer para backup diário

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```
```bash
systemctl daemon-reload
systemctl enable --now backup.timer
systemctl list-timers
```

### Q39. Crie uma unit systemd customizada para uma aplicação, com restart automático
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My App
After=network.target

[Service]
ExecStart=/opt/myapp/run.sh
Restart=on-failure
RestartSec=5
User=devops

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now myapp
systemctl status myapp
```

### Q40. Diagnostique um serviço que não sobe (troubleshooting sistemático)
```bash
systemctl status myapp
journalctl -u myapp -xe
journalctl -u myapp --since "10 min ago"
systemctl cat myapp        # mostra o unit file efetivo (com overrides/drop-ins)
```

### Q41. Ajuste parâmetro de kernel (sysctl) de forma persistente
```bash
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.d/99-custom.conf
sysctl -p /etc/sysctl.d/99-custom.conf
```
**Pegadinha:** `sysctl -w net.ipv4.ip_forward=1` sozinho NÃO sobrevive a reboot.

### Q42. Gerencie prioridade de processo (nice/renice)
```bash
nice -n 10 /usr/local/bin/heavy-job.sh      # inicia com prioridade baixa
renice -n -5 -p 1234                        # muda prioridade de processo já rodando
```

### Q43. Instale um pacote e trave (hold) a versão para não ser atualizada
```bash
# Debian/Ubuntu
apt-mark hold nginx
apt-mark unhold nginx

# RHEL/CentOS (dnf)
dnf versionlock add nginx
dnf versionlock delete nginx
```

### Q44. Configure boot para um target específico (equivalente a runlevel) persistente
```bash
systemctl set-default multi-user.target     # sem GUI
systemctl get-default
systemctl isolate rescue.target             # muda AGORA sem persistir
```

### Q45. Repare o GRUB após falha de boot (chroot via live/rescue)
```bash
mount /dev/sdX1 /mnt
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
chroot /mnt
grub-install /dev/sdX
update-grub          # Debian/Ubuntu
# ou
grub2-mkconfig -o /boot/grub2/grub.cfg   # RHEL
```

### Q46. Configure e rode um container simples (Docker/Podman), persistente entre reboots
```bash
docker run -d --name webapp --restart unless-stopped -p 8080:80 nginx
```
Podman + systemd (mais alinhado ao que a prova costuma cobrar em RHEL-based):
```bash
podman run -d --name webapp -p 8080:80 nginx
podman generate systemd --new --name webapp --files
mv container-webapp.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now container-webapp
```

### Q47. Configure log rotation customizado para uma aplicação
```
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
    create 0640 devops devops
}
```
Testar sem esperar o cron do sistema:
```bash
logrotate -f /etc/logrotate.d/myapp
```

### Q48. Faça snapshot de uma VM/imagem usando LVM (backup consistente)
```bash
lvcreate -L 1G -s -n lv_app_snap /dev/vg_data/lv_app
mount /dev/vg_data/lv_app_snap /mnt/snap
# ... backup do conteúdo em /mnt/snap ...
umount /mnt/snap
lvremove /dev/vg_data/lv_app_snap
```

---

## Checklist de erros que derrubam pontos na prova real

1. **Esquecer persistência** — qualquer config que não sobrevive a reboot vale zero na sub-task.
2. **Não validar sintaxe antes de restart** (`sshd -t`, `nginx -t`, `visudo`) — pode travar acesso.
3. **`usermod -G` sem `-a`** — apaga grupos secundários existentes.
4. **Misturar `resize2fs` (device) com `xfs_growfs` (mountpoint)**.
5. **Ordem de redirecionamento errada** (`2>&1 >file` vs `>file 2>&1`).
6. **Esquecer `daemon-reload`** depois de criar/editar unit file systemd.
7. **Confundir soft/hard limit em quotas** (unidade é KB por padrão no `edquota`).

---

## Como praticar isso de verdade

- Ambiente: VM Linux limpa (Ubuntu Server ou Rocky/AlmaLinux), sem GUI, snapshot antes de cada rodada.
- Simule as 2h reais: sem consultar nada além de `man`.
- Killer.sh (incluso na inscrição oficial) é o simulador mais fiel ao formato real — vale rodar antes do exame de verdade.

Quer que eu monte um roteiro de **lab guiado** (passo a passo, com verificação de cada etapa) pra você rodar direto na sua VM Linux, ou prefere que eu aumente o número de questões em algum domínio específico primeiro?
