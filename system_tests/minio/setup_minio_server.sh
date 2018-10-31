# Adapted from https://www.centosblog.com/install-configure-minio-object-storage-server-centos-linux/

sudo useradd -s /sbin/nologin -d /opt/minio minio

sudo mkdir -p /opt/minio/bin
sudo mkdir /opt/minio/data

sudo wget https://dl.minio.io/server/minio/release/linux-amd64/minio -O /opt/minio/bin/minio
sudo chmod +x /opt/minio/bin/minio

sudo cp /vagrant/minio/minio.conf /opt/minio/minio.conf

sudo chown -R minio:minio /opt/minio

sudo cp /vagrant/minio/minio.service /etc/systemd/system/minio.service

systemctl enable minio && systemctl start minio

systemctl status minio
