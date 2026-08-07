# LFCS — Domínio 1: Operations Deployment (25%)

Cobre: boot/GRUB, systemd (services/timers/targets), gerenciamento de pacotes, kernel/sysctl, gerenciamento de processos, virtualização/containers, recovery, logging.

Convenção: cada questão tem cenário → comando(s) → observação de prova quando relevante.

---

## 1. Boot Process & GRUB

**Q1.** Veja qual target (runlevel) é o padrão de boot atual.
```bash
systemctl get-default
```

**Q2.** Mude o boot padrão para modo texto (multi-user, sem GUI), persistente.
```bash
systemctl set-default multi-user.target
```

**Q3.** Mude o boot padrão para modo gráfico.
```bash
systemctl set-default graphical.target
```

**Q4.** Liste todos os targets disponíveis no sistema.
```bash
systemctl list-units --type=target --all
```

**Q5.** Entre em modo rescue (single-user) agora, sem alterar o default de boot.
```bash
systemctl isolate rescue.target
```

**Q6.** Sistema não bootou (kernel panic). Edite a entrada do GRUB no boot para adicionar `single` temporariamente (sem persistir).
```
No menu do GRUB: pressione 'e' na entrada, vá até a linha 'linux ...', adicione 'single' ou 'systemd.unit=rescue.target' no final, Ctrl+X para bootar.
```

**Q7.** Após alteração manual, regenere o `grub.cfg` permanentemente.
```bash
# Debian/Ubuntu
update-grub
# RHEL/CentOS/Fedora
grub2-mkconfig -o /boot/grub2/grub.cfg
```

**Q8.** Reinstale o GRUB no MBR de `/dev/sda` (recuperação via live/rescue com chroot).
```bash
mount /dev/sda1 /mnt
for d in dev proc sys; do mount --bind /$d /mnt/$d; done
chroot /mnt
grub-install /dev/sda
update-grub
exit
```

**Q9.** Aumente o timeout do menu GRUB para 10s, persistente.
```bash
# editar /etc/default/grub
GRUB_TIMEOUT=10
update-grub    # ou grub2-mkconfig conforme distro
```

**Q10.** Veja mensagens de boot do kernel (dmesg) filtrando por erros.
```bash
dmesg --level=err,warn
journalctl -k -p err
```

**Q11.** Root filesystem está montado read-only após boot falho (fsck error). Como sair desse estado e corrigir?
```bash
mount -o remount,rw /
fsck -y /dev/sdaX      # com partição desmontada, se possível via live/rescue
```

---

## 2. systemd — Services

