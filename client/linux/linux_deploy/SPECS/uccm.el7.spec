Name:       uccm
Version:    1.3
Release:    el7
Summary:    Unix Client Configuration Management
AutoReq:    no

License:    GPL
URL:        https://git.its.unibas.ch/projects/CCM/repos/client

%description
Client for Uni Basel Unix Client Configuration Management
A service form ITS Client Services

%pre
TMP_FILE=$(mktemp)
crontab -l > $TMP_FILE
echo "*/15 * * * * /usr/local/uccm/bin/uccm" >> $TMP_FILE
crontab $TMP_FILE
rm $TMP_FILE

%files
/usr/local/uccm
/root/.ssh/known_hosts
%changelog