**Q12.** Crie uma unit `.service` mínima para rodar um script, habilite e inicie.
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My App
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/opt/myapp/run.sh
Restart=on-failure
RestartSec=5
User=appuser

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now myapp
```

**Q13.** Diferencie `Type=simple`, `Type=forking`, `Type=oneshot`, `Type=notify`.
```
simple   → processo principal É o processo do ExecStart (padrão)
forking  → processo faz fork e o pai sai; systemd espera o pai encerrar (daemons clássicos)
oneshot  → processo roda e termina, sem processo residente (bom para tasks/scripts)
notify   → serviço avisa via sd_notify quando está realmente pronto
```

**Q14.** Faça um serviço depender de outro (só sobe depois que o banco estiver pronto).
```ini
[Unit]
After=postgresql.service
Requires=postgresql.service
```
**Pegadinha:** `After=` só define ordem, não garante que suba junto. `Requires=` garante dependência real (se o postgresql cair, o dependente também é afetado).

**Q15.** Adicione um "drop-in" (override) sem editar o unit file original.
```bash
systemctl edit myapp
```
```ini
# cria automaticamente /etc/systemd/system/myapp.service.d/override.conf
[Service]
Environment="ENV=production"
```

**Q16.** Veja o unit file efetivo (já com overrides aplicados).
```bash
systemctl cat myapp
```

**Q17.** Mascare um serviço para impedir que suba mesmo manualmente.
```bash
systemctl mask bluetooth.service
systemctl unmask bluetooth.service
```
**Pegadinha:** `disable` só impede boot automático; `mask` bloqueia até start manual (cria symlink pra `/dev/null`).

**Q18.** Configure um serviço para reiniciar automaticamente, mas parar de tentar após 3 falhas em 60s.
```ini
[Service]
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=3
```

**Q19.** Verifique todos os serviços que falharam no boot.
```bash
systemctl --failed
```

**Q20.** Recarregue a config de um serviço sem reiniciar o processo (se ele suportar).
```bash
systemctl reload nginx
systemctl reload-or-restart nginx    # fallback se não suportar reload puro
```

**Q21.** Liste dependências de um serviço (o que ele puxa e o que depende dele).
```bash
systemctl list-dependencies myapp
systemctl list-dependencies myapp --reverse
```

**Q22.** Limite recursos (CPU/memória) de um serviço via systemd (cgroups).
```ini
[Service]
CPUQuota=50%
MemoryMax=512M
```

**Q23.** Configure um serviço para rodar como usuário/grupo específico, com diretório de trabalho fixo.
```ini
[Service]
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
```

**Q24.** Um serviço demora pra parar e trava o shutdown. Configure timeout de stop.
```ini
[Service]
TimeoutStopSec=15
KillSignal=SIGTERM
```

**Q25.** Verifique se um serviço está habilitado no boot sem iniciar ele agora.
```bash
systemctl is-enabled myapp
systemctl is-active myapp
```

**Q26.** Analise o tempo de boot e quais serviços mais demoraram.
```bash
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
```

---

## 3. systemd Timers vs Cron

**Q27.** Substitua um cron job (`0 3 * * *`) por timer systemd equivalente.
```ini
# backup.timer
[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
[Install]
WantedBy=timers.target
```
`Persistent=true` roda a task perdida assim que o sistema voltar, se estava desligado na hora agendada — cron normal não faz isso.

**Q28.** Crie timer que roda a cada 15 minutos.
```ini
[Timer]
OnCalendar=*:0/15
```
Ou baseado em boot/monotonic:
```ini
OnBootSec=5min
OnUnitActiveSec=15min
```

**Q29.** Liste todos os timers ativos e seu próximo disparo.
```bash
systemctl list-timers --all
```

**Q30.** Rode manualmente o service associado a um timer, sem esperar o horário.
```bash
systemctl start myapp.service
```

**Q31.** Cron: agende job só para um usuário específico sem editar como ele.
```bash
echo "*/5 * * * * appuser /opt/scripts/check.sh" > /etc/cron.d/check
```

**Q32.** Diferença entre `/etc/cron.d/`, `crontab -e` (usuário), `/etc/crontab`, `/etc/cron.daily/`.
```
crontab -e (usuário)   → cron pessoal, roda como esse usuário
/etc/crontab            → cron do sistema, exige campo de usuário
/etc/cron.d/*           → mesma sintaxe do /etc/crontab, arquivos separados (usado por pacotes)
/etc/cron.{daily,weekly,hourly,monthly}/ → scripts executáveis, sem sintaxe cron, rodados por run-parts
```

**Q33.** Impeça um usuário específico de usar cron.
```bash
echo "usuario_bloqueado" >> /etc/cron.deny
```

**Q34.** Agende uma tarefa única (não recorrente) para daqui 1 hora.
```bash
echo "/opt/scripts/one-time.sh" | at now + 1 hour
atq          # lista jobs agendados
atrm 3       # remove job de ID 3
```

---

## 4. Gerenciamento de Pacotes — Debian/Ubuntu (apt/dpkg)

**Q35.** Atualize lista de pacotes e faça upgrade completo do sistema.
```bash
apt update && apt upgrade -y
apt full-upgrade -y      # também remove pacotes obsoletos se necessário
```

**Q36.** Instale uma versão específica de um pacote.
```bash
apt install nginx=1.18.0-0ubuntu1
```

**Q37.** Trave a versão de um pacote (não deixe o upgrade tocar nele).
```bash
apt-mark hold nginx
apt-mark unhold nginx
apt-mark showhold        # lista pacotes travados
```

**Q38.** Remova um pacote incluindo arquivos de configuração (purge).
```bash
apt purge nginx -y
apt autoremove -y        # remove dependências órfãs
```

**Q39.** Instale um `.deb` local resolvendo dependências.
```bash
apt install ./pacote-local.deb
# ou, se já tentou com dpkg e faltou dependência:
dpkg -i pacote-local.deb
apt --fix-broken install
```

**Q40.** Liste todos os arquivos instalados por um pacote.
```bash
dpkg -L nginx
```

**Q41.** Descubra a qual pacote pertence um arquivo já instalado.
```bash
dpkg -S /etc/nginx/nginx.conf
```

**Q42.** Verifique se um pacote está instalado.
```bash
dpkg -l | grep nginx
apt list --installed | grep nginx
```

**Q43.** Adicione um repositório PPA/terceiros de forma persistente.
```bash
add-apt-repository ppa:exemplo/ppa
apt update
```

**Q44.** Limpe cache de pacotes baixados para liberar espaço.
```bash
apt clean
apt autoclean
```

---

## 5. Gerenciamento de Pacotes — RHEL/Fedora (dnf/rpm)

**Q45.** Atualize todo o sistema.
```bash
dnf update -y
```

**Q46.** Instale versão específica e trave (versionlock).
```bash
dnf install nginx-1.20.1
dnf versionlock add nginx
dnf versionlock delete nginx
```

**Q47.** Liste arquivos de um pacote instalado.
```bash
rpm -ql nginx
```

**Q48.** Descubra a qual pacote pertence um arquivo.
```bash
rpm -qf /etc/nginx/nginx.conf
```

**Q49.** Instale um `.rpm` local com resolução de dependências.
```bash
dnf install ./pacote-local.rpm
```

**Q50.** Verifique integridade dos arquivos de um pacote instalado (detecta alteração indevida).
```bash
rpm -V nginx
```

**Q51.** Baixe um pacote sem instalar (só para cache/transferência).
```bash
dnf download nginx
```

**Q52.** Veja histórico de transações do dnf e reverta a última.
```bash
dnf history
dnf history undo last
```

**Q53.** Habilite um repositório específico temporariamente numa instalação.
```bash
dnf install --enablerepo=epel pacote
```

**Q54.** Grupo de pacotes (ex: "Development Tools").
```bash
dnf group list
dnf group install "Development Tools"
```

---

## 6. Kernel Parameters / sysctl

**Q55.** Habilite IP forwarding persistente (roteador/NAT).
```bash
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.d/99-network.conf
sysctl -p /etc/sysctl.d/99-network.conf
```

**Q56.** Aumente o limite máximo de conexões em fila (backlog) persistente.
```bash
echo 'net.core.somaxconn = 4096' >> /etc/sysctl.d/99-tuning.conf
sysctl --system
```

**Q57.** Veja valor atual de um parâmetro de kernel específico.
```bash
sysctl net.ipv4.ip_forward
cat /proc/sys/net/ipv4/ip_forward
```

**Q58.** Aplique mudança imediata sem persistir (teste rápido).
```bash
sysctl -w vm.swappiness=10
```
**Pegadinha:** isso NÃO sobrevive a reboot — sempre complementar com arquivo em `/etc/sysctl.d/`.

**Q59.** Recarregue todos os arquivos de sysctl.d de uma vez.
```bash
sysctl --system
```

**Q60.** Aumente limite de arquivos abertos por processo, persistente (ulimits, não sysctl puro).
```bash
# /etc/security/limits.d/custom.conf
appuser soft nofile 65536
appuser hard nofile 65536
```

**Q61.** Veja quais módulos de kernel estão carregados, carregue/remova um módulo.
```bash
lsmod
modprobe overlay
modprobe -r overlay
```

**Q62.** Carregue um módulo de kernel automaticamente no boot.
```bash
echo 'overlay' >> /etc/modules-load.d/custom.conf
```

---

## 7. Gerenciamento de Processos

**Q63.** Liste processos em árvore, mostrando relação pai-filho.
```bash
ps auxf
pstree -p
```

**Q64.** Envie SIGTERM, depois SIGKILL se não responder.
```bash
kill -15 1234
sleep 5
kill -9 1234
```

**Q65.** Mate todos os processos de um nome específico.
```bash
pkill -9 -f "python worker.py"
killall nginx
```

**Q66.** Inicie um processo com prioridade baixa (não atrapalhar o sistema).
```bash
nice -n 19 /usr/local/bin/backup.sh &
```

**Q67.** Mude prioridade de um processo já rodando.
```bash
renice -n -10 -p 4321
```
**Pegadinha:** valores negativos = maior prioridade; só root pode dar prioridade negativa (menor "nice value").

**Q68.** Coloque um processo em background, depois traga de volta ao foreground.
```bash
comando &
jobs
fg %1
bg %1        # continua em background após Ctrl+Z
```

**Q69.** Rode um processo que sobrevive ao logout da sessão SSH.
```bash
nohup /opt/scripts/long-task.sh &
disown
```
Alternativa mais robusta:
```bash
tmux new -s work
# roda o comando dentro do tmux, depois Ctrl+B D pra desanexar
```

**Q70.** Veja uso de CPU/memória em tempo real, ordenado por consumo de memória.
```bash
top -o %MEM
htop          # se instalado
```

**Q71.** Descubra qual processo está usando um arquivo ou porta específica.
```bash
lsof /var/log/app.log
lsof -i :8080
fuser -v /var/log/app.log
```

**Q72.** Limite CPU de um processo específico já em execução (cgroups v2, sem systemd unit).
```bash
systemd-run --scope -p CPUQuota=20% --pid 4321
# ou via cgroup manual em /sys/fs/cgroup/
```

---

## 8. Virtualização / Containers

**Q73.** Rode um container persistente entre reboots (Docker).
```bash
docker run -d --name web --restart unless-stopped -p 8080:80 nginx
```

**Q74.** Gere um systemd unit a partir de um container Podman (padrão em RHEL/rootless).
```bash
podman run -d --name web -p 8080:80 nginx
podman generate systemd --new --name web --files
mv container-web.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now container-web
```

**Q75.** Liste imagens e containers, remova containers parados.
```bash
docker ps -a
docker images
docker container prune -f
```

**Q76.** Veja logs de um container.
```bash
docker logs -f web
podman logs -f web
```

**Q77.** Execute um comando dentro de um container já rodando.
```bash
docker exec -it web bash
```

**Q78.** Crie uma VM básica com `virt-install` (KVM/libvirt), verifique status.
```bash
virt-install --name vm01 --ram 2048 --vcpus 2 \
  --disk path=/var/lib/libvirt/images/vm01.qcow2,size=20 \
  --os-variant ubuntu22.04 --network bridge=virbr0 \
  --cdrom /root/ubuntu.iso

virsh list --all
virsh start vm01
virsh autostart vm01     # persiste inicialização com o host
```

**Q79.** Pare, reinicie e destrua (delete) uma VM via virsh.
```bash
virsh shutdown vm01
virsh reboot vm01
virsh destroy vm01        # força stop (equivalente a desligar na tomada)
virsh undefine vm01       # remove definição da VM
```

**Q80.** Liste snapshots de uma VM e reverta para um snapshot.
```bash
virsh snapshot-list vm01
virsh snapshot-revert vm01 snap1
```

---

## 9. System Recovery / Troubleshooting

**Q81.** Sistema não inicia por erro em `/etc/fstab` (entrada inválida). Como recuperar?
```
Boot entra em modo emergency/rescue automaticamente.
Digite a senha de root, edite /etc/fstab removendo/corrigindo a linha problemática.
mount -o remount,rw /
vi /etc/fstab
reboot
```

**Q82.** Esqueceu a senha de root. Recupere via GRUB.
```
No GRUB, edite a entrada de boot ('e'), adicione ao final da linha linux:
  rd.break (RHEL) ou init=/bin/bash (genérico)
Boot, depois:
mount -o remount,rw /sysroot   (RHEL) ou / (genérico)
chroot /sysroot
passwd root
touch /.autorelabel   (se SELinux, RHEL)
exit; reboot
```

**Q83.** Verifique espaço em disco cheio impedindo boot/log — encontre o que está consumindo.
```bash
df -h
du -sh /var/log/* | sort -rh | head -10
journalctl --vacuum-size=200M
```

**Q84.** Serviço crítico falha no boot repetidamente e trava o systemd. Force boot ignorando ele temporariamente.
```
No GRUB, edite a linha linux, adicione: systemd.mask=nome-do-servico.service
```

**Q85.** Analise se o boot está lento devido a algum serviço específico.
```bash
systemd-analyze blame | head -20
```

**Q86.** initramfs corrompido após update de kernel — regenere.
```bash
# Debian/Ubuntu
update-initramfs -u -k all
# RHEL
dracut -f /boot/initramfs-$(uname -r).img $(uname -r)
```

---

## 10. Logging / journald

**Q87.** Veja logs apenas do boot atual.
```bash
journalctl -b
```

**Q88.** Veja logs de um boot anterior (ex: o boot que precedeu um crash).
```bash
journalctl --list-boots
journalctl -b -1
```

**Q89.** Filtre logs por período de tempo específico.
```bash
journalctl --since "2026-07-27 08:00" --until "2026-07-27 09:00"
```

**Q90.** Filtre logs por prioridade (só erros e acima).
```bash
journalctl -p err
```

**Q91.** Torne o journal persistente entre reboots (por padrão pode ser volátil, só em memória).
```bash
mkdir -p /var/log/journal
systemd-tmpfiles --create --prefix /var/log/journal
systemctl restart systemd-journald
```
Verificar: `/etc/systemd/journald.conf` → `Storage=persistent`.

**Q92.** Limite o tamanho máximo do journal em disco.
```bash
journalctl --vacuum-size=500M
```
Persistente:
```
# /etc/systemd/journald.conf
SystemMaxUse=500M
```

**Q93.** Acompanhe logs em tempo real de um serviço específico.
```bash
journalctl -u nginx -f
```

**Q94.** Exporte logs em formato JSON para análise externa.
```bash
journalctl -u nginx -o json-pretty
```

**Q95.** Envie logs para um servidor remoto (rsyslog forward).
```
# /etc/rsyslog.d/remote.conf
*.* @@192.168.1.100:514    # TCP
# ou @192.168.1.100:514    # UDP
```
```bash
systemctl restart rsyslog
```

---

## Resumo de comandos por frequência de cobrança na prova (minha estimativa com base nos objetivos oficiais)

**Altíssima frequência:** `systemctl`, `journalctl`, `sysctl`, unit files customizados, cron/timer, `apt`/`dnf` básico.
**Alta:** troubleshooting de boot (GRUB, fstab, senha root), gerenciamento de processo (`kill`, `nice`, `renice`).
**Média:** containers (Docker/Podman), virt-install/virsh, logrotate, versionlock/hold.

---

Próximo domínio sugerido: **Networking (25%)** — mesma profundidade, cobrindo IPv4/IPv6, SSH, firewall, DNS, NAT, bonding, troubleshooting.
